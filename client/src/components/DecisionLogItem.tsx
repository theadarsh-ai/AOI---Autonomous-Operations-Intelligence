import { Badge } from "@/components/ui/badge";
import { LucideIcon, CheckCircle2, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

export type AutonomyLevel = 1 | 2 | 3;

export interface DecisionLogItemProps {
  id: string;
  timestamp: string;
  agentName: string;
  agentIcon: LucideIcon;
  agentColor: string;
  decisionType: string;
  description: string;
  cost: number;
  roi: number;
  autonomyLevel: AutonomyLevel;
  autoApproved: boolean;
}

const autonomyLevelConfig = {
  1: { label: "Level 1 - Full Autonomy", color: "bg-status-online" },
  2: { label: "Level 2 - Conditional", color: "bg-status-away" },
  3: { label: "Level 3 - Human Required", color: "bg-status-busy" },
};

export function DecisionLogItem({
  timestamp,
  agentName,
  agentIcon: Icon,
  agentColor,
  decisionType,
  description,
  cost,
  roi,
  autonomyLevel,
  autoApproved,
}: DecisionLogItemProps) {
  const levelConfig = autonomyLevelConfig[autonomyLevel];

  return (
    <div className="py-3 border-b last:border-b-0" data-testid={`decision-log-${decisionType?.toLowerCase().replace(/\s+/g, '-') || 'unknown'}`}>
      <div className="flex items-start gap-3">
        <div className={cn("p-1.5 rounded-md flex-shrink-0", agentColor)}>
          <Icon className="h-3.5 w-3.5 text-white" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-muted-foreground">{timestamp}</span>
            <span className="text-xs text-muted-foreground">•</span>
            <span className="text-xs text-muted-foreground">{agentName}</span>
            {autoApproved && (
              <CheckCircle2 className="h-3.5 w-3.5 text-status-online flex-shrink-0" />
            )}
            {!autoApproved && (
              <AlertTriangle className="h-3.5 w-3.5 text-status-away flex-shrink-0" />
            )}
          </div>
          <p className="text-sm font-medium mb-1">{decisionType}</p>
          <p className="text-xs text-muted-foreground mb-2 line-clamp-2">
            {description}
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="outline" className="text-xs">
              Cost: ${(cost || 0).toLocaleString()}
            </Badge>
            <Badge variant="outline" className="text-xs">
              ROI: {(roi || 0)}:1
            </Badge>
            <Badge variant="secondary" className="text-xs">
              {levelConfig.label}
            </Badge>
          </div>
        </div>
      </div>
    </div>
  );
}
