import { Badge } from "@/components/ui/badge";
import { Wifi, WifiOff } from "lucide-react";
import { cn } from "@/lib/utils";

export interface ConnectionStatusProps {
  isConnected: boolean;
  lastUpdate?: string;
}

export function ConnectionStatus({ isConnected, lastUpdate }: ConnectionStatusProps) {
  return (
    <Badge
      variant="outline"
      className={cn(
        "gap-1.5",
        isConnected ? "text-status-online border-status-online/30" : "text-muted-foreground"
      )}
      data-testid="badge-connection-status"
    >
      {isConnected ? (
        <>
          <Wifi className="h-3 w-3" />
          <span className="text-xs">Live</span>
        </>
      ) : (
        <>
          <WifiOff className="h-3 w-3" />
          <span className="text-xs">Disconnected</span>
        </>
      )}
      {lastUpdate && (
        <>
          <span className="text-xs">•</span>
          <span className="text-xs">{lastUpdate}</span>
        </>
      )}
    </Badge>
  );
}
