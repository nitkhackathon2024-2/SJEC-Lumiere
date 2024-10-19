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
        # Extract file extension
        file_extension = file.filename.split(".")[-1].lower()
        
        # Process image files (jpg, jpeg, png, bmp, tiff)
        if file_extension in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            image_stream = io.BytesIO(await file.read())
            image = Image.open(image_stream)
            text = pytesseract.image_to_string(image, lang='eng')
        
        # Process text files
        elif file_extension == "txt":
            content = await file.read()
            text = content.decode("utf-8")
        
        # Process PDF files
        elif file_extension == "pdf":
            pdf_stream = io.BytesIO(await file.read())
            text = extract_text_from_pdf(pdf_stream)
        
        # Unsupported file type
        else:
            return {"error": "Unsupported file type"}
        
        # Pass the extracted text to the Llama model for structured data
        structured_data = await pass_to_llama_model(text)
        
        # Return the structured data as a JSON response
        if structured_data:
            return {
                "file_type": file_extension,
                "structured_data": structured_data  # This will be returned to the Next.js frontend
            }
        else:
            return {"error": "Failed to extract structured data from the text"}

    except Exception as e:
        return {"error": str(e)}

def extract_text_from_pdf(pdf_stream):
    """
    Extracts text from both native and image-based PDFs.
    """
    text = ""
    with fitz.open(stream=pdf_stream, filetype="pdf") as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            if page.get_text():
                text += page.get_text()
            else:
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    text += pytesseract.image_to_string(image)
    return text

def extract_first_json(response_text):
    """
    Extracts the first valid JSON object from a string by matching braces.
    """
    json_string = ""
    brace_count = 0
    in_json = False

    for char in response_text:
        if char == '{':
            if not in_json:
                in_json = True
            brace_count += 1
        if in_json:
            json_string += char
        if char == '}':
            brace_count -= 1
            if brace_count == 0:
                break

    return json_string if in_json and brace_count == 0 else None

# async def save_structured_data(data):
#     try:
#         if not data:
#             return {"error": "No data to save"}

#         os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        
#         # Overwrite the file with the new data
#         with open(JSON_FILE_PATH, 'w') as file:
#             json.dump(data, file, indent=4)

#         return {"success": "Data successfully saved."}
#     except Exception as e:
#         return {"error": f"Failed to save structured data: {str(e)}"}

def flatten_dict(data):
    """Flatten a nested dictionary into a single-level dictionary."""
    flat_dict = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in flatten_dict(value).items():
                flat_dict[f"{key}.{sub_key}"] = sub_value
        else:
            flat_dict[key] = value
    return flat_dict
async def save_structured_data(data):
    try:
        if not data:
            return {"error": "No data to save"}

        os.makedirs(ARTIFACTS_DIR, exist_ok=True)

        # Wrap the structured data in an array
        output_data = [
            {
                "type": data.get("type", "unknown"),  # Use 'unknown' if type is not provided
                "data": flatten_dict(data.get("data", {}))  # Flatten the data object if needed
            }
        ]

        # Overwrite the file with the new data
        with open(JSON_FILE_PATH, 'w') as file:
            # Writing the export statement and the JSON object
            file.write("export const data = ")
            json.dump(output_data, file, indent=4)
            file.write(";\n")  # Ensure a newline after the JSON object
            file.write("export default data;\n")  # Add the export default statement

        return {"success": "Data successfully saved."}
    except Exception as e:
        return {"error": f"Failed to save structured data: {str(e)}"}


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
            return {"error": f"Curl command failed: {result.stderr}"}

        try:
            response_data = json.loads(result.stdout)
            if "message" in response_data and "content" in response_data["message"]:
                content = response_data["message"]["content"].strip()
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    structured_data = json.loads(json_match.group())
                    
                    # Ensure the structure is correct
                    if "type" in structured_data and "data" in structured_data:
                        # Flatten the data object if it contains any nested structures
                        structured_data["data"] = flatten_dict(structured_data["data"])
                    else:
                        # If the model didn't provide the correct structure, create it
                        structured_data = {
                            "type": "unknown",
                            "data": flatten_dict(structured_data)
                        }
                    
                    await save_structured_data(structured_data)
                    return structured_data

        except json.JSONDecodeError as e:
            return {"error": f"Invalid response format: {e}"}

        return {"error": "No valid JSON found in response"}

    except Exception as e:
        return {"error": str(e)}

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)