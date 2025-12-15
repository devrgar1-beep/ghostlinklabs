export interface Probe {
  id: string;
  name: string;
  version: string;
  active: boolean;
  resonanceCount: number;
}

export interface Signal {
  id: string;
  kind: 'text' | 'image' | 'audio' | 'video';
  timestamp: number;
  content: string;
  sketch: string;
}

export interface Resonance {
  id: string;
  probeId: string;
  signalId: string;
  strength: number;
  timestamp: number;
  spectrum: number[];
}

export interface LatticeNode {
  id: string;
  type: 'probe' | 'signal' | 'resonance';
  x: number;
  y: number;
  data: Probe | Signal | Resonance;
}

export interface LatticeLink {
  source: string;
  target: string;
  strength: number;
}