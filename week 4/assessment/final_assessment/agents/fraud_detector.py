import pickle
import numpy as np
from utils.llama_llm import llama_prompt  # Your LLaMA client

class FraudDetector:
    def __init__(self):
        with open("models/lof_model.pkl", "rb") as f:
            self.model = pickle.load(f)
        with open("models/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

    def predict(self, features: dict):
        X = np.array([[features["PatientIncome"], features["ClaimAmount"]]])
        scaled = self.scaler.transform(X)
        prediction = self.model.predict(scaled)[0]

        # LOF usually: 1 = normal, -1 = anomaly
        status = "legit" if prediction == 1 else "fraud"

        prompt = (
            f"A medical insurance claim was classified as **{status}**.\n"
            f"Patient details:\n"
            f"- Patient Income: ${features['PatientIncome']}\n"
            f"- Claim Amount: ${features['ClaimAmount']}\n\n"
            f"As a medical insurance fraud expert, please provide a clear and concise explanation "
            f"why this claim might be considered {status}. "
            f"Provide specific factors related to the income and claim amount that influence the decision."
        )

        try:
            reason = llama_prompt(prompt)
        except Exception as e:
            reason = f"LLM error: {str(e)}"

        print("=== Prompt Sent to LLaMA ===\n", prompt)
        print("=== Response from LLaMA ===\n", reason)

        return {
            "status": status,
            "reason": reason.strip() or "No explanation provided by the model."
        }
