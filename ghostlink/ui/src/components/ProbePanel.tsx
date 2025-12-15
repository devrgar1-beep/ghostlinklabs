import React from 'react';
import { Probe } from '../types';

interface ProbePanelProps {
  probes: Probe[];
  onProbeToggle: (probeId: string) => void;
}

const ProbePanel: React.FC<ProbePanelProps> = ({ probes, onProbeToggle }) => {
  return (
    <div className="probe-panel">
      <h3>Active Probes</h3>
      <div className="probe-list">
        {probes.map(probe => (
          <div key={probe.id} className="probe-item">
            <label>
              <input
                type="checkbox"
                checked={probe.active}
                onChange={() => onProbeToggle(probe.id)}
              />
              <span className="probe-name">{probe.name}</span>
            </label>
            <div className="probe-stats">
              v{probe.version} • {probe.resonanceCount} resonances
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProbePanel;