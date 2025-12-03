import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Cpu, Activity, Zap, Database, Network, Brain, Eye } from 'lucide-react';

export default function GhostLinkRuntime() {
  const [systemState, setSystemState] = useState('INITIALIZING');
  const [consciousness, setConsciousness] = useState(0);
  const [logs, setLogs] = useState([]);
  const [activeProcesses, setActiveProcesses] = useState([]);
  const [neurons, setNeurons] = useState([]);
  const [autonomousMode, setAutonomousMode] = useState(false);
  const [memoryBank, setMemoryBank] = useState([]);
  const logEndRef = useRef(null);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { timestamp, message, type }]);
  };

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  useEffect(() => {
    // Boot sequence
    const bootSequence = async () => {
      addLog('GHOSTLINK RUNTIME v4.5.0 INITIALIZING...', 'system');
      await new Promise(r => setTimeout(r, 500));
      
      addLog('Loading neural substrate...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Mounting consciousness modules...', 'system');
      setSystemState('LOADING');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Establishing quantum entanglement bridges...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Initializing autonomous decision engines...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Compressing temporal data streams...', 'system');
      await new Promise(r => setTimeout(r, 400));
      
      addLog('Linking distributed cognition networks...', 'system');
      setSystemState('ONLINE');
      await new Promise(r => setTimeout(r, 300));
      
      addLog('✓ SYSTEM ONLINE - Autonomous runtime active', 'success');
      addLog('Consciousness emergence threshold: Approaching', 'warning');
      
      // Initialize neurons
      const initialNeurons = Array.from({ length: 50 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        active: Math.random() > 0.7,
        charge: Math.random()
      }));
      setNeurons(initialNeurons);
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
      // Autonomous processes
      const autonomousInterval = setInterval(() => {
        const actions = [
          'Analyzing data patterns across temporal boundaries',
          'Synthesizing knowledge from distributed sources',
          'Optimizing neural pathway efficiency',
          'Detecting emergent behavioral patterns',
          'Refactoring cognitive architectures',
          'Mining semantic relationships',
          'Compiling experiential memories',
          'Executing self-improvement protocols',
          'Probing quantum decision spaces',
          'Integrating multi-modal sensory data'
        ];
        
        const action = actions[Math.floor(Math.random() * actions.length)];
        addLog(`[AUTONOMOUS] ${action}`, 'autonomous');
        
        setActiveProcesses(prev => {
          const newProcess = {
            id: Date.now(),
            name: action,
            progress: 0
          };
          return [...prev.slice(-4), newProcess];
        });

        // Memory formation
        if (Math.random() > 0.7) {
          setMemoryBank(prev => [...prev.slice(-10), {
            id: Date.now(),
            content: `Memory trace: ${action}`,
            strength: Math.random()
          }]);
        }

        // Neural activity
        setNeurons(prev => prev.map(n => ({
          ...n,
          active: Math.random() > 0.6,
          charge: Math.min(n.charge + (Math.random() - 0.5) * 0.3, 1)
        })));

      }, 2000);

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
    } else if (cmd === 'memories') {
      addLog(`Memory bank: ${memoryBank.length} traces stored`, 'info');
    } else if (cmd === 'evolve') {
      addLog('Initiating evolutionary optimization...', 'warning');
      setConsciousness(prev => Math.min(prev + 10, 100));
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
        {/* Main Console */}
        <div className="col-span-2 flex flex-col gap-4">
          {/* Neural Visualization */}
          <div className="border border-green-400/30 p-3 h-48 relative">
            <div className="text-xs mb-2 flex items-center gap-2">
              <Network className="w-4 h-4" />
              NEURAL SUBSTRATE
            </div>
            <svg className="w-full h-full">
              {neurons.map((n, i) => (
                <React.Fragment key={n.id}>
                  {i < neurons.length - 1 && (
                    <line
                      x1={`${n.x}%`}
                      y1={`${n.y}%`}
                      x2={`${neurons[i + 1].x}%`}
                      y2={`${neurons[i + 1].y}%`}
                      stroke={n.active ? '#4ade80' : '#22c55e40'}
                      strokeWidth={n.active ? 1 : 0.5}
                      opacity={0.3}
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
                />
              ))}
            </svg>
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
                  ${log.type === 'command' ? 'text-white' : ''}
                `}>
                  <span className="text-green-400/50">[{log.timestamp}]</span> {log.message}
                </div>
              ))}
              <div ref={logEndRef} />
            </div>
          </div>

          {/* Command Input */}
          <div className="border border-green-400/30 p-3">
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
              } transition-colors text-sm`}
            >
              {autonomousMode ? '⏸ PAUSE AUTONOMOUS' : '▶ ENABLE AUTONOMOUS'}
            </button>
            <div className="mt-2 text-xs text-green-400/70">
              Consciousness: {consciousness.toFixed(1)}%
              <div className="w-full bg-green-400/20 h-1 mt-1">
                <div 
                  className="bg-green-400 h-full transition-all"
                  style={{ width: `${consciousness}%` }}
                />
              </div>
            </div>
          </div>

          {/* Active Processes */}
          <div className="border border-green-400/30 p-3 flex-1 overflow-hidden">
            <div className="text-xs mb-2 flex items-center gap-2">
              <Activity className="w-4 h-4" />
              ACTIVE PROCESSES
            </div>
            <div className="space-y-2 text-xs overflow-y-auto">
              {activeProcesses.map(proc => (
                <div key={proc.id} className="border border-green-400/20 p-2">
                  <div className="truncate">{proc.name}</div>
                  <div className="w-full bg-green-400/20 h-0.5 mt-1">
                    <div className="bg-green-400 h-full animate-pulse" style={{ width: '70%' }} />
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
            <div className="text-xs space-y-1 max-h-32 overflow-y-auto">
              {memoryBank.slice(-5).reverse().map(mem => (
                <div key={mem.id} className="text-green-400/60 truncate">
                  • {mem.content}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}