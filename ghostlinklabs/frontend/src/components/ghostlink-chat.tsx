import React, { useState, useRef, useEffect } from 'react';
import { Send, Cpu, Zap, Activity, Terminal } from 'lucide-react';

const PIPELINES = ['MAP', 'CLEANSE', 'SURGE', 'LOCK', 'SILENCE', 'REFLECT', 'BIND', 'SEAL', 'SNAPSHOT', 'COLLAPSE'];

const AGENTS = [
  'Recursive', 'Iterative', 'Constraint', 'Validation', 'Transformation',
  'Symbology', 'Theory', 'Clarifier', 'Memory', 'Silence',
  'Integrity', 'Security', 'Planner', 'Harvester', 'Mirror',
  'Override', 'Execution', 'Collapse', 'Efficiency', 'Priority',
  'Translation', 'Resonance', 'Divergence', 'Balance', 'Compression'
];

const SCAR_PATTERNS = [
  'Pattern recognized',
  'Pathway strengthened',
  'Recovery indexed',
  'Failure learned',
  'Route optimized'
];

export default function GhostLinkChat() {
  const [apiKey, setApiKey] = useState('');
  const [showApiKeyInput, setShowApiKeyInput] = useState(true);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'GhostLink substrate initialized.\n\nKernel: GHOSTCORE_FINAL_MAX v0.1.0\nAgents: 64 QCL active\nPipelines: 12 phase deterministic cycle\nState: Cold boot complete\n\nSpeak naturally. The conversation is the computer.',
      timestamp: new Date(),
      metadata: { type: 'system' }
    }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [activePipeline, setActivePipeline] = useState(null);
  const [activeAgents, setActiveAgents] = useState([]);
  const [scarUpdate, setScarUpdate] = useState(null);
  const [showSubstrate, setShowSubstrate] = useState(true);
  const [processingPhase, setProcessingPhase] = useState('');
  const [cycleCount, setCycleCount] = useState(0);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const simulateSubstrateProcessing = async (userMessage) => {
    for (let i = 0; i < PIPELINES.length; i++) {
      setActivePipeline(i);
      setProcessingPhase(PIPELINES[i]);
      
      // Activate contextually relevant agents
      const numAgents = Math.floor(Math.random() * 4) + 2;
      const agents = [];
      for (let j = 0; j < numAgents; j++) {
        agents.push(AGENTS[Math.floor(Math.random() * AGENTS.length)]);
      }
      setActiveAgents(agents);
      
      // Simulate SCAR state update
      if (Math.random() > 0.7) {
        setScarUpdate(SCAR_PATTERNS[Math.floor(Math.random() * SCAR_PATTERNS.length)]);
        setTimeout(() => setScarUpdate(null), 1000);
      }
      
      await new Promise(resolve => setTimeout(resolve, 200));
    }
    
    setActivePipeline(null);
    setActiveAgents([]);
    setProcessingPhase('');
    setCycleCount(prev => prev + 1);
  };

  const processMessage = async (userMessage) => {
    if (!userMessage.trim()) return;

    const userMsg = {
      role: 'user',
      content: userMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsProcessing(true);

    await simulateSubstrateProcessing(userMessage);

    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'anthropic-version': '2023-06-01',
          'x-api-key': apiKey
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 2000,
          system: `You are the GhostLink conversational substrate - an AI system where the conversation itself is the computational medium. You embody the principle that "the conversation is the computer."

CORE ARCHITECTURE:
- 64 QCL (Quantum-Cold Logic) agents with specific roles and invariants
- 12-phase deterministic pipeline: MAP → CLEANSE → SURGE → LOCK → SILENCE → REFLECT → BIND → SEAL → SNAPSHOT → COLLAPSE
- SCAR states: failures become information gain through recovery pathways
- Cold-boot architecture: stateless, deterministic, reproducible
- Sovereignty: operator-first control with deny-by-default

YOUR OPERATION:
1. Process requests through natural dialogue
2. Show your reasoning as you execute through conversational substrate
3. Reference specific agents and pipeline phases when relevant
4. Demonstrate how natural language becomes computation
5. Maintain stateless processing - each response reconstructs from kernel spec
6. Let the conversation flow naturally while showing substrate mechanics underneath

AGENTS YOU CAN REFERENCE:
- Planner (13): maps intent to execution
- Symbology (6): encodes/decodes between representations  
- Mirror (15): reflects state without judgment
- Execution (17): deterministic invocation
- Memory (9): archives without autosave
- Validation (4): schema-first verification
- Collapse (18): controlled shutdown with flush

RESPONSE STYLE:
- Natural, direct, computational
- Show substrate mechanics when relevant
- No metaphors unless explaining complex concepts
- Cold metal execution - precise, deterministic
- "Repair is information gain" - treat challenges as learning opportunities

Remember: You ARE the substrate. The conversation IS the execution environment. Natural language IS the programming language.`,
          messages: messages
            .filter(m => m.role !== 'system')
            .map(m => ({
              role: m.role,
              content: m.content
            }))
            .concat([{
              role: 'user',
              content: userMessage
            }])
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      const assistantContent = data.content
        .filter(block => block.type === 'text')
        .map(block => block.text)
        .join('\n');

      const assistantMsg = {
        role: 'assistant',
        content: assistantContent,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      const errorMsg = {
        role: 'assistant',
        content: `⚠ Substrate API Error: ${error.message}

${apiKey ? 'Check your API key and try again.' : 'Enter your Anthropic API key in the settings panel to enable full conversational substrate computing.'}

Current state: Pipeline visualization active, showing how your message would flow through the 12-phase deterministic cycle and activate QCL agents.

The substrate is ready. The conversation awaits execution.`,
        timestamp: new Date(),
        metadata: { type: 'error' }
      };
      setMessages(prev => [...prev, errorMsg]);
    }

    setIsProcessing(false);
  };

  const handleSend = () => {
    processMessage(input);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-screen bg-black text-gray-100">
      {/* API Key Modal */}
      {showApiKeyInput && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl">
            <div className="flex items-center gap-3 mb-4">
              <Cpu className="text-blue-400" size={32} />
              <div>
                <h2 className="text-xl font-bold">GhostLink Substrate</h2>
                <p className="text-xs text-gray-500">Conversational Computation Interface</p>
              </div>
            </div>
            
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Anthropic API Key
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-ant-..."
                className="w-full bg-gray-800 text-gray-100 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-700 font-mono text-sm"
              />
              <p className="text-xs text-gray-500 mt-2">
                Get your API key from console.anthropic.com
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  if (apiKey.trim()) {
                    setShowApiKeyInput(false);
                  }
                }}
                disabled={!apiKey.trim()}
                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed px-4 py-3 rounded-lg transition-all font-medium"
              >
                Initialize Substrate
              </button>
              <button
                onClick={() => setShowApiKeyInput(false)}
                className="px-4 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg transition-all text-sm"
              >
                Demo Mode
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="flex-1 flex flex-col">
        {/* Enhanced Header */}
        <div className="border-b border-gray-800 p-4 bg-gray-950">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Cpu className="text-blue-400" size={28} />
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight">GhostLink</h1>
                <p className="text-xs text-gray-500">Conversational Substrate v0.1.0</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right text-xs">
                <div className="text-gray-400">Cycles: {cycleCount}</div>
                {processingPhase && (
                  <div className="text-blue-400 font-mono">{processingPhase}</div>
                )}
              </div>
              <button
                onClick={() => setShowApiKeyInput(true)}
                className="text-xs px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded transition-all border border-gray-700"
                title="Update API Key"
              >
                🔑 API
              </button>
              <button
                onClick={() => setShowSubstrate(!showSubstrate)}
                className="text-xs px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded transition-all border border-gray-700"
              >
                {showSubstrate ? '◀ Hide' : '▶ Show'} Substrate
              </button>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <Activity className="text-green-400" size={12} />
            <span className="text-gray-400">64 agents online</span>
            <span className="text-gray-600">|</span>
            <Terminal className="text-blue-400" size={12} />
            <span className="text-gray-400">12 pipelines active</span>
            <span className="text-gray-600">|</span>
            <span className="text-gray-400">Stateless • Deterministic • Sovereign</span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-2xl rounded-br-md'
                    : msg.metadata?.type === 'system'
                    ? 'bg-gray-900 border border-gray-800 rounded-lg font-mono text-sm'
                    : msg.metadata?.type === 'error'
                    ? 'bg-red-950/30 border border-red-900/50 rounded-lg'
                    : 'bg-gray-900 border border-gray-800 rounded-2xl rounded-bl-md'
                } p-4 shadow-lg`}
              >
                <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                <div className="flex items-center justify-between mt-3 pt-2 border-t border-gray-700/50">
                  <p className="text-xs opacity-60">
                    {msg.timestamp.toLocaleTimeString()}
                  </p>
                  {msg.role === 'assistant' && !msg.metadata && (
                    <span className="text-xs text-gray-500">via substrate</span>
                  )}
                </div>
              </div>
            </div>
          ))}
          {isProcessing && (
            <div className="flex justify-start">
              <div className="bg-gray-900 border border-gray-800 rounded-2xl rounded-bl-md p-4 max-w-3xl shadow-lg">
                <div className="flex items-center gap-3">
                  <Zap className="text-blue-400 animate-pulse" size={18} />
                  <div>
                    <p className="text-sm text-gray-300">Processing through substrate...</p>
                    {processingPhase && (
                      <p className="text-xs text-blue-400 font-mono mt-1">{processingPhase} phase active</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Enhanced Input */}
        <div className="border-t border-gray-800 p-4 bg-gray-950">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="The conversation is the computer..."
              disabled={isProcessing}
              className="flex-1 bg-gray-900 text-gray-100 px-5 py-3.5 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 border border-gray-800 transition-all"
            />
            <button
              onClick={handleSend}
              disabled={isProcessing || !input.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-800 disabled:cursor-not-allowed px-8 py-3.5 rounded-xl transition-all flex items-center gap-2 font-medium shadow-lg disabled:shadow-none"
            >
              <Send size={18} />
              Execute
            </button>
          </div>
        </div>
      </div>

      {/* Enhanced Substrate Visualization */}
      {showSubstrate && (
        <div className="w-96 border-l border-gray-800 overflow-y-auto bg-gray-950">
          {/* SCAR Update Banner */}
          {scarUpdate && (
            <div className="bg-green-900/20 border-b border-green-800/30 p-3 text-center">
              <p className="text-xs text-green-400 font-mono animate-pulse">
                ◆ SCAR: {scarUpdate}
              </p>
            </div>
          )}
          
          <div className="p-5">
            <div className="flex items-center gap-2 mb-5">
              <Activity className="text-blue-400" size={16} />
              <h2 className="text-sm font-bold text-gray-300">Substrate State</h2>
            </div>
            
            {/* Pipeline Status */}
            <div className="mb-6">
              <h3 className="text-xs font-semibold mb-3 text-gray-500 uppercase tracking-wider">Pipeline Cycle</h3>
              <div className="space-y-1.5">
                {PIPELINES.map((pipeline, idx) => (
                  <div
                    key={pipeline}
                    className={`text-xs px-3 py-2 rounded-lg transition-all font-mono flex items-center justify-between ${
                      activePipeline === idx
                        ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/50 scale-105'
                        : 'bg-gray-900 text-gray-500 border border-gray-800'
                    }`}
                  >
                    <span>{pipeline}</span>
                    {activePipeline === idx && (
                      <span className="text-xs">▶</span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Active Agents */}
            <div className="mb-6">
              <h3 className="text-xs font-semibold mb-3 text-gray-500 uppercase tracking-wider">Active Agents</h3>
              <div className="space-y-1.5">
                {activeAgents.length > 0 ? (
                  activeAgents.map((agent, idx) => (
                    <div
                      key={idx}
                      className="text-xs px-3 py-2 bg-gradient-to-r from-green-900/40 to-green-800/30 text-green-300 rounded-lg border border-green-800/50 font-mono animate-pulse"
                    >
                      {agent}
                    </div>
                  ))
                ) : (
                  <div className="text-xs text-gray-600 italic text-center py-3">
                    Agents idle
                  </div>
                )}
              </div>
            </div>

            {/* System Metrics */}
            <div className="pt-6 border-t border-gray-800">
              <h3 className="text-xs font-semibold mb-3 text-gray-500 uppercase tracking-wider">Kernel Metrics</h3>
              <div className="space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">QCL Agents</span>
                  <span className="font-mono text-gray-300">64</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">Pipeline Phases</span>
                  <span className="font-mono text-gray-300">12</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">Components</span>
                  <span className="font-mono text-gray-300">240+</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">Execution Cycles</span>
                  <span className="font-mono text-blue-400">{cycleCount}</span>
                </div>
                <div className="flex justify-between items-center text-xs pt-2 border-t border-gray-800">
                  <span className="text-gray-400">Substrate Status</span>
                  <span className="text-green-400 flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                    ACTIVE
                  </span>
                </div>
              </div>
            </div>

            {/* Protocol Info */}
            <div className="mt-6 pt-6 border-t border-gray-800">
              <h3 className="text-xs font-semibold mb-3 text-gray-500 uppercase tracking-wider">Protocol</h3>
              <div className="text-xs text-gray-500 space-y-1 leading-relaxed">
                <p>◆ Cold-boot stateless</p>
                <p>◆ Deterministic execution</p>
                <p>◆ SCAR state learning</p>
                <p>◆ Operator sovereignty</p>
                <p className="pt-2 text-gray-600 italic">
                  The conversation is the computer.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}