import fitz  # PyMuPDF
import pytesseract
from PIL import Image


def extract_text_from_scanned_pdf(pdf_path):
    """Use OCR to extract text from a scanned PDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(img)
    return text
