import requests

MODEL_SERVER_URL = "http://localhost:11434/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json"
    # Add Authorization header if needed
}

def query_model(model: str, messages: list):
    payload = {
        "model": model,
        "messages": messages
    }
    try:
        response = requests.post(MODEL_SERVER_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}