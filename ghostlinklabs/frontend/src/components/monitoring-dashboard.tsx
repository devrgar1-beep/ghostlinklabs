import React, { useState, useEffect } from 'react';
import { LineChart, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Line, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Bell, Server, FileText, RefreshCw, AlertCircle, CheckCircle, Clock } from 'lucide-react';

// Mock data for demonstration
// In production, this would be fetched from your actual systems
const generateMockData = () => {
  const now = new Date();
  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(now.getDate() - (6 - i));
    return date.toISOString().split('T')[0];
  });

  // Build data
  const buildData = last7Days.map(day => ({
    date: day,
    success: Math.floor(Math.random() * 5),
    failure: Math.floor(Math.random() * 2),
  }));

  // Service status
  const services = [
    { name: 'Google Drive API', status: Math.random() > 0.1 ? 'up' : 'down', uptime: `${(Math.random() * 2 + 98).toFixed(2)}%`, responseTime: `${Math.floor(Math.random() * 200 + 100)}ms` },
    { name: 'Gmail API', status: Math.random() > 0.1 ? 'up' : 'down', uptime: `${(Math.random() * 2 + 98).toFixed(2)}%`, responseTime: `${Math.floor(Math.random() * 200 + 100)}ms` },
    { name: 'Calendar API', status: Math.random() > 0.1 ? 'up' : 'down', uptime: `${(Math.random() * 2 + 98).toFixed(2)}%`, responseTime: `${Math.floor(Math.random() * 200 + 100)}ms` },
    { name: 'Vercel Integration', status: Math.random() > 0.1 ? 'up' : 'down', uptime: `${(Math.random() * 2 + 98).toFixed(2)}%`, responseTime: `${Math.floor(Math.random() * 200 + 100)}ms` },
    { name: 'Cloudflare Integration', status: Math.random() > 0.1 ? 'up' : 'down', uptime: `${(Math.random() * 2 + 98).toFixed(2)}%`, responseTime: `${Math.floor(Math.random() * 200 + 100)}ms` },
  ];

  // Recent logs
  const logTypes = ['info', 'warning', 'error'];
  const logMessages = [
    'Build completed successfully',
    'API rate limit reached',
    'Failed to fetch data from Google Drive',
    'Deployment to staging completed',
    'Authentication token expired',
    'New component generated',
    'Service synchronization completed',
    'System backup created',
  ];

  const logs = Array.from({ length: 10 }, (_, i) => {
    const timestamp = new Date();
    timestamp.setMinutes(timestamp.getMinutes() - Math.floor(Math.random() * 60));
    return {
      id: i,
      timestamp: timestamp.toISOString(),
      type: logTypes[Math.floor(Math.random() * logTypes.length)],
      message: logMessages[Math.floor(Math.random() * logMessages.length)],
    };
  }).sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

  // Project stats
  const projectStats = {
    components: Math.floor(Math.random() * 20 + 30),
    hooks: Math.floor(Math.random() * 10 + 15),
    services: Math.floor(Math.random() * 5 + 8),
    tests: Math.floor(Math.random() * 100 + 150),
    coverage: Math.floor(Math.random() * 10 + 85),
  };

  return {
    buildData,
    services,
    logs,
    projectStats,
  };
};

