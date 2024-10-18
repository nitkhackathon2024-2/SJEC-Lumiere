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
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers (authorization, content-type, etc.)
)

# OLLAMA_API_URL = "http://localhost:11434/api/chat"  # Ollama API URL (for curl)
# JSON_FILE_PATH = "structured_data.json"  # Path to save the structured data

@app.post("/api/v1/uploads/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1].lower()
        
        if file_extension in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            image_stream = io.BytesIO(await file.read())
            image = Image.open(image_stream)
            text = pytesseract.image_to_string(image, lang='eng')
        elif file_extension == "txt":
            content = await file.read()
            text = content.decode("utf-8")
        elif file_extension == "pdf":
            pdf_stream = io.BytesIO(await file.read())
            text = extract_text_from_pdf(pdf_stream)
        else:
            return {"error": "Unsupported file type"}

        structured_data = await pass_to_llama_model(text)
        return {"file_type": file_extension, "structured_data": structured_data}

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
            # If the page has selectable text, extract it
            if page.get_text():
                text += page.get_text()
            else:
                # If there's no selectable text, treat it as a scanned image
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))

                    # Use Tesseract to extract text from the image
                    text += pytesseract.image_to_string(image)

    return text

def extract_first_json(response_text):
    """
    Extracts the first valid JSON object from a string by matching braces.
    """
    json_string = ""
    brace_count = 0
    in_json = False

    # Iterate through the response character by character
    for char in response_text:
        if char == '{':
            if not in_json:
                in_json = True  # Start of a new JSON object
            brace_count += 1
        if in_json:
            json_string += char
        if char == '}':
            brace_count -= 1
            if brace_count == 0:
                break  # End of the first JSON object

    # Return the extracted JSON string if valid, else None
    return json_string if in_json and brace_count == 0 else None


# 

async def save_structured_data(data):
    try:
        if not data:
            return {"error": "No data to save"}

        os.makedirs(settings.ARTIFACTS_DIR, exist_ok=True)
        with open(settings.JSON_FILE_PATH, 'w') as file:
            json.dump([data], file, indent=4)

        return {"success": "Data successfully saved."}
    except Exception as e:
        return {"error": f"Failed to save structured data: {str(e)}"}


async def pass_to_llama_model(extracted_text):
    try:
        # ... rest of the function remains same ...
        curl_command = [
            "curl",
            settings.OLLAMA_API_URL,
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
                    await save_structured_data(structured_data)
                    return structured_data

        except json.JSONDecodeError as e:
            return {"error": f"Invalid response format: {e}"}

        return {"error": "No valid JSON found in response"}

    except Exception as e:
        return {"error": str(e)}