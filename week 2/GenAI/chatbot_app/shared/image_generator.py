import requests

def generate_image(prompt: str):
    payload = {
        "model": "llama3.2-vision:11b",  # or another model name
        "prompt": prompt,
        "mode": "image"
    }
    try:
        response = requests.post("http://localhost:11434/v1/generate", json=payload)
        response.raise_for_status()
        return response.json().get("image_url")  # Adjust based on actual model output
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}