export default function GhostLinkDashboard() {
  const [data, setData] = useState(() => generateMockData());
  const [refreshing, setRefreshing] = useState(false);

  const refreshData = () => {
    setRefreshing(true);
    setTimeout(() => {
      setData(generateMockData());
      setRefreshing(false);
    }, 1000);
  };

  useEffect(() => {
    // Auto-refresh every 2 minutes
    const interval = setInterval(refreshData, 120000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <header className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">GhostLink Project Monitoring</h1>
            <p className="text-gray-500">Unified Tool Integration Dashboard</p>
          </div>
          <button 
            onClick={refreshData} 
            className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
            disabled={refreshing}
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
            {refreshing ? 'Refreshing...' : 'Refresh Data'}
          </button>
        </div>
      </header>

      {/* Status Overview */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <Server className="w-5 h-5 text-blue-500" />
            <h2 className="text-lg font-semibold">Service Status</h2>
          </div>
          <div className="space-y-3">
            {data.services.map(service => (
              <div key={service.name} className="flex items-center justify-between border-b pb-2">
                <span className="font-medium">{service.name}</span>
                <div className="flex items-center gap-2">
                  <span className={`inline-block w-3 h-3 rounded-full ${service.status === 'up' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                  <span className={service.status === 'up' ? 'text-green-600' : 'text-red-600'}>
                    {service.status.toUpperCase()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <FileText className="w-5 h-5 text-blue-500" />
            <h2 className="text-lg font-semibold">Project Stats</h2>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-sm text-gray-500">Components</div>
              <div className="text-xl font-bold">{data.projectStats.components}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Custom Hooks</div>
              <div className="text-xl font-bold">{data.projectStats.hooks}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Services</div>
              <div className="text-xl font-bold">{data.projectStats.services}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Tests</div>
              <div className="text-xl font-bold">{data.projectStats.tests}</div>
            </div>
            <div className="col-span-2">
              <div className="text-sm text-gray-500">Test Coverage</div>
              <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className={`h-full ${data.projectStats.coverage > 90 ? 'bg-green-500' : data.projectStats.coverage > 80 ? 'bg-yellow-500' : 'bg-red-500'}`}
                  style={{ width: `${data.projectStats.coverage}%` }}
                ></div>
              </div>
              <div className="text-right text-sm mt-1">{data.projectStats.coverage}%</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <Bell className="w-5 h-5 text-blue-500" />
            <h2 className="text-lg font-semibold">Recent Logs</h2>
          </div>
          <div className="space-y-3 max-h-[300px] overflow-y-auto">
            {data.logs.map(log => (
              <div key={log.id} className="flex gap-3 border-b pb-2">
                {log.type === 'error' && <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />}
                {log.type === 'warning' && <AlertCircle className="w-5 h-5 text-yellow-500 flex-shrink-0" />}
                {log.type === 'info' && <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />}
                <div className="flex-grow">
                  <div className={`font-medium ${log.type === 'error' ? 'text-red-600' : log.type === 'warning' ? 'text-yellow-600' : 'text-green-600'}`}>
                    {log.message}
                  </div>
                  <div className="text-xs text-gray-500 flex items-center">
                    <Clock className="w-3 h-3 mr-1" />
                    {new Date(log.timestamp).toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Charts */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4">Build History (Last 7 Days)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.buildData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="success" name="Successful Builds" fill="#22c55e" />
              <Bar dataKey="failure" name="Failed Builds" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4">API Response Times</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" 
                data={data.services} 
                type="category" 
                allowDuplicatedCategory={false} />
              <YAxis />
              <Tooltip formatter={(value) => `${value}ms`} />
              <Legend />
              <Line 
                data={data.services} 
                dataKey="responseTime" 
                name="Response Time" 
                stroke="#3b82f6" 
                activeDot={{ r: 8 }}
                isAnimationActive={true}
                dot={{ stroke: '#3b82f6', strokeWidth: 2, r: 4 }}
                type="monotone"
                connectNulls={true}
                strokeWidth={2}
                formatter={(value) => parseInt(value)}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Service Details */}
      <section className="mt-6 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">Service Details</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Service</th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uptime</th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Response Time</th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.services.map((service, index) => (
                <tr key={service.name} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{service.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${service.status === 'up' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {service.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{service.uptime}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{service.responseTime}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-blue-600 hover:text-blue-900">View Details</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <footer className="mt-6 text-center text-gray-500 text-sm">
        <p>GhostLink Unified Dashboard Monitoring • {new Date().toLocaleString()}</p>
      </footer>
    </div>
  );
}
