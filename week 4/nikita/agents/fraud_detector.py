import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

class FraudDetector:
    def __init__(self):
        self.model = joblib.load('models/lof_model.pkl')
        self.scaler = joblib.load('models/scaler.pkl')

    def predict(self, claim_features: dict):
        values = np.array([list(claim_features.values())])
        scaled = self.scaler.transform(values)
        prediction = self.model.predict(scaled)
        return {
            'status': 'legit' if prediction[0] == 1 else 'fraud',
            'reason': 'Legitimate claim' if prediction[0] == 1 else 'Suspicious pattern detected (potential fraud)'
        }
