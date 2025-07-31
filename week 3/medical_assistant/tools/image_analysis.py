from PIL import Image
from langchain.agents import Tool

def analyze_image(path):
    img = Image.open(path)
    return f"Image size: {img.size}. Content analysis not yet implemented."

tool = Tool(
    name="Image Analyzer",
    func=analyze_image,
    description="Analyzes uploaded medical images for insights."
)