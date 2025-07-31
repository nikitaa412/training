from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Message(BaseModel):
    user_input: str

@app.post("/chat")
def chat_with_llama(message: Message):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2-vision:11b",
                "prompt": message.user_input,
                "stream": False
            }
        )
        data = response.json()
        reply = data.get("response", "Sorry, I didn't understand that.")
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
