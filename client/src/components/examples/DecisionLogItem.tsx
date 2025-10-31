import { DecisionLogItem } from '../DecisionLogItem';
import { Activity } from 'lucide-react';

export default function DecisionLogItemExample() {
  return (
    <div className="max-w-md bg-card p-4 rounded-md">
      <DecisionLogItem
        id="decision-1"
        timestamp="14:23:45"
        agentName="Predictive Monitoring"
        agentIcon={Activity}
        agentColor="bg-agent-monitoring"
        decisionType="Preventive Maintenance Scheduled"
        description="Detected anomaly in DB-Server-03. Predicted disk failure in 36 hours. Scheduling maintenance window."
        cost={800}
        roi={15}
        autonomyLevel={1}
        autoApproved={true}
      />
    </div>
  );
}
