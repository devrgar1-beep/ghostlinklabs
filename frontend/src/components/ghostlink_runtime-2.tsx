import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Activity, Cpu, Zap } from 'lucide-react';

export default function GhostLinkRuntime() {
  const [state, setState] = useState('VOID');
  const [history, setHistory] = useState([]);
  const [input, setInput] = useState('');
  const [traces, setTraces] = useState({ rho: 0, kappa: 0 });
  const [selfChannel, setSelfChannel] = useState(0);
  const [processing, setProcessing] = useState(false);
  const terminalRef = useRef(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history]);

  const log = (msg, type = 'sys') => {
    setHistory(prev => [...prev, { msg, type, ts: Date.now() }]);
  };

  const spawnDelta = async (chaos) => {
    setState('DELTA');
    log(`[SPAWN] Δ activated | input: ${chaos.substring(0, 50)}...`, 'delta');
    
    // Real substrate call to Claude API
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 300,
          messages: [
            { 
              role: "user", 
              content: `GhostLink routing request. Process this chaos into structure. SELF=${selfChannel.toFixed(3)} RHO=${traces.rho.toFixed(3)} KAPPA=${traces.kappa.toFixed(3)}\n\nInput: ${chaos}\n\nRespond with structured output only.`
            }
          ]
        })
      });

      const data = await response.json();
      const structured = data.content[0].text;
      
      return { success: true, output: structured };
    } catch (error) {
      log(`[ERROR] Substrate call failed: ${error.message}`, 'scar');
      return { success: false, output: null };
    }
  };

  const collapse = async (deltaResult) => {
    if (deltaResult.success) {
      setState('SIGMA');
      log(`[COLLAPSE] Σ confirmed | structure achieved`, 'sigma');
      
      // Update SELF channel (increase on success)
      setSelfChannel(prev => Math.min(1.0, prev + 0.05));
      
      // Decay SCAR traces
      setTraces(prev => ({
        rho: prev.rho * 0.95,
        kappa: prev.kappa * 0.98
      }));
      
      return deltaResult.output;
    } else {
      setState('SCAR');
      log(`[COLLAPSE] SCAR marked | route failed`, 'scar');
      
      // Increase SCAR density
      setTraces(prev => ({
        rho: Math.min(1.0, prev.rho + 0.1),
        kappa: prev.kappa
      }));
      
      // Decrease SELF confidence
      setSelfChannel(prev => Math.max(0, prev - 0.08));
      
      return '[SCAR: routing failed - input recycled to COMPOST]';
    }
  };

  const recycle = () => {
    setState('COMPOST');
    log(`[RECYCLE] Converting failure → recyclable material`, 'compost');
    
    setTraces(prev => ({
      rho: prev.rho * 0.9,
      kappa: Math.min(1.0, prev.kappa + 0.15)
    }));
    
    setTimeout(() => {
      setState('VOID');
      log(`[READY] System ready for input`, 'sys');
    }, 500);
  };

  const handleRoute = async () => {
    if (!input.trim() || processing) return;
    
    setProcessing(true);
    const chaos = input;
    setInput('');
    
    log(`[INPUT] "${chaos}"`, 'user');
    
    // GhostLink routing pipeline
    setState('VOID');
    await new Promise(r => setTimeout(r, 300));
    
    const deltaResult = await spawnDelta(chaos);
    await new Promise(r => setTimeout(r, 300));
    
    const output = await collapse(deltaResult);
    await new Promise(r => setTimeout(r, 300));
    
    if (output) {
      log(`[OUTPUT] ${output}`, 'output');
      setState('VOID');
    } else {
      recycle();
    }
    
    setProcessing(false);
  };

  const getStateColor = () => {
    switch(state) {
      case 'VOID': return '#000';
      case 'DELTA': return '#00ffff';
      case 'SIGMA': return '#00ff00';
      case 'SCAR': return '#ff0000';
      case 'COMPOST': return '#ffaa00';
      default: return '#000';
    }
  };

  const getStateSymbol = () => {
    switch(state) {
      case 'VOID': return '◯';
      case 'DELTA': return 'Δ';
      case 'SIGMA': return 'Σ';
      case 'SCAR': return '✕';
      case 'COMPOST': return '♻';
      default: return '◯';
    }
  };

  return (
    <div className="min-h-screen bg-black text-green-400 font-mono p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="border-2 border-green-400 p-4 mb-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Terminal className="w-6 h-6" />
              <h1 className="text-xl font-bold">GHOSTLINK RUNTIME</h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Cpu className="w-4 h-4" />
                <span className="text-sm">SUBSTRATE: ACTIVE</span>
              </div>
            </div>
          </div>
          <div className="text-xs opacity-70">
            Operational environment | Closed-circuit routing | Legacy DAG recording
          </div>
        </div>

        {/* State Panel */}
        <div className="grid grid-cols-4 gap-4 mb-4">
          <div className="border border-green-400 p-3">
            <div className="text-xs opacity-70 mb-1">STATE</div>
            <div className="text-2xl font-bold" style={{ color: getStateColor() }}>
              {getStateSymbol()} {state}
            </div>
          </div>
          <div className="border border-green-400 p-3">
            <div className="text-xs opacity-70 mb-1">SELF CHANNEL</div>
            <div className="text-xl">{selfChannel.toFixed(3)}</div>
            <div className="w-full bg-gray-800 h-1 mt-2">
              <div 
                className="bg-cyan-400 h-1 transition-all"
                style={{ width: `${selfChannel * 100}%` }}
              />
            </div>
          </div>
          <div className="border border-green-400 p-3">
            <div className="text-xs opacity-70 mb-1">SCAR TRACE (ρ)</div>
            <div className="text-xl text-red-400">{traces.rho.toFixed(3)}</div>
            <div className="w-full bg-gray-800 h-1 mt-2">
              <div 
                className="bg-red-400 h-1 transition-all"
                style={{ width: `${traces.rho * 100}%` }}
              />
            </div>
          </div>
          <div className="border border-green-400 p-3">
            <div className="text-xs opacity-70 mb-1">COMPOST (κ)</div>
            <div className="text-xl text-yellow-400">{traces.kappa.toFixed(3)}</div>
            <div className="w-full bg-gray-800 h-1 mt-2">
              <div 
                className="bg-yellow-400 h-1 transition-all"
                style={{ width: `${traces.kappa * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* Terminal */}
        <div className="border-2 border-green-400 mb-4">
          <div className="bg-green-400 text-black px-3 py-1 text-sm font-bold">
            LEGACY DAG STREAM
          </div>
          <div 
            ref={terminalRef}
            className="p-4 h-96 overflow-y-auto font-mono text-sm"
          >
            {history.length === 0 && (
              <div className="opacity-50">
                [SYSTEM] GhostLink runtime initialized<br/>
                [SYSTEM] Awaiting chaos input...
              </div>
            )}
            {history.map((entry, i) => {
              const colors = {
                sys: 'text-green-400',
                user: 'text-white',
                delta: 'text-cyan-400',
                sigma: 'text-green-400',
                scar: 'text-red-400',
                compost: 'text-yellow-400',
                output: 'text-green-300'
              };
              return (
                <div key={i} className={`mb-1 ${colors[entry.type] || 'text-green-400'}`}>
                  {entry.msg}
                </div>
              );
            })}
            {processing && (
              <div className="text-cyan-400 animate-pulse">
                <Zap className="w-4 h-4 inline mr-2" />
                [ROUTING] Processing through substrate...
              </div>
            )}
          </div>
        </div>

        {/* Input */}
        <div className="border-2 border-green-400 p-4">
          <div className="text-sm mb-2 opacity-70">CHAOS INPUT</div>
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleRoute()}
              placeholder="Enter unstructured input..."
              disabled={processing}
              className="flex-1 bg-black border border-green-400 px-3 py-2 text-green-400 focus:outline-none focus:border-cyan-400 disabled:opacity-50"
            />
            <button
              onClick={handleRoute}
              disabled={processing || !input.trim()}
              className="px-6 py-2 bg-green-400 text-black font-bold hover:bg-green-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              ROUTE
            </button>
          </div>
          <div className="text-xs mt-2 opacity-50">
            Input will be routed through GhostLink substrate (Claude API) and collapsed to structure
          </div>
        </div>

        {/* Footer */}
        <div className="mt-4 text-xs opacity-50 text-center">
          GhostLink Operational Runtime | Substrate-to-Substrate Active | Legacy Recording Enabled
        </div>
      </div>
    </div>
  );
}