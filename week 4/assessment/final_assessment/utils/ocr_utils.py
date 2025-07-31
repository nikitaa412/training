import pytesseract
from pdf2image import convert_from_path
import os

def extract_text_from_document(file_path):
    pages = convert_from_path(file_path, poppler_path=r'C:\\Users\\NikitaRampurkarV-Sof\\Poppler\\poppler-24.08.0\\Library\\bin')
    if file_path.endswith('.pdf'):
        pages = convert_from_path(file_path)
        return "\n\n".join([pytesseract.image_to_string(page) for page in pages])
    else:
        return pytesseract.image_to_string(file_path)  # image case
