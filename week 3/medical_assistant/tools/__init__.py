from .symptom_checker import check_symptoms
from .medical_search import medical_doc_search_tool
from .document_analysis import analyze_pdf

from langchain.agents import Tool

medical_doc_search_tool = Tool(
    name="Medical Document Search",
    func=medical_doc_search_tool,
    description="Search medical documents and provide relevant information."
)

analyze_pdf = Tool(
    name="Medical Summarize",
    func=analyze_pdf,
    description="Summarize medical text or documents."
)

check_symptoms = Tool(
    name="Symptom Checker",
    func= check_symptoms,
    description="Check symptoms and suggest possible conditions."
)

# Assume you have similar for drug info tool if separate

all_tools = [
    medical_doc_search_tool,
    analyze_pdf,
    check_symptoms,
]