import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\NikitaRampurkarV-Sof\AppData\Local\Programs\Tesseract-OCR'
from pdf2image import convert_from_path
import os

def extract_text_from_document(file_path):
    if file_path.endswith('.pdf'):
        pages = convert_from_path(file_path)
        return "\n\n".join([pytesseract.image_to_string(page) for page in pages])
    return pytesseract.image_to_string(file_path)  # image case
