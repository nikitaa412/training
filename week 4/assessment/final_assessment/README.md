# Insurance Claim Validator

A multi-agent AI system to validate health insurance claims using LLaMA + ML model (LOF).

## Agents:
- Document Extractor (OCR + LLaMA)
- Policy Checker (LLM-based)
- Fraud Detector (LOF model)

## How to Run
1. Train model:
   ```bash
   python models/train_lof_model.py
