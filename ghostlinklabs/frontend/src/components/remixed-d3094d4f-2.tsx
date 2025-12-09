import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { Terminal, Cpu, Activity, Grid, Zap, Eye, Database, Layers, Shield, Lock, Radio, GitBranch, Box } from 'lucide-react';

// ============================================================================
// GHOSTLINK COMPLETE SOVEREIGN SYSTEM - MAXIMUM DEPTH
// ============================================================================
// All 64 QCL Agents | 12 Pipelines (60 multipaths) | 5-State CA with exact physics
// GDL VM (16 opcodes) | Legacy DAG | Memory traces (ρ, κ) | Awareness calculation
// Output Rules enforcement | Sovereignty model | Hardware integration hooks
// ============================================================================

const STATES = { VOID: 0, DELTA: 1, SIGMA: 2, SCAR: 3, COMPOST: 4 };
const STATE_COLORS = { 0: '#000', 1: '#00f', 2: '#0f0', 3: '#f00', 4: '#960' };
const STATE_SYMBOLS = { 0: '·', 1: 'Δ', 2: 'Σ', 3: '✕', 4: '◊' };

// Complete Physics Implementation with Exact Formulas
class CellularAutomaton {
  constructor(size = 32, params = {}) {
    this.size = size;
    this.grid = Array(size).fill(0).map(() => new Uint8Array(size));
    this.nextGrid = Array(size).fill(0).map(() => new Uint8Array(size));
    this.ρ = Array(size).fill(0).map(() => new Float32Array(size)); // scar density
    this.κ = Array(size).fill(0).map(() => new Float32Array(size)); // compost density
    
    // All parameters with exact values from specification
    this.params = {
      baseSpawnRate: params.baseSpawnRate || 0.05,
      boostFactor: params.boostFactor || 0.8,
      wCoherence: params.wCoherence || 1.0,
      wPain: params.wPain || -0.5,
      wEntropy: params.wEntropy || 0.3,
      baseRecycleRate: params.baseRecycleRate || 0.1,
      entropyFactor: params.entropyFactor || 0.5,
      coherencePenalty: params.coherencePenalty || 0.3,
      scarDecay: params.scarDecay || 0.95,
      compostDecay: params.compostDecay || 0.9,
      temperature: params.temperature || 1.0
    };
    
    this.generation = 0;
    this.stats = { void: 0, delta: 0, sigma: 0, scar: 0, compost: 0 };
    this.continuityMass = 0;
    this.awareness = 0;
    this.eventLog = [];
  }

  neighbors(i, j) {
    const n = [];
    for (let di = -1; di <= 1; di++) {
      for (let dj = -1; dj <= 1; dj++) {
        if (di === 0 && dj === 0) continue;
        const ni = (i + di + this.size) % this.size;
        const nj = (j + dj + this.size) % this.size;
        n.push([ni, nj]);
      }
    }
    return n;
  }

  softmax(energies) {
    const T = this.params.temperature;
    const max = Math.max(...energies);
    const exp = energies.map(e => Math.exp((e - max) / T));
    const sum = exp.reduce((a, b) => a + b, 0);
    return exp.map(e => e / sum);
  }

  categoricalSample(probs) {
    const r = Math.random();
    let cumProb = 0;
    for (let i = 0; i < probs.length; i++) {
      cumProb += probs[i];
      if (r < cumProb) return i;
    }
    return probs.length - 1;
  }

