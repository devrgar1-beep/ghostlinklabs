import React, { useState } from 'react';
import { Signal } from '../types';

interface SignalInputProps {
  onSignalSubmit: (signal: Signal) => void;
}

const SignalInput: React.FC<SignalInputProps> = ({ onSignalSubmit }) => {
  const [content, setContent] = useState('');
  const [kind, setKind] = useState<'text' | 'image' | 'audio' | 'video'>('text');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    const signal: Signal = {
      id: `signal-${Date.now()}`,
      kind,
      timestamp: Date.now(),
      content,
      sketch: `sketch-${Date.now()}`
    };

    onSignalSubmit(signal);
    setContent('');
  };

  return (
    <div className="signal-input">
      <h3>Signal Input</h3>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>
            Type:
            <select value={kind} onChange={(e) => setKind(e.target.value as any)}>
              <option value="text">Text</option>
              <option value="image">Image</option>
              <option value="audio">Audio</option>
              <option value="video">Video</option>
            </select>
          </label>
        </div>
        <div className="input-group">
          <label>
            Content:
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter signal content..."
              rows={4}
            />
          </label>
        </div>
        <button type="submit" disabled={!content.trim()}>
          Submit Signal
        </button>
      </form>
    </div>
  );
};

export default SignalInput;