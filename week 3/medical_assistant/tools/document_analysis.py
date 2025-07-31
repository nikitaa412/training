import fitz  # PyMuPDF
from langchain.agents import Tool

def analyze_pdf(path):
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    return f"Extracted {len(text)} characters. Summary:\n{text[:500]}..."

tool = Tool(
    name="Medical Report Analyzer",
    func=analyze_pdf,
    description="Analyzes uploaded PDF medical reports and summarizes findings."
)