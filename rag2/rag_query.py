import os
import re
import json
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from rag2.rag_store import build_vector_store


# ---------- JSON EXTRACTOR (BULLETPROOF) ----------
def extract_json(text: str):
    if not text:
        return None

    # Remove markdown fences
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # ---- BALANCED JSON EXTRACTION ----
    brace_count = 0
    json_start = None

    for i, ch in enumerate(text):
        if ch == "{":
            if brace_count == 0:
                json_start = i
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count == 0 and json_start is not None:
                json_str = text[json_start:i+1]

                # Fix Python booleans → JSON booleans
                json_str = json_str.replace("True", "true").replace("False", "false")

                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    print("❌ JSON parse failed:", e)
                    return None

        return None


# ---------- NORMALIZER ----------
def normalize_decision(parsed):
    result = {}
    products = parsed.get("products", {})

    for pid, info in products.items():
        result[pid] = {
            "send_email": bool(info.get("send_email", False)),
            "reason": info.get("reason", "Stock below threshold")
        }

    return result



# ---------- MAIN RAG FUNCTION ----------
def ask_rag(question: str):
    BASE_DIR = os.getcwd()
    VECTOR_DIR = os.path.join(BASE_DIR, "rag", "vector_db")

    if not os.path.exists(os.path.join(VECTOR_DIR, "index.faiss")):
        build_vector_store()

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.load_local(
        VECTOR_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(question, k=3)
    context = "\n".join(d.page_content for d in docs)

    llm = OllamaLLM(model="phi")

    prompt = f"""
You are a STRICT JSON generator.

Rules:
- Return ONLY JSON
- No explanations
- No markdown
- No extra text

Context:
{context}

Return format:
{{
  "products": {{
    "PROD_1": {{"send_email": true, "reason": "text"}},
    "PROD_2": {{"send_email": false, "reason": "text"}}
  }}
}}
"""

    raw = llm.invoke(prompt, stop=["}"])
    raw = raw + "}"

    print("🤖 Raw LLM response:\n", raw)

    parsed = extract_json(raw)
    if not parsed:
        print("❌ Failed to extract JSON from RAG")
        return None

    return normalize_decision(parsed)

