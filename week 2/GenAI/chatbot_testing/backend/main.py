from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union

from shared.model_client import query_model
from shared.image_generator import generate_image

app = FastAPI()

# ---- Message Formats ----
class TextContent(BaseModel):
    type: str
    text: str

class ImageContent(BaseModel):
    type: str
    image_url: dict  # e.g., {"url": "data:image/png;base64,..."}

MessageContent = Union[TextContent, ImageContent]

class Message(BaseModel):
    role: str
    content: Union[str, List[MessageContent]]

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]

# ---- Chat Endpoint ----
@app.post("/chat")
async def chat(request: ChatRequest):
    last_msg = request.messages[-1]

    # If multimodal (image + text), route to model directly
    if isinstance(last_msg.content, list):
        return query_model(request.model, [msg.dict() for msg in request.messages])

    # Fallback: detect text-based image generation requests
    last_text = last_msg.content.lower()
    if "generate an image of" in last_text or "show me an image of" in last_text:
        image_url = generate_image(last_text)
        if isinstance(image_url, dict):  # Error
            return image_url
        return {"choices": [{"message": {"content": f"![Generated Image]({image_url})"}}]}

    # Normal chat
    return query_model(request.model, [msg.dict() for msg in request.messages])
