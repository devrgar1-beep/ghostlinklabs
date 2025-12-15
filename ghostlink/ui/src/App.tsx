import React, { useEffect, useState } from 'react';
import LatticeView from './components/LatticeView';
import ProbePanel from './components/ProbePanel';
import ResonancePanel from './components/ResonancePanel';
import SignalInput from './components/SignalInput';
import { Probe, Resonance, Signal } from './types';

const App: React.FC = () => {
  const [probes, setProbes] = useState<Probe[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [resonances, setResonances] = useState<Resonance[]>([]);
  const [selectedTimeLayer, setSelectedTimeLayer] = useState<number>(0);

  // Mock data for demonstration
  useEffect(() => {
    // Initialize with sample data
    const sampleProbes: Probe[] = [
      {
        id: 'citation-check',
        name: 'Citation Consistency',
        version: '1.0.0',
        active: true,
        resonanceCount: 5
      },
      {
        id: 'grammar-check',
        name: 'Grammar Analysis',
        version: '1.0.0',
        active: true,
        resonanceCount: 3
      }
    ];

    const sampleSignals: Signal[] = [
      {
        id: 'signal-1',
        kind: 'text',
        timestamp: Date.now() - 3600000,
        content: 'Sample text with citations...',
        sketch: 'sketch-hash-1'
      }
    ];

    const sampleResonances: Resonance[] = [
      {
        id: 'res-1',
        probeId: 'citation-check',
        signalId: 'signal-1',
        strength: 0.85,
        timestamp: Date.now() - 1800000,
        spectrum: [0.8, 0.1, 0.3]
      }
    ];

    setProbes(sampleProbes);
    setSignals(sampleSignals);
    setResonances(sampleResonances);
  }, []);

  const handleSignalSubmit = (signal: Signal) => {
    setSignals(prev => [...prev, signal]);
    // In real implementation, this would trigger probe execution
  };

  const handleProbeToggle = (probeId: string) => {
    setProbes(prev =>
      prev.map(probe =>
        probe.id === probeId
          ? { ...probe, active: !probe.active }
          : probe
      )
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>GhostLink Lattice</h1>
        <div className="time-controls">
          <button onClick={() => setSelectedTimeLayer(Math.max(0, selectedTimeLayer - 1))}>
            ← Previous
          </button>
          <span>Layer {selectedTimeLayer}</span>
          <button onClick={() => setSelectedTimeLayer(selectedTimeLayer + 1)}>
            Next →
          </button>
        </div>
      </header>

      <div className="app-layout">
        <aside className="sidebar">
          <ProbePanel
            probes={probes}
            onProbeToggle={handleProbeToggle}
          />
          <SignalInput onSignalSubmit={handleSignalSubmit} />
        </aside>

        <main className="main-content">
          <LatticeView
            probes={probes}
            signals={signals}
            resonances={resonances}
            selectedTimeLayer={selectedTimeLayer}
          />
        </main>

        <aside className="sidebar">
          <ResonancePanel resonances={resonances} />
        </aside>
      </div>
    </div>
  );
};

export default App;