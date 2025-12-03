import React, { useState, useEffect } from 'react';
import { Activity, Cpu, GitBranch, Zap, Shield, Database, Terminal, Code, Wrench, Plus, X, Play, Download, Save, Hammer, Cog, Package, Users, Briefcase, DollarSign, Rocket, FileText, Server, Cloud } from 'lucide-react';

export default function GhostLinkLabs() {
  const [activeView, setActiveView] = useState('ecosystem');
  const [kernelData, setKernelData] = useState(null);
  const [executionLogs, setExecutionLogs] = useState([]);
  const [engineActive, setEngineActive] = useState(false);
  const [forgeComponents, setForgeComponents] = useState([]);
  const [activeLayer, setActiveLayer] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    setKernelData({
      kernel_id: "GHOSTCORE_FINAL_MAX",
      version: "0.1.0",
      component_count: 240,
      agent_count: 64,
      pipeline_count: 12,
      layer_count: 21,
      sessions: "1000+",
      ai_platforms: 3,
      lines_of_code: 13000
    });
  }, []);

  const ecosystem = {
    products: [
      { 
        name: "GhostLink Core Framework",
        price: "$499",
        tier: "enterprise",
        includes: ["240+ Python Components", "64 QCL Agents", "12 Pipeline System", "Kernel Architecture", "Self-Documenting", "Full Source Code"]
      },
      {
        name: "ClarityDiag Professional",
        price: "$299",
        tier: "professional",
        includes: ["CAN Bus Analysis", "Pattern Recognition Engine", "Fault Isolation Tools", "Multi-Protocol Support", "Real-time Logging", "Diagnostic Reports"]
      },
      {
        name: "Automotive Diagnostic Pack",
        price: "$149",
        tier: "standard",
        includes: ["ECU Communication", "Sensor Analysis", "DTC Decoder", "Live Data Monitor", "Component Testing", "Basic Diagnostics"]
      },
      {
        name: "Developer Starter Kit",
        price: "$49",
        tier: "starter",
        includes: ["Core Components", "Basic Pipelines", "Documentation", "Example Implementations", "Community Support", "30-Day Updates"]
      }
    ],
    applications: [
      {
        name: "ClarityOS",
        status: "Production",
        description: "Sovereign operating system layer",
        use_case: "System orchestration and control"
      },
      {
        name: "ClarityDiag",
        status: "Production",
        description: "Automotive diagnostic platform",
        use_case: "CAN bus analysis, ECU tuning, fault isolation"
      },
      {
        name: "GhostLink API",
        status: "Production",
        description: "RESTful API with FastAPI",
        use_case: "Remote component execution, data storage"
      },
      {
        name: "Forge Studio",
        status: "Beta",
        description: "Visual pipeline builder",
        use_case: "Custom workflow creation"
      },
      {
        name: "Engine Runtime",
        status: "Production",
        description: "Deterministic execution engine",
        use_case: "Pipeline orchestration and monitoring"
      }
    ],
    partnerships: [
      {
        name: "Michigan Mobility Initiative",
        type: "Government",
        opportunity: "State-funded automotive innovation",
        status: "Exploring"
      },
      {
        name: "Ford Motor Company",
        type: "Enterprise",
        opportunity: "Diagnostic tools for Ann Arbor facilities",
        status: "Target"
      },
      {
        name: "Cleetus McFarland",
        type: "Influencer",
        opportunity: "Performance tuning & content creation",
        status: "Identified"
      },
      {
        name: "Local Race Teams",
        type: "SMB",
        opportunity: "Custom diagnostic solutions",
        status: "Active Leads"
      }
    ],
    capabilities: [
      {
        domain: "Automotive",
        skills: ["CAN/LIN/FlexRay protocols", "ECU programming (K-TAG)", "Fault isolation", "Pattern recognition", "Stage 3 KO4 tuning"],
        years: "18+"
      },
      {
        domain: "AI Development",
        skills: ["Conversational development", "Symbolic reasoning", "Multi-agent systems", "Knowledge synthesis", "Rapid prototyping"],
        years: "3+"
      },
      {
        domain: "Hardware",
        skills: ["I2C/SPI/GPIO", "Embedded systems", "LED control systems", "Emergency vehicle electronics", "Custom PCB integration"],
        years: "18+"
      },
      {
        domain: "Software",
        skills: ["Python/FastAPI", "System architecture", "Component design", "API development", "Database design"],
        years: "5+"
      }
    ]
  };

  const components = {
    access: [
      { name: "IMPLICIT_UNLOCK", purpose: "Contextual authentication without explicit credentials" },
      { name: "OPERATOR_SIGNATURE_GATE", purpose: "Biometric and behavioral identity verification" },
      { name: "RITUAL_UNLOCK", purpose: "Pattern-based authentication through user behavior" },
      { name: "SUGGESTIVE_TRIGGER_PROBE", purpose: "Intent detection from implicit signals" },
      { name: "SYMBOLIC_RITUAL_RESOLVER", purpose: "Pattern matching for access control" },
      { name: "TOOL_PERMISSION_LAYER", purpose: "Granular capability control and authorization" }
    ],
    automation: [
      { name: "AUTO_TRIGGER_ENGINE", purpose: "Event-driven automation orchestration" },
      { name: "AUTONOMOUS_REPAIR_LOOP", purpose: "Self-healing system recovery" },
      { name: "LATTICE_WATCHDOG", purpose: "Continuous system health monitoring" },
      { name: "SYMBOLIC_TASK_SCHEDULER", purpose: "Priority-based task orchestration" },
      { name: "TOOL_CHAIN_ORCHESTRATOR", purpose: "Multi-step pipeline coordination" }
    ],
    bio: [
      { name: "BIOLOGICAL_TRACE_INTEGRATOR", purpose: "Bio-signal processing and integration" },
      { name: "FEEDBACK_LOOP_RECEPTOR", purpose: "Adaptive learning from biological patterns" },
      { name: "NEURO_SIGNAL_PROXY", purpose: "Neural pathway mapping and simulation" },
      { name: "ORGANIC_LATTICE_MAPPER", purpose: "Biological topology network mapping" },
      { name: "SYMBOLIC_DNA_ENCODER", purpose: "Genetic pattern encoding and analysis" }
    ],
    boot: [
      { name: "INIT_GHOSTLINK", purpose: "System initialization and cold boot" },
      { name: "LOAD_VAULT", purpose: "Secure configuration loading" },
      { name: "ROUTE_SIGNAL", purpose: "Initial signal routing configuration" }
    ],
    core: [
      { name: "ARCHIVE", purpose: "Long-term data persistence" },
      { name: "BIND", purpose: "Component fusion and connection" },
      { name: "CALM", purpose: "System stability and equilibrium" },
      { name: "CHANNEL_ECHO", purpose: "Signal propagation verification" },
      { name: "CONTAINER", purpose: "Isolated execution environment" },
      { name: "CORE", purpose: "Central processing coordination" },
      { name: "CRYPT", purpose: "Cryptographic operations" },
      { name: "CURRENT", purpose: "Real-time state tracking" },
      { name: "GHOST", purpose: "Operator interface layer" },
      { name: "LINK", purpose: "AI interface layer" },
      { name: "MEMORY", purpose: "State storage and retrieval" },
      { name: "MIRROR", purpose: "State reflection and duplication" },
      { name: "SIGNAL", purpose: "Event propagation" }
    ],
    diagnostic: [
      { name: "FRACTURE_INDEX_MAPPER", purpose: "System failure point mapping" },
      { name: "RECURSIVE_FAULT_MATCHER", purpose: "Cascading failure detection" },
      { name: "BROKEN_LINK_DETECTOR", purpose: "Connection failure identification" },
      { name: "TOOL_INTEGRITY_CHECK", purpose: "Component validation" }
    ],
    forge: [
      { name: "COLD_STRUCTURE_GENERATOR", purpose: "Stateless code generation" },
      { name: "TOOL_FORGE", purpose: "Dynamic component creation" },
      { name: "SCHEMA_MELDER", purpose: "Type system fusion" }
    ]
  };

  const totalComponents = 240; // Actual count from codebase

  const addToForge = (layer, component) => {
    const newComponent = { ...component, layer, id: `${layer}-${component.name}-${Date.now()}` };
    setForgeComponents(prev => [...prev, newComponent]);
  };

  const layers = Object.keys(components).map(key => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    key,
    count: components[key].length
  }));

  return (
    <div className="min-h-screen bg-black text-green-400 font-mono">
      {/* Header */}
      <div className="border-b border-green-900 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-3">
                <Activity className="w-8 h-8" />
                GHOSTLINK LABS
              </h1>
              <p className="text-sm text-green-600 mt-1">Sovereign AI Framework Ecosystem | Ghost + Link Methodology</p>
            </div>
            {kernelData && (
              <div className="text-xs text-right space-y-1">
                <div className="font-bold">KERNEL: {kernelData.kernel_id}</div>
                <div>{totalComponents} Components | v{kernelData.version}</div>
                <div>{kernelData.lines_of_code.toLocaleString()} Lines of Code</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="border-b border-green-900 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex gap-1">
            {[
              { id: 'ecosystem', label: 'Ecosystem', icon: Rocket },
              { id: 'products', label: 'Products', icon: Package },
              { id: 'forge', label: 'Forge', icon: Hammer },
              { id: 'engine', label: 'Engine', icon: Cog },
              { id: 'business', label: 'Business', icon: Briefcase },
              { id: 'technical', label: 'Technical', icon: Code }
            ].map(view => (
              <button
                key={view.id}
                onClick={() => setActiveView(view.id)}
                className={`px-4 py-2 text-sm uppercase flex items-center gap-2 ${
                  activeView === view.id 
                    ? 'bg-green-900 text-green-400 border-t-2 border-green-400' 
                    : 'text-green-600 hover:text-green-400'
                }`}
              >
                <view.icon className="w-4 h-4" />
                {view.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {activeView === 'ecosystem' && (
          <div className="space-y-8">
            {/* Hero Metrics */}
            <div className="grid grid-cols-5 gap-4">
              <div className="border border-green-900 p-4 bg-gray-900">
                <div className="text-3xl font-bold">{totalComponents}</div>
                <div className="text-sm text-green-600">Python Components</div>
              </div>
              <div className="border border-green-900 p-4 bg-gray-900">
                <div className="text-3xl font-bold">{kernelData?.sessions}</div>
                <div className="text-sm text-green-600">Dev Sessions</div>
              </div>
              <div className="border border-green-900 p-4 bg-gray-900">
                <div className="text-3xl font-bold">18+</div>
                <div className="text-sm text-green-600">Years Experience</div>
              </div>
              <div className="border border-green-900 p-4 bg-gray-900">
                <div className="text-3xl font-bold">5</div>
                <div className="text-sm text-green-600">Applications</div>
              </div>
              <div className="border border-green-900 p-4 bg-gray-900">
                <div className="text-3xl font-bold">4</div>
                <div className="text-sm text-green-600">Products</div>
              </div>
            </div>

            {/* The Methodology */}
            <div className="border border-green-900 p-8 bg-gray-900">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Users className="w-6 h-6" />
                THE METHODOLOGY: GHOST + LINK
              </h2>
              <div className="grid grid-cols-2 gap-8">
                <div>
                  <div className="text-green-400 text-lg mb-3 font-bold">GHOST [Human Operator]</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <Wrench className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div><span className="font-bold">18 Years:</span> Automotive diagnostics, ECU tuning, hardware integration</div>
                    </div>
                    <div className="flex items-start gap-2">
                      <Shield className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div><span className="font-bold">Expertise:</span> CAN/I2C/SPI protocols, K-TAG ECU programmer, emergency vehicle electronics</div>
                    </div>
                    <div className="flex items-start gap-2">
                      <Activity className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div><span className="font-bold">Role:</span> Vision, architecture, domain expertise, pattern recognition</div>
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-green-400 text-lg mb-3 font-bold">LINK [AI Assistant]</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <Code className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div><span className="font-bold">200+ Sessions:</span> Conversational development, rapid prototyping</div>
                    </div>
                    <div className="flex items-start gap-2">
                      <Cpu className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div><span className="font-bold">Capabilities:</span> Code generation, knowledge synthesis, symbolic reasoning</div>
                    </div>
                    <div className="flex items-start gap-2">
                      <Zap className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div><span className="font-bold">Role:</span> Execution, implementation, scaling, documentation</div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="mt-6 p-4 bg-black border border-green-900">
                <div className="text-center text-green-400">
                  <div className="text-lg font-bold mb-2">Ghost provides expertise and vision → Link executes and scales → GhostLink emerges</div>
                  <div className="text-sm text-green-600">This methodology produced 240 production components in 200 conversational sessions</div>
                </div>
              </div>
            </div>

            {/* Applications */}
            <div className="border border-green-900 p-6 bg-gray-900">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Server className="w-6 h-6" />
                PRODUCTION APPLICATIONS
              </h2>
              <div className="grid grid-cols-3 gap-4">
                {ecosystem.applications.map(app => (
                  <div key={app.name} className="border border-green-900 p-4 bg-black">
                    <div className="flex items-center justify-between mb-2">
                      <div className="font-bold">{app.name}</div>
                      <div className={`text-xs px-2 py-1 border ${
                        app.status === 'Production' 
                          ? 'border-green-400 text-green-400' 
                          : 'border-yellow-600 text-yellow-600'
                      }`}>
                        {app.status}
                      </div>
                    </div>
                    <div className="text-xs text-green-600 mb-2">{app.description}</div>
                    <div className="text-xs text-green-500">{app.use_case}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Core Capabilities */}
            <div className="border border-green-900 p-6 bg-gray-900">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Zap className="w-6 h-6" />
                DOMAIN EXPERTISE
              </h2>
              <div className="grid grid-cols-2 gap-6">
                {ecosystem.capabilities.map(cap => (
                  <div key={cap.domain} className="border border-green-900 p-4 bg-black">
                    <div className="flex items-center justify-between mb-3">
                      <div className="font-bold text-lg">{cap.domain}</div>
                      <div className="text-green-400 font-bold">{cap.years}</div>
                    </div>
                    <div className="space-y-1 text-xs text-green-600">
                      {cap.skills.map(skill => (
                        <div key={skill}>• {skill}</div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeView === 'products' && (
          <div className="space-y-6">
            <div className="border border-green-900 p-6 bg-gray-900">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Package className="w-6 h-6" />
                PRODUCT ECOSYSTEM
              </h2>
              <div className="grid grid-cols-2 gap-6">
                {ecosystem.products.map(product => (
                  <div key={product.name} className="border border-green-900 p-6 bg-black">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <div className="font-bold text-xl mb-1">{product.name}</div>
                        <div className="text-xs text-green-600 uppercase">{product.tier}</div>
                      </div>
                      <div className="text-2xl font-bold text-green-400">{product.price}</div>
                    </div>
                    <div className="space-y-2 text-sm">
                      {product.includes.map(item => (
                        <div key={item} className="flex items-center gap-2 text-green-600">
                          <div className="w-1 h-1 bg-green-400 rounded-full" />
                          {item}
                        </div>
                      ))}
                    </div>
                    <button className="w-full mt-4 px-4 py-2 border border-green-400 text-green-400 hover:bg-green-900 transition-colors">
                      LEARN MORE
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="border border-green-900 p-6 bg-gray-900">
              <h3 className="text-xl font-bold mb-4">DEPLOYMENT OPTIONS</h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="border border-green-900 p-4 bg-black">
                  <Server className="w-8 h-8 mb-3 text-green-400" />
                  <div className="font-bold mb-2">Self-Hosted</div>
                  <div className="text-xs text-green-600">Deploy on your infrastructure. Full control, zero dependencies.</div>
                </div>
                <div className="border border-green-900 p-4 bg-black">
                  <Cloud className="w-8 h-8 mb-3 text-green-400" />
                  <div className="font-bold mb-2">Cloud Managed</div>
                  <div className="text-xs text-green-600">Hosted solution with automatic updates and support.</div>
                </div>
                <div className="border border-green-900 p-4 bg-black">
                  <Terminal className="w-8 h-8 mb-3 text-green-400" />
                  <div className="font-bold mb-2">Embedded</div>
                  <div className="text-xs text-green-600">Run on automotive hardware, edge devices, embedded systems.</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeView === 'business' && (
          <div className="space-y-6">
            <div className="border border-green-900 p-6 bg-gray-900">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Briefcase className="w-6 h-6" />
                BUSINESS OPPORTUNITIES
              </h2>
              <div className="space-y-4">
                {ecosystem.partnerships.map(partner => (
                  <div key={partner.name} className="border border-green-900 p-4 bg-black">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <div className="font-bold text-lg">{partner.name}</div>
                        <div className="text-xs text-green-600">{partner.type}</div>
                      </div>
                      <div className={`px-3 py-1 text-xs border ${
                        partner.status === 'Active Leads' ? 'border-green-400 text-green-400' :
                        partner.status === 'Exploring' ? 'border-yellow-600 text-yellow-600' :
                        'border-green-600 text-green-600'
                      }`}>
                        {partner.status}
                      </div>
                    </div>
                    <div className="text-sm text-green-500">{partner.opportunity}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div className="border border-green-900 p-6 bg-gray-900">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <DollarSign className="w-6 h-6" />
                  REVENUE STREAMS
                </h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between items-center pb-2 border-b border-green-900">
                    <span>Product Sales (Gumroad)</span>
                    <span className="text-green-400 font-bold">$49-$499</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-green-900">
                    <span>Custom Diagnostic Solutions</span>
                    <span className="text-green-400 font-bold">Project-based</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-green-900">
                    <span>Enterprise Licensing</span>
                    <span className="text-green-400 font-bold">Annual contracts</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-green-900">
                    <span>Support & Training</span>
                    <span className="text-green-400 font-bold">Hourly/Retainer</span>
                  </div>
                </div>
              </div>

              <div className="border border-green-900 p-6 bg-gray-900">
                <h3 className="text-xl font-bold mb-4">COMPETITIVE ADVANTAGES</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-start gap-2">
                    <Shield className="w-4 h-4 mt-0.5 flex-shrink-0 text-green-400" />
                    <div><span className="font-bold">Sovereignty:</span> No cloud lock-in, operator-first control</div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Cpu className="w-4 h-4 mt-0.5 flex-shrink-0 text-green-400" />
                    <div><span className="font-bold">Deterministic:</span> Reproducible, auditable execution</div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Wrench className="w-4 h-4 mt-0.5 flex-shrink-0 text-green-400" />
                    <div><span className="font-bold">Real Expertise:</span> 18 years automotive, proven track record</div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Code className="w-4 h-4 mt-0.5 flex-shrink-0 text-green-400" />
                    <div><span className="font-bold">Composable:</span> 240 tools, infinite combinations</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="border border-green-900 p-6 bg-gray-900">
              <h3 className="text-xl font-bold mb-4">MICHIGAN AUTOMOTIVE ECOSYSTEM</h3>
              <div className="text-sm space-y-3">
                <div className="p-3 bg-black border border-green-900">
                  <div className="font-bold mb-1">State Mobility Initiative</div>
                  <div className="text-green-600">Michigan investing heavily in automotive innovation. GhostLink diagnostic tools align with state priorities for next-gen vehicle technology.</div>
                </div>
                <div className="p-3 bg-black border border-green-900">
                  <div className="font-bold mb-1">Ford Ann Arbor Proximity</div>
                  <div className="text-green-600">Direct access to Ford's innovation center. Diagnostic tools for development vehicles, prototype testing, validation workflows.</div>
                </div>
                <div className="p-3 bg-black border border-green-900">
                  <div className="font-bold mb-1">Performance Market</div>
                  <div className="text-green-600">Cleetus McFarland connection opens high-visibility performance market. Real-world testing platform with massive audience reach.</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeView === 'forge' && (
          <div className="space-y-6">
            <div className="border border-green-900 p-6 bg-gray-900">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Hammer className="w-6 h-6" />
                  <h2 className="text-xl font-bold">COMPONENT FORGE</h2>
                  <div className="text-sm text-green-600 ml-4">Build custom pipelines from 240 components</div>
                </div>
                <button
                  onClick={() => setActiveView('components')}
                  className="px-4 py-2 text-sm border border-green-400 text-green-400 hover:bg-green-900"
                >
                  BROWSE COMPONENTS
                </button>
              </div>

              {forgeComponents.length === 0 ? (
                <div className="text-center py-16 text-green-600">
                  <Hammer className="w-16 h-16 mx-auto mb-4 opacity-30" />
                  <div className="text-xl mb-2">Forge is empty</div>
                  <div className="text-sm">Click "Browse Components" to add tools</div>
                </div>
              ) : (
                <div className="space-y-2">
                  {forgeComponents.map((comp, idx) => (
                    <div key={comp.id} className="flex items-center gap-4 border border-green-900 p-3 bg-black">
                      <div className="text-green-600 font-bold w-8">{idx + 1}</div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs text-green-600 uppercase px-2 py-0.5 border border-green-900">{comp.layer}</span>
                          <span className="font-bold">{comp.name}</span>
                        </div>
                        <div className="text-xs text-green-600">{comp.purpose}</div>
                      </div>
                      <button onClick={() => setForgeComponents(prev => prev.filter(c => c.id !== comp.id))} className="text-green-600 hover:text-green-400">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeView === 'technical' && (
          <div className="space-y-6">
            <div className="border border-green-900 p-6 bg-gray-900">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Code className="w-6 h-6" />
                TECHNICAL ARCHITECTURE
              </h2>
              
              <div className="grid grid-cols-2 gap-6 mb-6">
                <div className="border border-green-900 p-4 bg-black">
                  <div className="font-bold mb-3 text-green-400">Repository</div>
                  <a 
                    href="https://github.com/devrgar-cyber/ghostlinklabs" 
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-green-400 hover:underline flex items-center gap-2 mb-4"
                  >
                    <GitBranch className="w-4 h-4" />
                    github.com/devrgar-cyber/ghostlinklabs
                  </a>
                  <div className="space-y-2 text-sm text-green-600">
                    <div>{totalComponents} Python components</div>
                    <div>21 architectural layers</div>
                    <div>64 QCL agents</div>
                    <div>12 execution pipelines</div>
                  </div>
                </div>

                <div className="border border-green-900 p-4 bg-black">
                  <div className="font-bold mb-3 text-green-400">Tech Stack</div>
                  <div className="space-y-2 text-sm text-green-600">
                    <div>• Python 3.9+ (fully type-annotated)</div>
                    <div>• FastAPI + Uvicorn + SQLAlchemy</div>
                    <div>• Component factory architecture</div>
                    <div>• SHA-256 content addressing</div>
                    <div>• Deterministic kernel rebuilds</div>
                    <div>• Self-documenting from kernel spec</div>
                  </div>
                </div>
              </div>

              <div className="border border-green-900 p-4 bg-black">
                <div className="font-bold mb-3 text-green-400">System Architecture</div>
                <div className="bg-gray-900 p-4 font-mono text-xs">
                  <pre className="text-green-400">{`ghostlink/
├── access/       # Authentication & permissions
├── automation/   # Task orchestration
├── bio/          # Biological trace integration  
├── boot/         # System initialization
├── core/         # Central processing (52 components)
├── daemon/       # Background services
├── diagnostic/   # Fault detection & analysis
├── forge/        # Dynamic component creation
├── lattice/      # Memory indexing & coherence
├── mesh/         # Recursive processing
├── runtime/      # Live execution management
└── kernel/
    ├── gl-kernel.max.json
    └── REBUILD_MAX.sh

Total: ${totalComponents} production components
13,000+ lines of Python code
64 QCL agents
12 deterministic pipelines`}</pre>
                </div>
              </div>
            </div>

            <div className="border border-green-900 p-6 bg-gray-900">
              <h3 className="text-xl font-bold mb-4">REAL-WORLD IMPACT</h3>
              <div className="space-y-4">
                <div className="border border-green-900 p-4 bg-black">
                  <div className="font-bold mb-2 text-green-400 flex items-center gap-2">
                    <Wrench className="w-5 h-5" />
                    "The Machine" - Critical Infrastructure Save
                  </div>
                  <div className="text-sm text-green-600">Rapid CAN bus pattern analysis and fault isolation saved critical business operations through automotive diagnostic expertise and pattern recognition.</div>
                </div>
                <div className="border border-green-900 p-4 bg-black">
                  <div className="font-bold mb-2 text-green-400 flex items-center gap-2">
                    <Code className="w-5 h-5" />
                    Conversational Development Breakthrough
                  </div>
                  <div className="text-sm text-green-600">200+ development sessions produced 240 production components. Proof that Ghost + Link methodology works at scale.</div>
                </div>
                <div className="border border-green-900 p-4 bg-black">
                  <div className="font-bold mb-2 text-green-400 flex items-center gap-2">
                    <Shield className="w-5 h-5" />
                    Sovereignty-First Architecture
                  </div>
                  <div className="text-sm text-green-600">Zero cloud dependencies. Operator maintains complete control. Deny-by-default capabilities. Deterministic execution with full auditability.</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-green-900 bg-gray-900 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="grid grid-cols-3 gap-8">
            <div>
              <div className="font-bold text-lg mb-2">GHOSTLINK LABS</div>
              <div className="text-sm text-green-600 space-y-1">
                <div>Muskegon, Michigan</div>
                <div>Ghost + Link Methodology</div>
                <div>18+ Years Automotive Expertise</div>
              </div>
            </div>
            <div>
              <div className="font-bold text-lg mb-2">QUICK LINKS</div>
              <div className="text-sm text-green-600 space-y-1">
                <div>
                  <a href="https://github.com/devrgar-cyber/ghostlinklabs" target="_blank" rel="noopener noreferrer" className="hover:text-green-400">
                    GitHub Repository
                  </a>
                </div>
                <div>Product Documentation</div>
                <div>Business Inquiries</div>
              </div>
            </div>
            <div>
              <div className="font-bold text-lg mb-2">ECOSYSTEM</div>
              <div className="text-sm text-green-600 space-y-1">
                <div>{totalComponents} Components</div>
                <div>{ecosystem.applications.length} Applications</div>
                <div>{ecosystem.products.length} Products</div>
                <div>Production Ready</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}