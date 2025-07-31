from langchain.agents import Tool

def check_symptoms(text):
    if "fever" in text and "cough" in text:
        return "Possible flu or COVID-19. Please consult a doctor."
    return "Cannot determine. Please consult a healthcare provider."

tool = Tool(
    name="Symptom Checker",
    func=check_symptoms,
    description="Analyzes symptoms to suggest possible conditions."
)