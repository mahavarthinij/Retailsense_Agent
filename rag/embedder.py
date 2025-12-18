import subprocess

def embed(text: str) -> list:
    prompt = f"Generate embedding for:\n{text}"
    result = subprocess.run(
        ["ollama", "run", "nomic-embed-text"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return eval(result.stdout)
