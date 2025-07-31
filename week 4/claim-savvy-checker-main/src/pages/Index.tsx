
import React, { useState } from 'react';
import { Upload, FileText, Shield, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import ClaimsUploader from '@/components/ClaimsUploader';
import ValidationResults from '@/components/ValidationResults';
import ClaimsProcessor from '@/components/ClaimsProcessor';

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

const Index = () => {
  const [claims, setClaims] = useState<ClaimData[]>([]);
  const [validationResults, setValidationResults] = useState<ValidationResult[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  // Sample claims data for demonstration
  const sampleClaims: ClaimData[] = [
    {
      claim_id: "CLM-001",
      patient: "Alice Johnson",
      service_date: "2025-05-15",
      diagnosis_code: "J45.909",
      procedure_code: "99213",
      provider: "Dr. Smith",
      policy_number: "POL-123",
      amount: 250.00,
      text: "Claim ID: CLM-001, Patient: Alice Johnson, Service Date: 2025-05-15, Diagnosis Code: J45.909, Procedure Code: 99213, Provider: Dr. Smith, Policy: POL-123, Amount: $250.00"
    },
    {
      claim_id: "CLM-002",
      patient: "Robert Williams",
      service_date: "2025-05-10",
      diagnosis_code: "M54.5",
      procedure_code: "29881",
      provider: "Dr. Jones",
      policy_number: "POL-456",
      amount: 1200.00,
      text: "Claim ID: CLM-002, Patient: Robert Williams, Service Date: 2025-05-10, Diagnosis Code: M54.5, Procedure Code: 29881, Provider: Dr. Jones, Policy: POL-456, Amount: $1200.00"
    },
    {
      claim_id: "CLM-003",
      patient: "Linda Martinez",
      service_date: "2025-04-01",
      diagnosis_code: "E11.9",
      procedure_code: "99214",
      provider: "Dr. Brown",
      policy_number: "POL-789",
      amount: 350.00,
      text: "Claim ID: CLM-003, Patient: Linda Martinez, Service Date: 2025-04-01, Diagnosis Code: E11.9, Procedure Code: 99214, Provider: Dr. Brown, Policy: POL-789, Amount: $350.00"
    }
  ];

  const loadSampleData = () => {
    setClaims(sampleClaims);
    toast({
      title: "Sample Data Loaded",
      description: "3 sample claims have been loaded for demonstration.",
    });
  };

  const handleClaimsUpload = (newClaims: ClaimData[]) => {
    setClaims(prev => [...prev, ...newClaims]);
    toast({
      title: "Claims Uploaded",
      description: `${newClaims.length} claims uploaded successfully.`,
    });
  };

  const handleValidationComplete = (results: ValidationResult[]) => {
    setValidationResults(results);
    setIsProcessing(false);
    toast({
      title: "Validation Complete",
      description: `${results.length} claims have been processed.`,
    });
  };

  const startValidation = () => {
    if (claims.length === 0) {
      toast({
        title: "No Claims to Process",
        description: "Please upload claims first or load sample data.",
        variant: "destructive",
      });
      return;
    }
    setIsProcessing(true);
  };

  const stats = {
    totalClaims: claims.length,
    validClaims: validationResults.filter(r => r.issue === "None").length,
    flaggedClaims: validationResults.filter(r => r.issue !== "None").length,
    pendingClaims: validationResults.filter(r => r.status === "pending").length,
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Shield className="w-12 h-12 text-blue-600 mr-4" />
            <h1 className="text-4xl font-bold text-gray-900">
              Insurance Claims Validator
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Advanced AI-powered system for validating healthcare insurance claims, 
            detecting fraud, and ensuring policy compliance.
          </p>
        </div>

        {/* Stats Dashboard */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Claims</CardTitle>
              <FileText className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalClaims}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Valid Claims</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.validClaims}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Flagged Claims</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{stats.flaggedClaims}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending Review</CardTitle>
              <XCircle className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{stats.pendingClaims}</div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Upload and Controls */}
          <div className="lg:col-span-1 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Upload className="w-5 h-5 mr-2" />
                  Upload Claims
                </CardTitle>
                <CardDescription>
                  Upload claim documents or use sample data for testing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ClaimsUploader onClaimsUpload={handleClaimsUpload} />
                <div className="text-center">
                  <p className="text-sm text-gray-500 mb-3">Or try with sample data</p>
                  <Button 
                    variant="outline" 
                    onClick={loadSampleData}
                    className="w-full"
                  >
                    Load Sample Claims
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Processing Controls */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Shield className="w-5 h-5 mr-2" />
                  Validation Control
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ClaimsProcessor
                  claims={claims}
                  isProcessing={isProcessing}
                  onStartValidation={startValidation}
                  onValidationComplete={handleValidationComplete}
                />
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2">
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="w-5 h-5 mr-2" />
                  Validation Results
                </CardTitle>
                <CardDescription>
                  Review processed claims and take appropriate actions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ValidationResults 
                  results={validationResults}
                  onUpdateStatus={(claimId, status) => {
                    setValidationResults(prev => 
                      prev.map(result => 
                        result.claim_id === claimId 
                          ? { ...result, status }
                          : result
                      )
                    );
                  }}
                />
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
