import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, Clock, DollarSign } from "lucide-react";
import { cn } from "@/lib/utils";

export type SeverityLevel = "critical" | "high" | "medium" | "low";

export interface PredictionCardProps {
  id: string;
  title: string;
  description: string;
  severity: SeverityLevel;
  confidence: number;
  timeToFailure: string;
  estimatedImpact: number;
  scheduledAction: string;
  scheduledTime: string;
}

const severityConfig = {
  critical: { label: "Critical", color: "text-status-busy bg-status-busy/10" },
  high: { label: "High", color: "text-status-away bg-status-away/10" },
  medium: { label: "Medium", color: "text-yellow-600 bg-yellow-600/10" },
  low: { label: "Low", color: "text-status-online bg-status-online/10" },
};

export function PredictionCard({
  title,
  description,
  severity,
  confidence,
  timeToFailure,
  estimatedImpact,
  scheduledAction,
  scheduledTime,
}: PredictionCardProps) {
  const severityInfo = severityConfig[severity];

  return (
    <Card className="p-4" data-testid={`prediction-${title.toLowerCase().replace(/\s+/g, '-')}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <AlertTriangle className={cn("h-4 w-4", severityInfo.color.split(' ')[0])} />
          <h3 className="text-sm font-semibold">{title}</h3>
        </div>
        <Badge className={severityInfo.color}>
          {severityInfo.label}
        </Badge>
      </div>

      <p className="text-xs text-muted-foreground mb-3">{description}</p>

      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="flex items-center gap-2">
          <Clock className="h-3.5 w-3.5 text-muted-foreground" />
          <div>
            <div className="text-xs text-muted-foreground">Time to Failure</div>
            <div className="text-sm font-mono font-medium">{timeToFailure}</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <DollarSign className="h-3.5 w-3.5 text-muted-foreground" />
          <div>
            <div className="text-xs text-muted-foreground">Est. Impact</div>
            <div className="text-sm font-mono font-medium">${estimatedImpact?.toLocaleString() || '0'}</div>
          </div>
        </div>
      </div>

      <div className="space-y-2 pt-3 border-t">
        <div className="flex items-center justify-between">
          <span className="text-xs text-muted-foreground">Confidence Score</span>
          <span className="text-xs font-mono font-medium">{confidence}%</span>
        </div>
        <div>
          <div className="text-xs text-muted-foreground mb-1">Scheduled Action</div>
          <div className="text-xs font-medium">{scheduledAction}</div>
          <div className="text-xs text-muted-foreground mt-0.5">{scheduledTime}</div>
        </div>
      </div>
    </Card>
  );
}
