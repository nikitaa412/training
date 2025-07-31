
import React, { useState } from 'react';
import { CheckCircle, XCircle, AlertTriangle, Eye, Download, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';

interface ValidationResult {
  claim_id: string;
  patient: string;
  issue: string;
  action: string;
  severity: 'low' | 'medium' | 'high';
  status: 'pending' | 'approved' | 'rejected';
}

interface ValidationResultsProps {
  results: ValidationResult[];
  onUpdateStatus: (claimId: string, status: 'approved' | 'rejected') => void;
}

const ValidationResults: React.FC<ValidationResultsProps> = ({ results, onUpdateStatus }) => {
  const [filter, setFilter] = useState<string>('all');
  const [selectedClaim, setSelectedClaim] = useState<ValidationResult | null>(null);
  const { toast } = useToast();

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status: string, issue: string) => {
    if (issue === "None") return <CheckCircle className="w-4 h-4 text-green-600" />;
    if (status === 'approved') return <CheckCircle className="w-4 h-4 text-green-600" />;
    if (status === 'rejected') return <XCircle className="w-4 h-4 text-red-600" />;
    return <AlertTriangle className="w-4 h-4 text-yellow-600" />;
  };

  const filteredResults = results.filter(result => {
    if (filter === 'all') return true;
    if (filter === 'valid') return result.issue === "None";
    if (filter === 'flagged') return result.issue !== "None";
    if (filter === 'pending') return result.status === 'pending';
    if (filter === 'approved') return result.status === 'approved';
    if (filter === 'rejected') return result.status === 'rejected';
    return true;
  });

  const handleApprove = (claimId: string) => {
    onUpdateStatus(claimId, 'approved');
    toast({
      title: "Claim Approved",
      description: `Claim ${claimId} has been approved for processing.`,
    });
  };

  const handleReject = (claimId: string) => {
    onUpdateStatus(claimId, 'rejected');
    toast({
      title: "Claim Rejected",
      description: `Claim ${claimId} has been rejected.`,
      variant: "destructive",
    });
  };

  const exportResults = () => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + "Claim ID,Patient,Issue,Action,Severity,Status\n"
      + results.map(r => 
          `"${r.claim_id}","${r.patient}","${r.issue}","${r.action}","${r.severity}","${r.status}"`
        ).join("\n");
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "validation_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    toast({
      title: "Export Complete",
      description: "Validation results exported to CSV file.",
    });
  };

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-700 mb-2">No Results Yet</h3>
        <p className="text-gray-500">
          Upload claims and start the validation process to see results here.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-gray-500" />
          <Select value={filter} onValueChange={setFilter}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter results" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Claims ({results.length})</SelectItem>
              <SelectItem value="valid">Valid Claims ({results.filter(r => r.issue === "None").length})</SelectItem>
              <SelectItem value="flagged">Flagged Claims ({results.filter(r => r.issue !== "None").length})</SelectItem>
              <SelectItem value="pending">Pending ({results.filter(r => r.status === 'pending').length})</SelectItem>
              <SelectItem value="approved">Approved ({results.filter(r => r.status === 'approved').length})</SelectItem>
              <SelectItem value="rejected">Rejected ({results.filter(r => r.status === 'rejected').length})</SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <Button variant="outline" onClick={exportResults}>
          <Download className="w-4 h-4 mr-2" />
          Export CSV
        </Button>
      </div>

      {/* Results Table */}
      <div className="space-y-3">
        {filteredResults.map((result) => (
          <Card key={result.claim_id} className="transition-all hover:shadow-md">
            <CardContent className="p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1 space-y-2">
                  <div className="flex items-center space-x-3">
                    {getStatusIcon(result.status, result.issue)}
                    <h4 className="font-semibold text-lg">{result.claim_id}</h4>
                    <Badge className={getSeverityColor(result.severity)}>
                      {result.severity.toUpperCase()}
                    </Badge>
                    <Badge variant={result.status === 'approved' ? 'default' : result.status === 'rejected' ? 'destructive' : 'secondary'}>
                      {result.status.toUpperCase()}
                    </Badge>
                  </div>
                  
                  <p className="text-gray-700">
                    <span className="font-medium">Patient:</span> {result.patient}
                  </p>
                  
                  <div className="space-y-1">
                    <p className={`font-medium ${result.issue === "None" ? "text-green-700" : "text-red-700"}`}>
                      Issue: {result.issue}
                    </p>
                    <p className="text-gray-600 text-sm">
                      {result.action}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-2 ml-4">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedClaim(result)}
                  >
                    <Eye className="w-4 h-4" />
                  </Button>
                  
                  {result.status === 'pending' && result.issue !== "None" && (
                    <>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleApprove(result.claim_id)}
                        className="text-green-600 hover:text-green-700 hover:bg-green-50"
                      >
                        <CheckCircle className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleReject(result.claim_id)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <XCircle className="w-4 h-4" />
                      </Button>
                    </>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredResults.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500">No claims match the current filter.</p>
        </div>
      )}

      {/* Detailed View Modal */}
      {selectedClaim && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl max-h-[80vh] overflow-y-auto">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Claim Details: {selectedClaim.claim_id}</span>
                <Button variant="ghost" onClick={() => setSelectedClaim(null)}>
                  <XCircle className="w-4 h-4" />
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold mb-2">Basic Information</h4>
                  <p><span className="font-medium">Claim ID:</span> {selectedClaim.claim_id}</p>
                  <p><span className="font-medium">Patient:</span> {selectedClaim.patient}</p>
                  <p><span className="font-medium">Status:</span> 
                    <Badge className="ml-2" variant={selectedClaim.status === 'approved' ? 'default' : selectedClaim.status === 'rejected' ? 'destructive' : 'secondary'}>
                      {selectedClaim.status.toUpperCase()}
                    </Badge>
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Validation Results</h4>
                  <p><span className="font-medium">Issue:</span> {selectedClaim.issue}</p>
                  <p><span className="font-medium">Severity:</span> 
                    <Badge className={`ml-2 ${getSeverityColor(selectedClaim.severity)}`}>
                      {selectedClaim.severity.toUpperCase()}
                    </Badge>
                  </p>
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-2">Recommended Action</h4>
                <p className="text-gray-700 bg-gray-50 p-3 rounded">{selectedClaim.action}</p>
              </div>

              {selectedClaim.status === 'pending' && selectedClaim.issue !== "None" && (
                <div className="flex space-x-2 pt-4">
                  <Button 
                    onClick={() => {
                      handleApprove(selectedClaim.claim_id);
                      setSelectedClaim(null);
                    }}
                    className="flex-1"
                  >
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Approve Claim
                  </Button>
                  <Button 
                    variant="destructive"
                    onClick={() => {
                      handleReject(selectedClaim.claim_id);
                      setSelectedClaim(null);
                    }}
                    className="flex-1"
                  >
                    <XCircle className="w-4 h-4 mr-2" />
                    Reject Claim
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ValidationResults;
