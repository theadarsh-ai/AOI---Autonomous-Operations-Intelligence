import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { AgentCard } from "@/components/AgentCard";
import { MetricCard } from "@/components/MetricCard";
import { DecisionLogItem } from "@/components/DecisionLogItem";
import { PredictionCard } from "@/components/PredictionCard";
import { EscalationCard } from "@/components/EscalationCard";
import { PerformanceChart } from "@/components/PerformanceChart";
import { FinancialImpactChart } from "@/components/FinancialImpactChart";
import { ConnectionStatus } from "@/components/ConnectionStatus";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Target, TrendingUp, AlertTriangle, DollarSign } from "lucide-react";
import { AGENTS as MOCK_AGENTS, RECENT_DECISIONS as MOCK_DECISIONS, PREDICTIONS as MOCK_PREDICTIONS } from "@/lib/mockData";
import { wsManager } from "@/lib/websocket";

export default function Dashboard() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isConnected, setIsConnected] = useState(false);

  // Fetch live data from REST API
  const { data: agentsData } = useQuery({
    queryKey: ['/api/agents'],
    refetchInterval: 5000, // Poll every 5 seconds
  });

  const { data: decisionsData } = useQuery({
    queryKey: ['/api/decisions'],
    refetchInterval: 5000,
  });

  const { data: predictionsData } = useQuery({
    queryKey: ['/api/predictions'],
    refetchInterval: 5000,
  });

  const { data: metricsData } = useQuery({
    queryKey: ['/api/metrics'],
    refetchInterval: 5000,
  });

  // Use live data if available, otherwise fall back to mock data
  const [agents, setAgents] = useState(MOCK_AGENTS);
  const [decisions, setDecisions] = useState(MOCK_DECISIONS);
  const [predictions, setPredictions] = useState(MOCK_PREDICTIONS);
  const [metrics, setMetrics] = useState({
    autonomousActions: 95,
    preventionSavings: 128000,
    predictionAccuracy: 89,
    activeIncidents: 3
  });

  // Update state when API data arrives
  useEffect(() => {
    if (agentsData) {
      const mappedAgents = agentsData.map((agent: any) => ({
        id: agent.id,
        name: agent.name,
        icon: MOCK_AGENTS.find(a => a.name === agent.name)?.icon || MOCK_AGENTS[0].icon,
        color: MOCK_AGENTS.find(a => a.name === agent.name)?.color || MOCK_AGENTS[0].color,
        status: agent.status,
        activeTasks: agent.active_tasks || agent.decisions_made || 0,
        uptime: agent.uptime_percent || 99.9,
        decisionsPerHour: agent.decisions_per_hour || 0,
        accuracy: agent.accuracy_percent || agent.prediction_accuracy || 90,
      }));
      setAgents(mappedAgents);
    }
  }, [agentsData]);

  useEffect(() => {
    if (decisionsData?.recent_decisions) {
      const mappedDecisions = decisionsData.recent_decisions.slice(0, 10).map((decision: any) => ({
        id: decision.decision_id,
        timestamp: new Date(decision.timestamp).toLocaleTimeString(),
        agentName: "Decision Agent",
        agentIcon: MOCK_DECISIONS[0].agentIcon,
        agentColor: MOCK_DECISIONS[0].agentColor,
        decisionType: decision.decision_type?.replace(/_/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase()) || "Unknown",
        description: decision.action_description || decision.predicted_impact || "No description",
        cost: decision.estimated_cost_usd || 0,
        roi: decision.estimated_roi || 0,
        autonomyLevel: decision.autonomy_level || 1,
        autoApproved: decision.auto_approved || false,
      }));
      setDecisions(mappedDecisions);
    }
  }, [decisionsData]);

  useEffect(() => {
    if (predictionsData?.predictions) {
      setPredictions(predictionsData.predictions);
    }
  }, [predictionsData]);

  useEffect(() => {
    if (metricsData) {
      setMetrics({
        autonomousActions: metricsData.autonomous_approval_rate || metricsData.autonomous_percentage || 95,
        preventionSavings: metricsData.monthly_savings_usd || metricsData.prevention_savings || 128000,
        predictionAccuracy: metricsData.prediction_accuracy || 89,
        activeIncidents: metricsData.active_incidents || 3,
      });
    }
  }, [metricsData]);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // WebSocket connection for real-time updates from Python backend
  useEffect(() => {
    // Subscribe to connection status changes
    const unsubscribeConnection = wsManager.onConnectionChange((connected) => {
      setIsConnected(connected);
    });

    const unsubscribe = wsManager.subscribe((message) => {
      console.log("Received WebSocket message:", message);
      
      if (message.type === "system_update") {
        // Update agents if provided
        if (message.agents && message.agents.length > 0) {
          const updatedAgents = MOCK_AGENTS.map((mockAgent) => {
            const liveAgent = message.agents?.find((a: any) => a.id === mockAgent.id);
            if (liveAgent) {
              return {
                ...mockAgent,
                status: liveAgent.status as any,
                activeTasks: liveAgent.active_tasks || mockAgent.activeTasks,
                uptime: liveAgent.uptime || mockAgent.uptime,
                decisionsPerHour: liveAgent.decisions_per_hour || mockAgent.decisionsPerHour,
                accuracy: liveAgent.accuracy || mockAgent.accuracy
              };
            }
            return mockAgent;
          });
          setAgents(updatedAgents);
        }

        // Update predictions if provided
        if (message.predictions && message.predictions.length > 0) {
          const updatedPredictions = message.predictions.map((p: any) => ({
            id: p.id,
            agentName: p.agent_name,
            agentIcon: MOCK_PREDICTIONS[0].agentIcon,
            agentColor: MOCK_PREDICTIONS[0].agentColor,
            type: p.type as 'outage' | 'performance' | 'cost' | 'security',
            description: p.description,
            probability: p.probability,
            timeframe: p.timeframe,
            impact: p.impact,
            preventiveCost: p.preventive_cost,
            failureCost: p.failure_cost
          }));
          setPredictions(updatedPredictions);
        }

        // Update recent decision if provided
        if (message.recent_decision) {
          const newDecision = {
            id: message.recent_decision.id,
            timestamp: message.recent_decision.timestamp,
            agentName: message.recent_decision.agent_name,
            agentIcon: MOCK_DECISIONS[0].agentIcon,
            agentColor: MOCK_DECISIONS[0].agentColor,
            decisionType: message.recent_decision.decision_type,
            description: message.recent_decision.description,
            cost: message.recent_decision.cost,
            roi: message.recent_decision.roi,
            autonomyLevel: message.recent_decision.autonomy_level as 1 | 2 | 3,
            autoApproved: message.recent_decision.auto_approved
          };
          setDecisions((prev) => [newDecision, ...prev.slice(0, 9)]);
        }

        // Update metrics if provided - use functional update to avoid stale closures
        if (message.metrics) {
          setMetrics((prev) => ({
            autonomousActions: message.metrics.autonomous_percentage ?? prev.autonomousActions,
            preventionSavings: message.metrics.prevention_savings ?? prev.preventionSavings,
            predictionAccuracy: message.metrics.prediction_accuracy ?? prev.predictionAccuracy,
            activeIncidents: message.metrics.active_incidents ?? prev.activeIncidents
          }));
        }
      }
    });

    return () => {
      unsubscribe();
      unsubscribeConnection();
    };
  }, []);

  const performanceData = [
    { time: '6h ago', accuracy: 82, falsePositives: 15 },
    { time: '5h ago', accuracy: 84, falsePositives: 14 },
    { time: '4h ago', accuracy: 85, falsePositives: 12 },
    { time: '3h ago', accuracy: 86, falsePositives: 11 },
    { time: '2h ago', accuracy: 87, falsePositives: 9 },
    { time: '1h ago', accuracy: 88, falsePositives: 8 },
    { time: 'Now', accuracy: 89, falsePositives: 7 },
  ];

  const financialData = [
    { agent: 'Monitor', savings: 45000, cost: 3200, roi: 14 },
    { agent: 'Decision', savings: 38000, cost: 2800, roi: 13 },
    { agent: 'Resource', savings: 28000, cost: 2400, roi: 11 },
    { agent: 'Security', savings: 52000, cost: 4200, roi: 12 },
    { agent: 'Financial', savings: 34000, cost: 2600, roi: 13 },
    { agent: 'Lifecycle', savings: 22000, cost: 2000, roi: 11 },
  ];

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-16 items-center justify-between px-6 max-w-[1920px] mx-auto">
          <div className="flex items-center gap-4">
            <div>
              <h1 className="text-xl font-semibold">MSP AI Orchestrator</h1>
              <p className="text-xs text-muted-foreground">Autonomous Multi-Agent System</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <ConnectionStatus 
              isConnected={isConnected} 
              lastUpdate={isConnected ? "live" : undefined}
            />
            <div className="text-xs font-mono text-muted-foreground">
              {currentTime.toLocaleTimeString()}
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="p-6 max-w-[1920px] mx-auto">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList data-testid="tabs-main-navigation">
            <TabsTrigger value="overview" data-testid="tab-overview">Overview</TabsTrigger>
            <TabsTrigger value="agents" data-testid="tab-agents">Agents</TabsTrigger>
            <TabsTrigger value="predictions" data-testid="tab-predictions">Predictions</TabsTrigger>
            <TabsTrigger value="decisions" data-testid="tab-decisions">Decisions</TabsTrigger>
            <TabsTrigger value="analytics" data-testid="tab-analytics">Analytics</TabsTrigger>
            <TabsTrigger value="escalations" data-testid="tab-escalations">
              Escalations
              <Badge variant="destructive" className="ml-2">2</Badge>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                label="Autonomous Actions"
                value={`${metrics.autonomousActions}%`}
                icon={Target}
                trend={{ value: 2.3, isPositive: true }}
                testId="metric-autonomous-actions"
              />
              <MetricCard
                label="Prevention Savings"
                value={`$${Math.round(metrics.preventionSavings / 1000)}K`}
                icon={DollarSign}
                trend={{ value: 12, isPositive: true }}
                testId="metric-prevention-savings"
              />
              <MetricCard
                label="Prediction Accuracy"
                value={`${Math.round(metrics.predictionAccuracy)}%`}
                icon={TrendingUp}
                trend={{ value: 2.1, isPositive: true }}
                testId="metric-prediction-accuracy"
              />
              <MetricCard
                label="Active Incidents"
                value={metrics.activeIncidents}
                icon={AlertTriangle}
                trend={{ value: 40, isPositive: false }}
                testId="metric-active-incidents"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <div>
                  <h2 className="text-lg font-semibold mb-4">Active Agents</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
                    {agents.map((agent) => (
                      <AgentCard 
                        key={agent.id} 
                        {...agent} 
                        onViewDetails={() => {
                          alert(`Agent: ${agent.name}\n\nStatus: ${agent.status}\nActive Tasks: ${agent.activeTasks}\nUptime: ${agent.uptime}%\nDecisions/Hour: ${agent.decisionsPerHour}\nAccuracy: ${agent.accuracy}%\n\nRecent Activity:\n${agent.recentActivity}`);
                        }}
                      />
                    ))}
                  </div>
                </div>

                <div>
                  <h2 className="text-lg font-semibold mb-4">Upcoming Predictions</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {predictions.slice(0, 2).map((prediction) => (
                      <PredictionCard key={prediction.id} {...prediction} />
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <Card className="p-4">
                  <h2 className="text-sm font-semibold mb-4">Live Decision Feed</h2>
                  <div className="space-y-0 max-h-[800px] overflow-y-auto">
                    {decisions.map((decision) => (
                      <DecisionLogItem key={decision.id} {...decision} />
                    ))}
                  </div>
                </Card>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="agents" className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold mb-4">All Agents Status</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
                {agents.map((agent) => (
                  <AgentCard 
                    key={agent.id} 
                    {...agent} 
                    onViewDetails={() => {
                      alert(`Agent: ${agent.name}\n\nStatus: ${agent.status}\nActive Tasks: ${agent.activeTasks}\nUptime: ${agent.uptime}%\nDecisions/Hour: ${agent.decisionsPerHour}\nAccuracy: ${agent.accuracy}%\n\nRecent Activity:\n${agent.recentActivity}`);
                    }}
                  />
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="predictions" className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold mb-4">Predictive Timeline - Next 72 Hours</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {predictions.map((prediction) => (
                  <PredictionCard key={prediction.id} {...prediction} />
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="decisions" className="space-y-6">
            <Card className="p-6">
              <h2 className="text-lg font-semibold mb-4">Autonomous Decision Log</h2>
              <div className="space-y-0">
                {decisions.map((decision) => (
                  <DecisionLogItem key={decision.id} {...decision} />
                ))}
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <PerformanceChart
                title="Learning Performance - Last 6 Hours"
                data={performanceData}
                dataKeys={[
                  { key: 'accuracy', label: 'Prediction Accuracy (%)', color: 'hsl(var(--chart-1))' },
                  { key: 'falsePositives', label: 'False Positive Rate (%)', color: 'hsl(var(--chart-5))' },
                ]}
              />
              <FinancialImpactChart
                title="ROI by Agent - Last 30 Days"
                data={financialData}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard label="Avg Decision Time" value="4.2s" />
              <MetricCard label="Success Rate" value="92%" trend={{ value: 1.5, isPositive: true }} />
              <MetricCard label="Cost Avoidance" value="$428K" trend={{ value: 18, isPositive: true }} />
              <MetricCard label="Model Updates" value="147" />
            </div>
          </TabsContent>

          <TabsContent value="escalations" className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold mb-4">Pending Escalations - Requires Human Approval</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
                  onApprove={() => console.log('Approved infrastructure upgrade')}
                  onReject={() => console.log('Rejected infrastructure upgrade')}
                  onRequestInfo={() => console.log('Requested more info')}
                />
                <EscalationCard
                  id="esc-2"
                  decisionType="Custom Client Contract Negotiation"
                  timestamp="14:28:55"
                  urgencyLevel="medium"
                  whyEscalated="Contract terms outside standard parameters - requires custom pricing structure"
                  riskAssessment="Low risk - client has strong credit history and existing relationship. Non-standard SLA requirements."
                  businessImpact="High-value enterprise client (projected $180K annual revenue). Custom terms could set precedent for similar deals."
                  actionPreview="Approve custom 99.99% uptime SLA with dedicated support team and 15-minute response time guarantee"
                  estimatedCost={8500}
                  onApprove={() => console.log('Approved contract terms')}
                  onReject={() => console.log('Rejected contract terms')}
                  onRequestInfo={() => console.log('Requested more info')}
                />
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
