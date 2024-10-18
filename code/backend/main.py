from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pytesseract
import io
import os
import fitz
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# os.environ['TESSDATA_PREFIX']='/home/askeladd/anaconda3/share/tessdata' 

# CORS Middleware for frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers (authorization, content-type, etc.)
)

@app.post("/api/v1/uploads/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1].lower()
        
        if file_extension in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            # Process image files
            image_stream = io.BytesIO(await file.read())
            image = Image.open(image_stream)
            text = pytesseract.image_to_string(image, lang='eng')
            return {"file_type": "image", "text": text}
        
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

# def extract_text_from_pdf(pdf_stream):
#     """
#     Extracts text from a PDF file using PyMuPDF (fitz).
#     """
#     text = ""
#     with fitz.open(stream=pdf_stream, filetype="pdf") as pdf_document:
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)  # Load each page
#             text += page.get_text()  # Extract text from the page
#     return text

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