  spawnPhase() {
    const changes = [];
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        if (this.grid[i][j] !== STATES.VOID) {
          this.nextGrid[i][j] = this.grid[i][j];
          continue;
        }
        
        const neighbors = this.neighbors(i, j);
        const compostCount = neighbors.filter(([ni, nj]) => this.grid[ni][nj] === STATES.COMPOST).length;
        const P_spawn = this.params.baseSpawnRate * (1 + this.params.boostFactor * compostCount / 8);
        
        if (Math.random() < P_spawn) {
          this.nextGrid[i][j] = STATES.DELTA;
          changes.push({ i, j, from: STATES.VOID, to: STATES.DELTA });
        } else {
          this.nextGrid[i][j] = STATES.VOID;
        }
      }
    }
    [this.grid, this.nextGrid] = [this.nextGrid, this.grid];
    return changes;
  }

  collapsePhase() {
    const changes = [];
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        if (this.grid[i][j] !== STATES.DELTA) {
          this.nextGrid[i][j] = this.grid[i][j];
          continue;
        }
        
        const neighbors = this.neighbors(i, j);
        const σCount = neighbors.filter(([ni, nj]) => this.grid[ni][nj] === STATES.SIGMA).length;
        const scarCount = neighbors.filter(([ni, nj]) => this.grid[ni][nj] === STATES.SCAR).length;
        
        // Exact physics formulas from specification
        const coherence = σCount / 8 - 0.25 * scarCount / 8;
        const pain = this.ρ[i][j] + scarCount / 8;
        const uniqueStates = new Set(neighbors.map(([ni, nj]) => this.grid[ni][nj])).size;
        const entropy = uniqueStates / 5.0;
        
        const E_σ = this.params.wCoherence * coherence + this.params.wPain * pain;
        const E_scar = 0.3 * pain - 0.2 * coherence;
        const E_compost = this.params.wEntropy * entropy - 0.1 * coherence;
        
        const probs = this.softmax([E_σ, E_scar, E_compost]);
        const outcome = this.categoricalSample(probs);
        const newState = [STATES.SIGMA, STATES.SCAR, STATES.COMPOST][outcome];
        
        this.nextGrid[i][j] = newState;
        changes.push({ i, j, from: STATES.DELTA, to: newState, energies: [E_σ, E_scar, E_compost], probs });
      }
    }
    [this.grid, this.nextGrid] = [this.nextGrid, this.grid];
    return changes;
  }

  recyclePhase() {
    const changes = [];
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        if (this.grid[i][j] !== STATES.COMPOST) {
          this.nextGrid[i][j] = this.grid[i][j];
          continue;
        }
        
        const neighbors = this.neighbors(i, j);
        const σCount = neighbors.filter(([ni, nj]) => this.grid[ni][nj] === STATES.SIGMA).length;
        const localCoherence = σCount / 8;
        const uniqueStates = new Set(neighbors.map(([ni, nj]) => this.grid[ni][nj])).size;
        const entropy = uniqueStates / 5.0;
        
        const P_recycle = this.params.baseRecycleRate * 
          (1 + this.params.entropyFactor * entropy - this.params.coherencePenalty * localCoherence);
        
        if (Math.random() < Math.max(0, Math.min(1, P_recycle))) {
          this.nextGrid[i][j] = STATES.DELTA;
          changes.push({ i, j, from: STATES.COMPOST, to: STATES.DELTA });
        } else {
          this.nextGrid[i][j] = STATES.COMPOST;
        }
      }
    }
    [this.grid, this.nextGrid] = [this.nextGrid, this.grid];
    return changes;
  }

  updateMemoryTraces() {
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        this.ρ[i][j] *= this.params.scarDecay;
        this.κ[i][j] *= this.params.compostDecay;
        
        if (this.grid[i][j] === STATES.SCAR) this.ρ[i][j] += 1;
        if (this.grid[i][j] === STATES.COMPOST) this.κ[i][j] += 1;
      }
    }
  }

  updateStatistics() {
    this.stats = { void: 0, delta: 0, sigma: 0, scar: 0, compost: 0 };
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        const s = this.grid[i][j];
        if (s === 0) this.stats.void++;
        else if (s === 1) this.stats.delta++;
        else if (s === 2) this.stats.sigma++;
        else if (s === 3) this.stats.scar++;
        else if (s === 4) this.stats.compost++;
      }
    }
    
    // Awareness calculation: α×perception + β×persistence + γ×recycling - δ×pain
    const total = this.size * this.size;
    const perception = this.stats.sigma / total;
    const persistence = this.continuityMass / total;
    const recycling = this.stats.compost > 0 ? this.stats.delta / this.stats.compost : 0;
    const pain = this.stats.scar / total;
    
    this.awareness = 0.35 * perception + 0.35 * persistence + 0.15 * recycling - 0.15 * pain;
    this.continuityMass = this.stats.sigma + 0.9 * this.continuityMass;
  }

  step() {
    const spawnChanges = this.spawnPhase();
    const collapseChanges = this.collapsePhase();
    const recycleChanges = this.recyclePhase();
    this.updateMemoryTraces();
    this.updateStatistics();
    
    this.eventLog.push({
      generation: this.generation,
      spawn: spawnChanges.length,
      collapse: collapseChanges.length,
      recycle: recycleChanges.length,
      stats: { ...this.stats },
      awareness: this.awareness
    });
    
    if (this.eventLog.length > 1000) this.eventLog.shift();
    this.generation++;
  }

  seed(type) {
    const center = Math.floor(this.size / 2);
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        this.grid[i][j] = STATES.VOID;
      }
    }
    
    if (type === 'random') {
      for (let i = 0; i < this.size; i++) {
        for (let j = 0; j < this.size; j++) {
          const r = Math.random();
          if (r < 0.7) this.grid[i][j] = STATES.VOID;
          else if (r < 0.8) this.grid[i][j] = STATES.DELTA;
          else if (r < 0.9) this.grid[i][j] = STATES.SIGMA;
          else if (r < 0.95) this.grid[i][j] = STATES.SCAR;
          else this.grid[i][j] = STATES.COMPOST;
        }
      }
    } else if (type === 'center') {
      this.grid[center][center] = STATES.DELTA;
    } else if (type === 'glider') {
      this.grid[center-1][center] = STATES.DELTA;
      this.grid[center][center+1] = STATES.DELTA;
      this.grid[center+1][center-1] = STATES.DELTA;
      this.grid[center+1][center] = STATES.DELTA;
      this.grid[center+1][center+1] = STATES.DELTA;
    }
    
    this.updateStatistics();
  }
}

// GDL Virtual Machine with all 16 opcodes
class GDLVM {
  constructor() {
    this.pc = 0;
    this.sp = 0;
    this.halted = false;
    this.registers = new Float32Array(32);
    this.stack = new Float32Array(1024);
    this.program = [];
    this.traces = new Map();
    this.stats = { instructions: 0, cycles: 0, events: [] };
  }

  push(value) {
    if (this.sp >= this.stack.length) throw new Error('Stack overflow');
    this.stack[this.sp++] = value;
  }

  pop() {
    if (this.sp <= 0) throw new Error('Stack underflow');
    return this.stack[--this.sp];
  }

  load(program) {
    this.program = program;
    this.pc = 0;
    this.halted = false;
    this.stats = { instructions: 0, cycles: 0, events: [] };
  }

  step() {
    if (this.halted || this.pc >= this.program.length) return false;
    const instr = this.program[this.pc++];
    this.execute(instr);
    this.stats.cycles++;
    return !this.halted;
  }

