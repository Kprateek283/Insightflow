import os
import faiss
import numpy as np
import cohere
from typing import List
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)
EMBED_MODEL = "embed-english-v3.0"

INDEX_DIR = "app/vectorstore/indexes"
os.makedirs(INDEX_DIR, exist_ok=True)

# 🔹 Generate embedding for a question
async def generate_question_embedding(question: str) -> np.ndarray:
    try:
        response = co.embed(texts=[question], model=EMBED_MODEL, input_type='search_query')
        return np.array(response.embeddings).astype("float32")
    except Exception as e:
        print(f"[Cohere Error] Question Embedding Failed: {e}")
        raise

# 🔹 Generate embeddings for a list of chunks
async def generate_embeddings(chunks: List[str]) -> np.ndarray:
    try:
        response = co.embed(texts=chunks, model=EMBED_MODEL, input_type='search_document')
        return np.array(response.embeddings).astype("float32")
    except Exception as e:
        print(f"[Cohere Error] Chunk Embedding Failed: {e}")
        raise

# 🔹 Save FAISS index
async def save_faiss_index(doc_id: str, embeddings: np.ndarray):
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    index_path = os.path.join(INDEX_DIR, f"{doc_id}.faiss")
    faiss.write_index(index, index_path)

# 🔹 Generate & Save FAISS index for chunks
async def add_document_embeddings(doc_id: str, chunks: List[str]):
    embeddings = await generate_embeddings(chunks)
    await save_faiss_index(doc_id, embeddings)

# 🔹 Search FAISS index by question embedding
async def search_faiss_by_document(document_id: str, query_embedding: np.ndarray, top_k: int = 5) -> List[dict]:
    index_path = os.path.join(INDEX_DIR, f"{document_id}.faiss")
    if not os.path.exists(index_path):
        return []

    index = faiss.read_index(index_path)
    distances, indices = index.search(query_embedding, top_k)

    # ⚠️ Replace with logic to get actual text for each index
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        chunk_text = f"[Chunk {idx}] Placeholder text"  # TODO: link to actual chunk
        results.append({"text": chunk_text, "distance": dist})

    return results
