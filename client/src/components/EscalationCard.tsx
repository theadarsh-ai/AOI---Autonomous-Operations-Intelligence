import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AlertTriangle, DollarSign, TrendingUp } from "lucide-react";
import { useState } from "react";

export interface EscalationCardProps {
  id: string;
  decisionType: string;
  timestamp: string;
  urgencyLevel: "high" | "medium" | "low";
  whyEscalated: string;
  riskAssessment: string;
  businessImpact: string;
  actionPreview: string;
  estimatedCost: number;
  onApprove: () => void;
  onReject: () => void;
  onRequestInfo: () => void;
}

const urgencyConfig = {
  high: { label: "High Urgency", color: "text-status-busy bg-status-busy/10" },
  medium: { label: "Medium Urgency", color: "text-status-away bg-status-away/10" },
  low: { label: "Low Urgency", color: "text-status-online bg-status-online/10" },
};

export function EscalationCard({
  decisionType,
  timestamp,
  urgencyLevel,
  whyEscalated,
  riskAssessment,
  businessImpact,
  actionPreview,
  estimatedCost,
  onApprove,
  onReject,
  onRequestInfo,
}: EscalationCardProps) {
  const [processing, setProcessing] = useState(false);
  const urgencyInfo = urgencyConfig[urgencyLevel];

  const handleApprove = () => {
    setProcessing(true);
    onApprove();
    setTimeout(() => setProcessing(false), 1000);
  };

  const handleReject = () => {
    setProcessing(true);
    onReject();
    setTimeout(() => setProcessing(false), 1000);
  };

  return (
    <Card className="p-4 border-l-4 border-l-status-busy" data-testid={`escalation-${decisionType.toLowerCase().replace(/\s+/g, '-')}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-status-busy" />
          <h3 className="text-sm font-semibold">{decisionType}</h3>
        </div>
        <div className="flex flex-col items-end gap-1">
          <Badge className={urgencyInfo.color}>
            {urgencyInfo.label}
          </Badge>
          <span className="text-xs font-mono text-muted-foreground">{timestamp}</span>
        </div>
      </div>

      <div className="space-y-3 mb-4">
        <div>
          <h4 className="text-xs font-medium text-muted-foreground mb-1">Why Escalated</h4>
          <p className="text-xs">{whyEscalated}</p>
        </div>

        <div>
          <h4 className="text-xs font-medium text-muted-foreground mb-1">Risk Assessment</h4>
          <p className="text-xs">{riskAssessment}</p>
        </div>

        <div>
          <h4 className="text-xs font-medium text-muted-foreground mb-1">Business Impact</h4>
          <p className="text-xs">{businessImpact}</p>
        </div>

        <div>
          <h4 className="text-xs font-medium text-muted-foreground mb-1">Action Preview</h4>
          <p className="text-xs font-medium">{actionPreview}</p>
        </div>

        <div className="flex items-center gap-4 pt-2 border-t">
          <div className="flex items-center gap-2">
            <DollarSign className="h-3.5 w-3.5 text-muted-foreground" />
            <div>
              <div className="text-xs text-muted-foreground">Estimated Cost</div>
              <div className="text-sm font-mono font-medium">${estimatedCost.toLocaleString()}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex gap-2">
        <Button
          size="sm"
          className="flex-1"
          onClick={handleApprove}
          disabled={processing}
          data-testid="button-approve-escalation"
        >
          <TrendingUp className="h-3.5 w-3.5 mr-1" />
          Approve
        </Button>
        <Button
          size="sm"
          variant="outline"
          className="flex-1"
          onClick={handleReject}
          disabled={processing}
          data-testid="button-reject-escalation"
        >
          Reject
        </Button>
        <Button
          size="sm"
          variant="secondary"
          onClick={onRequestInfo}
          disabled={processing}
          data-testid="button-request-info"
        >
          More Info
        </Button>
      </div>
    </Card>
  );
}
