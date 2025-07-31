import networkx as nx
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load embedder
embedder = SentenceTransformer('mxbai-embed-large')

# Build a simple graph
G = nx.DiGraph()
G.add_edge("Einstein", "Relativity", relation="developed", year=1905)
G.add_edge("Relativity", "Physics", relation="part_of", year=None)
G.add_edge("Einstein", "Quantum Theory", relation="contributed_to", year=1905)

# Prepare nodes with context
nodes = list(G.nodes)
node_texts = [f"{node} — {'; '.join([f'{G.edges[e]['relation']} {e[1]}' for e in G.edges(node)])}"
              for node in nodes]

# Create embeddings
embeddings = embedder.encode(node_texts, normalize_embeddings=True)
embedding_dim = embeddings.shape[1]

# Save embeddings in FAISS index
index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(embeddings))

# Save objects
with open("nodes.pkl", "wb") as f:
    pickle.dump((G, nodes, node_texts), f)
faiss.write_index(index, "index.faiss")
