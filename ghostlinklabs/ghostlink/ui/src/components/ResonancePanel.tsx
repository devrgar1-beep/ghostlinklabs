import React from 'react';
import { Resonance } from '../types';

interface ResonancePanelProps {
  resonances: Resonance[];
}

const ResonancePanel: React.FC<ResonancePanelProps> = ({ resonances }) => {
  return (
    <div className="resonance-panel">
      <h3>Recent Resonances</h3>
      <div className="resonance-list">
        {resonances.map(resonance => (
          <div key={resonance.id} className="resonance-item">
            <div className="resonance-header">
              <span className="strength">
                {resonance.strength.toFixed(3)}
              </span>
              <span className="timestamp">
                {new Date(resonance.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <div className="resonance-details">
              <div>Probe: {resonance.probeId}</div>
              <div>Signal: {resonance.signalId}</div>
              <div className="spectrum">
                Spectrum: {resonance.spectrum.map(s => s.toFixed(2)).join(', ')}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResonancePanel;