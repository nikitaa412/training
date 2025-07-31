# ingest_web.py
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def ingest_websites():
    urls = [
        "https://www.vsoftconsulting.com",
        "https://www.vsoftconsulting.com/about/",
        "https://www.vsoftconsulting.com/services/",
        "https://www.vsoftconsulting.com/blog/",
        "https://www.vsoftconsulting.com/contact/"
    ]

    loader = WebBaseLoader(urls)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings()
    vectordb = Chroma.from_documents(split_docs, embeddings, persist_directory="vsoft_chroma")
    vectordb.persist()
    print(f"Ingested {len(split_docs)} chunks from VSoft website")

if __name__ == "__main__":
    ingest_websites()