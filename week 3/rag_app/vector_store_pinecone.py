import os
import pinecone
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))
index = pinecone.Index(os.getenv("PINECONE_INDEX"))
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def upsert_chunks(chunks):
    vectors = [(str(i), embedder.encode(c['text']).tolist(), {"text": c['text']}) for i, c in enumerate(chunks)]
    index.upsert(vectors=vectors)

def retrieve_chunks(query, top_k=5):
    vec = embedder.encode(query).tolist()
    res = index.query(vector=vec, top_k=top_k, include_metadata=True)
    return res['matches']
