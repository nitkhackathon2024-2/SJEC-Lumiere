from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pytesseract
import io
import fitz

app = FastAPI()

app.post("/api/v1/uploads/")
async def upload_fiel(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            image_stream = io.BytesIO(await file.read())
            image = Image.open(image_stream)
            text = pytesseract.image_to_string(image)
            return{"file_type": "image", "text": text}
        elif file_extension == "txt":
            # Process text files
            content = await file.read()
            text = content.decode("utf-8")
            return {"file_type": "text", "text": text}

        elif file_extension == "pdf":
            # Process PDF files
            pdf_stream = io.BytesIO(await file.read())
            text = extract_text_from_pdf(pdf_stream)
            return {"file_type": "pdf", "text": text}

        else:
            return {"error": "Unsupported file type"}

    except Exception as e:
        return {"error": str(e)}

def extract_text_from_pdf(pdf_stream):
    """
    Extracts text from a PDF file using PyMuPDF (fitz).
    """
    text = ""
    with fitz.open(stream=pdf_stream, filetype="pdf") as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Load each page
            text += page.get_text()  # Extract text from the page
    return text
