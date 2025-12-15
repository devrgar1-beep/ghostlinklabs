# GhostLink Lattice UI

A React-based visualization interface for the GhostLink probe system, displaying probes, signals, and resonances in an interactive time-layered graph.

## Features

- **Lattice Visualization**: Interactive D3.js force-directed graph showing relationships between probes, signals, and resonances
- **Time Layer Navigation**: Browse through different temporal layers of the resonance lattice
- **Probe Management**: Enable/disable probes and view their resonance statistics
- **Signal Input**: Submit new signals (text, image, audio, video) for processing
- **Resonance Monitoring**: Real-time display of resonance events with strength metrics

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open http://localhost:3000 in your browser

## Architecture

- **React 18** with TypeScript for type safety
- **D3.js** for interactive data visualization
- **Webpack** for bundling and development server
- **CSS** for styling with dark theme

## Components

- `App`: Main application container with state management
- `LatticeView`: D3.js force-directed graph visualization
- `ProbePanel`: Probe management and statistics
- `SignalInput`: Signal submission interface
- `ResonancePanel`: Resonance event monitoring

## Data Flow

1. Signals are submitted through the SignalInput component
2. Active probes process signals and generate resonances
3. The LatticeView displays the current state of probes × signals × resonances
4. Resonance events are shown in real-time in the ResonancePanel

## Integration

This UI is designed to integrate with the GhostLink probe system backend. In a full implementation, it would:

- Connect to the probe runtime via WebSocket or REST API
- Receive real-time resonance events
- Allow dynamic probe loading and configuration
- Support governance policy management