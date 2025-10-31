import { PredictionCard } from '../PredictionCard';

export default function PredictionCardExample() {
  return (
    <div className="max-w-sm">
      <PredictionCard
        id="pred-1"
        title="DB Server Disk Failure"
        description="DB-Server-03 showing abnormal I/O patterns. Disk failure predicted based on SMART data analysis."
        severity="critical"
        confidence={87}
        timeToFailure="36 hours"
        estimatedImpact={12000}
        scheduledAction="Replace disk, migrate data"
        scheduledTime="Tomorrow at 2:00 AM PST"
      />
    </div>
  );
}
