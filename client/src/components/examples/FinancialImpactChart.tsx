import { FinancialImpactChart } from '../FinancialImpactChart';

export default function FinancialImpactChartExample() {
  const data = [
    { agent: 'Monitoring', savings: 45000, cost: 3200, roi: 14 },
    { agent: 'Decision', savings: 38000, cost: 2800, roi: 13 },
    { agent: 'Resource', savings: 28000, cost: 2400, roi: 11 },
    { agent: 'Security', savings: 52000, cost: 4200, roi: 12 },
  ];

  return (
    <div className="max-w-3xl">
      <FinancialImpactChart
        title="ROI by Agent - Last 30 Days"
        data={data}
      />
    </div>
  );
}
