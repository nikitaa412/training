import weaviate
from sentence_transformers import SentenceTransformer

client = weaviate.Client("https://YOUR-WEAVIATE-INSTANCE")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def upsert_chunks(chunks):
    for c in chunks:
        vec = embedder.encode(c['text']).tolist()
        client.data_object.create({
            "text": c['text']
        }, class_name="Document", vector=vec)

def retrieve_chunks(query, top_k=5):
    vec = embedder.encode(query).tolist()
    result = client.query.get("Document", ["text"])\
        .with_near_vector({"vector": vec})\
        .with_limit(top_k).do()
    return [{"text": d["text"]} for d in result["data"]["Get"]["Document"]]
