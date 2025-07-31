import streamlit as st
import tempfile
import os

from agents.document_extractor import DocumentExtractor
from agents.policy_checker import PolicyChecker
from agents.fraud_detector import FraudDetector

st.set_page_config(page_title="Insurance Claim Validator", layout="centered")
st.title("Insurance Claim Validator")

# --- Step 1: Choose Input Method ---
st.markdown("### Step 1: Choose Input Method")
option = st.radio("Choose input type:", ["Upload Document", "Enter Manually"])

# --- Input for just 2 features used in model ---
def get_required_claim_inputs():
    patient_income = st.number_input("Patient Income", min_value=0, value=30000)
    claim_amount = st.number_input("Claim Amount", min_value=0, value=5000)
    return {
        "PatientIncome": patient_income,
        "ClaimAmount": claim_amount
    }

fraud = FraudDetector()  # Load once

# --- Upload Document Flow ---
if option == "Upload Document":
    uploaded_file = st.file_uploader("Upload Health Insurance Document", type=["pdf", "txt", "docx"])

    if uploaded_file:
        if st.button("Validate Document"):
            with st.spinner("Analyzing document..."):
                suffix = os.path.splitext(uploaded_file.name)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.read())
                    file_path = tmp.name

                extractor = DocumentExtractor()
                policy = PolicyChecker()

                doc_result = extractor.extract(file_path)
                if doc_result["status"] != "valid":
                    st.error(f"❌ Document Invalid: {doc_result['reason']}")
                else:
                    policy_result = policy.check(doc_result["text"])
                    if policy_result["status"] != "valid":
                        st.error(f"❌ Claim Rejected (Policy Issue): {policy_result['reason']}")
                    else:
                        st.success("✅ Document passed validation. Now enter claim details below.")
                        features = get_required_claim_inputs()
                        if st.button("Run Fraud Detection"):
                            result = fraud.predict(features)
                            if result["status"] == "legit":
                                st.success(f"✅ Claim Approved: {result['reason']}")
                            else:
                                st.error(f"❌ Claim Rejected (Fraud Detected): {result['reason']}")

# --- Manual Input Flow ---
elif option == "Enter Manually":
    st.markdown("### Step 2: Enter Claim Details")
    features = get_required_claim_inputs()
    if st.button("Run Fraud Detection"):
        with st.spinner("🔍 Detecting fraud..."):
            result = fraud.predict(features)
            if result["status"] == "legit":
                st.success(f"✅ Claim Approved: {result['reason']}")
            else:
                st.error(f"❌ Claim Rejected (Fraud Detected): {result['reason']}")
