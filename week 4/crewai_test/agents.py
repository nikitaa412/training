from crewai import Agent
from crewai_tools import PDFTool, RagTool
from model.fraud_model import FraudModel

# Ask the user to enter the PDF path
file_path = input("Enter the path to your PDF file: ")
pdf_tool = PDFTool(file_path=file_path)
rag_tool = RagTool()
fraud_model = FraudModel

# Create the document extractor
document_extractor = Agent (
    name="Document Extractor",
    role="Extracts structured data from medical claim documents.",
    goal="Identify key fields such as name, DOB, claim date, amount, and procedure from the PDF{pdf}.",
    verbose=True,
    memory=True,
    tools=[pdf_tool],
    backstory="An expert in reading and interpreting medical forms and documents.",
    allow_delegation=True
)

extracted_data = document_extractor.run("Extract structured claim data from the document.")
print("\nExtracted Data:\n", extracted_data)

#create a policy checker
policy_checker = Agent (
    name="Policy Checker",
    role="Verifies if claims are eligible under the given policy.",
    goal="Compare the extracted claim info with policy terms and conditions{t_and_c}.",
    verbose=True,
    memory=True,
    tools=[rag_tool],
    backstory="A meticulous analyst who knows every clause in a health insurance policy.",
    allow_delegation=True
)
policy_check = policy_checker.run(f"Check if this claim is valid based on policy terms: {extracted_data}")
print("\nPolicy Validation:\n", policy_check)

#create fraud detector
fraud_detector = Agent (
    name="Fraud Detector",
    role="Evaluates potential fraud in the insurance claim.",
    goal="Flag claims with anomalies or suspicious patterns.",
    verbose=True,
    memory=True,
    tools=[fraud_model],
    backstory="An investigator trained in identifying fraudulent claim behavior."
)