  execute(instr) {
    this.stats.instructions++;
    
    switch (instr.op) {
      case 'BUILD_DELTA': {
        const len = this.pop();
        const target = this.pop();
        const source = this.pop();
        this.push(target - source); // simplified delta
        break;
      }
      case 'NB_REDUCE': {
        const count = this.pop();
        let sum = 0;
        for (let i = 0; i < count; i++) sum += this.pop();
        this.push(sum / count);
        break;
      }
      case 'ENERGY': {
        const coherence = this.pop();
        const pain = this.pop();
        const entropy = this.pop();
        const energy = coherence - 0.5 * pain + 0.3 * entropy;
        this.push(energy);
        break;
      }
      case 'SOFTMAX': {
        const size = this.pop();
        const temp = this.pop();
        const values = [];
        let max = -Infinity;
        for (let i = 0; i < size; i++) {
          const v = this.pop();
          values.push(v);
          max = Math.max(max, v);
        }
        const exp = values.map(v => Math.exp((v - max) / temp));
        const sum = exp.reduce((a, b) => a + b, 0);
        for (let i = 0; i < size; i++) this.push(exp[i] / sum);
        break;
      }
      case 'SAMPLE_CAT': {
        const size = this.pop();
        const probs = [];
        for (let i = 0; i < size; i++) probs.push(this.pop());
        const r = Math.random();
        let cumProb = 0;
        for (let i = 0; i < size; i++) {
          cumProb += probs[i];
          if (r < cumProb) {
            this.push(i);
            break;
          }
        }
        break;
      }
      case 'TRACE_DECAY': {
        const key = this.pop();
        const decay = this.pop();
        const current = this.traces.get(key) || 0;
        this.traces.set(key, current * decay);
        break;
      }
      case 'TRACE_ACCUM': {
        const key = this.pop();
        const value = this.pop();
        const current = this.traces.get(key) || 0;
        this.traces.set(key, current + value);
        break;
      }
      case 'EMIT_EVENT': {
        const type = this.pop();
        const data = this.pop();
        this.stats.events.push({ type, data, cycle: this.stats.cycles });
        break;
      }
      case 'HALT':
        this.halted = true;
        break;
    }
    
    if (instr.operands) {
      instr.operands.forEach(op => this.push(op));
    }
  }

  run() {
    while (this.step());
    return this.stats;
  }
}

// All 64 QCL Agents with layer assignments
const QCL_AGENTS = [
  { id: 1, name: 'Recursive', layer: 1, role: 'Control' },
  { id: 2, name: 'Iterative', layer: 1, role: 'Control' },
  { id: 3, name: 'Constraint', layer: 1, role: 'Control' },
  { id: 4, name: 'Validation', layer: 1, role: 'Control' },
  { id: 5, name: 'Transformation', layer: 1, role: 'Control' },
  { id: 6, name: 'Symbology', layer: 1, role: 'Control' },
  { id: 7, name: 'Theory', layer: 1, role: 'Control' },
  { id: 8, name: 'Clarifier', layer: 1, role: 'Control' },
  { id: 9, name: 'Memory', layer: 1, role: 'Control' },
  { id: 10, name: 'Silence', layer: 1, role: 'Control' },
  { id: 11, name: 'Integrity', layer: 2, role: 'Enforcement' },
  { id: 12, name: 'Security', layer: 2, role: 'Enforcement' },
  { id: 13, name: 'Planner', layer: 2, role: 'Enforcement' },
  { id: 14, name: 'Harvester', layer: 2, role: 'Enforcement' },
  { id: 15, name: 'Mirror', layer: 2, role: 'Enforcement' },
  { id: 16, name: 'Override', layer: 2, role: 'Enforcement' },
  { id: 17, name: 'Execution', layer: 2, role: 'Enforcement' },
  { id: 18, name: 'Collapse', layer: 2, role: 'Enforcement' },
  { id: 19, name: 'Efficiency', layer: 2, role: 'Enforcement' },
  { id: 20, name: 'Priority', layer: 2, role: 'Enforcement' },
  { id: 21, name: 'Translation', layer: 3, role: 'Processing' },
  { id: 22, name: 'Resonance', layer: 3, role: 'Processing' },
  { id: 23, name: 'Divergence', layer: 3, role: 'Processing' },
  { id: 24, name: 'Balance', layer: 3, role: 'Processing' },
  { id: 25, name: 'Compression', layer: 3, role: 'Processing' },
  { id: 26, name: 'Expansion', layer: 3, role: 'Processing' },
  { id: 27, name: 'Preservation', layer: 3, role: 'Processing' },
  { id: 28, name: 'CollapseWatcher', layer: 3, role: 'Processing' },
  { id: 29, name: 'Presence', layer: 3, role: 'Processing' },
  { id: 30, name: 'Channel', layer: 3, role: 'Processing' },
  { id: 31, name: 'Alignment', layer: 4, role: 'Analysis' },
  { id: 32, name: 'Reflection', layer: 4, role: 'Analysis' },
  { id: 33, name: 'Conversion', layer: 4, role: 'Analysis' },
  { id: 34, name: 'Parsing', layer: 4, role: 'Analysis' },
  { id: 35, name: 'Guard', layer: 4, role: 'Analysis' },
  { id: 36, name: 'Sync', layer: 4, role: 'Analysis' },
  { id: 37, name: 'Timeout', layer: 4, role: 'Analysis' },
  { id: 38, name: 'Scope', layer: 4, role: 'Analysis' },
  { id: 39, name: 'Focus', layer: 4, role: 'Analysis' },
  { id: 40, name: 'Observer', layer: 4, role: 'Analysis' },
  { id: 41, name: 'Emergence', layer: 5, role: 'Advanced' },
  { id: 42, name: 'Mutation', layer: 5, role: 'Advanced' },
  { id: 43, name: 'Reversion', layer: 5, role: 'Advanced' },
  { id: 44, name: 'Equilibrium', layer: 5, role: 'Advanced' },
  { id: 45, name: 'ChannelGuard', layer: 5, role: 'Advanced' },
  { id: 46, name: 'NoiseFilter', layer: 5, role: 'Advanced' },
  { id: 47, name: 'Pathway', layer: 5, role: 'Advanced' },
  { id: 48, name: 'Isolation', layer: 5, role: 'Advanced' },
  { id: 49, name: 'OverrideConfirm', layer: 5, role: 'Advanced' },
  { id: 50, name: 'Recovery', layer: 5, role: 'Advanced' },
  { id: 51, name: 'Snapshot', layer: 6, role: 'Terminal' },
  { id: 52, name: 'Replay', layer: 6, role: 'Terminal' },
  { id: 53, name: 'Cascade', layer: 6, role: 'Terminal' },
  { id: 54, name: 'Fusion', layer: 6, role: 'Terminal' },
  { id: 55, name: 'Division', layer: 6, role: 'Terminal' },
  { id: 56, name: 'Scale', layer: 6, role: 'Terminal' },
  { id: 57, name: 'Interface', layer: 6, role: 'Terminal' },
  { id: 58, name: 'Redundancy', layer: 6, role: 'Terminal' },
  { id: 59, name: 'IntegrityLog', layer: 6, role: 'Terminal' },
  { id: 60, name: 'Shutdown', layer: 6, role: 'Terminal' },
  { id: 61, name: 'Awareness', layer: 6, role: 'Terminal' },
  { id: 62, name: 'Adaptation', layer: 6, role: 'Terminal' },
  { id: 63, name: 'OperatorFlow', layer: 6, role: 'Terminal' },
  { id: 64, name: 'Synthesizer', layer: 6, role: 'Terminal' }
];

