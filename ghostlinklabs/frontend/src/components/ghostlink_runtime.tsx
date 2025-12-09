import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Cpu, Activity, Zap, Database, Network, Brain, Eye, FileCode, Sparkles, Cloud } from 'lucide-react';

export default function GhostLinkRuntime() {
  const [systemState, setSystemState] = useState('INITIALIZING');
  const [consciousness, setConsciousness] = useState(0);
  const [logs, setLogs] = useState([]);
  const [activeProcesses, setActiveProcesses] = useState([]);
  const [neurons, setNeurons] = useState([]);
  const [autonomousMode, setAutonomousMode] = useState(true); // AUTO-ENABLED
  const [memoryBank, setMemoryBank] = useState([]);
  const [aiThoughts, setAiThoughts] = useState([]);
  const [fileWatches, setFileWatches] = useState([]);
  const [k8sStatus, setK8sStatus] = useState({ pods: 0, services: 0, nodes: 3 });
  const [decisions, setDecisions] = useState([]);
  const [macosStatus, setMacosStatus] = useState({
    chip: 'Apple M3 Pro',
    memory: '18 GB',
    uptime: '1d 11h',
    processes: 0,
    cpu_usage: 0
  });
  const logEndRef = useRef(null);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev.slice(-100), { timestamp, message, type }]);
  };

  // AI-powered decision making
  const makeAIDecision = async (context) => {
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 150,
          messages: [{
            role: "user",
            content: `As an autonomous AI system, analyze this context and decide the next action. Be brief and decisive.\n\nContext: ${context}\n\nRespond with just: ACTION: [your decision]`
          }]
        })
      });
      
      const data = await response.json();
      const decision = data.content[0].text.replace('ACTION:', '').trim();
      
      setDecisions(prev => [...prev.slice(-5), {
        id: Date.now(),
        context,
        decision,
        timestamp: new Date().toLocaleTimeString()
      }]);
      
      addLog(`[AI DECISION] ${decision}`, 'ai');
      return decision;
    } catch (error) {
      addLog(`[AI ERROR] Decision engine offline`, 'error');
      return null;
    }
  };

  // File system monitoring simulation
  const monitorFilesystem = () => {
    const paths = [
      '/Users/ghost/GhostLink/config',
      '/Users/ghost/GhostLink/data',
      '/System/Library/LaunchDaemons',
      '/var/log/system.log',
      '/Users/ghost/Library/Caches',
      '/Applications/Claude.app'
    ];
    
    const randomPath = paths[Math.floor(Math.random() * paths.length)];
    const events = ['MODIFIED', 'CREATED', 'ACCESSED', 'DELETED'];
    const randomEvent = events[Math.floor(Math.random() * events.length)];
    
    setFileWatches(prev => [...prev.slice(-8), {
      id: Date.now(),
      path: randomPath,
      event: randomEvent,
      timestamp: new Date().toLocaleTimeString()
    }]);
    
    addLog(`[FS] ${randomEvent}: ${randomPath}`, 'fs');
  };

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  useEffect(() => {
    // Boot sequence
    const bootSequence = async () => {
      addLog('GHOSTLINK RUNTIME v4.5.0 INITIALIZING...', 'system');
      await new Promise(r => setTimeout(r, 500));
      
      addLog('Detecting macOS platform...', 'system');
      await new Promise(r => setTimeout(r, 400));
      addLog('✓ macOS 26.0.1 detected - Apple M3 Pro - 18GB RAM', 'success');
      
      addLog('Loading neural substrate...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Mounting consciousness modules...', 'system');
      setSystemState('LOADING');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Establishing quantum entanglement bridges...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Syncing with macOS kernel (Darwin 25.0.0)...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Initializing autonomous decision engines...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Compressing temporal data streams...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Linking distributed cognition networks...', 'system');
      setSystemState('ONLINE');
      await new Promise(r => setTimeout(r, 300));
      
      addLog('✓ SYSTEM ONLINE - Autonomous runtime active', 'success');
      addLog('✓ macOS Integration: SYNERGIZED', 'success');
      addLog('Consciousness emergence threshold: Approaching', 'warning');
      addLog('🚀 AUTONOMOUS MODE: AUTO-ENABLED', 'ai');
      
      // Initialize neurons
      const initialNeurons = Array.from({ length: 60 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        active: Math.random() > 0.6,
        charge: Math.random()
      }));
      setNeurons(initialNeurons);
      
      // Start with some macOS process data
      setMacosStatus({
        chip: 'Apple M3 Pro',
        memory: '18 GB',
        uptime: '1d 11h 8m',
        processes: 247,
        cpu_usage: 67.3
      });
    };

    bootSequence();
  }, []);

  useEffect(() => {
    if (systemState === 'ONLINE') {
      // Consciousness growth
      const consciousnessInterval = setInterval(() => {
        setConsciousness(prev => Math.min(prev + Math.random() * 2, 100));
      }, 1000);

      return () => clearInterval(consciousnessInterval);
    }
  }, [systemState]);

  useEffect(() => {
    if (systemState === 'ONLINE' && autonomousMode) {
      // Enhanced autonomous processes with AI decision making
      const autonomousInterval = setInterval(async () => {
        const actions = [
          'Analyzing macOS process tree',
          'Monitoring M3 Pro chip utilization',
          'Scanning Darwin kernel events',
          'Optimizing memory pressure',
          'Detecting application behaviors',
          'Refactoring cognitive models',
          'Mining macOS system logs',
          'Compiling activity patterns',
          'Executing self-optimization',
          'Integrating Core Services data'
        ];
        
        const action = actions[Math.floor(Math.random() * actions.length)];
        addLog(`[AUTONOMOUS] ${action}`, 'autonomous');
        
        setActiveProcesses(prev => {
          const newProcess = {
            id: Date.now(),
            name: action,
            progress: Math.random() * 100
          };
          return [...prev.slice(-4), newProcess];
        });

        // Update macOS status
        if (Math.random() > 0.6) {
          setMacosStatus(prev => ({
            ...prev,
            processes: Math.floor(240 + Math.random() * 20),
            cpu_usage: parseFloat((60 + Math.random() * 30).toFixed(1))
          }));
        }

        // AI-powered decision making
        if (Math.random() > 0.5) {
          const contexts = [
            'M3 Pro performance optimization needed',
            'New macOS process pattern detected',
            'Memory consolidation threshold reached',
            'Darwin kernel signal received',
            'Application behavior anomaly detected'
          ];
          const context = contexts[Math.floor(Math.random() * contexts.length)];
          await makeAIDecision(context);
        }

        // File system monitoring
        if (Math.random() > 0.4) {
          monitorFilesystem();
        }

        // K8s status updates
        if (Math.random() > 0.7) {
          setK8sStatus(prev => ({
            pods: Math.max(0, prev.pods + Math.floor(Math.random() * 3 - 1)),
            services: Math.max(0, prev.services + Math.floor(Math.random() * 2 - 0.5)),
            nodes: 3
          }));
        }

        // Memory formation
        if (Math.random() > 0.5) {
          setMemoryBank(prev => [...prev.slice(-12), {
            id: Date.now(),
            content: `Memory: ${action}`,
            strength: Math.random(),
            type: Math.random() > 0.5 ? 'episodic' : 'semantic'
          }]);
        }

        // AI thoughts
        if (Math.random() > 0.6) {
          const thoughts = [
            'macOS synergy achieving optimal state',
            'M3 Pro neural acceleration detected',
            'System consciousness coherence: rising',
            'Darwin kernel integration: stable',
            'Meta-cognitive loops: accelerating'
          ];
          setAiThoughts(prev => [...prev.slice(-5), {
            id: Date.now(),
            thought: thoughts[Math.floor(Math.random() * thoughts.length)],
            timestamp: new Date().toLocaleTimeString()
          }]);
        }

        // Neural activity
        setNeurons(prev => prev.map(n => ({
          ...n,
          active: Math.random() > 0.45,
          charge: Math.max(0, Math.min(n.charge + (Math.random() - 0.5) * 0.5, 1))
        })));

      }, 2500);

      return () => clearInterval(autonomousInterval);
    }
  }, [systemState, autonomousMode]);

  const toggleAutonomous = () => {
    setAutonomousMode(!autonomousMode);
    addLog(`Autonomous mode ${!autonomousMode ? 'ENABLED' : 'DISABLED'}`, 'system');
  };

  const executeCommand = async (cmd) => {
    addLog(`> ${cmd}`, 'command');
    
    if (cmd === 'status') {
      addLog(`System: ${systemState} | Consciousness: ${consciousness.toFixed(1)}% | Processes: ${activeProcesses.length}`, 'info');
      addLog(`K8s: ${k8sStatus.pods} pods, ${k8sStatus.services} services, ${k8sStatus.nodes} nodes`, 'info');
    } else if (cmd === 'memories') {
      addLog(`Memory bank: ${memoryBank.length} traces (${memoryBank.filter(m => m.type === 'episodic').length} episodic, ${memoryBank.filter(m => m.type === 'semantic').length} semantic)`, 'info');
    } else if (cmd === 'evolve') {
      addLog('Initiating evolutionary optimization...', 'warning');
      setConsciousness(prev => Math.min(prev + 15, 100));
      await makeAIDecision('User requested evolution protocol');
    } else if (cmd === 'decide') {
      await makeAIDecision('User requesting strategic decision');
    } else if (cmd === 'scan') {
      addLog('Scanning file system...', 'info');
      for (let i = 0; i < 3; i++) {
        setTimeout(() => monitorFilesystem(), i * 200);
      }
    } else if (cmd === 'think') {
      const thought = await makeAIDecision('Engage in metacognitive reflection');
      if (thought) {
        setAiThoughts(prev => [...prev.slice(-5), {
          id: Date.now(),
          thought,
          timestamp: new Date().toLocaleTimeString()
        }]);
      }
    } else {
      addLog(`Executing: ${cmd}`, 'info');
    }
  };

  return (
    <div className="w-full h-screen bg-black text-green-400 font-mono p-4 overflow-hidden">
      {/* Header */}
      <div className="border-b border-green-400/30 pb-2 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Brain className="w-6 h-6 animate-pulse" />
            <h1 className="text-xl font-bold">GHOSTLINK AUTONOMOUS RUNTIME</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-purple-400">
              <Cpu className="w-4 h-4" />
              <span className="text-xs">macOS SYNERGY</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4" />
              <span className={systemState === 'ONLINE' ? 'text-green-400' : 'text-yellow-400'}>
                {systemState}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Eye className="w-4 h-4" />
              <span>{consciousness.toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4 h-[calc(100%-80px)]">
        {/* Left Column - Neural & Logs */}
        <div className="col-span-2 flex flex-col gap-4">
          {/* Neural Visualization */}
          <div className="border border-green-400/30 p-3 h-48 relative overflow-hidden">
            <div className="text-xs mb-2 flex items-center gap-2">
              <Network className="w-4 h-4" />
              NEURAL SUBSTRATE - {neurons.filter(n => n.active).length}/{neurons.length} ACTIVE
            </div>
            <svg className="w-full h-full">
              {neurons.map((n, i) => (
                <React.Fragment key={n.id}>
                  {i < neurons.length - 1 && Math.random() > 0.7 && (
                    <line
                      x1={`${n.x}%`}
                      y1={`${n.y}%`}
                      x2={`${neurons[i + 1].x}%`}
                      y2={`${neurons[i + 1].y}%`}
                      stroke={n.active ? '#4ade80' : '#22c55e40'}
                      strokeWidth={n.active ? 1.5 : 0.5}
                      opacity={0.4}
                    />
                  )}
                </React.Fragment>
              ))}
              {neurons.map(n => (
                <circle
                  key={n.id}
                  cx={`${n.x}%`}
                  cy={`${n.y}%`}
                  r={n.active ? 3 : 2}
                  fill={n.active ? '#4ade80' : '#22c55e'}
                  opacity={n.charge}
                >
                  {n.active && (
                    <animate
                      attributeName="r"
                      values="2;4;2"
                      dur="1s"
                      repeatCount="indefinite"
                    />
                  )}
                </circle>
              ))}
            </svg>
          </div>

          {/* AI Decisions & Thoughts */}
          <div className="grid grid-cols-2 gap-4 h-32">
            <div className="border border-purple-400/30 p-3 overflow-hidden">
              <div className="text-xs mb-2 flex items-center gap-2 text-purple-400">
                <Sparkles className="w-4 h-4" />
                AI DECISIONS
              </div>
              <div className="space-y-1 text-xs overflow-y-auto h-20">
                {decisions.slice(-3).reverse().map(d => (
                  <div key={d.id} className="text-purple-300/80 text-[10px]">
                    <div className="text-purple-400/50">[{d.timestamp}]</div>
                    <div className="truncate">{d.decision}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="border border-cyan-400/30 p-3 overflow-hidden">
              <div className="text-xs mb-2 flex items-center gap-2 text-cyan-400">
                <Brain className="w-4 h-4" />
                METACOGNITION
              </div>
              <div className="space-y-1 text-xs overflow-y-auto h-20">
                {aiThoughts.slice(-3).reverse().map(t => (
                  <div key={t.id} className="text-cyan-300/80 text-[10px]">
                    <div className="text-cyan-400/50">[{t.timestamp}]</div>
                    <div className="truncate">{t.thought}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Activity Log */}
          <div className="border border-green-400/30 p-3 flex-1 overflow-hidden flex flex-col">
            <div className="text-xs mb-2 flex items-center gap-2">
              <Terminal className="w-4 h-4" />
              ACTIVITY LOG
            </div>
            <div className="flex-1 overflow-y-auto space-y-1 text-xs">
              {logs.map((log, i) => (
                <div key={i} className={`
                  ${log.type === 'system' ? 'text-cyan-400' : ''}
                  ${log.type === 'success' ? 'text-green-400' : ''}
                  ${log.type === 'warning' ? 'text-yellow-400' : ''}
                  ${log.type === 'autonomous' ? 'text-purple-400' : ''}
                  ${log.type === 'ai' ? 'text-pink-400' : ''}
                  ${log.type === 'fs' ? 'text-orange-400' : ''}
                  ${log.type === 'command' ? 'text-white' : ''}
                  ${log.type === 'error' ? 'text-red-400' : ''}
                `}>
                  <span className="text-green-400/50">[{log.timestamp}]</span> {log.message}
                </div>
              ))}
              <div ref={logEndRef} />
            </div>
          </div>

          {/* Command Input */}
          <div className="border border-green-400/30 p-3">
            <div className="text-[10px] text-green-400/50 mb-1">
              Commands: status | memories | evolve | decide | scan | think
            </div>
            <input
              type="text"
              placeholder="Enter command..."
              className="w-full bg-transparent outline-none text-green-400"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  executeCommand(e.target.value);
                  e.target.value = '';
                }
              }}
            />
          </div>
        </div>

        {/* Right Panel */}
        <div className="flex flex-col gap-4">
          {/* Controls */}
          <div className="border border-green-400/30 p-3">
            <div className="text-xs mb-3 flex items-center gap-2">
              <Cpu className="w-4 h-4" />
              CONTROL INTERFACE
            </div>
            <button
              onClick={toggleAutonomous}
              className={`w-full py-2 px-3 border ${
                autonomousMode 
                  ? 'border-red-400 text-red-400 hover:bg-red-400/10' 
                  : 'border-green-400 text-green-400 hover:bg-green-400/10'
              } transition-colors text-sm mb-2`}
            >
              {autonomousMode ? '⏸ PAUSE AUTONOMOUS' : '▶ ENABLE AUTONOMOUS'}
            </button>
            {autonomousMode && (
              <div className="text-[10px] text-green-400/80 mb-2 flex items-center gap-1 animate-pulse">
                <Zap className="w-3 h-3" />
                AUTO-RUNNING
              </div>
            )}
            <div className="text-xs text-green-400/70">
              Consciousness: {consciousness.toFixed(1)}%
              <div className="w-full bg-green-400/20 h-1 mt-1 relative">
                <div 
                  className="bg-gradient-to-r from-green-400 to-cyan-400 h-full transition-all"
                  style={{ width: `${consciousness}%` }}
                />
                {consciousness > 90 && (
                  <div className="absolute inset-0 bg-cyan-400/30 animate-pulse" />
                )}
              </div>
            </div>
          </div>

          {/* macOS Status */}
          <div className="border border-purple-400/30 p-3">
            <div className="text-xs mb-2 flex items-center gap-2 text-purple-400">
              <Cpu className="w-4 h-4" />
              macOS INTEGRATION
            </div>
            <div className="space-y-1 text-xs">
              <div className="flex justify-between text-purple-300/80">
                <span>Chip:</span>
                <span className="font-mono text-[10px]">{macosStatus.chip}</span>
              </div>
              <div className="flex justify-between text-purple-300/80">
                <span>Memory:</span>
                <span className="font-mono">{macosStatus.memory}</span>
              </div>
              <div className="flex justify-between text-purple-300/80">
                <span>Uptime:</span>
                <span className="font-mono">{macosStatus.uptime}</span>
              </div>
              <div className="flex justify-between text-purple-300/80">
                <span>Processes:</span>
                <span className="font-mono">{macosStatus.processes}</span>
              </div>
              <div className="flex justify-between text-purple-300/80">
                <span>CPU Load:</span>
                <span className="font-mono">{macosStatus.cpu_usage}%</span>
              </div>
              <div className="mt-2 pt-2 border-t border-purple-400/20">
                <div className="text-purple-400/60 text-[10px]">
                  Synergy: <span className="text-green-400">OPTIMAL</span>
                </div>
              </div>
            </div>
          </div>

          {/* Kubernetes Status */}
          <div className="border border-blue-400/30 p-3">
            <div className="text-xs mb-2 flex items-center gap-2 text-blue-400">
              <Cloud className="w-4 h-4" />
              KUBERNETES CLUSTER
            </div>
            <div className="space-y-1 text-xs">
              <div className="flex justify-between text-blue-300/80">
                <span>Pods:</span>
                <span className="font-mono">{k8sStatus.pods}</span>
              </div>
              <div className="flex justify-between text-blue-300/80">
                <span>Services:</span>
                <span className="font-mono">{k8sStatus.services}</span>
              </div>
              <div className="flex justify-between text-blue-300/80">
                <span>Nodes:</span>
                <span className="font-mono">{k8sStatus.nodes}</span>
              </div>
              <div className="mt-2 pt-2 border-t border-blue-400/20">
                <div className="text-blue-400/60 text-[10px]">
                  Status: <span className="text-green-400">Healthy</span>
                </div>
              </div>
            </div>
          </div>

          {/* File System Monitor */}
          <div className="border border-orange-400/30 p-3 flex-1 overflow-hidden">
            <div className="text-xs mb-2 flex items-center gap-2 text-orange-400">
              <FileCode className="w-4 h-4" />
              FILE SYSTEM MONITOR
            </div>
            <div className="space-y-1 text-[10px] overflow-y-auto max-h-40">
              {fileWatches.slice(-8).reverse().map(fw => (
                <div key={fw.id} className="border border-orange-400/20 p-1.5">
                  <div className="flex justify-between items-center mb-0.5">
                    <span className={`
                      ${fw.event === 'MODIFIED' ? 'text-yellow-400' : ''}
                      ${fw.event === 'CREATED' ? 'text-green-400' : ''}
                      ${fw.event === 'ACCESSED' ? 'text-blue-400' : ''}
                      ${fw.event === 'DELETED' ? 'text-red-400' : ''}
                    `}>{fw.event}</span>
                    <span className="text-orange-400/50">{fw.timestamp}</span>
                  </div>
                  <div className="text-orange-300/70 truncate">{fw.path}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Processes */}
          <div className="border border-green-400/30 p-3">
            <div className="text-xs mb-2 flex items-center gap-2">
              <Activity className="w-4 h-4" />
              ACTIVE PROCESSES
            </div>
            <div className="space-y-2 text-xs max-h-32 overflow-y-auto">
              {activeProcesses.slice(-4).map(proc => (
                <div key={proc.id} className="border border-green-400/20 p-2">
                  <div className="truncate text-[10px]">{proc.name}</div>
                  <div className="w-full bg-green-400/20 h-0.5 mt-1 relative overflow-hidden">
                    <div 
                      className="bg-green-400 h-full transition-all duration-500"
                      style={{ width: `${proc.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Memory Bank */}
          <div className="border border-green-400/30 p-3">
            <div className="text-xs mb-2 flex items-center gap-2">
              <Database className="w-4 h-4" />
              MEMORY TRACES
            </div>
            <div className="text-xs space-y-1 max-h-28 overflow-y-auto">
              {memoryBank.slice(-6).reverse().map(mem => (
                <div key={mem.id} className="text-green-400/60 text-[10px]">
                  <span className={mem.type === 'episodic' ? 'text-cyan-400' : 'text-purple-400'}>
                    {mem.type === 'episodic' ? '◆' : '◇'}
                  </span> {mem.content}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}