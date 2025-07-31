
import React, { useState } from 'react';
import { Upload, FileText, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

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

interface ClaimsUploaderProps {
  onClaimsUpload: (claims: ClaimData[]) => void;
}

const ClaimsUploader: React.FC<ClaimsUploaderProps> = ({ onClaimsUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [manualEntry, setManualEntry] = useState({
    claim_id: '',
    patient: '',
    service_date: '',
    diagnosis_code: '',
    procedure_code: '',
    provider: '',
    policy_number: '',
    amount: ''
  });
  const { toast } = useToast();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    handleFiles(files);
  };

  const handleFiles = (files: File[]) => {
    files.forEach(file => {
      if (file.type === 'application/json' || file.name.endsWith('.json')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          try {
            const claims = JSON.parse(e.target?.result as string);
            onClaimsUpload(Array.isArray(claims) ? claims : [claims]);
            toast({
              title: "File Uploaded",
              description: `Successfully processed ${file.name}`,
            });
          } catch (error) {
            toast({
              title: "Error",
              description: "Invalid JSON format",
              variant: "destructive",
            });
          }
        };
        reader.readAsText(file);
      } else {
        // For non-JSON files, simulate OCR extraction
        const simulatedClaim: ClaimData = {
          claim_id: `CLM-${Date.now()}`,
          patient: "Extracted Patient Name",
          service_date: new Date().toISOString().split('T')[0],
          diagnosis_code: "Z00.00",
          procedure_code: "99213",
          provider: "Extracted Provider",
          policy_number: "EXT-001",
          amount: 150.00,
          text: `Extracted claim from ${file.name}`
        };
        onClaimsUpload([simulatedClaim]);
        toast({
          title: "Document Processed",
          description: `Extracted data from ${file.name} (simulated OCR)`,
        });
      }
    });
  };

  const handleManualSubmit = () => {
    if (!manualEntry.claim_id || !manualEntry.patient) {
      toast({
        title: "Missing Information",
        description: "Please fill in required fields (Claim ID and Patient)",
        variant: "destructive",
      });
      return;
    }

    const claim: ClaimData = {
      ...manualEntry,
      amount: parseFloat(manualEntry.amount) || 0,
      text: `Manual entry: ${JSON.stringify(manualEntry)}`
    };

    onClaimsUpload([claim]);
    setManualEntry({
      claim_id: '',
      patient: '',
      service_date: '',
      diagnosis_code: '',
      procedure_code: '',
      provider: '',
      policy_number: '',
      amount: ''
    });

    toast({
      title: "Claim Added",
      description: "Manual claim entry successful",
    });
  };

  return (
    <div className="space-y-6">
      {/* File Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <p className="text-lg font-medium text-gray-900 mb-2">
          Drop files here or click to upload
        </p>
        <p className="text-sm text-gray-500 mb-4">
          Supports PDF, JSON, and text files
        </p>
        <input
          type="file"
          multiple
          accept=".json,.pdf,.txt"
          onChange={handleFileInput}
          className="hidden"
          id="file-upload"
        />
        <Button asChild variant="outline">
          <label htmlFor="file-upload" className="cursor-pointer">
            <FileText className="w-4 h-4 mr-2" />
            Choose Files
          </label>
        </Button>
      </div>

      {/* Manual Entry Form */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center mb-4">
            <Plus className="w-5 h-5 mr-2" />
            <h3 className="font-semibold">Manual Claim Entry</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="claim_id">Claim ID *</Label>
              <Input
                id="claim_id"
                value={manualEntry.claim_id}
                onChange={(e) => setManualEntry(prev => ({ ...prev, claim_id: e.target.value }))}
                placeholder="CLM-001"
              />
            </div>
            
            <div>
              <Label htmlFor="patient">Patient Name *</Label>
              <Input
                id="patient"
                value={manualEntry.patient}
                onChange={(e) => setManualEntry(prev => ({ ...prev, patient: e.target.value }))}
                placeholder="John Doe"
              />
            </div>
            
            <div>
              <Label htmlFor="service_date">Service Date</Label>
              <Input
                id="service_date"
                type="date"
                value={manualEntry.service_date}
                onChange={(e) => setManualEntry(prev => ({ ...prev, service_date: e.target.value }))}
              />
            </div>
            
            <div>
              <Label htmlFor="diagnosis_code">Diagnosis Code</Label>
              <Input
                id="diagnosis_code"
                value={manualEntry.diagnosis_code}
                onChange={(e) => setManualEntry(prev => ({ ...prev, diagnosis_code: e.target.value }))}
                placeholder="J45.909"
              />
            </div>
            
            <div>
              <Label htmlFor="procedure_code">Procedure Code</Label>
              <Input
                id="procedure_code"
                value={manualEntry.procedure_code}
                onChange={(e) => setManualEntry(prev => ({ ...prev, procedure_code: e.target.value }))}
                placeholder="99213"
              />
            </div>
            
            <div>
              <Label htmlFor="provider">Provider</Label>
              <Input
                id="provider"
                value={manualEntry.provider}
                onChange={(e) => setManualEntry(prev => ({ ...prev, provider: e.target.value }))}
                placeholder="Dr. Smith"
              />
            </div>
            
            <div>
              <Label htmlFor="policy_number">Policy Number</Label>
              <Input
                id="policy_number"
                value={manualEntry.policy_number}
                onChange={(e) => setManualEntry(prev => ({ ...prev, policy_number: e.target.value }))}
                placeholder="POL-123"
              />
            </div>
            
            <div>
              <Label htmlFor="amount">Amount ($)</Label>
              <Input
                id="amount"
                type="number"
                step="0.01"
                value={manualEntry.amount}
                onChange={(e) => setManualEntry(prev => ({ ...prev, amount: e.target.value }))}
                placeholder="250.00"
              />
            </div>
          </div>
          
          <Button onClick={handleManualSubmit} className="w-full mt-4">
            <Plus className="w-4 h-4 mr-2" />
            Add Claim
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default ClaimsUploader;
