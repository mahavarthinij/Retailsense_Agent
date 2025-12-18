from rag2.rag_store import build_vector_store
from rag2.rag_query import ask_rag

print("🚀 Testing RAG module")

build_vector_store()

response = ask_rag(
    "What happens when product stock goes below threshold?"
)

print("\n🧠 RAG Answer:\n", response)
