import { AgentCard } from '../AgentCard';
import { Activity } from 'lucide-react';

export default function AgentCardExample() {
  return (
    <div className="max-w-sm">
      <AgentCard
        id="monitoring"
        name="Predictive Monitoring"
        icon={Activity}
        status="active"
        activeTasks={3}
        recentActivity="Analyzing system metrics for DB-Server-03. Predicted disk failure in 36 hours."
        uptime="99.8%"
        decisionsPerHour={24}
        accuracy={87}
        color="bg-agent-monitoring"
        onViewDetails={() => console.log('View details clicked')}
      />
    </div>
  );
}
