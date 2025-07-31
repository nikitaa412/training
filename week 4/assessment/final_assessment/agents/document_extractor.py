from utils.ocr_utils import extract_text_from_document
from utils.llama_llm import llama_prompt

class DocumentExtractor:
    def extract(self, file_path):
        text = extract_text_from_document(file_path)
        check_prompt = f"Is the following text from a health insurance claim document?\n\n{text}\n\nAnswer yes or no."
        result = llama_prompt(check_prompt)
        if 'yes' in result.lower():
            return {'status': 'valid', 'text': text}
        return {'status': 'invalid', 'reason': 'Not a health insurance claim document.'}
