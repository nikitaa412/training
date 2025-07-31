import requests

def generate_marketing_content(prompt, model='qwen2.5-coder:0.5b'):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No content received.")
    except Exception as e:
        return f"Error: {str(e)}"
