import os
from rag2.rag_store import build_vector_store
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM

def ask_rag(question: str):
    BASE_DIR = os.getcwd()
    VECTOR_DIR = os.path.join(BASE_DIR, "rag", "vector_db")
    INDEX_FILE = os.path.join(VECTOR_DIR, "index.faiss")

    print("🔍 Looking for index at:", INDEX_FILE)

    if not os.path.exists(INDEX_FILE):
        print("⚠️ index.faiss NOT FOUND → building vector store")
        build_vector_store()

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    db = FAISS.load_local(
        VECTOR_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(question, k=3)
    context = "\n".join(d.page_content for d in docs)

    llm = OllamaLLM(model="mistral")

    prompt = f"""
    Use ONLY the context below.

    Context:
    {context}

    Question:
    {question}
    """

    return llm.invoke(prompt)
