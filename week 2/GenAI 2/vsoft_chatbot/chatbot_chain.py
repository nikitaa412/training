# chatbot_chain.py
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from llm_interface import get_llm

def get_chatbot_chain():
    embeddings = HuggingFaceEmbeddings()
    vectordb = Chroma(persist_directory="vsoft_chroma", embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    llm = get_llm()

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )
