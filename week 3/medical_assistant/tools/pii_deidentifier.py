from langchain.agents import Tool
import re

def remove_pii(text):
    return re.sub(r"\b(?:Name|DOB|SSN):\s*\S+\b", "[REDACTED]", text)

tool = Tool(
    name="PII Deidentifier",
    func=remove_pii,
    description="Removes personally identifiable info (PII) from text."
)