from langchain.agents import Tool

def lookup_condition(name):
    return f"{name}: A medical condition characterized by various symptoms and causes."

tool = Tool(
    name="Condition Lookup",
    func=lookup_condition,
    description="Provides definitions and information about medical conditions."
)