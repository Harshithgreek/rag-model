import json
import numpy as np
import faiss
from openai import OpenAI

client=OpenAI()
EMBEDDING_MODEL = "text-embedding-3-small"

def embed_texts(texts):
    Response = client.embeddings.create(input=texts, model=EMBEDDING_MODEL)
    vectors = [d.embedding for d in Response.data]
    arr=np.array(vectors, dtype="float32")
    faiss.normalize_L2(arr)
    return arr

def build_and_save_index(chunks, index_path, meta_path):
    vectors=embed_texts(chunks)
    dim=vectors.shape[1]

    index=faiss.IndexFlatIp(dim)
    index.add(vectors)

    faiss.write_index(index, index_path)
    index.add(vectors)

    faiss.write_index(index, index_path)
    
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks}, f, ensure_ascii=False, indent=2)

def load_index(index_path, meta_path):
    index=faiss.read_index(index_path)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta=json.load(f)
        chunks=meta["chunks"]

    return index, chunks