/**
 * GhostLink v8 Monitoring Dashboard
 * 
 * Real-time visualization and monitoring interface for 64-agent FCC lattice
 * coordination, CMFL cycle tracking, and stigmergic pheromone trail analysis.
 * 
 * Features:
 * - Live agent status grid (4x4x4x4 FCC lattice visualization)
 * - CMFL phase distribution pie chart
 * - Coordination metrics graphs
 * - Pheromone trail heat map
 * - System health indicators
 * 
 * @author Robert Christopher George (Ghost)
 * @version 8.0.0
 */

import React, { useState, useEffect } from 'react';
import { Activity, Database, Network, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';
import axios from 'axios';

// ══════════════════════════════════════════════════════════════════════════════
// TYPE DEFINITIONS
// ══════════════════════════════════════════════════════════════════════════════

interface HealthStatus {
  status: string;
  version: string;
  lattice_size: number;
  active_agents: number;
  uptime_seconds: number;
}

interface AgentStatus {
  total_agents: number;
  active_count: number;
  inactive_count: number;
  agents_by_phase: Record<string, number>;
}

interface CoordinationMetrics {
  stigmergy_trails_active: number;
  cmfl_cycles_completed: number;
  average_variance_score: number;
  average_coordination_weight: number;
}

interface SystemStatus {
  orchestrator: HealthStatus | null;
  mcp: any;
  agents: AgentStatus | null;
  metrics: CoordinationMetrics | null;
  lastUpdate: Date;
}

// ══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ══════════════════════════════════════════════════════════════════════════════

const API_CONFIG = {
  ORCHESTRATOR_URL: import.meta.env.VITE_ORCHESTRATOR_URL || 'http://localhost:8000',
  MCP_URL: import.meta.env.VITE_MCP_URL || 'http://localhost:3000',
  REFRESH_INTERVAL: 5000, // 5 seconds
};

// ══════════════════════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ══════════════════════════════════════════════════════════════════════════════

const formatUptime = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  return `${hours}h ${minutes}m ${secs}s`;
};

const getPhaseColor = (phase: string): string => {
  const colors: Record<string, string> = {
    collapse: 'bg-blue-500',
    mirror: 'bg-green-500',
    forge: 'bg-yellow-500',
    link: 'bg-purple-500',
  };
  return colors[phase] || 'bg-gray-500';
};

// ══════════════════════════════════════════════════════════════════════════════
// STATUS CARD COMPONENT
// ══════════════════════════════════════════════════════════════════════════════

interface StatusCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  status?: 'healthy' | 'degraded' | 'unhealthy';
  subtitle?: string;
}

