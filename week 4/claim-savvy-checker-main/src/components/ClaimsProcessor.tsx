
import React, { useEffect, useState } from 'react';
import { Play, Loader2, Brain, Shield, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

interface ClaimData {
  claim_id: string;
  patient: string;
  service_date: string;
  diagnosis_code: string;
  procedure_code: string;
  provider: string;
  policy_number: string;
  amount: number;
  text: string;
}

interface ValidationResult {
  claim_id: string;
  patient: string;
  issue: string;
  action: string;
  severity: 'low' | 'medium' | 'high';
  status: 'pending' | 'approved' | 'rejected';
}

interface ClaimsProcessorProps {
  claims: ClaimData[];
  isProcessing: boolean;
  onStartValidation: () => void;
  onValidationComplete: (results: ValidationResult[]) => void;
}

// Mock policy database
const policyDatabase = {
  "POL-1000": { start_date: "2023-05-12", end_date: "2025-01-11", coverage_limits: { max_annual: 5000 } },
"POL-1001": { start_date: "2024-01-28", end_date: "2025-09-03", coverage_limits: { max_annual: 10000 } },
"POL-1002": { start_date: "2024-10-09", end_date: "2025-03-23", coverage_limits: { max_annual: 3000 } },
"POL-1003": { start_date: "2023-03-02", end_date: "2025-03-31", coverage_limits: { max_annual: 8000 } },
"POL-1004": { start_date: "2024-12-23", end_date: "2025-08-22", coverage_limits: { max_annual: 2000 } },
"POL-1005": { start_date: "2024-04-14", end_date: "2026-11-27", coverage_limits: { max_annual: 5000 } },
"POL-1006": { start_date: "2024-06-10", end_date: "2025-10-11", coverage_limits: { max_annual: 10000 } },
"POL-1007": { start_date: "2023-03-26", end_date: "2026-05-31", coverage_limits: { max_annual: 8000 } },
"POL-1008": { start_date: "2024-07-12", end_date: "2025-10-30", coverage_limits: { max_annual: 10000 } },
"POL-1009": { start_date: "2024-11-05", end_date: "2026-03-15", coverage_limits: { max_annual: 3000 } },
"POL-1010": { start_date: "2023-07-28", end_date: "2025-01-25", coverage_limits: { max_annual: 8000 } },
"POL-1011": { start_date: "2023-01-23", end_date: "2025-05-29", coverage_limits: { max_annual: 2000 } },
"POL-1012": { start_date: "2024-10-17", end_date: "2026-03-05", coverage_limits: { max_annual: 3000 } },
"POL-1013": { start_date: "2024-03-09", end_date: "2025-07-16", coverage_limits: { max_annual: 10000 } },
"POL-1014": { start_date: "2024-02-01", end_date: "2025-01-27", coverage_limits: { max_annual: 3000 } },
"POL-1015": { start_date: "2024-12-13", end_date: "2025-09-21", coverage_limits: { max_annual: 5000 } },
"POL-1016": { start_date: "2023-06-18", end_date: "2026-12-28", coverage_limits: { max_annual: 8000 } },
"POL-1017": { start_date: "2024-10-27", end_date: "2026-06-19", coverage_limits: { max_annual: 10000 } },
"POL-1018": { start_date: "2024-11-07", end_date: "2026-07-22", coverage_limits: { max_annual: 8000 } },
"POL-1019": { start_date: "2023-09-13", end_date: "2025-07-01", coverage_limits: { max_annual: 2000 } },
"POL-1020": { start_date: "2023-06-06", end_date: "2025-03-07", coverage_limits: { max_annual: 3000 } },
"POL-1021": { start_date: "2024-08-20", end_date: "2025-10-23", coverage_limits: { max_annual: 5000 } },
"POL-1022": { start_date: "2023-08-17", end_date: "2025-09-05", coverage_limits: { max_annual: 8000 } },
"POL-1023": { start_date: "2024-04-08", end_date: "2025-03-12", coverage_limits: { max_annual: 3000 } },
"POL-1024": { start_date: "2023-02-10", end_date: "2026-06-02", coverage_limits: { max_annual: 5000 } },
"POL-1025": { start_date: "2024-07-21", end_date: "2025-02-05", coverage_limits: { max_annual: 8000 } },
"POL-1026": { start_date: "2024-12-19", end_date: "2026-05-26", coverage_limits: { max_annual: 2000 } },
"POL-1027": { start_date: "2023-01-07", end_date: "2025-04-14", coverage_limits: { max_annual: 10000 } },
"POL-1028": { start_date: "2024-11-30", end_date: "2025-08-17", coverage_limits: { max_annual: 8000 } },
"POL-1029": { start_date: "2024-05-05", end_date: "2026-12-25", coverage_limits: { max_annual: 2000 } },
"POL-1030": { start_date: "2023-06-01", end_date: "2025-12-30", coverage_limits: { max_annual: 10000 } },
"POL-1031": { start_date: "2023-08-04", end_date: "2026-04-04", coverage_limits: { max_annual: 5000 } },
"POL-1032": { start_date: "2024-01-12", end_date: "2025-12-01", coverage_limits: { max_annual: 3000 } },
"POL-1033": { start_date: "2023-10-23", end_date: "2026-02-22", coverage_limits: { max_annual: 8000 } },
"POL-1034": { start_date: "2023-12-18", end_date: "2026-11-05", coverage_limits: { max_annual: 3000 } },
"POL-1035": { start_date: "2024-06-06", end_date: "2025-12-06", coverage_limits: { max_annual: 10000 } },
"POL-1036": { start_date: "2023-04-22", end_date: "2025-10-03", coverage_limits: { max_annual: 5000 } },
"POL-1037": { start_date: "2023-11-01", end_date: "2025-03-22", coverage_limits: { max_annual: 2000 } },
"POL-1038": { start_date: "2023-10-06", end_date: "2025-01-15", coverage_limits: { max_annual: 8000 } },
"POL-1039": { start_date: "2023-05-20", end_date: "2026-09-06", coverage_limits: { max_annual: 3000 } },
"POL-1040": { start_date: "2024-09-30", end_date: "2026-08-19", coverage_limits: { max_annual: 8000 } },
"POL-1041": { start_date: "2024-07-16", end_date: "2025-08-14", coverage_limits: { max_annual: 3000 } },
"POL-1042": { start_date: "2023-06-28", end_date: "2025-02-13", coverage_limits: { max_annual: 5000 } },
"POL-1043": { start_date: "2024-06-24", end_date: "2025-07-04", coverage_limits: { max_annual: 8000 } },
"POL-1044": { start_date: "2023-12-25", end_date: "2025-07-15", coverage_limits: { max_annual: 2000 } },
"POL-1045": { start_date: "2024-09-22", end_date: "2025-02-20", coverage_limits: { max_annual: 10000 } },
"POL-1046": { start_date: "2024-08-11", end_date: "2025-04-02", coverage_limits: { max_annual: 8000 } },
"POL-1047": { start_date: "2024-02-21", end_date: "2025-05-26", coverage_limits: { max_annual: 5000 } },
"POL-1048": { start_date: "2023-03-30", end_date: "2025-06-05", coverage_limits: { max_annual: 3000 } },
"POL-1049": { start_date: "2023-07-11", end_date: "2025-11-12", coverage_limits: { max_annual: 10000 } },
"POL-1050": { start_date: "2023-02-15", end_date: "2025-10-09", coverage_limits: { max_annual: 8000 } },
"POL-1051": { start_date: "2024-03-11", end_date: "2026-01-18", coverage_limits: { max_annual: 2000 } },
"POL-1052": { start_date: "2023-05-03", end_date: "2025-08-27", coverage_limits: { max_annual: 5000 } },
"POL-1053": { start_date: "2024-11-13", end_date: "2026-10-24", coverage_limits: { max_annual: 3000 } },
"POL-1054": { start_date: "2023-09-01", end_date: "2026-04-29", coverage_limits: { max_annual: 10000 } },
"POL-1055": { start_date: "2024-04-03", end_date: "2026-08-14", coverage_limits: { max_annual: 5000 } },
"POL-1056": { start_date: "2023-06-17", end_date: "2025-01-01", coverage_limits: { max_annual: 3000 } },
"POL-1057": { start_date: "2024-02-05", end_date: "2026-07-19", coverage_limits: { max_annual: 8000 } },
"POL-1058": { start_date: "2023-08-07", end_date: "2025-12-06", coverage_limits: { max_annual: 5000 } },
"POL-1059": { start_date: "2024-07-04", end_date: "2025-03-21", coverage_limits: { max_annual: 2000 } },
"POL-1060": { start_date: "2023-04-11", end_date: "2025-09-17", coverage_limits: { max_annual: 10000 } },
"POL-1061": { start_date: "2024-10-15", end_date: "2026-06-04", coverage_limits: { max_annual: 5000 } },
"POL-1062": { start_date: "2024-05-24", end_date: "2025-08-02", coverage_limits: { max_annual: 3000 } },
"POL-1063": { start_date: "2023-01-14", end_date: "2025-11-29", coverage_limits: { max_annual: 8000 } },
"POL-1064": { start_date: "2024-12-07", end_date: "2026-03-09", coverage_limits: { max_annual: 5000 } },
"POL-1065": { start_date: "2023-11-10", end_date: "2025-05-13", coverage_limits: { max_annual: 2000 } },
"POL-1066": { start_date: "2023-03-06", end_date: "2026-02-26", coverage_limits: { max_annual: 8000 } },
"POL-1067": { start_date: "2024-01-19", end_date: "2025-10-12", coverage_limits: { max_annual: 10000 } },
"POL-1068": { start_date: "2023-10-03", end_date: "2025-01-04", coverage_limits: { max_annual: 3000 } },
"POL-1069": { start_date: "2023-09-25", end_date: "2026-05-08", coverage_limits: { max_annual: 10000 } },
"POL-1070": { start_date: "2024-03-30", end_date: "2026-11-18", coverage_limits: { max_annual: 2000 } },
"POL-1071": { start_date: "2023-12-29", end_date: "2025-06-27", coverage_limits: { max_annual: 8000 } },
"POL-1072": { start_date: "2023-07-18", end_date: "2025-10-16", coverage_limits: { max_annual: 3000 } },
"POL-1073": { start_date: "2024-06-13", end_date: "2026-09-13", coverage_limits: { max_annual: 5000 } },
"POL-1074": { start_date: "2024-05-15", end_date: "2025-07-19", coverage_limits: { max_annual: 2000 } },
"POL-1075": { start_date: "2023-02-19", end_date: "2025-03-29", coverage_limits: { max_annual: 8000 } },
"POL-1076": { start_date: "2024-02-09", end_date: "2025-12-03", coverage_limits: { max_annual: 3000 } },
"POL-1077": { start_date: "2023-06-09", end_date: "2025-11-24", coverage_limits: { max_annual: 5000 } },
"POL-1078": { start_date: "2024-07-06", end_date: "2026-01-14", coverage_limits: { max_annual: 8000 } },
"POL-1079": { start_date: "2023-10-26", end_date: "2026-12-16", coverage_limits: { max_annual: 10000 } },
"POL-1080": { start_date: "2024-08-03", end_date: "2025-05-10", coverage_limits: { max_annual: 2000 } },
"POL-1081": { start_date: "2024-10-19", end_date: "2026-08-31", coverage_limits: { max_annual: 5000 } },
"POL-1082": { start_date: "2023-07-25", end_date: "2025-02-28", coverage_limits: { max_annual: 3000 } },
"POL-1083": { start_date: "2024-12-05", end_date: "2026-04-27", coverage_limits: { max_annual: 10000 } },
"POL-1084": { start_date: "2023-03-18", end_date: "2025-09-23", coverage_limits: { max_annual: 5000 } },
"POL-1085": { start_date: "2024-09-08", end_date: "2025-06-08", coverage_limits: { max_annual: 8000 } },
"POL-1086": { start_date: "2023-04-06", end_date: "2025-10-28", coverage_limits: { max_annual: 2000 } },
"POL-1087": { start_date: "2024-06-16", end_date: "2026-05-16", coverage_limits: { max_annual: 3000 } },
"POL-1088": { start_date: "2024-11-09", end_date: "2025-01-22", coverage_limits: { max_annual: 10000 } },
"POL-1089": { start_date: "2023-01-10", end_date: "2025-11-20", coverage_limits: { max_annual: 5000 } },
"POL-1090": { start_date: "2024-07-30", end_date: "2025-04-01", coverage_limits: { max_annual: 2000 } },
"POL-1091": { start_date: "2023-08-15", end_date: "2025-08-20", coverage_limits: { max_annual: 3000 } },
"POL-1092": { start_date: "2023-09-04", end_date: "2026-07-17", coverage_limits: { max_annual: 8000 } },
"POL-1093": { start_date: "2024-05-09", end_date: "2026-03-20", coverage_limits: { max_annual: 10000 } },
"POL-1094": { start_date: "2024-02-28", end_date: "2025-06-12", coverage_limits: { max_annual: 5000 } },
"POL-1095": { start_date: "2024-01-05", end_date: "2025-08-25", coverage_limits: { max_annual: 3000 } },
"POL-1096": { start_date: "2024-03-04", end_date: "2026-10-06", coverage_limits: { max_annual: 10000 } },
"POL-1097": { start_date: "2023-11-25", end_date: "2025-09-30", coverage_limits: { max_annual: 8000 } },
"POL-1098": { start_date: "2024-08-25", end_date: "2025-11-01", coverage_limits: { max_annual: 2000 } },
"POL-1099": { start_date: "2023-02-26", end_date: "2025-05-11", coverage_limits: { max_annual: 5000 } }
};

const ClaimsProcessor: React.FC<ClaimsProcessorProps> = ({
  claims,
  isProcessing,
  onStartValidation,
  onValidationComplete
}) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  const [processedClaims, setProcessedClaims] = useState(0);

  // Document Extraction Agent (simulated)
  const extractClaimData = (claim: ClaimData): ClaimData => {
    console.log(`🤖 Document Extractor: Processing claim ${claim.claim_id}`);
    // In real implementation, this would use Hugging Face API for document extraction
    return claim; // Already structured for this demo
  };

  // Policy Checker Agent
  const validatePolicy = (claim: ClaimData): ValidationResult => {
    console.log(`🛡️ Policy Checker: Validating claim ${claim.claim_id}`);
    
    const policy = policyDatabase[claim.policy_number as keyof typeof policyDatabase];
    
    // Check for missing information
    if (!claim.claim_id || !claim.patient || !claim.service_date) {
      return {
        claim_id: claim.claim_id,
        patient: claim.patient,
        issue: "Missing Information",
        action: "Please ensure all mandatory fields are filled before submitting.",
        severity: 'high',
        status: 'pending'
      };
    }

    // Check if policy exists
    if (!policy) {
      return {
        claim_id: claim.claim_id,
        patient: claim.patient,
        issue: "Invalid Policy",
        action: "Policy number not found in our database. Please verify policy details.",
        severity: 'high',
        status: 'pending'
      };
    }

    // Check policy expiry
    const serviceDate = new Date(claim.service_date);
    const policyEndDate = new Date(policy.end_date);
    if (serviceDate > policyEndDate) {
      return {
        claim_id: claim.claim_id,
        patient: claim.patient,
        issue: "Policy Expired",
        action: "Claim cannot be processed as the service date falls after policy expiry.",
        severity: 'high',
        status: 'pending'
      };
    }

    // Check procedure-diagnosis compatibility
    if (claim.diagnosis_code.startsWith('J') && claim.procedure_code.startsWith('2')) {
      return {
        claim_id: claim.claim_id,
        patient: claim.patient,
        issue: "Procedure-Diagnosis Mismatch",
        action: "Respiratory diagnosis does not align with orthopedic procedure code.",
        severity: 'medium',
        status: 'pending'
      };
    }

    // Check amount limits
    if (claim.amount > policy.coverage_limits.max_annual / 10) {
      return {
        claim_id: claim.claim_id,
        patient: claim.patient,
        issue: "High Amount",
        action: "Claim amount exceeds typical limits. Requires manual review.",
        severity: 'medium',
        status: 'pending'
      };
    }

    return {
      claim_id: claim.claim_id,
      patient: claim.patient,
      issue: "None",
      action: "Claim is valid and ready for processing.",
      severity: 'low',
      status: 'approved'
    };
  };

  // Fraud Detector Agent
  const detectFraud = (claim: ClaimData, allClaims: ClaimData[]): ValidationResult | null => {
    console.log(`🔍 Fraud Detector: Analyzing claim ${claim.claim_id}`);
    
    // Check for duplicate claims
    const duplicates = allClaims.filter(c => 
      c.claim_id !== claim.claim_id &&
      c.patient === claim.patient &&
      c.service_date === claim.service_date &&
      c.procedure_code === claim.procedure_code
    );

    if (duplicates.length > 0) {
      return {
        claim_id: claim.claim_id,
        patient: claim.patient,
        issue: "Duplicate Claim",
        action: "Potential duplicate detected. Review for similar claims submitted.",
        severity: 'high',
        status: 'pending'
      };
    }

    // Check for suspicious patterns (multiple high-value claims)
    const recentClaims = allClaims.filter(c => 
      c.patient === claim.patient &&
      c.amount > 500
    );

    if (recentClaims.length > 2) {
      return {
        claim_id: claim.claim_id,
        patient: claim.patient,
        issue: "Suspicious Pattern",
        action: "Multiple high-value claims detected. Manual review recommended.",
        severity: 'medium',
        status: 'pending'
      };
    }

    return null;
  };

  // Main processing function
  const processClaims = async () => {
    if (claims.length === 0) return;

    setProgress(0);
    setProcessedClaims(0);
    const results: ValidationResult[] = [];

    for (let i = 0; i < claims.length; i++) {
      const claim = claims[i];
      
      // Step 1: Document Extraction
      setCurrentStep(`Extracting data from claim ${claim.claim_id}`);
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate processing time
      const extractedClaim = extractClaimData(claim);
      
      // Step 2: Policy Validation
      setCurrentStep(`Validating policy for claim ${claim.claim_id}`);
      await new Promise(resolve => setTimeout(resolve, 800));
      const policyResult = validatePolicy(extractedClaim);
      
      // Step 3: Fraud Detection
      setCurrentStep(`Checking for fraud in claim ${claim.claim_id}`);
      await new Promise(resolve => setTimeout(resolve, 600));
      const fraudResult = detectFraud(extractedClaim, claims);
      
      // Use fraud result if found, otherwise use policy result
      results.push(fraudResult || policyResult);
      
      setProcessedClaims(i + 1);
      setProgress(((i + 1) / claims.length) * 100);
    }

    setCurrentStep('Validation complete!');
    onValidationComplete(results);
  };

  useEffect(() => {
    if (isProcessing) {
      processClaims();
    }
  }, [isProcessing]);

  return (
    <div className="space-y-4">
      {!isProcessing && (
        <Button 
          onClick={onStartValidation} 
          className="w-full" 
          size="lg"
          disabled={claims.length === 0}
        >
          <Play className="w-4 h-4 mr-2" />
          Start Validation Process
        </Button>
      )}

      {isProcessing && (
        <div className="space-y-4">
          <div className="flex items-center justify-center space-x-2 text-blue-600">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span className="font-medium">Processing Claims...</span>
          </div>
          
          <Progress value={progress} className="w-full" />
          
          <div className="text-center text-sm text-gray-600">
            {currentStep}
          </div>
          
          <div className="text-center text-sm font-medium">
            {processedClaims} of {claims.length} claims processed
          </div>

          {/* Agent Status */}
          <div className="grid grid-cols-3 gap-2 text-xs">
            <div className="flex items-center justify-center p-2 bg-blue-50 rounded">
              <Brain className="w-3 h-3 mr-1 text-blue-600" />
              <span>Document AI</span>
            </div>
            <div className="flex items-center justify-center p-2 bg-green-50 rounded">
              <Shield className="w-3 h-3 mr-1 text-green-600" />
              <span>Policy Check</span>
            </div>
            <div className="flex items-center justify-center p-2 bg-purple-50 rounded">
              <Search className="w-3 h-3 mr-1 text-purple-600" />
              <span>Fraud Detect</span>
            </div>
          </div>
        </div>
      )}

      {claims.length > 0 && !isProcessing && (
        <div className="text-center p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600 mb-2">
            Ready to process {claims.length} claims
          </p>
          <div className="flex justify-center space-x-2">
            <Badge variant="outline">
              <Brain className="w-3 h-3 mr-1" />
              Document Extraction
            </Badge>
            <Badge variant="outline">
              <Shield className="w-3 h-3 mr-1" />
              Policy Validation
            </Badge>
            <Badge variant="outline">
              <Search className="w-3 h-3 mr-1" />
              Fraud Detection
            </Badge>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClaimsProcessor;