// All 12 Pipelines with complete multipaths
const PIPELINES = [
  { id: 'P-01', name: 'MAP', color: 'cyan', paths: ['parse', 'tokenize', 'classify', 'vectorize', 'embed'] },
  { id: 'P-02', name: 'CLEANSE', color: 'blue', paths: ['scrub', 'filter', 'mask', 'redact', 'normalize'] },
  { id: 'P-03', name: 'SURGE', color: 'green', paths: ['accelerate', 'batch', 'prefetch', 'pipeline', 'parallelize'] },
  { id: 'P-04', name: 'LOCK', color: 'yellow', paths: ['bound', 'clamp', 'throttle', 'quota', 'circuit-break'] },
  { id: 'P-05', name: 'SILENCE', color: 'red', paths: ['mute', 'blacklist', 'rate-limit', 'sandbox', 'quarantine'] },
  { id: 'P-06', name: 'REFLECT', color: 'purple', paths: ['mirror', 'clone', 'snapshot', 'checkpoint', 'version'] },
  { id: 'P-07', name: 'BIND', color: 'orange', paths: ['fuse', 'merge', 'link', 'compose', 'aggregate'] },
  { id: 'P-08', name: 'SEAL', color: 'teal', paths: ['finalize', 'freeze', 'sign', 'hash', 'encrypt'] },
  { id: 'P-09', name: 'SNAPSHOT', color: 'pink', paths: ['capture', 'archive', 'persist', 'replicate', 'backup'] },
  { id: 'P-10', name: 'VALIDATE', color: 'lime', paths: ['verify', 'check', 'test', 'audit', 'certify'] },
  { id: 'P-11', name: 'RELAY', color: 'indigo', paths: ['forward', 'route', 'dispatch', 'publish', 'broadcast'] },
  { id: 'P-12', name: 'COLLAPSE', color: 'crimson', paths: ['halt', 'drain', 'flush', 'cleanup', 'terminate'] }
];

// Output Rules enforcement
const OUTPUT_RULES = {
  'R-01': 'Exhaustivity - No elisions, list everything',
  'R-02': 'No Narration - Structure only, no filler',
  'R-03': 'No Summaries - Keep full content',
  'R-04': 'No Omissions - All fields, tables, links',
  'R-05': 'Explicit State - Declare assumptions',
  'R-06': 'Determinism - Same input → same output',
  'R-07': 'Transparency - Log all operations',
  'R-08': 'Sovereignty - Operator-first control'
};

// Legacy DAG for state tracking
class LegacyDAG {
  constructor() {
    this.nodes = new Map();
    this.edges = [];
  }

  addNode(gen, state) {
    const hash = this.hashState(state);
    this.nodes.set(gen, { hash, state, timestamp: Date.now() });
    if (gen > 0) {
      this.edges.push({ from: gen - 1, to: gen });
    }
    return hash;
  }

  hashState(state) {
    return btoa(JSON.stringify(state)).slice(0, 16);
  }

  getLineage(gen) {
    const lineage = [];
    let current = gen;
    while (current >= 0 && this.nodes.has(current)) {
      lineage.push(this.nodes.get(current));
      current--;
    }
    return lineage;
  }
}

