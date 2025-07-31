# tools/drug_info.py
from langchain.agents import Tool

def get_drug_info(name):
    return f"{name}: Common side effects include nausea and headache."

tool = Tool(
    name="Drug Info",
    func=get_drug_info,
    description="Returns drug usage, side effects, interactions."
)