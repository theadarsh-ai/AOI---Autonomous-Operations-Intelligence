import { EscalationCard } from '../EscalationCard';

export default function EscalationCardExample() {
  return (
    <div className="max-w-2xl">
      <EscalationCard
        id="esc-1"
        decisionType="Major Infrastructure Upgrade"
        timestamp="15:42:18"
        urgencyLevel="high"
        whyEscalated="Cost exceeds $10K threshold for autonomous approval"
        riskAssessment="Medium risk - requires brief downtime during migration. Failure scenario includes potential 2-hour service disruption."
        businessImpact="Upgrading database cluster will improve performance by 40% and prevent predicted capacity issues in Q2."
        actionPreview="Migrate 3 production databases to new AWS RDS instances with enhanced IOPS and automated backups"
        estimatedCost={15000}
        onApprove={() => console.log('Approved')}
        onReject={() => console.log('Rejected')}
        onRequestInfo={() => console.log('Request more info')}
      />
    </div>
  );
}
