import subprocess
from rag.retriever import retrieve_context

def decide(action_context):
    retrieved = retrieve_context(action_context)

    prompt = f"""
You are a retail decision agent.

Past context:
{retrieved}

Current situation:
{action_context}

Answer YES or NO:
Should we send alert?
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore",
    )
    return result.stdout.strip()
