from utils.rag_utils import vector_search

def medical_doc_search_tool(query: str) -> str:
    return vector_search(query
    )