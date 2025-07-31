from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from shared.model_client import query_model
from shared.image_generator import generate_image

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]

@app.post("/chat")
async def chat(request: ChatRequest):
    last_message = request.messages[-1].content.lower()

    # Naive image trigger detection
    if "generate an image of" in last_message or "show me an image of" in last_message:
        image_url = generate_image(last_message)
        if isinstance(image_url, dict):  # Error
            return image_url
        return {"choices": [{"message": {"content": f"![Generated Image]({image_url})"}}]}

    # Regular chat
    return query_model(request.model, [msg.dict() for msg in request.messages])