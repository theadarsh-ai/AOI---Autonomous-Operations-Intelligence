import { Badge } from "@/components/ui/badge";
import { Activity, AlertCircle, CheckCircle2, Info, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

export interface ActivityLogItemProps {
  id: string;
  timestamp: string;
  agent: string;
  action: string;
  details: string;
  level: "info" | "success" | "warning" | "escalation";
}

const levelConfig = {
  info: {
    icon: Info,
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
    label: "Info",
  },
  success: {
    icon: CheckCircle2,
    color: "text-status-online",
    bgColor: "bg-status-online/10",
    label: "Success",
  },
  warning: {
    icon: AlertTriangle,
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
    label: "Warning",
  },
  escalation: {
    icon: AlertCircle,
    color: "text-destructive",
    bgColor: "bg-destructive/10",
    label: "Escalation",
  },
};

export function ActivityLogItem({
  timestamp,
  agent,
  action,
  details,
  level,
}: ActivityLogItemProps) {
  const levelInfo = levelConfig[level];
  const Icon = levelInfo.icon;

  // Convert timestamp to exact same format as header
  const formatTime = (time: string) => {
    const [hours24, minutes, seconds] = time.split(':');
    const date = new Date();
    date.setHours(parseInt(hours24), parseInt(minutes), parseInt(seconds));
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit', 
      second: '2-digit', 
      hour12: true 
    });
  };

  const formattedTime = formatTime(timestamp);

  return (
    <div
      className="flex items-start gap-3 py-3 px-4 hover-elevate rounded-md transition-colors border-b border-border last:border-0"
      data-testid={`activity-${level}`}
    >
      <div className={cn("p-1.5 rounded-md mt-0.5", levelInfo.bgColor)}>
        <Icon className={cn("h-4 w-4", levelInfo.color)} />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <Badge variant="outline" className="text-xs font-medium">
            {agent}
          </Badge>
          <span className="text-xs text-muted-foreground">{formattedTime}</span>
        </div>
        <div className="text-sm font-medium mb-0.5">{action}</div>
        <div className="text-xs text-muted-foreground">{details}</div>
      </div>
    </div>
  );
}