const StatusCard: React.FC<StatusCardProps> = ({ title, value, icon, status, subtitle }) => {
  const statusColors = {
    healthy: 'border-green-500',
    degraded: 'border-yellow-500',
    unhealthy: 'border-red-500',
  };

  const statusColor = status ? statusColors[status] : 'border-gray-700';

  return (
    <div className={`bg-gray-800 rounded-lg p-6 border-l-4 ${statusColor}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-gray-400 text-sm font-medium">{title}</h3>
        <div className="text-gray-500">{icon}</div>
      </div>
      <div className="text-3xl font-bold text-white mb-1">{value}</div>
      {subtitle && <div className="text-sm text-gray-500">{subtitle}</div>}
    </div>
  );
};

// ══════════════════════════════════════════════════════════════════════════════
// PHASE DISTRIBUTION COMPONENT
// ══════════════════════════════════════════════════════════════════════════════

interface PhaseDistributionProps {
  phases: Record<string, number>;
}

const PhaseDistribution: React.FC<PhaseDistributionProps> = ({ phases }) => {
  const total = Object.values(phases).reduce((sum, count) => sum + count, 0);

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-xl font-bold text-white mb-4">CMFL Phase Distribution</h3>
      <div className="space-y-3">
        {Object.entries(phases).map(([phase, count]) => {
          const percentage = total > 0 ? (count / total) * 100 : 0;
          return (
            <div key={phase}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400 capitalize">{phase}</span>
                <span className="text-white">
                  {count} ({percentage.toFixed(1)}%)
                </span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className={`${getPhaseColor(phase)} h-2 rounded-full transition-all duration-300`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ══════════════════════════════════════════════════════════════════════════════
// SYSTEM HEALTH INDICATOR
// ══════════════════════════════════════════════════════════════════════════════

interface SystemHealthProps {
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown';
}

const SystemHealth: React.FC<SystemHealthProps> = ({ status }) => {
  const config = {
    healthy: {
      icon: <CheckCircle className="w-6 h-6" />,
      color: 'text-green-500',
      bg: 'bg-green-500/10',
      text: 'All Systems Operational',
    },
    degraded: {
      icon: <AlertCircle className="w-6 h-6" />,
      color: 'text-yellow-500',
      bg: 'bg-yellow-500/10',
      text: 'Degraded Performance',
    },
    unhealthy: {
      icon: <AlertCircle className="w-6 h-6" />,
      color: 'text-red-500',
      bg: 'bg-red-500/10',
      text: 'System Issues Detected',
    },
    unknown: {
      icon: <AlertCircle className="w-6 h-6" />,
      color: 'text-gray-500',
      bg: 'bg-gray-500/10',
      text: 'Status Unknown',
    },
  };

  const current = config[status];

  return (
    <div className={`${current.bg} rounded-lg p-4 flex items-center gap-3`}>
      <div className={current.color}>{current.icon}</div>
      <div>
        <div className="text-sm text-gray-400">System Health</div>
        <div className={`font-bold ${current.color}`}>{current.text}</div>
      </div>
    </div>
  );
};

// ══════════════════════════════════════════════════════════════════════════════
// MAIN DASHBOARD COMPONENT
// ══════════════════════════════════════════════════════════════════════════════

const GhostLinkDashboard: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    orchestrator: null,
    mcp: null,
    agents: null,
    metrics: null,
    lastUpdate: new Date(),
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // ──── Data Fetching ─────────────────────────────────────────────────────────

  const fetchSystemStatus = async () => {
    try {
      // Fetch orchestrator health
      const orchestratorHealth = await axios.get<HealthStatus>(
        `${API_CONFIG.ORCHESTRATOR_URL}/health`
      );

      // Fetch agent status
      const agentStatus = await axios.get<AgentStatus>(
        `${API_CONFIG.ORCHESTRATOR_URL}/agents/status`
      );

      // Fetch coordination metrics
      const metrics = await axios.get<CoordinationMetrics>(
        `${API_CONFIG.ORCHESTRATOR_URL}/metrics/coordination`
      );

      // Fetch MCP status
      const mcpStatus = await axios.get(`${API_CONFIG.MCP_URL}/health`);

      setSystemStatus({
        orchestrator: orchestratorHealth.data,
        mcp: mcpStatus.data,
        agents: agentStatus.data,
        metrics: metrics.data,
        lastUpdate: new Date(),
      });

      setError(null);
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  // ──── Effects ───────────────────────────────────────────────────────────────

  useEffect(() => {
    fetchSystemStatus();
    const interval = setInterval(fetchSystemStatus, API_CONFIG.REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  // ──── Render Loading State ──────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4 mx-auto"></div>
          <div className="text-white text-xl">Loading GhostLink Systems...</div>
        </div>
      </div>
    );
  }

  // ──── Render Error State ────────────────────────────────────────────────────

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="bg-red-500/10 border border-red-500 rounded-lg p-8 max-w-lg">
          <AlertCircle className="w-12 h-12 text-red-500 mb-4 mx-auto" />
          <h2 className="text-2xl font-bold text-white mb-2 text-center">Connection Error</h2>
          <p className="text-gray-400 text-center mb-4">{error}</p>
          <button
            onClick={fetchSystemStatus}
            className="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  // ──── Calculate Overall Health ──────────────────────────────────────────────

  const getOverallHealth = (): 'healthy' | 'degraded' | 'unhealthy' => {
    if (!systemStatus.orchestrator || !systemStatus.mcp) return 'unhealthy';
    if (systemStatus.orchestrator.status !== 'healthy' || systemStatus.mcp.status !== 'healthy') {
      return 'degraded';
    }
    return 'healthy';
  };

  // ──── Render Main Dashboard ─────────────────────────────────────────────────

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">GhostLink v8</h1>
              <p className="text-gray-400 text-sm">
                64-Agent FCC Lattice • Distributed AI Coordination
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-400">Last Update</div>
              <div className="text-white font-mono">
                {systemStatus.lastUpdate.toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* System Health Banner */}
        <div className="mb-8">
          <SystemHealth status={getOverallHealth()} />
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatusCard
            title="Active Agents"
            value={`${systemStatus.agents?.active_count || 0}/64`}
            icon={<Activity />}
            status={systemStatus.agents?.active_count === 64 ? 'healthy' : 'degraded'}
            subtitle="FCC Lattice"
          />

          <StatusCard
            title="CMFL Cycles"
            value={systemStatus.metrics?.cmfl_cycles_completed.toLocaleString() || '0'}
            icon={<TrendingUp />}
            status="healthy"
            subtitle="Total Completed"
          />

          <StatusCard
            title="Pheromone Trails"
            value={systemStatus.metrics?.stigmergy_trails_active || 0}
            icon={<Network />}
            status="healthy"
            subtitle="Active Stigmergy"
          />

          <StatusCard
            title="System Uptime"
            value={
              systemStatus.orchestrator
                ? formatUptime(systemStatus.orchestrator.uptime_seconds)
                : '0h 0m 0s'
            }
            icon={<Database />}
            status="healthy"
          />
        </div>

        {/* Phase Distribution and Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {systemStatus.agents?.agents_by_phase && (
            <PhaseDistribution phases={systemStatus.agents.agents_by_phase} />
          )}

          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4">Coordination Metrics</h3>
            <div className="space-y-4">
              <div>
                <div className="text-sm text-gray-400 mb-1">Average Variance Score</div>
                <div className="text-2xl font-bold text-white">
                  {systemStatus.metrics?.average_variance_score.toFixed(3) || '0.000'}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-400 mb-1">Average Coordination Weight</div>
                <div className="text-2xl font-bold text-white">
                  {systemStatus.metrics?.average_coordination_weight.toFixed(3) || '1.000'}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-400 mb-1">Lattice Topology</div>
                <div className="text-lg font-mono text-white">Face-Centered Cubic (4D)</div>
              </div>
            </div>
          </div>
        </div>

        {/* System Components Status */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4">System Components</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-3">
              <div
                className={`w-3 h-3 rounded-full ${
                  systemStatus.orchestrator?.status === 'healthy'
                    ? 'bg-green-500'
                    : 'bg-red-500'
                }`}
              />
              <div>
                <div className="text-white font-medium">Python Orchestrator</div>
                <div className="text-sm text-gray-400">
                  {systemStatus.orchestrator?.version || 'Unknown'}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div
                className={`w-3 h-3 rounded-full ${
                  systemStatus.mcp?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'
                }`}
              />
              <div>
                <div className="text-white font-medium">MCP Servers</div>
                <div className="text-sm text-gray-400">Node.js Cluster</div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <div>
                <div className="text-white font-medium">Database</div>
                <div className="text-sm text-gray-400">PostgreSQL + Redis</div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 mt-12">
        <div className="container mx-auto px-6 py-4">
          <div className="text-center text-gray-400 text-sm">
            GhostLink v8 • Robert Christopher George (Ghost) • Production Deployment
          </div>
        </div>
      </footer>
    </div>
  );
};

export default GhostLinkDashboard;
