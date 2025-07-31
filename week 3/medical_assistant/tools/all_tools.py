from langchain.agents import Tool
from utils.rag_utils import (
    search_medical_docs,
    analyze_pdf,
    check_symptoms,
    get_drug_info,
    analyze_image
)

def medical_doc_search_tool(query: str) -> str:
    return search_medical_docs(query)

def analyze_pdf_tool(text: str) -> str:  # 🔄 renamed to avoid conflict
    return analyze_pdf(text)  # this now works correctly

def symptom_checker_tool(symptoms: str) -> str:
    return check_symptoms(symptoms)

def drug_info_tool(drug_query: str) -> str:
    return get_drug_info(drug_query)

def medical_image_analysis_tool(image_path: str) -> str:
    return analyze_image(image_path)

medical_search = Tool(
    name="Medical Document Search",
    func=medical_doc_search_tool,
    description="Search medical documents and provide relevant information."
)

document_analysis = Tool(
    name="Medical Summarize",
    func=analyze_pdf_tool,
    description="Summarize medical text or documents."
)

symptom_checker = Tool(
    name="Symptom Checker",
    func=symptom_checker_tool,
    description="Check symptoms and suggest possible conditions."
)

drug_info = Tool(
    name="Drug Info",
    func=drug_info_tool,
    description="Provide drug information and usage."
)

medical_image_analysis = Tool(
    name="Medical Image Analysis",
    func=medical_image_analysis_tool,
    description="Analyze medical images like scans or reports."
)

all_tools = [
    medical_search,
    document_analysis,
    symptom_checker,
    drug_info,
    medical_image_analysis
]