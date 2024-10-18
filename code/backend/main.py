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

app = FastAPI()

# CORS Middleware for frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers (authorization, content-type, etc.)
)

OLLAMA_API_URL = "http://localhost:11434/api/chat"  # Ollama API URL (for curl)
JSON_FILE_PATH = "structured_data.json"  # Path to save the structured data

@app.post("/api/v1/uploads/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1].lower()
        
        if file_extension in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            # Process image files
            image_stream = io.BytesIO(await file.read())
            image = Image.open(image_stream)
            text = pytesseract.image_to_string(image, lang='eng')
            structured_data = await pass_to_llama_model(text)
            await save_structured_data(structured_data)
            return {"file_type": "image", "structured_data": structured_data}
        
        elif file_extension == "txt":
            # Process text files
            content = await file.read()
            text = content.decode("utf-8")
            structured_data = await pass_to_llama_model(text)
            await save_structured_data(structured_data)
            return {"file_type": "text", "structured_data": structured_data}
        
        elif file_extension == "pdf":
            # Process PDF files
            pdf_stream = io.BytesIO(await file.read())
            text = extract_text_from_pdf(pdf_stream)
            structured_data = await pass_to_llama_model(text)
            await save_structured_data(structured_data)
            return {"file_type": "pdf", "structured_data": structured_data}
        
        else:
            return {"error": "Unsupported file type"}

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
            in_json = True
            brace_count += 1
        if in_json:
            json_string += char
        if char == '}':
            brace_count -= 1
            if brace_count == 0:
                break  # End of the first JSON object

    # Return the extracted JSON string if valid, else None
    return json_string if in_json and brace_count == 0 else None

def save_structured_data(data, file_path="structured_data.json"):
    """
    Saves the structured data into a JSON file. If the file already exists, it appends and updates it.
    
    :param data: The structured JSON data to be saved.
    :param file_path: The path to the JSON file (default: 'structured_data.json').
    """
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Read existing data from the file
            with open(file_path, 'r') as file:
                try:
                    existing_data = json.load(file)
                    if isinstance(existing_data, list):
                        existing_data.append(data)
                    else:
                        existing_data = [existing_data, data]
                except json.JSONDecodeError:
                    existing_data = [data]
        else:
            existing_data = [data]

        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

        return {"success": "Data successfully saved."}

    except Exception as e:
        return {"error": f"Failed to save structured data: {str(e)}"}


# async def pass_to_llama_model(extracted_text):
#     try:

#         print(extracted_text)
#         # Construct the curl command to send the extracted text to llama3.1
#         curl_command = [
#             "curl",
#             "http://localhost:11434/api/chat",
#             "-d", json.dumps({
#                 "model": "llama3.1",
#                 "messages": [{"role": "user", "content": extracted_text}]
#             }),
#               "-H", "Content-Type: application/json"    
#         ]

#         # Run the curl command and capture the output
#         result = subprocess.run(curl_command, capture_output=True, text=True)

#         # Check if the request was successful
#         if result.returncode != 0:
#             return {"error": "Failed to communicate with llama3.1 model"}

#         # Print the raw response for debugging
#         response = result.stdout
#         print("Raw response:", response)  # Debugging step

#         # Try to decode the response as JSON
#         try:
#             response_data = json.loads(response)
#         except json.JSONDecodeError as e:
#             # If there's a JSON decoding error, return the raw response for further debugging
#             return {"error": f"JSON decode error: {str(e)}", "raw_response": response}

#         # Check for a valid message in the response
#         if "message" in response_data and "content" in response_data["message"]:
#             json_string = response_data["message"]["content"]

#             # Load the structured JSON data from the content
#             structured_data = json.loads(json_string)

#             # Save the structured data to a file (synchronous call without await)
#             save_result = save_structured_data(structured_data)

#             # Return the result of the save operation
#             print('save:', save_result)
#             return save_result
#         else:
#             return {"error": "No structured content found in response"}

#     except Exception as e:
#         return {"error": str(e)}

async def pass_to_llama_model(extracted_text):
    try:
        # Print extracted text for debugging
        print(extracted_text)
        
        # Construct the curl command to send the extracted text to the Llama model
        curl_command = [
            "curl",
            OLLAMA_API_URL,  # Use the URL variable defined earlier
            "-d", json.dumps({
                "model": "llama3.1",
                "messages": [{"role": "user", "content": extracted_text}]
            }),
            "-H", "Content-Type: application/json"
        ]

        # Run the curl command and capture the output
        result = subprocess.run(curl_command, capture_output=True, text=True)

        # Check if the curl command succeeded
        if result.returncode != 0:
            return {"error": "Failed to communicate with llama3.1 model"}

        # Capture the raw response from the model
        response = result.stdout
        print("Raw response:", response)  # Debugging output
        
        # Initialize a variable to accumulate the content
        full_response_content = ""

        # Split the response by lines (since it's coming in parts)
        for line in response.splitlines():
            try:
                # Parse each line as JSON
                line_data = json.loads(line)
                if "message" in line_data and "content" in line_data["message"]:
                    # Append the content to the full response
                    full_response_content += line_data["message"]["content"]
            except json.JSONDecodeError:
                # Skip lines that are not valid JSON
                continue

        # At this point, we have the full accumulated content
        print("Full response content:", full_response_content)  # Debugging step

        # You can now pass this full content to any further processing or save it
        structured_data = {"content": full_response_content}
        
        # Save the structured data to a file
        save_result = save_structured_data(structured_data)

        # Return the result of the save operation
        return {"success": "Data processed successfully", "structured_data": structured_data}

    except Exception as e:
        return {"error": str(e)}
