import axios from 'axios';
import { AlertCircle, Bell, CheckCircle, Clock, Cpu, HardDrive, MemoryStick, RefreshCw, Server, Wifi } from 'lucide-react';
import { useEffect, useState } from 'react';
import { CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

// API base URL - adjust for your setup
const API_BASE_URL = 'http://localhost:5001';

// Colors for charts
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

interface SystemMetrics {
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  timestamp: number;
  platform: string;
  hostname: string;
  is_raspberry_pi?: boolean;
  raspberry_pi?: {
    cpu_temp?: number;
    gpu_memory_mb?: number;
    throttled?: number;
  };
  arduino_devices?: any;
  system?: {
    cpu_percent: number;
    memory_percent: number;
    disk_percent: number;
    cpu_count: number;
    memory_total: number;
    memory_used: number;
    disk_total: number;
    disk_used: number;
  };
}

interface USBDriveInfo {
  name?: string;
  mount_point?: string;
  device?: string;
  size_gb?: number;
  used_gb?: number;
  free_gb?: number;
  usage_percent?: number;
  file_system?: string;
  serial_number?: string;
  vendor?: string;
  model?: string;
  is_removable?: boolean;
  last_mounted?: string;
  files?: Array<{
    name: string;
    path: string;
    size_mb?: number;
    modified?: string;
    extension?: string;
  }>;
}

interface USBDrivesData {
  drives: USBDriveInfo[];
  last_scan?: string;
  platform?: string;
  usb_support?: boolean;
}

// Chart data interfaces
interface ChartDataPoint {
  time: string;
  cpu: number;
  memory: number;
  disk: number;
  temperature: number | null;
}

interface PlatformDataPoint {
  name: string;
  value: number;
}

interface Alert {
  id: number;
  timestamp: string;
  type: string;
  severity: string;
  message: string;
  resolved: boolean;
}

interface Analytics {
  cpu?: {
    average: number;
    max: number;
    min: number;
    samples: number;
  };
  memory?: {
    average: number;
    max: number;
    min: number;
    samples: number;
  };
  platforms: Record<string, number>;
  raspberry_pi_devices: number;
  recent_alerts: Alert[];
  metrics?: any[];
  platform_stats?: Record<string, number>;
}

export default function GhostLinkDashboard() {
  const [currentMetrics, setCurrentMetrics] = useState<SystemMetrics | null>(null);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);
  const [platformData, setPlatformData] = useState<PlatformDataPoint[]>([]);
  const [usbDrives, setUsbDrives] = useState<USBDrivesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  // Process chart data from analytics
  const processChartData = (analyticsData: Analytics | null): ChartDataPoint[] => {
    if (!analyticsData?.metrics) return [];

    const dataPoints: ChartDataPoint[] = [];
    const maxPoints = 50; // Show last 50 data points

    analyticsData.metrics.slice(-maxPoints).forEach((metric: any) => {
      dataPoints.push({
        time: new Date(metric.timestamp).toLocaleTimeString(),
        cpu: metric.cpu_percent,
        memory: metric.memory_percent,
        disk: metric.disk_percent,
        temperature: metric.raspberry_pi?.cpu_temp || null
      });
    });

    return dataPoints;
  };

  // Process platform distribution
  const processPlatformData = (analyticsData: Analytics | null): PlatformDataPoint[] => {
    if (!analyticsData?.platform_stats) return [];

    return Object.entries(analyticsData.platform_stats).map(([platform, count]: [string, number]) => ({
      name: platform,
      value: count
    }));
  };

  const fetchData = async () => {
    try {
      setRefreshing(true);
      setError(null);

      console.log('🔄 Fetching data from API...');

      // Fetch monitoring data (replaces /metrics endpoint)
      try {
        console.log('📊 Fetching monitoring data...');
        const monitoringResponse = await axios.get(`${API_BASE_URL}/monitoring`, { timeout: 5000 });
        const monitoringData = monitoringResponse.data;

        // Extract system metrics from the nested structure
        if (monitoringData.system) {
          setCurrentMetrics(monitoringData.system);
          console.log('✅ Monitoring data loaded');
        } else {
          console.warn('⚠️ No system data in monitoring response');
        }
      } catch (monitoringError: any) {
        console.error('❌ Failed to fetch monitoring data:', monitoringError);
        setError('Failed to load system monitoring data. Please check the API server.');
        return;
      }

      // Fetch analytics data
      try {
        console.log('📈 Fetching analytics data...');
        const analyticsResponse = await axios.get(`${API_BASE_URL}/analytics`, { timeout: 5000 });
        const analyticsData = analyticsResponse.data;
        setAnalytics(analyticsData);
        console.log('✅ Analytics data loaded');

        // Process chart and platform data using the fetched data directly
        setChartData(processChartData(analyticsData));
        setPlatformData(processPlatformData(analyticsData));
      } catch (analyticsError: any) {
        console.warn('⚠️ Analytics data failed, continuing without it:', analyticsError);
        // Don't fail completely if analytics fails
      }

      // Fetch USB drives data
      try {
        console.log('💾 Fetching USB drives data...');
        const usbResponse = await axios.get(`${API_BASE_URL}/usb-drives`, { timeout: 5000 });
        setUsbDrives(usbResponse.data);
        console.log('✅ USB drives data loaded');
      } catch (usbError: any) {
        console.warn('⚠️ USB drives data failed, continuing without it:', usbError);
        // Don't fail completely if USB drives fails
      }

      // Generate alerts based on current metrics
      const newAlerts: Alert[] = [];
      if (currentMetrics) {
        const system = currentMetrics;
        if (system.cpu_percent > 90) {
          newAlerts.push({
            id: Date.now(),
            timestamp: new Date().toISOString(),
            type: 'warning',
            severity: 'high',
            message: `High CPU usage: ${system.cpu_percent.toFixed(1)}%`,
            resolved: false,
          });
        }
        if (system.memory_percent > 85) {
          newAlerts.push({
            id: Date.now() + 1,
            timestamp: new Date().toISOString(),
            type: 'warning',
            severity: 'high',
            message: `High memory usage: ${system.memory_percent.toFixed(1)}%`,
            resolved: false,
          });
        }
        if (system.disk_percent > 90) {
          newAlerts.push({
            id: Date.now() + 2,
            timestamp: new Date().toISOString(),
            type: 'error',
            severity: 'critical',
            message: `Critical disk usage: ${system.disk_percent.toFixed(1)}%`,
            resolved: false,
          });
        }
      }
      setAlerts(newAlerts);
      console.log('✅ Data fetch completed successfully');

    } catch (err: any) {
      console.error('❌ Critical error fetching data:', err);
      const errorMessage = err.response?.data?.error ||
        err.message ||
        'Failed to fetch monitoring data. Please check if the API server is running.';
      setError(errorMessage);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const refreshData = () => {
    fetchData();
  };

  if (loading) {
    return (
      <div className="bg-gray-100 min-h-screen p-6 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="mx-auto h-12 w-12 text-blue-500 animate-spin" />
          <p className="mt-4 text-gray-600">Loading GhostLink Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gray-100 min-h-screen p-6 flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertCircle className="mx-auto h-12 w-12 text-red-500" />
          <h2 className="mt-4 text-xl font-semibold text-gray-900">Connection Error</h2>
          <p className="mt-2 text-gray-600">{error}</p>
          <button
            onClick={refreshData}
            className="mt-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

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

      {/* System Metrics Overview */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <Cpu className="w-5 h-5 text-blue-500" />
            <h2 className="text-lg font-semibold">CPU Usage</h2>
          </div>
          <div className="text-3xl font-bold text-blue-600">
            {currentMetrics?.cpu_percent?.toFixed(1) || 'N/A'}%
          </div>
          {analytics?.cpu && (
            <div className="text-sm text-gray-500 mt-2">
              Avg: {analytics.cpu.average.toFixed(1)}% | Max: {analytics.cpu.max.toFixed(1)}%
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <MemoryStick className="w-5 h-5 text-green-500" />
            <h2 className="text-lg font-semibold">Memory</h2>
          </div>
          <div className="text-3xl font-bold text-green-600">
            {currentMetrics?.memory_percent?.toFixed(1) || 'N/A'}%
          </div>
          {analytics?.memory && (
            <div className="text-sm text-gray-500 mt-2">
              Avg: {analytics.memory.average.toFixed(1)}% | Max: {analytics.memory.max.toFixed(1)}%
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <HardDrive className="w-5 h-5 text-purple-500" />
            <h2 className="text-lg font-semibold">Disk Usage</h2>
          </div>
          <div className="text-3xl font-bold text-purple-600">
            {currentMetrics?.disk_percent?.toFixed(1) || 'N/A'}%
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <Server className="w-5 h-5 text-orange-500" />
            <h2 className="text-lg font-semibold">Platform</h2>
          </div>
          <div className="text-lg font-bold text-orange-600">
            {currentMetrics?.platform || 'Unknown'}
          </div>
          {currentMetrics?.is_raspberry_pi && (
            <div className="text-sm text-green-600 mt-2">🍓 Raspberry Pi</div>
          )}
          {currentMetrics?.raspberry_pi?.cpu_temp && (
            <div className="text-sm text-gray-500">
              Temp: {currentMetrics.raspberry_pi.cpu_temp}°C
            </div>
          )}
        </div>
      </section>

      {/* Charts Section */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4">System Metrics Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="cpu" stroke="#8884d8" name="CPU %" />
              <Line type="monotone" dataKey="memory" stroke="#82ca9d" name="Memory %" />
              <Line type="monotone" dataKey="disk" stroke="#ffc658" name="Disk %" />
              {currentMetrics?.is_raspberry_pi && (
                <Line type="monotone" dataKey="temperature" stroke="#ff7300" name="Temp °C" />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4">Platform Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={platformData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {platformData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Alerts and Arduino Section */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <Bell className="w-5 h-5 text-red-500" />
            <h2 className="text-lg font-semibold">Recent Alerts</h2>
          </div>
          <div className="space-y-3 max-h-[300px] overflow-y-auto">
            {alerts.slice(0, 10).map(alert => (
              <div key={alert.id} className="flex gap-3 border-b pb-2">
                {alert.severity === 'critical' && <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />}
                {alert.severity === 'error' && <AlertCircle className="w-5 h-5 text-orange-500 flex-shrink-0" />}
                {alert.severity === 'warning' && <AlertCircle className="w-5 h-5 text-yellow-500 flex-shrink-0" />}
                {alert.severity === 'info' && <CheckCircle className="w-5 h-5 text-blue-500 flex-shrink-0" />}
                <div className="flex-grow">
                  <div className={`font-medium ${alert.severity === 'critical' ? 'text-red-600' :
                    alert.severity === 'error' ? 'text-orange-600' :
                      alert.severity === 'warning' ? 'text-yellow-600' : 'text-blue-600'
                    }`}>
                    {alert.message}
                  </div>
                  <div className="text-xs text-gray-500 flex items-center">
                    <Clock className="w-3 h-3 mr-1" />
                    {new Date(alert.timestamp).toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
            {alerts.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <CheckCircle className="w-12 h-12 mx-auto text-green-500 mb-2" />
                <p>No active alerts</p>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <Wifi className="w-5 h-5 text-indigo-500" />
            <h2 className="text-lg font-semibold">Connected Devices</h2>
          </div>
          <div className="space-y-3">
            {currentMetrics?.arduino_devices && Object.keys(currentMetrics.arduino_devices).length > 0 ? (
              Object.entries(currentMetrics.arduino_devices).map(([deviceId, deviceData]: [string, any]) => (
                <div key={deviceId} className="border rounded-lg p-3">
                  <div className="font-medium text-indigo-600">📡 {deviceId}</div>
                  <div className="text-sm text-gray-600 mt-1">
                    {deviceData.raw ? `Raw: ${deviceData.raw}` : JSON.stringify(deviceData)}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center text-gray-500 py-8">
                <Wifi className="w-12 h-12 mx-auto text-gray-300 mb-2" />
                <p>No Arduino devices connected</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* USB Drives Section */}
      <section className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <HardDrive className="w-5 h-5 text-purple-500" />
          <h2 className="text-lg font-semibold">USB Drive Monitoring</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {usbDrives?.drives && usbDrives.drives.length > 0 ? (
            usbDrives.drives.map((drive: USBDriveInfo, index: number) => (
              <div key={index} className="border rounded-lg p-4 bg-gray-50">
                <div className="flex items-center gap-2 mb-2">
                  <HardDrive className="w-4 h-4 text-purple-500" />
                  <span className="font-medium text-purple-600">{drive.name || 'Unknown Drive'}</span>
                </div>
                <div className="space-y-1 text-sm text-gray-600">
                  <div>Mount Point: {drive.mount_point || 'N/A'}</div>
                  <div>Size: {drive.size_gb ? `${drive.size_gb.toFixed(2)} GB` : 'Unknown'}</div>
                  <div>Used: {drive.used_gb ? `${drive.used_gb.toFixed(2)} GB` : 'Unknown'}</div>
                  <div>Free: {drive.free_gb ? `${drive.free_gb.toFixed(2)} GB` : 'Unknown'}</div>
                  <div>Usage: {drive.usage_percent ? `${drive.usage_percent.toFixed(1)}%` : 'Unknown'}</div>
                  <div>File System: {drive.file_system || 'Unknown'}</div>
                  {drive.serial_number && <div>Serial: {drive.serial_number}</div>}
                  {drive.vendor && <div>Vendor: {drive.vendor}</div>}
                  {drive.model && <div>Model: {drive.model}</div>}
                  {drive.last_mounted && (
                    <div>Last Mounted: {new Date(drive.last_mounted).toLocaleString()}</div>
                  )}
                  {drive.is_removable !== undefined && (
                    <div className={`font-medium ${drive.is_removable ? 'text-green-600' : 'text-gray-600'}`}>
                      {drive.is_removable ? '✓ Removable' : 'Internal Drive'}
                    </div>
                  )}
                </div>
                {drive.files && drive.files.length > 0 && (
                  <div className="mt-3">
                    <div className="text-xs font-medium text-gray-700 mb-1">Recent Files:</div>
                    <div className="max-h-20 overflow-y-auto space-y-1">
                      {drive.files.slice(0, 5).map((file: any, fileIndex: number) => (
                        <div key={fileIndex} className="text-xs text-gray-500 bg-white p-1 rounded">
                          {file.name} ({file.size_mb ? `${file.size_mb.toFixed(2)} MB` : 'Unknown'})
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="col-span-full text-center text-gray-500 py-8">
              <HardDrive className="w-12 h-12 mx-auto text-gray-300 mb-2" />
              <p>No USB drives detected</p>
              <p className="text-xs mt-1">Connect a USB drive to see monitoring data</p>
            </div>
          )}
        </div>
        {usbDrives?.last_scan && (
          <div className="mt-4 text-xs text-gray-500 text-center">
            Last scanned: {new Date(usbDrives.last_scan).toLocaleString()}
          </div>
        )}
      </section>

      <footer className="mt-6 text-center text-gray-500 text-sm">
        <p>GhostLink Unified Dashboard Monitoring • {new Date().toLocaleString()}</p>
      </footer>
    </div>
  );
}
