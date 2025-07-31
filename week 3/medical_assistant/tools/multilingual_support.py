from langchain.agents import Tool
from deep_translator import GoogleTranslator

def translate_to_english(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

tool = Tool(
    name="Translator",
    func=translate_to_english,
    description="Translates any language into English."
)