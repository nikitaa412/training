from utils.llama_llm import llama_prompt

class PolicyChecker:
    def check(self, text):
        prompt = f"Review this health insurance claim and determine if it complies with standard policy terms:\n\n{text}"
        result = llama_prompt(prompt)
        if 'yes' in result.lower() or 'complies' in result.lower():
            return {'status': 'valid'}
        return {'status': 'invalid', 'reason': result}
