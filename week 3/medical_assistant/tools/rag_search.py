from langchain.agents import Tool

def ask_question(question):
    return f"This is a placeholder answer for '{question}'. RAG system not connected yet."

tool = Tool(
    name="Medical Literature Q&A",
    func=ask_question,
    description="Answers questions based on medical documents."
)