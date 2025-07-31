from langchain.agents import Tool

def suggest_tests(symptoms):
    if "chest pain" in symptoms:
        return "Recommend ECG and Troponin blood test."
    return "Further assessment needed."

tool = Tool(
    name="Clinical Decision Support",
    func=suggest_tests,
    description="Recommends tests based on clinical symptoms."
)