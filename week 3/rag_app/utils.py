from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_and_chunk(file_path):
    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages])
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    return [{"text": chunk} for chunk in chunks]

def call_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
