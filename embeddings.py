import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# def get_device():
#     if torch.cuda.is_available():
#         return "cuda"
#     elif torch.backends.mps.is_available():
#         return "mps"
    
#     return "cpu"

# device = get_device()
# print("Using device:", device)

# model = SentenceTransformer("BAAI/bge-small-en", device=device)

import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")

# EMBEDDING_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/BAAI/bge-small-en-v1.5"
EMBEDDING_URL = "https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5/pipeline/feature-extraction"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def get_embedding(texts):
    response = requests.post(
        EMBEDDING_URL,
        headers=headers,
        json={"inputs": texts}
    )

    # Handle cold start (very common on HF)
    if response.status_code == 503:
        import time
        time.sleep(5)
        return get_embedding(texts)

    response.raise_for_status()

    return response.json()


# def get_embedding_for_chunks(chunks):
#     texts = [chunk["text"] for chunk in chunks]

#     embeddings = model.encode(
#         texts,
#         batch_size=32,
#         show_progress_bar=True
#     )

#     return embeddings

def get_embedding_for_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = get_embedding(texts)

    return np.array(embeddings).astype("float32")


# def store_embeddings(embeddings, chunks):
#     dimension = embeddings.shape[1]

#     index = faiss.IndexFlatL2(dimension)
#     index.add(np.array(embeddings))

#     print("Total vectors:", index.ntotal)

#     with open("chunks.pkl", "wb") as f:
#         pickle.dump(chunks, f)

#     faiss.write_index(index, "faiss_index.bin")

def store_embeddings(embeddings, chunks):
    embeddings = np.array(embeddings).astype("float32")

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity
    index.add(embeddings)

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    faiss.write_index(index, "faiss_index.bin")
    

def load_embeddings_and_index(index_path="faiss_index.bin", metadata_path="chunks.pkl"):
    # Load FAISS index
    index = faiss.read_index(index_path)

    # Load metadata (chunks)
    with open(metadata_path, "rb") as f:
        chunks = pickle.load(f)

    print("Loaded:", index.ntotal, "vectors")

    return index, chunks


# def retrieve_context_from_query(query, 
#                                 index, 
#                                 chunks, 
#                                 top_k=5
#                                 ):
    
#     query_embedding = model.encode([query])

#     D, I = index.search(query_embedding, k=top_k)

#     results = []
#     for score, idx in zip(D[0], I[0]):
#         results.append({
#             "score": float(score), # Represents the L2 distance. Lower is better.
#             "chunk": chunks[idx]
#         })

#     return results

def retrieve_context_from_query(query, index, chunks, top_k=5):
    query_embedding = get_embedding([query])
    query_embedding = np.array(query_embedding).astype("float32")

    faiss.normalize_L2(query_embedding)

    D, I = index.search(query_embedding, k=top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({
            "score": float(score),  # cosine similarity (higher better)
            "chunk": chunks[idx]
        })

    return results


def filter_results(results, threshold=0.6):
    filtered = []

    for r in results:
        text = r["chunk"]["text"].strip()

        if r["score"] < threshold:
            continue

        if "TABLE OF CONTENTS" in r["chunk"]["section_path"]:
            continue

        if len(text) < 50:
            continue

        filtered.append(r)

    return filtered


def build_context(results, max_chunks=3):
    context_parts = []

    for r in results[:max_chunks]:
        sec = r["chunk"]["section_path"]
        text = r["chunk"]["text"]

        context_parts.append(f"[{sec}]\n{text}")

    return "\n\n".join(context_parts)
