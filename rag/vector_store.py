import json
import numpy as np

VECTOR_DB = "data/logs/vector_store.json"

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class VectorStore:

    def add(self, embedding, text):
        try:
            data = json.load(open(VECTOR_DB))
        except:
            data = []

        data.append({"embedding": embedding, "text": text})
        json.dump(data, open(VECTOR_DB, "w"))

    def search(self, query_embedding, top_k=3):
        data = json.load(open(VECTOR_DB))
        scored = [
            (cosine(query_embedding, d["embedding"]), d["text"])
            for d in data
        ]
        scored.sort(reverse=True)
        return [t for _, t in scored[:top_k]]
