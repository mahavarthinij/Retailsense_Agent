from rag.embedder import embed
from rag.vector_store import VectorStore

store = VectorStore()

def retrieve_context(query):
    q_emb = embed(query)
    return store.search(q_emb)