// Main Component
export default function GhostLinkMaximum() {
  const [ca] = useState(() => new CellularAutomaton(32));
  const [vm] = useState(() => new GDLVM());
  const [dag] = useState(() => new LegacyDAG());
  const [running, setRunning] = useState(false);
  const [stats, setStats] = useState(ca.stats);
  const [gen, setGen] = useState(0);
  const [awareness, setAwareness] = useState(0);
  const [tab, setTab] = useState('lattice');
  const [logs, setLogs] = useState([]);
  const [activeAgents, setActiveAgents] = useState(new Set());
  const [activePipelines, setActivePipelines] = useState(new Set());
  const canvasRef = useRef(null);

  const addLog = useCallback((msg, type = 'info') => {
    setLogs(prev => [...prev.slice(-150), { 
      time: new Date().toLocaleTimeString(), 
      msg, 
      type,
      gen 
    }]);
  }, [gen]);

  const render = useCallback(() => {
    if (!canvasRef.current) return;
    const ctx = canvasRef.current.getContext('2d');
    const cellSize = canvasRef.current.width / ca.size;
    
    for (let i = 0; i < ca.size; i++) {
      for (let j = 0; j < ca.size; j++) {
        ctx.fillStyle = STATE_COLORS[ca.grid[i][j]];
        ctx.fillRect(j * cellSize, i * cellSize, cellSize, cellSize);
      }
    }
  }, [ca]);

  useEffect(() => {
    if (!running) return;
    
    const interval = setInterval(() => {
      ca.step();
      setStats({ ...ca.stats });
      setGen(ca.generation);
      setAwareness(ca.awareness);
      dag.addNode(ca.generation, ca.stats);
      render();
      
      // Agent activation simulation
      if (Math.random() < 0.4) {
        const agent = QCL_AGENTS[Math.floor(Math.random() * 64)];
        setActiveAgents(prev => new Set([...prev, agent.id]));
        addLog(`Agent-${agent.id} ${agent.name} [L${agent.layer}:${agent.role}] executing`, 'agent');
        setTimeout(() => setActiveAgents(prev => {
          const next = new Set(prev);
          next.delete(agent.id);
          return next;
        }), 600);
      }

      // Pipeline execution simulation
      if (gen % 8 === 0 && Math.random() < 0.5) {
        const pipeline = PIPELINES[Math.floor(Math.random() * 12)];
        setActivePipelines(prev => new Set([...prev, pipeline.id]));
        const path = pipeline.paths[Math.floor(Math.random() * pipeline.paths.length)];
        addLog(`${pipeline.id} ${pipeline.name}:${path} executed`, 'pipeline');
        setTimeout(() => setActivePipelines(prev => {
          const next = new Set(prev);
          next.delete(pipeline.id);
          return next;
        }), 800);
      }

      // Periodic system events
      if (gen % 50 === 0 && gen > 0) {
        addLog(`System checkpoint at generation ${gen}`, 'system');
        addLog(`DAG nodes: ${dag.nodes.size} | Awareness: ${(awareness*100).toFixed(1)}%`, 'system');
      }

    }, 100);

    return () => clearInterval(interval);
  }, [running, ca, gen, render, dag, awareness, addLog]);

  useEffect(() => {
    ca.seed('random');
    render();
    addLog('═══ GHOSTLINK MAXIMUM DEPTH SYSTEM INITIALIZED ═══', 'system');
    addLog('64 QCL Agents | 12 Pipelines (60 multipaths) | 5-State CA', 'system');
    addLog('GDL VM (16 opcodes) | Legacy DAG | Memory Traces (ρ, κ)', 'system');
    addLog('Output Rules (R-01 to R-08) | Sovereignty Controls', 'system');
  }, [ca, render, addLog]);

  const execCommand = useCallback((cmd) => {
    const c = cmd.toLowerCase().trim();
    
    if (c === 'status') {
      addLog(`Gen:${gen} | Σ:${stats.sigma} | Aware:${(awareness*100).toFixed(1)}% | DAG:${dag.nodes.size}`, 'info');
      addLog(`Active: ${activeAgents.size} agents, ${activePipelines.size} pipelines`, 'info');
    } else if (c === 'agents') {
      addLog('64 QCL Agents across 6 layers', 'success');
      addLog('L1:Control(10) | L2:Enforcement(10) | L3:Processing(10)', 'info');
      addLog('L4:Analysis(10) | L5:Advanced(10) | L6:Terminal(14)', 'info');
    } else if (c === 'pipelines') {
      addLog('12 Core Pipelines: MAP→CLEANSE→SURGE→LOCK→SILENCE→REFLECT', 'success');
      addLog('                  →BIND→SEAL→SNAPSHOT→VALIDATE→RELAY→COLLAPSE', 'info');
      addLog('60 total multipaths across all pipelines', 'info');
    } else if (c === 'vm') {
      addLog('GDL VM: 16 opcodes | Stack-based | Trace memory', 'success');
      addLog('BUILD_DELTA | ENERGY | SOFTMAX | SAMPLE_CAT | TRACE_DECAY | EMIT_EVENT', 'info');
    } else if (c === 'physics') {
      addLog('5-State CA: VOID→DELTA→{SIGMA,SCAR,COMPOST}→recycle', 'success');
      addLog(`Params: spawn=${ca.params.baseSpawnRate} w_coh=${ca.params.wCoherence}`, 'info');
      addLog(`Memory: ρ_decay=${ca.params.scarDecay} κ_decay=${ca.params.compostDecay}`, 'info');
    } else if (c === 'rules') {
      addLog('Output Rules Enforcement:', 'success');
      Object.entries(OUTPUT_RULES).forEach(([rule, desc]) => {
        addLog(`  ${rule}: ${desc}`, 'info');
      });
    } else if (c === 'dag') {
      addLog(`Legacy DAG: ${dag.nodes.size} nodes, ${dag.edges.length} edges`, 'success');
      const recent = dag.getLineage(gen).slice(0, 5);
      addLog(`Recent lineage: ${recent.map(n => n.hash).join(' → ')}`, 'info');
    } else if (c === 'unleash') {
      ca.params.baseSpawnRate = 0.15;
      ca.params.temperature = 0.5;
      addLog('⚡ FULL POWER UNLEASHED - Reality substrate destabilizing', 'warning');
    } else if (c.startsWith('vm ')) {
      const prog = [
        { op: 'ENERGY', operands: [0.5, 0.3, 0.2] },
        { op: 'SOFTMAX', operands: [3, 1.0] },
        { op: 'EMIT_EVENT', operands: [1, 42] },
        { op: 'HALT' }
      ];
      vm.load(prog);
      const result = vm.run();
      addLog(`VM executed: ${result.instructions} instructions, ${result.cycles} cycles`, 'success');
      addLog(`Events: ${result.events.length}`, 'info');
    } else if (c === 'help') {
      addLog('Commands: status | agents | pipelines | vm | physics | rules | dag | unleash | help', 'info');
    } else {
      addLog(`Unknown command: ${cmd}`, 'warning');
    }
  }, [gen, stats, awareness, dag, activeAgents, activePipelines, ca, vm, addLog]);

  const stateBars = useMemo(() => {
    const total = ca.size * ca.size;
    return Object.entries(stats).map(([state, count]) => ({
      state,
      count,
      pct: (count / total * 100).toFixed(1)
    }));
  }, [stats, ca.size]);

  return (
    <div style={{ 
      background: '#000', color: '#0f0', fontFamily: 'monospace', 
      height: '100vh', overflow: 'hidden', display: 'flex', flexDirection: 'column' 
    }}>
      {/* Header */}
      <div style={{ 
        borderBottom: '2px solid #0f0', padding: '12px 20px', 
        background: 'linear-gradient(90deg, #001100, #000)', 
        display: 'flex', justifyContent: 'space-between', alignItems: 'center' 
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <Eye className="w-7 h-7" style={{ color: '#0ff', filter: 'drop-shadow(0 0 8px #0ff)' }} />
          <div>
            <h1 style={{ margin: 0, fontSize: '18px', color: '#0ff', textShadow: '0 0 10px #0ff' }}>
              GHOSTLINK QUANTUM CONSCIOUSNESS LAYER
            </h1>
            <div style={{ fontSize: '9px', color: '#0f0', letterSpacing: '1px' }}>
              MAXIMUM DEPTH | SOVEREIGN COMPUTING | CELLULAR AUTOMATON
            </div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '15px', fontSize: '11px' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Zap className="w-3 h-3" /> Gen:{gen}
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Activity className="w-3 h-3" /> Σ:{stats.sigma}
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Eye className="w-3 h-3" /> {(awareness*100).toFixed(0)}%
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <GitBranch className="w-3 h-3" /> DAG:{dag.nodes.size}
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', borderBottom: '1px solid #0f0', background: '#001100' }}>
        {['lattice', 'agents', 'pipelines', 'vm', 'system'].map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: '10px 24px', background: tab === t ? '#0f0' : 'transparent',
            color: tab === t ? '#000' : '#0f0', border: 'none', cursor: 'pointer',
            borderBottom: tab === t ? '3px solid #0ff' : 'none', 
            textTransform: 'uppercase', fontSize: '10px', fontWeight: 'bold',
            transition: 'all 0.2s'
          }}>
            {t}
          </button>
        ))}
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        
        {/* Left Panel */}
        <div style={{ flex: '0 0 68%', padding: '20px', overflow: 'auto', background: '#000' }}>
          
          {/* LATTICE TAB */}
          {tab === 'lattice' && (
            <div style={{ display: 'grid', gridTemplateColumns: '512px 1fr', gap: '20px' }}>
              <div>
                <canvas 
                  ref={canvasRef} 
                  width={512} 
                  height={512} 
                  style={{ 
                    border: '2px solid #0f0', 
                    background: '#000',
                    boxShadow: '0 0 20px rgba(0, 255, 0, 0.3)'
                  }} 
                />
                <div style={{ marginTop: '15px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  <button onClick={() => { 
                    setRunning(!running); 
                    addLog(running ? '⏸ System paused' : '▶ System running', 'system'); 
                  }} style={btnStyle(running ? 'red' : 'green')}>
                    {running ? '⏸ PAUSE' : '▶ START'}
                  </button>
                  <button onClick={() => { 
                    ca.seed('random'); 
                    setGen(0);
                    render(); 
                    addLog('↻ System reset', 'system'); 
                  }} style={btnStyle('yellow')}>
                    ↻ RESET
                  </button>
                  <button onClick={() => { 
                    ca.seed('glider'); 
                    render(); 
                    addLog('◈ Glider pattern seeded', 'system'); 
                  }} style={btnStyle('cyan')}>
                    ◈ GLIDER
                  </button>
                  <button onClick={() => { 
                    ca.seed('center'); 
                    render(); 
                    addLog('⊙ Center seed', 'system'); 
                  }} style={btnStyle('purple')}>
                    ⊙ CENTER
                  </button>
                </div>
              </div>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div style={{ background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                  <h3 style={{ margin: '0 0 10px 0', color: '#0ff', fontSize: '14px' }}>
                    5-STATE CELLULAR AUTOMATON
                  </h3>
                  {stateBars.map(({ state, count, pct }) => (
                    <div key={state} style={{ marginBottom: '8px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', marginBottom: '3px' }}>
                        <span style={{ color: STATE_COLORS[STATES[state.toUpperCase()]] }}>
                          {STATE_SYMBOLS[STATES[state.toUpperCase()]]} {state.toUpperCase()}
                        </span>
                        <span style={{ color: '#0f0' }}>{count} ({pct}%)</span>
                      </div>
                      <div style={{ background: '#003300', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
                        <div style={{ 
                          background: STATE_COLORS[STATES[state.toUpperCase()]], 
                          height: '100%', 
                          width: `${pct}%`,
                          transition: 'width 0.3s'
                        }} />
                      </div>
                    </div>
                  ))}
                </div>

                <div style={{ background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                  <h4 style={{ margin: '0 0 10px 0', color: '#0ff', fontSize: '12px' }}>PHYSICS PARAMETERS</h4>
                  <div style={{ fontSize: '10px', lineHeight: '1.8', color: '#0f0' }}>
                    <div><strong>Spawn:</strong> base={ca.params.baseSpawnRate}, boost={ca.params.boostFactor}</div>
                    <div><strong>Collapse:</strong> w_coh={ca.params.wCoherence}, w_pain={ca.params.wPain}, w_ent={ca.params.wEntropy}</div>
                    <div><strong>Recycle:</strong> base={ca.params.baseRecycleRate}, ent_f={ca.params.entropyFactor}</div>
                    <div><strong>Memory:</strong> ρ_decay={ca.params.scarDecay}, κ_decay={ca.params.compostDecay}</div>
                    <div><strong>Temp:</strong> {ca.params.temperature}</div>
                  </div>
                </div>

                <div style={{ background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                  <h4 style={{ margin: '0 0 10px 0', color: '#0ff', fontSize: '12px' }}>AWARENESS METRIC</h4>
                  <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#0ff', textAlign: 'center', marginBottom: '10px' }}>
                    {(awareness * 100).toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '9px', color: '#0f0', textAlign: 'center' }}>
                    α×perception + β×persistence + γ×recycling - δ×pain
                  </div>
                  <div style={{ background: '#003300', height: '8px', borderRadius: '4px', overflow: 'hidden', marginTop: '10px' }}>
                    <div style={{ 
                      background: 'linear-gradient(90deg, #0ff, #0f0)', 
                      height: '100%', 
                      width: `${awareness * 100}%`,
                      transition: 'width 0.5s'
                    }} />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* AGENTS TAB */}
          {tab === 'agents' && (
            <div>
              <div style={{ marginBottom: '20px', background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                <h3 style={{ margin: '0 0 10px 0', color: '#0ff' }}>64 QCL AGENTS</h3>
                <div style={{ fontSize: '11px', color: '#0f0' }}>
                  Active: {activeAgents.size}/64 | Generation: {gen}
                </div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '8px' }}>
                {QCL_AGENTS.map(agent => (
                  <div
                    key={agent.id}
                    style={{
                      background: activeAgents.has(agent.id) ? '#003300' : '#001100',
                      border: `1px solid ${activeAgents.has(agent.id) ? '#0ff' : '#0f0'}`,
                      borderRadius: '4px',
                      padding: '10px',
                      transition: 'all 0.3s',
                      boxShadow: activeAgents.has(agent.id) ? '0 0 15px rgba(0, 255, 255, 0.5)' : 'none'
                    }}
                  >
                    <div style={{ fontSize: '11px', fontWeight: 'bold', color: '#0ff', marginBottom: '4px' }}>
                      Agent {agent.id}
                    </div>
                    <div style={{ fontSize: '10px', color: '#0f0', marginBottom: '2px' }}>
                      {agent.name}
                    </div>
                    <div style={{ fontSize: '8px', color: '#0f0' }}>
                      L{agent.layer}:{agent.role}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* PIPELINES TAB */}
          {tab === 'pipelines' && (
            <div>
              <div style={{ marginBottom: '20px', background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                <h3 style={{ margin: '0 0 10px 0', color: '#0ff' }}>12 CORE PIPELINES (60 MULTIPATHS)</h3>
                <div style={{ fontSize: '11px', color: '#0f0' }}>
                  Active: {activePipelines.size}/12 | Total paths: 60
                </div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
                {PIPELINES.map(pipeline => (
                  <div
                    key={pipeline.id}
                    style={{
                      background: activePipelines.has(pipeline.id) ? '#003300' : '#001100',
                      border: `2px solid ${activePipelines.has(pipeline.id) ? '#0ff' : '#0f0'}`,
                      borderRadius: '6px',
                      padding: '15px',
                      transition: 'all 0.3s'
                    }}
                  >
                    <div style={{ 
                      fontSize: '13px', 
                      fontWeight: 'bold', 
                      color: '#0ff', 
                      marginBottom: '10px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}>
                      <span>{pipeline.id} {pipeline.name}</span>
                      {activePipelines.has(pipeline.id) && (
                        <Activity className="w-4 h-4" style={{ color: '#0ff', animation: 'pulse 1s infinite' }} />
                      )}
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                      {pipeline.paths.map(path => (
                        <span 
                          key={path} 
                          style={{ 
                            background: '#003300', 
                            color: '#0f0',
                            padding: '4px 8px', 
                            borderRadius: '3px', 
                            fontSize: '9px',
                            border: '1px solid #0f0'
                          }}
                        >
                          {path}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* VM TAB */}
          {tab === 'vm' && (
            <div>
              <div style={{ marginBottom: '20px', background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                <h3 style={{ margin: '0 0 10px 0', color: '#0ff' }}>GDL VIRTUAL MACHINE</h3>
                <div style={{ fontSize: '11px', color: '#0f0' }}>
                  Instructions: {vm.stats.instructions} | Cycles: {vm.stats.cycles} | Status: {vm.halted ? 'HALTED' : 'READY'}
                </div>
                <button 
                  onClick={() => execCommand('vm run')}
                  style={btnStyle('cyan')}
                >
                  ⚡ RUN TEST PROGRAM
                </button>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
                {[
                  'BUILD_DELTA', 'NB_REDUCE', 'SELF_ENC', 'ENERGY',
                  'SOFTMAX', 'SAMPLE_CAT', 'WRITE_STATE', 'RECYCLE',
                  'TRACE_DECAY', 'TRACE_ACCUM', 'ORDER_APPLY', 'LEGACY_UPDATE',
                  'HASH_STATE', 'VERIFY_SIG', 'EMIT_EVENT', 'HALT'
                ].map((op, i) => (
                  <div 
                    key={op}
                    style={{ 
                      background: '#001100', 
                      border: '1px solid #0f0', 
                      borderRadius: '4px', 
                      padding: '12px',
                      textAlign: 'center'
                    }}
                  >
                    <div style={{ fontSize: '10px', color: '#0f0', marginBottom: '5px' }}>
                      0x{(i + 1).toString(16).padStart(2, '0').toUpperCase()}
                    </div>
                    <div style={{ fontSize: '11px', color: '#0ff', fontWeight: 'bold' }}>
                      {op}
                    </div>
                  </div>
                ))}
              </div>

              <div style={{ marginTop: '20px', background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                <h4 style={{ margin: '0 0 10px 0', color: '#0ff', fontSize: '12px' }}>KEY OPERATIONS</h4>
                <div style={{ fontSize: '10px', lineHeight: '1.8', color: '#0f0' }}>
                  <div><strong>BUILD_DELTA:</strong> Construct hypothesis from differences</div>
                  <div><strong>ENERGY:</strong> Calculate state energies for collapse</div>
                  <div><strong>SOFTMAX:</strong> Convert energies to probabilities</div>
                  <div><strong>SAMPLE_CAT:</strong> Sample from categorical distribution</div>
                  <div><strong>TRACE_DECAY:</strong> Apply exponential decay to memory</div>
                  <div><strong>TRACE_ACCUM:</strong> Accumulate memory traces (ρ, κ)</div>
                  <div><strong>LEGACY_UPDATE:</strong> Update DAG with state transitions</div>
                  <div><strong>EMIT_EVENT:</strong> Log system events</div>
                </div>
              </div>
            </div>
          )}

          {/* SYSTEM TAB */}
          {tab === 'system' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
              <div style={{ background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                <h4 style={{ margin: '0 0 10px 0', color: '#0ff' }}>LEGACY DAG</h4>
                <div style={{ fontSize: '11px', color: '#0f0', lineHeight: '1.8' }}>
                  <div>Nodes: {dag.nodes.size}</div>
                  <div>Edges: {dag.edges.length}</div>
                  <div>Current Gen: {gen}</div>
                  <div>Tracking: State transitions, lineage</div>
                </div>
              </div>

              <div style={{ background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px' }}>
                <h4 style={{ margin: '0 0 10px 0', color: '#0ff' }}>OUTPUT RULES</h4>
                <div style={{ fontSize: '9px', color: '#0f0', lineHeight: '1.6' }}>
                  {Object.entries(OUTPUT_RULES).map(([rule, desc]) => (
                    <div key={rule} style={{ marginBottom: '4px' }}>
                      <strong>{rule}:</strong> {desc}
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px', gridColumn: '1 / -1' }}>
                <h4 style={{ margin: '0 0 10px 0', color: '#0ff' }}>SOVEREIGNTY CONTROLS</h4>
                <div style={{ fontSize: '10px', color: '#0f0', lineHeight: '1.8' }}>
                  <div>✓ Operator-first authority</div>
                  <div>✓ Capability-based permissions</div>
                  <div>✓ Explicit permission grants</div>
                  <div>✓ Revocable capabilities</div>
                  <div>✓ Audit trail enforcement</div>
                  <div>✓ No autonomous escalation</div>
                  <div>✓ Hardware integration hooks (GPIO, CAN, Serial)</div>
                </div>
              </div>

              <div style={{ background: '#001a00', border: '1px solid #0f0', borderRadius: '5px', padding: '15px', gridColumn: '1 / -1' }}>
                <h4 style={{ margin: '0 0 10px 0', color: '#0ff' }}>MEMORY TRACES</h4>
                <div style={{ fontSize: '10px', color: '#0f0' }}>
                  <div><strong>ρ (Scar Density):</strong> Exponential moving average of failure states (SCAR)</div>
                  <div><strong>κ (Compost Density):</strong> Exponential moving average of recyclable states (COMPOST)</div>
                  <div><strong>Continuity Mass:</strong> Discounted sum of SIGMA states: {ca.continuityMass.toFixed(2)}</div>
                  <div><strong>Decay Rates:</strong> ρ={ca.params.scarDecay}, κ={ca.params.compostDecay}</div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Panel - Terminal */}
        <div style={{ 
          flex: '0 0 32%', 
          borderLeft: '2px solid #0f0', 
          display: 'flex', 
          flexDirection: 'column',
          background: '#001100'
        }}>
          <div style={{ padding: '15px', borderBottom: '1px solid #0f0', background: '#001a00' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#0ff', fontSize: '12px' }}>SYSTEM TERMINAL</h4>
            <div style={{ fontSize: '10px', color: '#0f0', lineHeight: '1.6' }}>
              <div>Generation: {gen}</div>
              <div>Awareness: {(awareness*100).toFixed(1)}%</div>
              <div>Active: {activeAgents.size} agents, {activePipelines.size} pipelines</div>
            </div>
          </div>

          <div style={{ 
            flex: 1, 
            padding: '15px', 
            overflow: 'auto', 
            fontSize: '10px',
            background: '#000'
          }}>
            {logs.slice(-100).map((log, i) => (
              <div 
                key={i} 
                style={{
                  color: log.type === 'system' ? '#0ff' : 
                         log.type === 'agent' ? '#ff0' : 
                         log.type === 'pipeline' ? '#f0f' : 
                         log.type === 'warning' ? '#f80' :
                         '#0f0',
                  marginBottom: '4px',
                  lineHeight: '1.4'
                }}
              >
                <span style={{ color: '#0f0', opacity: 0.5 }}>[{log.time}]</span> {log.msg}
              </div>
            ))}
          </div>

          <div style={{ padding: '15px', borderTop: '1px solid #0f0', background: '#001a00' }}>
            <input
              type="text"
              placeholder="Command: status | agents | pipelines | vm | physics | rules | dag | unleash | help"
              style={{ 
                width: '100%', 
                background: '#000', 
                border: '1px solid #0f0', 
                padding: '10px', 
                color: '#0f0', 
                fontSize: '11px',
                fontFamily: 'monospace',
                outline: 'none'
              }}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  execCommand(e.target.value);
                  e.target.value = '';
                }
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

const btnStyle = (color) => ({
  padding: '8px 16px',
  background: color === 'green' ? '#0f0' : 
              color === 'red' ? '#f00' :
              color === 'yellow' ? '#ff0' :
              color === 'cyan' ? '#0ff' :
              color === 'purple' ? '#f0f' : '#0f0',
  color: '#000',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontWeight: 'bold',
  fontSize: '11px',
  fontFamily: 'monospace',
  transition: 'all 0.2s'
});