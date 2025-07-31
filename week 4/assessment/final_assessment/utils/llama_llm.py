import requests

def llama_prompt(prompt, model="phi:2.7b", timeout=60):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )

        if response.status_code != 200:
            return f"LLM Error {response.status_code}: {response.text}"

        print("=== RAW LLaMA RESPONSE ===")
        print(response.text)

        json_data = response.json()
        result = json_data.get("response", "").strip()

        return result or "No explanation provided by the model."

    except requests.exceptions.Timeout:
        return "Timeout: The LLaMA model did not respond within the allotted time."
    except requests.exceptions.ConnectionError:
        return "Connection Error: Ensure the LLaMA model server is running at http://localhost:11434."
    except Exception as e:
        return f"Unexpected error communicating with the LLaMA model: {e}"
