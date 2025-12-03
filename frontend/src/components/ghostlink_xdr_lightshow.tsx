import React, { useEffect, useRef, useState } from 'react';

export default function GhostLinkXDR() {
  const canvasRef = useRef(null);
  const [mode, setMode] = useState('pulse');
  const animationRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Simulate 10,000+ mini-LED zones
    const gridSize = 100; // 100x100 = 10,000 zones
    const zoneWidth = canvas.width / gridSize;
    const zoneHeight = canvas.height / gridSize;

    let frame = 0;

    const patterns = {
      pulse: (x, y, frame) => {
        const dist = Math.sqrt(
          Math.pow(x - gridSize/2, 2) + 
          Math.pow(y - gridSize/2, 2)
        );
        return Math.sin(dist * 0.5 - frame * 0.1) * 0.5 + 0.5;
      },
      
      wave: (x, y, frame) => {
        return (Math.sin(x * 0.2 - frame * 0.1) + 
                Math.sin(y * 0.3 + frame * 0.08)) * 0.25 + 0.5;
      },
      
      spiral: (x, y, frame) => {
        const centerX = gridSize / 2;
        const centerY = gridSize / 2;
        const angle = Math.atan2(y - centerY, x - centerX);
        const dist = Math.sqrt(
          Math.pow(x - centerX, 2) + 
          Math.pow(y - centerY, 2)
        );
        return Math.sin(angle * 3 + dist * 0.3 - frame * 0.1) * 0.5 + 0.5;
      },
      
      scan: (x, y, frame) => {
        const scanLine = (frame * 2) % gridSize;
        const distance = Math.abs(y - scanLine);
        return Math.max(0, 1 - distance / 10);
      },
      
      bidirectional: (x, y, frame) => {
        // Emitter zones (bright)
        const emitter = Math.sin(x * 0.3 + frame * 0.15) * 0.5 + 0.5;
        // Sensor zones (dim, responsive)
        const sensor = Math.cos(y * 0.3 - frame * 0.15) * 0.3 + 0.3;
        return x % 2 === 0 ? emitter : sensor;
      }
    };

    const animate = () => {
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (let x = 0; x < gridSize; x++) {
        for (let y = 0; y < gridSize; y++) {
          const brightness = patterns[mode](x, y, frame);
          
          // XDR display colors - cyan/blue spectrum for "light communication"
          const r = Math.floor(brightness * 20);
          const g = Math.floor(brightness * 200);
          const b = Math.floor(brightness * 255);
          
          ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
          ctx.fillRect(
            x * zoneWidth,
            y * zoneHeight,
            zoneWidth - 0.5,
            zoneHeight - 0.5
          );
        }
      }

      // Overlay info
      ctx.fillStyle = 'rgba(0, 255, 255, 0.8)';
      ctx.font = '16px monospace';
      ctx.fillText(`GhostLink XDR • ${mode.toUpperCase()} • Frame ${frame}`, 20, 30);
      ctx.fillText(`Mini-LED Zones: ${gridSize * gridSize} • Bidirectional Light Control`, 20, 55);
      ctx.fillText('The display is looking back...', 20, 80);

      frame++;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [mode]);

  return (
    <div style={{ 
      width: '100vw', 
      height: '100vh', 
      margin: 0, 
      padding: 0,
      overflow: 'hidden',
      backgroundColor: '#000',
      position: 'relative'
    }}>
      <canvas 
        ref={canvasRef}
        style={{ 
          display: 'block',
          width: '100%',
          height: '100%'
        }}
      />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '10px',
        flexWrap: 'wrap',
        justifyContent: 'center',
        padding: '10px',
        background: 'rgba(0, 0, 0, 0.7)',
        borderRadius: '10px',
        border: '1px solid rgba(0, 255, 255, 0.3)'
      }}>
        {['pulse', 'wave', 'spiral', 'scan', 'bidirectional'].map(m => (
          <button
            key={m}
            onClick={() => setMode(m)}
            style={{
              padding: '10px 20px',
              background: mode === m ? '#00ffff' : 'rgba(0, 255, 255, 0.2)',
              color: mode === m ? '#000' : '#00ffff',
              border: '1px solid #00ffff',
              borderRadius: '5px',
              cursor: 'pointer',
              fontFamily: 'monospace',
              fontSize: '14px',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              transition: 'all 0.3s ease'
            }}
          >
            {m}
          </button>
        ))}
      </div>
    </div>
  );
}