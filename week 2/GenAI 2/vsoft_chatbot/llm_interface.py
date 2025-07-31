# llm_interface.py
from langchain.llms.base import LLM
import requests

class LLaMA3VisionLLM(LLM):
    def _call(self, prompt, stop=None):
        response = requests.post(
            "http://localhost:11434/api/generate",  # Replace if different port
            json={
                "model": "llama3.2-vision:11b",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

    @property
    def _llm_type(self):
        return "llama3.2-vision"

def get_llm():
    return LLaMA3VisionLLM()
