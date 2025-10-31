import { MetricCard } from '../MetricCard';
import { Target } from 'lucide-react';

export default function MetricCardExample() {
  return (
    <div className="grid grid-cols-2 gap-4 max-w-2xl">
      <MetricCard
        label="Autonomous Actions"
        value="95%"
        icon={Target}
        trend={{ value: 2.3, isPositive: true }}
      />
      <MetricCard
        label="Prevention Savings"
        value="$128K"
        trend={{ value: 12, isPositive: true }}
      />
    </div>
  );
}
