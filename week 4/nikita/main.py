import sys
from agents.document_extractor import DocumentExtractor
from agents.policy_checker import PolicyChecker
from agents.fraud_detector import FraudDetector

def simulate_pipeline(file_path, claim_features):
    extractor = DocumentExtractor()
    policy = PolicyChecker()
    fraud = FraudDetector()

    print("\n1. Extracting Document...")
    result = extractor.extract(file_path)
    if result['status'] != 'valid':
        print("❌", result['reason'])
        return

    print("\n2. Checking Policy Compliance...")
    policy_result = policy.check(result['text'])
    if policy_result['status'] != 'valid':
        print("❌ Claim Rejected:", policy_result['reason'])
        return

    print("\n3. Detecting Fraud...")
    fraud_result = fraud.predict(claim_features)
    if fraud_result['status'] == 'legit':
        print("✅ Claim Approved:", fraud_result['reason'])
    else:
        print("❌ Claim Rejected:", fraud_result['reason'])

if __name__ == "__main__":
    file_path = sys.argv[1]  # pass file path as command line arg
    # Simulate claim features (replace with actual feature extraction logic)
    fake_features = {
        'age': 45,
        'hospital_days': 5,
        'claimed_amount': 5000,
        'num_prior_claims': 2
    }
    simulate_pipeline(file_path, fake_features)
