import { Card } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

export interface FinancialImpactChartProps {
  title: string;
  data: Array<{
    agent: string;
    savings: number;
    cost: number;
    roi: number;
  }>;
}

export function FinancialImpactChart({ title, data }: FinancialImpactChartProps) {
  return (
    <Card className="p-4">
      <h3 className="text-sm font-semibold mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
          <XAxis
            dataKey="agent"
            className="text-xs"
            tick={{ fill: "hsl(var(--muted-foreground))" }}
          />
          <YAxis
            className="text-xs"
            tick={{ fill: "hsl(var(--muted-foreground))" }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "6px",
            }}
            labelStyle={{ color: "hsl(var(--card-foreground))" }}
            formatter={(value: number) => `$${value.toLocaleString()}`}
          />
          <Legend />
          <Bar dataKey="savings" name="Prevention Savings" fill="hsl(var(--chart-2))" />
          <Bar dataKey="cost" name="Operational Cost" fill="hsl(var(--chart-5))" />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
