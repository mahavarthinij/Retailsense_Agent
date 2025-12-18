import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

import pandas as pd

def build_vector_store():
    print("🛠️ build_vector_store() CALLED")

    BASE_DIR = os.getcwd()
    VECTOR_DIR = os.path.join(BASE_DIR, "rag", "vector_db")

    print("📍 Current working dir:", BASE_DIR)
    print("📂 Vector dir:", VECTOR_DIR)

    os.makedirs(VECTOR_DIR, exist_ok=True)

    df = pd.read_csv(r"D:\orchestrator_core\data\live\inventory.csv")

    docs = []
    for _, row in df.iterrows():
        docs.append(
            Document(
                page_content=f"Product {row.product_id} has stock {row.stock_quantity} and threshold {row.threshold}"
            )
        )

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTOR_DIR)

    print("✅ Vector store SAVED at:", VECTOR_DIR)
