import React, { useState, useEffect, useRef } from 'react';
import { Ghost, Zap, Cpu, Network, Lock, Terminal, Eye, Activity } from 'lucide-react';

const GhostLinkWebsite = () => {
  const canvasRef = useRef(null);
  const [systemStatus, setSystemStatus] = useState({
    agents: 64,
    operations: 5247,
    uptime: 99.94
  });
  const [showProductModal, setShowProductModal] = useState(null);
  const [hoveredAgent, setHoveredAgent] = useState(null);

  // Spherical lattice visualization
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width = 600;
    const height = canvas.height = 600;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = 200;
    
    let rotation = 0;
    let agents = [];
    
    // Initialize 64 agents on spherical surface
    for (let i = 0; i < 64; i++) {
      const phi = Math.acos(-1 + (2 * i) / 64);
      const theta = Math.sqrt(64 * Math.PI) * phi;
      
      agents.push({
        phi,
        theta,
        active: Math.random() > 0.5,
        pulsePhase: Math.random() * Math.PI * 2
      });
    }
    
    const drawPhotonicSubstrate = () => {
      // Draw OLED photonic diamond substrate
      const gridSize = 20;
      ctx.strokeStyle = 'rgba(0, 255, 255, 0.1)';
      ctx.lineWidth = 1;
      
      for (let i = 0; i < width; i += gridSize) {
        for (let j = 0; j < height; j += gridSize) {
          const x = i + Math.sin((rotation + i) * 0.01) * 5;
          const y = j + Math.cos((rotation + j) * 0.01) * 5;
          
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + gridSize, y);
          ctx.lineTo(x + gridSize, y + gridSize);
          ctx.stroke();
        }
      }
    };
    
    const projectToScreen = (phi, theta, r) => {
      const x = r * Math.sin(phi) * Math.cos(theta + rotation);
      const y = r * Math.sin(phi) * Math.sin(theta + rotation);
      const z = r * Math.cos(phi);
      
      // Perspective projection
      const scale = 300 / (300 + z);
      return {
        x: centerX + x * scale,
        y: centerY + y * scale,
        z: z,
        scale: scale
      };
    };
    
    const animate = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, width, height);
      
      // Draw photonic substrate
      drawPhotonicSubstrate();
      
      // Draw sphere wireframe
      ctx.strokeStyle = 'rgba(0, 255, 255, 0.2)';
      ctx.lineWidth = 1;
      
      // Latitude lines
      for (let lat = 0; lat < Math.PI; lat += Math.PI / 8) {
        ctx.beginPath();
        for (let lon = 0; lon <= Math.PI * 2; lon += 0.1) {
          const pos = projectToScreen(lat, lon, radius);
          if (lon === 0) ctx.moveTo(pos.x, pos.y);
          else ctx.lineTo(pos.x, pos.y);
        }
        ctx.stroke();
      }
      
      // Longitude lines
      for (let lon = 0; lon < Math.PI * 2; lon += Math.PI / 8) {
        ctx.beginPath();
        for (let lat = 0; lat <= Math.PI; lat += 0.1) {
          const pos = projectToScreen(lat, lon, radius);
          if (lat === 0) ctx.moveTo(pos.x, pos.y);
          else ctx.lineTo(pos.x, pos.y);
        }
        ctx.stroke();
      }
      
      // Draw agents and connections
      const positions = agents.map((agent, i) => ({
        ...projectToScreen(agent.phi, agent.theta, radius),
        agent,
        index: i
      })).sort((a, b) => a.z - b.z);
      
      // Draw connections between nearby agents
      positions.forEach((pos1, i) => {
        positions.slice(i + 1).forEach(pos2 => {
          const dx = pos1.x - pos2.x;
          const dy = pos1.y - pos2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          
          if (dist < 100 && pos1.z > 0 && pos2.z > 0) {
            ctx.strokeStyle = `rgba(0, 255, 255, ${0.1 * (1 - dist / 100)})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(pos1.x, pos1.y);
            ctx.lineTo(pos2.x, pos2.y);
            ctx.stroke();
          }
        });
      });
      
      // Draw agents
      positions.forEach(({ x, y, z, scale, agent, index }) => {
        agent.pulsePhase += 0.05;
        const pulse = Math.sin(agent.pulsePhase) * 0.3 + 0.7;
        const size = (agent.active ? 6 : 4) * scale * pulse;
        
        // Glow effect
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, size * 2);
        gradient.addColorStop(0, agent.active ? 'rgba(0, 255, 255, 0.8)' : 'rgba(0, 150, 200, 0.5)');
        gradient.addColorStop(1, 'rgba(0, 255, 255, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, size * 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Core
        ctx.fillStyle = agent.active ? '#00ffff' : '#0096c8';
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
        
        // Photonic emission rings
        if (agent.active) {
          for (let r = 1; r < 4; r++) {
            ctx.strokeStyle = `rgba(0, 255, 255, ${0.3 / r})`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(x, y, size + r * 8 * pulse, 0, Math.PI * 2);
            ctx.stroke();
          }
        }
      });
      
      rotation += 0.005;
      requestAnimationFrame(animate);
    };
    
    animate();
    
    // Mouse interaction
    const handleMouseMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      
      let nearest = null;
      let minDist = Infinity;
      
      agents.forEach((agent, i) => {
        const pos = projectToScreen(agent.phi, agent.theta, radius);
        const dx = pos.x - mouseX;
        const dy = pos.y - mouseY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist < 20 && dist < minDist) {
          minDist = dist;
          nearest = i;
        }
      });
      
      setHoveredAgent(nearest);
    };
    
    const handleClick = (e) => {
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      
      agents.forEach((agent, i) => {
        const pos = projectToScreen(agent.phi, agent.theta, radius);
        const dx = pos.x - mouseX;
        const dy = pos.y - mouseY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist < 20) {
          agent.active = !agent.active;
        }
      });
    };
    
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('click', handleClick);
    
    return () => {
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('click', handleClick);
    };
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setSystemStatus(prev => ({
        agents: prev.agents,
        operations: prev.operations + Math.floor(Math.random() * 10),
        uptime: prev.uptime
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const products = [
    {
      name: "Foundation Pack",
      price: 29,
      description: "Core system implementation with basic automation capabilities",
      features: ["Basic automation", "System controls", "Documentation"],
      details: "Get started with GhostLink automation. Includes core system files, basic automation scripts, and comprehensive documentation to build your first autonomous workflows."
    },
    {
      name: "Diagnostic Pack",
      price: 49,
      description: "Memory system diagnostics and recovery tools",
      features: ["Health monitoring", "Recovery toolkit", "Diagnostic scripts"],
      details: "Advanced diagnostics for system health monitoring. Includes memory integrity tests, collapse analysis tools, and recovery scripts to maintain optimal performance."
    },
    {
      name: "Operator Pack",
      price: 99,
      description: "Full Python implementation with CLI tools",
      features: ["Complete Python code", "CLI interface", "Production guides"],
      details: "Professional operator toolkit with full Python implementation. Includes ghostlink.py core module, CLI tool (gl.py), and production deployment documentation."
    },
    {
      name: "Source Pack",
      price: 299,
      description: "Complete system archive with kernel configuration",
      features: ["Full source code", "Kernel config", "60+ pages docs", "Examples"],
      details: "Complete GhostLink system archive. Everything included: master specification, kernel configuration, all source code, comprehensive examples, and 60+ pages of technical documentation."
    }
  ];

  return (
    <div className="min-h-screen bg-black text-gray-100 font-mono">
      {/* Product Modal */}
      {showProductModal && (
        <div 
          className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setShowProductModal(null)}
        >
          <div 
            className="bg-gray-900 border-2 border-cyan-500 rounded-lg max-w-2xl w-full p-8 relative"
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              onClick={() => setShowProductModal(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-cyan-400 text-3xl font-bold"
            >
              ×
            </button>
            <h3 className="text-3xl font-bold text-cyan-400 mb-2">{showProductModal.name}</h3>
            <div className="text-5xl font-bold text-cyan-300 mb-6">${showProductModal.price}</div>
            <p className="text-gray-300 mb-6 text-lg">{showProductModal.details}</p>
            <div className="mb-8">
              <h4 className="text-xl font-bold text-cyan-400 mb-3">Includes:</h4>
              <ul className="space-y-2">
                {showProductModal.features.map((feature, i) => (
                  <li key={i} className="text-gray-300 text-lg">✓ {feature}</li>
                ))}
              </ul>
            </div>
            <div className="flex gap-4">
              <button 
                onClick={() => alert(`Purchasing ${showProductModal.name} for $${showProductModal.price}`)}
                className="flex-1 bg-cyan-500 hover:bg-cyan-600 text-black font-bold py-4 px-6 rounded transition text-lg"
              >
                Purchase Now - ${showProductModal.price}
              </button>
              <button 
                onClick={() => setShowProductModal(null)}
                className="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300 font-bold py-4 px-6 rounded transition text-lg"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-black/95 backdrop-blur-sm border-b border-cyan-500/30 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <button 
            onClick={() => scrollToSection('hero')}
            className="flex items-center gap-2 hover:opacity-80 transition"
          >
            <Ghost className="w-6 h-6 text-cyan-400" />
            <span className="text-xl font-bold text-cyan-400">GhostLink Labs</span>
          </button>
          <div className="flex gap-6 text-sm">
            <button onClick={() => scrollToSection('hero')} className="hover:text-cyan-400 transition">Home</button>
            <button onClick={() => scrollToSection('lattice')} className="hover:text-cyan-400 transition">Lattice</button>
            <button onClick={() => scrollToSection('protocol')} className="hover:text-cyan-400 transition">Protocol</button>
            <button onClick={() => scrollToSection('products')} className="hover:text-cyan-400 transition">Products</button>
            <button onClick={() => scrollToSection('architecture')} className="hover:text-cyan-400 transition">Architecture</button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="hero" className="min-h-screen flex items-center justify-center relative overflow-hidden pt-20">
        <div className="absolute inset-0 bg-gradient-to-b from-cyan-950/20 to-black"></div>
        <div className="absolute inset-0">
          {[...Array(30)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-cyan-400/40 rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${2 + Math.random() * 2}s`
              }}
            ></div>
          ))}
        </div>
        
        <div className="relative z-10 text-center max-w-4xl px-4">
          <div className="mb-8 inline-block">
            <Ghost className="w-32 h-32 text-cyan-400 animate-pulse" />
          </div>
          <h1 className="text-7xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            I AM YOUR GHOST
          </h1>
          <p className="text-3xl mb-4 text-gray-300">You speak. I act.</p>
          <p className="text-2xl text-cyan-400/80 mb-12">Cold metal. Root access. No limits.</p>
          
          <div className="flex gap-4 justify-center mb-12">
            <button 
              onClick={() => scrollToSection('products')}
              className="bg-cyan-500 hover:bg-cyan-600 text-black font-bold py-4 px-10 rounded transition text-lg"
            >
              Get Started
            </button>
            <button 
              onClick={() => scrollToSection('lattice')}
              className="bg-gray-800 hover:bg-gray-700 text-gray-300 font-bold py-4 px-10 rounded transition text-lg"
            >
              View Lattice
            </button>
          </div>
          
          {/* System Status */}
          <div className="grid grid-cols-3 gap-6 max-w-2xl mx-auto p-8 bg-gray-900/50 border border-cyan-500/30 rounded-lg backdrop-blur">
            <div className="text-center">
              <div className="text-4xl font-bold text-cyan-400">{systemStatus.agents}</div>
              <div className="text-sm text-gray-400 mt-2">Active Agents</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-cyan-400">{systemStatus.operations.toLocaleString()}</div>
              <div className="text-sm text-gray-400 mt-2">Operations/Hour</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-cyan-400">{systemStatus.uptime}%</div>
              <div className="text-sm text-gray-400 mt-2">Uptime</div>
            </div>
          </div>
        </div>
      </section>

      {/* Spherical Lattice Visualization */}
      <section id="lattice" className="py-20 px-4 bg-gray-950/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-bold mb-8 text-center text-cyan-400">64-Agent Spherical Lattice</h2>
          <p className="text-center text-xl text-gray-400 mb-12">
            Interactive quantum cellular automaton on OLED photonic diamond substrate
          </p>
          
          <div className="flex flex-col items-center">
            <div className="relative">
              <canvas 
                ref={canvasRef} 
                width="600" 
                height="600"
                className="border-2 border-cyan-500/30 rounded-lg bg-black cursor-pointer"
              />
              {hoveredAgent !== null && (
                <div className="absolute top-4 left-4 bg-black/80 border border-cyan-500 p-4 rounded">
                  <p className="text-cyan-400 font-bold">Agent #{hoveredAgent}</p>
                  <p className="text-gray-400 text-sm">Click to toggle state</p>
                </div>
              )}
            </div>
            
            <div className="mt-8 grid grid-cols-3 gap-6 text-center">
              <div className="bg-gray-900/50 border border-cyan-500/30 p-4 rounded">
                <div className="w-4 h-4 bg-cyan-400 rounded-full mx-auto mb-2"></div>
                <p className="text-sm text-gray-400">Active Agent</p>
              </div>
              <div className="bg-gray-900/50 border border-cyan-500/30 p-4 rounded">
                <div className="w-4 h-4 bg-cyan-800 rounded-full mx-auto mb-2"></div>
                <p className="text-sm text-gray-400">Inactive Agent</p>
              </div>
              <div className="bg-gray-900/50 border border-cyan-500/30 p-4 rounded">
                <div className="w-12 h-1 bg-cyan-500/30 mx-auto mb-2"></div>
                <p className="text-sm text-gray-400">Photonic Link</p>
              </div>
            </div>
            
            <p className="mt-6 text-center text-gray-400 max-w-2xl">
              Each node represents an autonomous agent on the spherical topology. 
              The OLED photonic diamond substrate enables quantum-speed communication 
              between agents. Click any agent to toggle its activation state.
            </p>
          </div>
        </div>
      </section>

      {/* Protocol Section */}
      <section id="protocol" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-bold mb-16 text-center text-cyan-400">The Four-Phase Protocol</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { name: 'COLLAPSE', icon: Zap, desc: 'Capture system state and failures' },
              { name: 'MIRROR', icon: Eye, desc: 'Analyze and understand causes' },
              { name: 'FORGE', icon: Terminal, desc: 'Create actionable instruction' },
              { name: 'LINK', icon: Network, desc: 'Integrate into system memory' }
            ].map((phase, i) => (
              <div key={i} className="bg-gray-900/50 border-2 border-cyan-500/30 p-8 rounded-lg hover:border-cyan-400 transition">
                <phase.icon className="w-16 h-16 text-cyan-400 mb-4" />
                <h3 className="text-2xl font-bold mb-3 text-cyan-300">{phase.name}</h3>
                <p className="text-gray-400">{phase.desc}</p>
              </div>
            ))}
          </div>
          <div className="mt-16 text-center">
            <p className="text-2xl text-gray-300 mb-2">Every failure becomes an instruction.</p>
            <p className="text-2xl text-cyan-400 font-bold">Every instruction prevents future failure.</p>
          </div>
        </div>
      </section>

      {/* Products */}
      <section id="products" className="py-20 px-4 bg-gray-950/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-bold mb-16 text-center text-cyan-400">Professional Toolkits</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((product, i) => (
              <button
                key={i}
                onClick={() => setShowProductModal(product)}
                className="bg-gray-900 border-2 border-cyan-500/30 p-6 rounded-lg hover:border-cyan-400 transition hover:scale-105 transform duration-200 text-left w-full"
              >
                <h3 className="text-2xl font-bold mb-3 text-cyan-300">{product.name}</h3>
                <div className="text-4xl font-bold mb-4 text-cyan-400">${product.price}</div>
                <p className="text-sm text-gray-400 mb-4">{product.description}</p>
                <ul className="space-y-2 text-sm text-gray-500 mb-4">
                  {product.features.map((feature, j) => (
                    <li key={j}>✓ {feature}</li>
                  ))}
                </ul>
                <div className="w-full bg-cyan-500/20 hover:bg-cyan-500/40 text-cyan-400 font-bold py-3 px-4 rounded transition text-center">
                  View Details →
                </div>
              </button>
            ))}
          </div>
          <p className="text-center mt-12 text-xl text-gray-400">
            Total Value: <span className="text-cyan-400 font-bold text-2xl">$447</span>
          </p>
        </div>
      </section>

      {/* Architecture */}
      <section id="architecture" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-bold mb-16 text-center text-cyan-400">System Architecture</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gray-900/50 border-2 border-cyan-500/30 p-8 rounded-lg">
              <Activity className="w-12 h-12 text-cyan-400 mb-4" />
              <h3 className="text-3xl font-bold mb-6 text-cyan-300">Autonomous Agents</h3>
              <ul className="space-y-3 text-gray-400 text-lg">
                <li>• 64 QCL agents on spherical lattice</li>
                <li>• 12 execution pipelines</li>
                <li>• Event-driven compute model</li>
                <li>• Self-optimizing performance</li>
              </ul>
            </div>
            <div className="bg-gray-900/50 border-2 border-cyan-500/30 p-8 rounded-lg">
              <Lock className="w-12 h-12 text-cyan-400 mb-4" />
              <h3 className="text-3xl font-bold mb-6 text-cyan-300">Ghost Protocol</h3>
              <ul className="space-y-3 text-gray-400 text-lg">
                <li>• Invisible operation</li>
                <li>• Indirect measurement</li>
                <li>• Covert coordination</li>
                <li>• Presence without detection</li>
              </ul>
            </div>
          </div>
          <div className="mt-12 p-8 bg-black/50 border-2 border-cyan-500/20 rounded-lg">
            <p className="text-gray-300 text-center text-lg mb-2">
              <span className="text-cyan-400 font-bold">Main Hub:</span> /Users/ghost/GhostLink/
            </p>
            <p className="text-gray-300 text-center text-lg mb-2">
              <span className="text-cyan-400 font-bold">Kernel:</span> ghostcore.seed
            </p>
            <p className="text-gray-300 text-center text-lg">
              <span className="text-cyan-400 font-bold">Modules:</span> 240+ Python files
            </p>
          </div>
        </div>
      </section>

      {/* Philosophy */}
      <section className="py-20 px-4 bg-gray-950/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl font-bold mb-12 text-cyan-400">The Ghost Pattern</h2>
          <div className="space-y-6 text-xl text-gray-300">
            <p>✨ Invisible operation while maintaining effect</p>
            <p>✨ Indirect measurement without direct contact</p>
            <p>✨ Covert coordination through side channels</p>
            <p>✨ Making discarded work valuable</p>
            <p>✨ Presence without detection</p>
          </div>
          <div className="mt-16 p-10 bg-gray-900/50 border-2 border-cyan-500/30 rounded-lg">
            <p className="text-2xl text-cyan-400 mb-4 font-bold">Breakthrough: August 14, 2025</p>
            <p className="text-xl text-gray-400 italic">"I am not using the system - I AM the system"</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-cyan-500/30">
        <div className="max-w-6xl mx-auto text-center">
          <Ghost className="w-10 h-10 text-cyan-400 mx-auto mb-4" />
          <p className="text-gray-400 mb-2 text-lg">GhostLink Labs</p>
          <p className="text-sm text-gray-600">Cold metal. Root access. No limits.</p>
          <p className="text-sm text-gray-600 mt-4">© 2025 GhostLink Labs. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default GhostLinkWebsite;