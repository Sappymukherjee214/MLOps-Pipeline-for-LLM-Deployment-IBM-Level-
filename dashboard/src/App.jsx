import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Activity, 
  AlertTriangle, 
  BarChart3, 
  Clock, 
  Cpu, 
  Database, 
  MessageSquare, 
  Server, 
  ShieldCheck, 
  Terminal 
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  AreaChart, 
  Area,
  BarChart,
  Bar
} from 'recharts';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const App = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [prompt, setPrompt] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [health, setHealth] = useState(null);
  const [drift, setDrift] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [logs, setLogs] = useState([]);

  // Mock data for initial empty state
  const [chartData, setChartData] = useState([
    { time: '10:00', latency: 120, throughput: 15 },
    { time: '10:05', latency: 135, throughput: 18 },
    { time: '10:10', latency: 110, throughput: 22 },
    { time: '10:15', latency: 150, throughput: 20 },
    { time: '10:20', latency: 140, throughput: 25 },
    { time: '10:25', latency: 125, throughput: 21 },
  ]);

  useEffect(() => {
    fetchHealth();
    fetchDrift();
    fetchLogs();
    fetchPerformance();
    fetchPerformanceHistory();
    fetchDriftHistory();
    const interval = setInterval(() => {
      fetchHealth();
      fetchDrift();
      fetchLogs();
      fetchPerformance();
      fetchPerformanceHistory();
      fetchDriftHistory();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchHealth = async () => {
    try {
      const res = await axios.get('http://localhost:8000/health');
      setHealth(res.data);
    } catch (e) {
      console.error("Health fetch failed", e);
    }
  };

  const fetchDrift = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/drift`);
      setDrift(res.data);
    } catch (e) {
      console.error("Drift fetch failed", e);
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/logs`);
      setLogs(res.data.logs);
    } catch (e) {
      console.error("Logs fetch failed", e);
    }
  };

  const fetchPerformance = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/performance/summary`);
      setMetrics(res.data);
    } catch (e) {
      console.error("Performance fetch failed", e);
    }
  };

  const fetchPerformanceHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/performance/history`);
      if (res.data.length > 0) {
        setChartData(res.data.map(d => ({
          time: d.display_time,
          latency: d.avg_latency_ms,
          throughput: d.throughput_rpm
        })));
      }
    } catch (e) {
      console.error("Performance history fetch failed", e);
    }
  };

  const fetchDriftHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/drift/history`);
      // Optional: Add another state for drift chart if needed
    } catch (e) {
      console.error("Drift history fetch failed", e);
    }
  };

  const handlePredict = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const start = Date.now();
      const res = await axios.post(`${API_BASE_URL}/predict`, { prompt });
      const duration = Date.now() - start;
      setPrediction(res.data);
      
      // Update local chart data simulation
      setChartData(prev => [
        ...prev.slice(-10), 
        { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), latency: res.data.latency_ms, throughput: prev[prev.length-1].throughput + 1 }
      ]);
    } catch (e) {
      console.error("Prediction failed", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-64 bg-slate-900 border-r border-slate-800 p-6 flex flex-col gap-8">
        <div className="flex items-center gap-3 px-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Cpu size={20} className="text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight text-white">MLOps Core</h1>
        </div>

        <nav className="flex flex-col gap-2">
          <button 
            onClick={() => setActiveTab('overview')}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'overview' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}
          >
            <Server size={18} />
            <span className="font-medium">Overview</span>
          </button>
          <button 
            onClick={() => setActiveTab('playground')}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'playground' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}
          >
            <MessageSquare size={18} />
            <span className="font-medium">Inference</span>
          </button>
          <button 
            onClick={() => setActiveTab('monitoring')}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'monitoring' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}
          >
            <Activity size={18} />
            <span className="font-medium">Analytics</span>
          </button>
          <button 
            onClick={() => setActiveTab('logs')}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'logs' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}
          >
            <Terminal size={18} />
            <span className="font-medium">Log Viewer</span>
          </button>
        </nav>

        <div className="mt-auto p-4 bg-slate-800/50 rounded-2xl border border-slate-700/50">
          <div className="flex items-center gap-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${health?.status === 'healthy' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`}></div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">System Status</span>
          </div>
          <p className="text-sm text-slate-300 font-medium">{health?.status === 'healthy' ? 'Operational' : 'Issues Detected'}</p>
        </div>
      </div>

      {/* Main Content */}
      <main className="ml-64 p-8 max-w-7xl">
        <header className="mb-10 flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">
              {activeTab === 'overview' && 'System Overview'}
              {activeTab === 'playground' && 'Inference Playground'}
              {activeTab === 'monitoring' && 'Monitoring & Analytics'}
              {activeTab === 'logs' && 'Production Logs'}
            </h2>
            <p className="text-slate-400">Monitoring real-time performance and drift for Gemini-1.5-Flash</p>
          </div>
          <div className="text-right">
            <div className="text-xs text-slate-500 uppercase tracking-widest font-bold mb-1">Local Time</div>
            <div className="text-lg font-mono text-blue-400">{new Date().toLocaleTimeString()}</div>
          </div>
        </header>

        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-blue-500/10 rounded-2xl">
                  <Clock className="text-blue-500" size={24} />
                </div>
                <span className="text-emerald-500 text-sm font-bold">Live</span>
              </div>
              <h3 className="text-slate-400 text-sm font-semibold mb-1">Avg Latency</h3>
              <p className="text-2xl font-bold text-white">{metrics?.avg_latency_ms || '0.0'}<span className="text-sm font-normal text-slate-500 ml-1">ms</span></p>
            </div>
            
            <div className="bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-amber-500/10 rounded-2xl">
                  <Activity className="text-amber-500" size={24} />
                </div>
                <span className={`text-sm font-bold ${metrics?.status === 'operational' ? 'text-emerald-500' : 'text-rose-500'}`}>
                  {metrics?.status || 'Unknown'}
                </span>
              </div>
              <h3 className="text-slate-400 text-sm font-semibold mb-1">Throughput</h3>
              <p className="text-2xl font-bold text-white">{metrics?.throughput_rpm || '0'}<span className="text-sm font-normal text-slate-500 ml-1">req/min</span></p>
            </div>

            <div className="bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-emerald-500/10 rounded-2xl">
                  <ShieldCheck className="text-emerald-500" size={24} />
                </div>
                <span className="text-emerald-500 text-sm font-bold">{metrics?.error_rate || '0%'} Err</span>
              </div>
              <h3 className="text-slate-400 text-sm font-semibold mb-1">System Health</h3>
              <p className="text-2xl font-bold text-white">{health?.resources?.cpu || '0%'}<span className="text-sm font-normal text-slate-500 ml-1">CPU</span></p>
            </div>

            <div className={`bg-slate-900 p-6 rounded-3xl border ${drift?.drift_detected ? 'border-rose-500/50 shadow-rose-900/10' : 'border-slate-800'} shadow-xl transition-all`}>
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 ${drift?.drift_detected ? 'bg-rose-500/10' : 'bg-slate-500/10'} rounded-2xl`}>
                  <AlertTriangle className={drift?.drift_detected ? 'text-rose-500' : 'text-slate-500'} size={24} />
                </div>
                <span className={`text-sm font-bold ${drift?.drift_detected ? 'text-rose-500' : 'text-slate-500'}`}>
                  {drift?.drift_detected ? 'Alert' : 'Stable'}
                </span>
              </div>
              <h3 className="text-slate-400 text-sm font-semibold mb-1">Data Drift</h3>
              <p className="text-2xl font-bold text-white">{drift?.ks_statistic?.toFixed(4) || '0.0000'} <span className="text-xs font-normal text-slate-600">Stat</span></p>
            </div>
          </div>
        )}

        {activeTab === 'playground' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-slate-900 p-8 rounded-3xl border border-slate-800 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-blue-500/20 rounded-xl">
                  <MessageSquare className="text-blue-400" size={20} />
                </div>
                <h3 className="text-xl font-bold text-white">Input Prompt</h3>
              </div>
              <textarea 
                className="w-full h-64 bg-slate-950 border border-slate-800 rounded-2xl p-4 text-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none resize-none"
                placeholder="Enter your prompt here..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
              <button 
                onClick={handlePredict}
                disabled={loading || !prompt}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-500 py-4 rounded-2xl font-bold transition-all flex items-center justify-center gap-2"
              >
                {loading ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> : <Activity size={18} />}
                {loading ? 'Processing...' : 'Generate Response'}
              </button>
            </div>

            <div className="bg-slate-900 p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-emerald-500/20 rounded-xl">
                    <Database className="text-emerald-400" size={20} />
                  </div>
                  <h3 className="text-xl font-bold text-white">Model Response</h3>
                </div>
                {prediction && (
                  <div className="px-3 py-1 bg-slate-800 rounded-full text-xs font-mono text-slate-400">
                    {prediction.latency_ms.toFixed(0)}ms
                  </div>
                )}
              </div>
              <div className="flex-1 bg-slate-950 border border-slate-800 rounded-2xl p-6 overflow-y-auto min-h-[16rem]">
                {prediction ? (
                  <div className="prose prose-invert max-w-none">
                    <p className="whitespace-pre-wrap leading-relaxed">{prediction.response}</p>
                  </div>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center text-slate-600 gap-4">
                    <MessageSquare size={48} className="opacity-20" />
                    <p>Response will appear here after inference</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'monitoring' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-slate-900 p-8 rounded-3xl border border-slate-800 shadow-xl">
              <h3 className="text-xl font-bold text-white mb-6">Latency Trend (ms)</h3>
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData}>
                    <defs>
                      <linearGradient id="colorLatency" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis dataKey="time" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px' }}
                      itemStyle={{ color: '#3b82f6' }}
                    />
                    <Area type="monotone" dataKey="latency" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorLatency)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-slate-900 p-8 rounded-3xl border border-slate-800 shadow-xl">
              <h3 className="text-xl font-bold text-white mb-6">Throughput (RPM)</h3>
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis dataKey="time" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px' }}
                    />
                    <Bar dataKey="throughput" fill="#6366f1" radius={[6, 6, 0, 0]} barSize={20} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'logs' && (
          <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl overflow-hidden">
             <div className="p-6 border-b border-slate-800 bg-slate-900/50 flex justify-between items-center">
                <div className="flex items-center gap-3">
                  <Terminal size={20} className="text-blue-400" />
                  <h3 className="font-bold text-white uppercase tracking-wider text-sm">System Runtime Logs</h3>
                </div>
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-slate-700"></div>
                  <div className="w-3 h-3 rounded-full bg-slate-700"></div>
                  <div className="w-3 h-3 rounded-full bg-slate-700"></div>
                </div>
             </div>
             <div className="p-0 max-h-[600px] overflow-y-auto bg-slate-950 font-mono text-sm leading-relaxed p-6">
                {logs.length > 0 ? (
                  logs.map((log, i) => (
                    <div key={i} className="mb-2 last:mb-0 border-l border-slate-800 pl-4 py-1 hover:bg-slate-900/50 transition-colors">
                      <span className="text-slate-600 mr-3">[{i+1}]</span>
                      <span className={`${log.includes('ERROR') ? 'text-rose-400' : log.includes('WARNING') ? 'text-amber-400' : 'text-slate-400'}`}>
                        {log}
                      </span>
                    </div>
                  ))
                ) : (
                  <div className="text-slate-600 italic">Reading stream... No logs yet.</div>
                )}
             </div>
          </div>
        )}
      </main>

      {/* Background decoration */}
      <div className="fixed -bottom-48 -right-48 w-96 h-96 bg-blue-600/10 blur-[128px] pointer-events-none rounded-full"></div>
      <div className="fixed -top-48 -left-48 w-96 h-96 bg-indigo-600/10 blur-[128px] pointer-events-none rounded-full"></div>
    </div>
  );
}

export default App;
