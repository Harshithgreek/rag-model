import numpy as np
import faiss
from openai import OpenAI

client = OpenAI()
CHAT_MODEL = "gpt-3.5-turbo"
EMBED_MODEL = "text-embedding-3-small"


def embed_query(query: str):
    resp = client.embeddings.create(model=EMBED_MODEL, input=[query])
    vec = np.array([resp.data[0].embedding], dtype="float32")
    faiss.normalize_L2(vec)
    return vec


def retrieve(query, index, chunks, k=4):
    qvec = embed_query(query)
    _, ids = index.search(qvec, k)

    results = []
    for i in ids[0]:
        if i != -1:
            results.append(chunks[i])

    return results


def generate_answer(user_question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Use only the provided context to answer. If the answer is not present, say you do not have it."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_question}"}
        ]
    )

    return response.choices[0].message.content