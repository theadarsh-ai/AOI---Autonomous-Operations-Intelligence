import { PerformanceChart } from '../PerformanceChart';

export default function PerformanceChartExample() {
  const data = [
    { time: '00:00', accuracy: 82, predictions: 45 },
    { time: '04:00', accuracy: 84, predictions: 52 },
    { time: '08:00', accuracy: 86, predictions: 58 },
    { time: '12:00', accuracy: 87, predictions: 61 },
    { time: '16:00', accuracy: 88, predictions: 64 },
    { time: '20:00', accuracy: 89, predictions: 67 },
  ];

  const dataKeys = [
    { key: 'accuracy', label: 'Prediction Accuracy (%)', color: 'hsl(var(--chart-1))' },
    { key: 'predictions', label: 'Predictions Made', color: 'hsl(var(--chart-2))' },
  ];

  return (
    <div className="max-w-3xl">
      <PerformanceChart
        title="Agent Learning Performance - Last 24 Hours"
        data={data}
        dataKeys={dataKeys}
      />
    </div>
  );
}
