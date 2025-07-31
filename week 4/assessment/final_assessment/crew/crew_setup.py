from crewai import Agent, Task, Crew
from agents.document_extractor import DocumentExtractor
from agents.policy_checker import PolicyChecker
from agents.fraud_detector import FraudDetector

# Wrappers for CrewAI agents
def get_document_extractor_agent():
    return Agent(
        role="Document Extractor",
        goal="Identify if uploaded document is a health insurance claim",
        backstory="Expert in OCR and document classification using LLM",
        verbose=True,
        tools=[],
        allow_delegation=False
    )

def get_policy_checker_agent():
    return Agent(
        role="Policy Checker",
        goal="Ensure the claim complies with insurance policy rules",
        backstory="Insurance policy specialist using LLM to interpret legal compliance",
        verbose=True,
        tools=[],
        allow_delegation=False
    )

def get_fraud_detector_agent():
    return Agent(
        role="Fraud Detector",
        goal="Detect fraudulent health insurance claims using ML",
        backstory="Expert in fraud detection using anomaly detection algorithms like LOF",
        verbose=True,
        tools=[],
        allow_delegation=False
    )

def run_claim_pipeline(file_path, claim_features):
    # Instantiate local logic modules
    doc_extractor = DocumentExtractor()
    policy_checker = PolicyChecker()
    fraud_detector = FraudDetector()

    # CrewAI Agents
    doc_agent = get_document_extractor_agent()
    policy_agent = get_policy_checker_agent()
    fraud_agent = get_fraud_detector_agent()

    # Tasks using actual Python logic (crew-ai v0.29+ supports tool/task invocation via function)
    def extract_task(_input):
        return doc_extractor.extract(file_path)

    def policy_task(_input):
        return policy_checker.check(_input["text"])

    def fraud_task(_input):
        return fraud_detector.predict(claim_features)

    # Define tasks
    task1 = Task(
        description="Check if uploaded document is a valid health insurance claim.",
        expected_output="Valid or Invalid document status with reason.",
        agent=doc_agent,
        function=extract_task
    )

    task2 = Task(
        description="Validate compliance of the claim with insurance policies.",
        expected_output="Compliant or Not compliant with reason.",
        agent=policy_agent,
        function=policy_task
    )

    task3 = Task(
        description="Run LOF model on claim features and return legitimacy.",
        expected_output="Legitimate or Fraud with reason.",
        agent=fraud_agent,
        function=fraud_task
    )

    # Create and run Crew
    crew = Crew(
        agents=[doc_agent, policy_agent, fraud_agent],
        tasks=[task1, task2, task3],
        verbose=True
    )

    return crew.kickoff()
