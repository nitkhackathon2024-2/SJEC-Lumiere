import subprocess
import json
import re
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pytesseract
import io
import os
import fitz
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Environment variables
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR")
JSON_FILE_PATH = os.path.join(ARTIFACTS_DIR, os.getenv("JSON_FILE_NAME"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")
TESSERACT_CMD = os.getenv("TESSERACT_CMD")

# CORS Middleware for frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/uploads/")
async def upload_file(file: UploadFile = File(...)):
    try:
        print(f"Received file: {file.filename}")

        # Extract file extension
        file_extension = file.filename.split(".")[-1].lower()
        print(f"File extension: {file_extension}")
        
        # Process image files (jpg, jpeg, png, bmp, tiff)
        if file_extension in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            print("Processing image file...")
            image_stream = io.BytesIO(await file.read())
            image = Image.open(image_stream)
            text = pytesseract.image_to_string(image, lang='eng')
            print("Image text extraction completed.")

        # Process text files
        elif file_extension == "txt":
            print("Processing text file...")
            content = await file.read()
            text = content.decode("utf-8")
            print("Text extraction completed.")

        # Process PDF files
        elif file_extension == "pdf":
            print("Processing PDF file...")
            pdf_stream = io.BytesIO(await file.read())
            text = extract_text_from_pdf(pdf_stream)
            print("PDF text extraction completed.")
        
        # Unsupported file type
        else:
            print("Unsupported file type.")
            return {"error": "Unsupported file type"}
        
        # Pass the extracted text to the Llama model for structured data
        print("Passing extracted text to Llama model...")
        structured_data = await pass_to_llama_model(text)
        print("Llama model processing completed.")
        
        # Return the structured data as a JSON response
        if structured_data:
            print(f"Returning structured data: {structured_data}")
            return {
                "file_type": file_extension,
                "structured_data": structured_data  # This will be returned to the Next.js frontend
            }
        else:
            print("Failed to extract structured data.")
            return {"error": "Failed to extract structured data from the text"}

    except Exception as e:
        print(f"Error during file processing: {str(e)}")
        return {"error": str(e)}

def extract_text_from_pdf(pdf_stream):
    """
    Extracts text from both native and image-based PDFs.
    """
    text = ""
    try:
        print("Opening PDF for text extraction...")
        with fitz.open(stream=pdf_stream, filetype="pdf") as pdf_document:
            for page_num in range(len(pdf_document)):
                print(f"Processing page {page_num + 1}...")
                page = pdf_document.load_page(page_num)
                if page.get_text():
                    text += page.get_text()
                else:
                    image_list = page.get_images(full=True)
                    for img_index, img in enumerate(image_list):
                        print(f"Extracting image {img_index + 1} from page...")
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        image = Image.open(io.BytesIO(image_bytes))
                        text += pytesseract.image_to_string(image)
        print("PDF text extraction completed.")
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
    return text

async def pass_to_llama_model(extracted_text):
    try:
        prompt = f"""
Extract structured data from the following text and provide the output as a JSON object with the following structure:

{{
    "type": "<type_value>",
    "data": {{
        "key1": "value1",
        "key2": "value2",
        ...
    }}
}}

The "type" should be a single word that best describes the overall category of the information (e.g., "student", "course", "faculty", etc.).
The "data" object should contain all the extracted information as key-value pairs without any further nesting.

Here's the text to process:

{extracted_text}

Provide the output as a JSON object following the specified structure.
"""
        print("Sending request to Llama model...")
        curl_command = [
            "curl",
            OLLAMA_API_URL,
            "-d", json.dumps({
                "model": "llama3.1",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }),
            "-H", "Content-Type: application/json"
        ]

        result = subprocess.run(curl_command, capture_output=True, text=True)
        print(f"Model Response: {result.stdout}")

        if result.returncode != 0:
            print(f"Curl command failed: {result.stderr}")
            return {"error": f"Curl command failed: {result.stderr}"}

        try:
            response_data = json.loads(result.stdout)
            print("Parsing model response JSON...")

            if "message" in response_data and "content" in response_data["message"]:
                content = response_data["message"]["content"].strip()
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    structured_data = json.loads(json_match.group())
                    
                    # Ensure the structure is correct
                    if "type" in structured_data and "data" in structured_data:
                        print("Model returned valid structured data.")
                        structured_data["data"] = flatten_dict(structured_data["data"])
                    else:
                        print("Model did not return the correct structure. Fixing structure...")
                        structured_data = {
                            "type": "unknown",
                            "data": flatten_dict(structured_data)
                        }

                    print("Saving structured data...")
                    await save_structured_data(structured_data)
                    return structured_data

        except json.JSONDecodeError as e:
            print(f"Error decoding model response: {e}")
            return {"error": f"Invalid response format: {e}"}

        return {"error": "No valid JSON found in response"}

    except Exception as e:
        print(f"Error in Llama model processing: {str(e)}")
        return {"error": str(e)}

async def save_structured_data(data):
    try:
        if not data:
            print("No data to save.")
            return {"error": "No data to save"}

        os.makedirs(ARTIFACTS_DIR, exist_ok=True)

        # Wrap the structured data in an array
        output_data = [
            {
                "type": data.get("type", "unknown"),  # Use 'unknown' if type is not provided
                "data": flatten_dict(data.get("data", {}))  # Flatten the data object if needed
            }
        ]

        print(f"Saving data to {JSON_FILE_PATH}...")
        # Overwrite the file with the new data
        with open(JSON_FILE_PATH, 'w') as file:
            # Writing the export statement and the JSON object
            file.write("export const data = ")
            json.dump(output_data, file, indent=4)
            file.write(";\n")  # Ensure a newline after the JSON object
            file.write("export default data;\n")  # Add the export default statement

        print("Data successfully saved.")
        return {"success": "Data successfully saved."}
    except Exception as e:
        print(f"Failed to save structured data: {str(e)}")
        return {"error": f"Failed to save structured data: {str(e)}"}
