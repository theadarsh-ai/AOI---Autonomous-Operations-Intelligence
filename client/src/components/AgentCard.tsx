import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

export type AgentStatus = "active" | "idle" | "processing";

export interface AgentCardProps {
  id: string;
  name: string;
  icon: LucideIcon;
  status: AgentStatus;
  activeTasks: number;
  recentActivity: string;
  uptime: string;
  decisionsPerHour: number;
  accuracy: number;
  color: string;
  onViewDetails: () => void;
}

const statusConfig = {
  active: { label: "Active", color: "bg-status-online" },
  idle: { label: "Idle", color: "bg-status-away" },
  processing: { label: "Processing", color: "bg-status-busy" },
};

export function AgentCard({
  name,
  icon: Icon,
  status,
  activeTasks,
  recentActivity,
  uptime,
  decisionsPerHour,
  accuracy,
  color,
  onViewDetails,
}: AgentCardProps) {
  const statusInfo = statusConfig[status];

  return (
    <Card className="p-4 hover-elevate" data-testid={`card-agent-${name.toLowerCase().replace(/\s+/g, '-')}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={cn("p-2 rounded-md", color)}>
            <Icon className="h-5 w-5 text-white" />
          </div>
          <div>
            <h3 className="text-sm font-semibold">{name}</h3>
            <div className="flex items-center gap-2 mt-1">
              <div className={cn("w-2 h-2 rounded-full", statusInfo.color)} />
              <span className="text-xs text-muted-foreground">{statusInfo.label}</span>
            </div>
          </div>
        </div>
        <Badge variant="secondary" className="text-xs">
          {activeTasks} Tasks
        </Badge>
      </div>

      <div className="space-y-2 mb-4">
        <p className="text-xs text-muted-foreground line-clamp-2">
          {recentActivity}
        </p>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-3">
        <div>
          <div className="text-xs text-muted-foreground">Uptime</div>
          <div className="text-sm font-mono font-medium">{uptime}</div>
        </div>
        <div>
          <div className="text-xs text-muted-foreground">Dec/hr</div>
          <div className="text-sm font-mono font-medium">{decisionsPerHour}</div>
        </div>
        <div>
          <div className="text-xs text-muted-foreground">Accuracy</div>
          <div className="text-sm font-mono font-medium">{accuracy}%</div>
        </div>
      </div>

      <Button
        variant="outline"
        size="sm"
        className="w-full"
        onClick={onViewDetails}
        data-testid={`button-view-details-${name.toLowerCase().replace(/\s+/g, '-')}`}
      >
        View Details
      </Button>
    </Card>
  );
}
