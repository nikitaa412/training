import requests

def llama_prompt(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
        "model": "llama3.2-vision",
        "prompt": prompt
        }
    )
    return response.json().get("response", "")
