import React, { useState, useEffect } from 'react';
import { Smartphone, Laptop, Wifi, Activity, Battery, Bell, PlayCircle, PauseCircle, SkipForward, RefreshCw, Zap } from 'lucide-react';

export default function UniversalControlHub() {
  const [devices, setDevices] = useState([
    { id: 'mac', name: 'MacBook Pro', type: 'laptop', status: 'online', battery: 56, apps: 12, focus: 'Claude' },
    { id: 'iphone', name: 'iPhone', type: 'phone', status: 'online', battery: 85, apps: 24, focus: 'Messages' }
  ]);
  
  const [selectedDevice, setSelectedDevice] = useState('mac');
  const [logs, setLogs] = useState([]);
  const [actions, setActions] = useState([]);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev.slice(-20), { timestamp, message, type }]);
  };

  useEffect(() => {
    addLog('🌐 Universal Control Hub initialized', 'success');
    addLog('🍎 Mac connected: Apple M3 Pro', 'success');
    addLog('📱 iPhone connected: Ready', 'success');
    addLog('✨ Cross-device synergy active', 'info');
  }, []);

  const executeAction = (action) => {
    setActions(prev => [...prev.slice(-5), { 
      id: Date.now(), 
      action, 
      device: selectedDevice,
      timestamp: new Date().toLocaleTimeString()
    }]);
    
    addLog(`▶️ ${action} on ${devices.find(d => d.id === selectedDevice)?.name}`, 'action');
    
    // Simulate action completion
    setTimeout(() => {
      addLog(`✅ ${action} completed`, 'success');
    }, 1000);
  };

  const quickActions = [
    { label: 'Get Status', icon: Activity, action: 'Get system status' },
    { label: 'Check Battery', icon: Battery, action: 'Check battery level' },
    { label: 'Send Alert', icon: Bell, action: 'Send notification' },
    { label: 'Refresh', icon: RefreshCw, action: 'Refresh device state' }
  ];

  const spotifyControls = [
    { label: 'Play', icon: PlayCircle, action: 'Play music' },
    { label: 'Pause', icon: PauseCircle, action: 'Pause music' },
    { label: 'Next', icon: SkipForward, action: 'Next track' }
  ];

  const currentDevice = devices.find(d => d.id === selectedDevice);

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
            GhostLink Universal Control Hub
          </h1>
          <p className="text-blue-300">Control all your devices from anywhere - No Terminal needed!</p>
        </div>

        {/* Device Selector */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {devices.map(device => (
            <button
              key={device.id}
              onClick={() => {
                setSelectedDevice(device.id);
                addLog(`📱 Switched to ${device.name}`, 'info');
              }}
              className={`p-6 rounded-xl border-2 transition-all ${
                selectedDevice === device.id
                  ? 'bg-purple-600/30 border-purple-400 shadow-lg shadow-purple-500/50'
                  : 'bg-white/5 border-white/10 hover:border-purple-400/50'
              }`}
            >
              <div className="flex items-center gap-4 mb-4">
                {device.type === 'laptop' ? (
                  <Laptop className="w-12 h-12 text-cyan-400" />
                ) : (
                  <Smartphone className="w-12 h-12 text-purple-400" />
                )}
                <div className="text-left">
                  <h3 className="text-xl font-bold">{device.name}</h3>
                  <p className="text-sm text-gray-300">{device.type}</p>
                </div>
              </div>
              
              <div className="space-y-2 text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Status:</span>
                  <span className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${
                      device.status === 'online' ? 'bg-green-400' : 'bg-gray-400'
                    }`} />
                    {device.status}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Battery:</span>
                  <span className="flex items-center gap-2">
                    <Battery className="w-4 h-4" />
                    {device.battery}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Apps:</span>
                  <span>{device.apps}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Focus:</span>
                  <span className="text-cyan-400">{device.focus}</span>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* Control Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Quick Actions */}
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Zap className="w-6 h-6 text-yellow-400" />
              Quick Actions
            </h2>
            
            <div className="grid grid-cols-2 gap-3 mb-6">
              {quickActions.map((qa, i) => (
                <button
                  key={i}
                  onClick={() => executeAction(qa.action)}
                  className="p-4 bg-gradient-to-br from-purple-500/20 to-blue-500/20 hover:from-purple-500/30 hover:to-blue-500/30 rounded-lg border border-purple-400/30 transition-all flex flex-col items-center gap-2"
                >
                  <qa.icon className="w-8 h-8 text-purple-300" />
                  <span className="text-sm font-medium">{qa.label}</span>
                </button>
              ))}
            </div>

            <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
              🎵 Spotify Control
            </h3>
            <div className="grid grid-cols-3 gap-3">
              {spotifyControls.map((sc, i) => (
                <button
                  key={i}
                  onClick={() => executeAction(sc.action)}
                  className="p-3 bg-green-500/20 hover:bg-green-500/30 rounded-lg border border-green-400/30 transition-all flex flex-col items-center gap-2"
                >
                  <sc.icon className="w-6 h-6 text-green-300" />
                  <span className="text-xs">{sc.label}</span>
                </button>
              ))}
            </div>

            <div className="mt-6">
              <h3 className="text-lg font-bold mb-3">Custom Command</h3>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Type any command..."
                  className="flex-1 px-4 py-2 bg-white/10 rounded-lg border border-white/20 outline-none focus:border-purple-400"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      executeAction(e.target.value);
                      e.target.value = '';
                    }
                  }}
                />
                <button
                  onClick={() => {
                    const input = document.querySelector('input');
                    if (input.value) {
                      executeAction(input.value);
                      input.value = '';
                    }
                  }}
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium transition-all"
                >
                  Send
                </button>
              </div>
            </div>
          </div>

          {/* Activity Log & Recent Actions */}
          <div className="space-y-6">
            {/* Recent Actions */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold mb-4">Recent Actions</h2>
              <div className="space-y-2">
                {actions.length === 0 ? (
                  <p className="text-gray-400 text-sm">No actions yet. Try clicking a button!</p>
                ) : (
                  actions.slice(-5).reverse().map(action => (
                    <div key={action.id} className="p-3 bg-purple-500/20 rounded-lg border border-purple-400/30">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium">{action.action}</span>
                        <span className="text-xs text-gray-400">{action.timestamp}</span>
                      </div>
                      <div className="text-sm text-gray-300">
                        Device: {devices.find(d => d.id === action.device)?.name}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Activity Log */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold mb-4">Activity Log</h2>
              <div className="space-y-1 max-h-64 overflow-y-auto">
                {logs.map((log, i) => (
                  <div key={i} className={`text-sm flex gap-2 ${
                    log.type === 'success' ? 'text-green-400' :
                    log.type === 'action' ? 'text-cyan-400' :
                    log.type === 'error' ? 'text-red-400' :
                    'text-gray-300'
                  }`}>
                    <span className="text-gray-500">[{log.timestamp}]</span>
                    <span>{log.message}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-8 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 backdrop-blur-lg rounded-xl p-6 border border-cyan-400/30">
          <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
            <Wifi className="w-6 h-6 text-cyan-400" />
            How This Works
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <div className="font-bold text-cyan-400 mb-2">1. Select Device</div>
              <p className="text-gray-300">Click on Mac or iPhone above to control that device</p>
            </div>
            <div>
              <div className="font-bold text-purple-400 mb-2">2. Click Actions</div>
              <p className="text-gray-300">Use the buttons to control your device - no Terminal needed!</p>
            </div>
            <div>
              <div className="font-bold text-green-400 mb-2">3. Watch Logs</div>
              <p className="text-gray-300">See everything happening in real-time on the right</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}