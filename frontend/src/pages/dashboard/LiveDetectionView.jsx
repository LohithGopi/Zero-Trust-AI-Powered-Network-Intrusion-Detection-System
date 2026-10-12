import React, { useState, useEffect, useRef } from 'react';
import { 
  Radio, Play, Square, RefreshCw, Download, 
  ShieldAlert, ShieldCheck, Activity, AlertTriangle, 
  Server, Wifi, Filter, Search, ArrowUpRight, Cpu, 
  HelpCircle, CheckCircle2, Info, Trash2
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const LiveDetectionView = ({ onNavigate }) => {
  const { resetModelStatus } = useAuth();
  const [interfaces, setInterfaces] = useState([]);
  const [selectedInterface, setSelectedInterface] = useState('');
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [npcapStatus, setNpcapStatus] = useState({ available: false, message: '' });
  
  const [isRunning, setIsRunning] = useState(false);
  const [stats, setStats] = useState({
    total_flows: 0,
    normal_flows: 0,
    attack_flows: 0,
    high_risk: 0,
    medium_risk: 0,
    low_risk: 0,
    total_packets: 0,
    total_bytes: 0,
    flows_per_sec: 0,
    packets_per_sec: 0,
    kb_per_sec: 0
  });
  
  const [detections, setDetections] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [activeTab, setActiveTab] = useState('all'); // 'all' or 'alerts'
  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState('ALL');
  
  const [loading, setLoading] = useState(false);
  const [actionMessage, setActionMessage] = useState(null);
  const pollTimerRef = useRef(null);

  // 1. Initial Load: Interfaces and Models
  useEffect(() => {
    fetchInterfaces();
    fetchModels();
    fetchTrafficFeed();

    pollTimerRef.current = setInterval(() => {
      fetchTrafficFeed();
    }, 2000);

    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    };
  }, []);

  const fetchInterfaces = async () => {
    try {
      const res = await fetch('/api/live-detection/interfaces');
      if (res.ok) {
        const data = await res.json();
        setInterfaces(data.interfaces || []);
        setNpcapStatus(data.npcap || { available: false, message: '' });
        if (data.interfaces && data.interfaces.length > 0) {
          // Select first active routable interface (prefer Wi-Fi/Ethernet with real IP)
          const activeRoutable = data.interfaces.find(i => 
            !i.is_loopback && 
            i.ip !== 'No IP' && 
            !i.ip.startsWith('169.254.')
          );
          const fallbackNonLoopback = data.interfaces.find(i => !i.is_loopback && i.ip !== 'No IP');
          const chosen = activeRoutable || fallbackNonLoopback || data.interfaces[0];
          setSelectedInterface(chosen.id);
        }
      }
    } catch (e) {
      console.error('Error fetching interfaces:', e);
    }
  };

  const fetchModels = async () => {
    try {
      const res = await fetch('/api/live-detection/models');
      if (res.ok) {
        const data = await res.json();
        const availableModels = data.models || [];
        setModels(availableModels);
        if (availableModels.length > 0) {
          const defModel = data.active_model || availableModels.find(m => m.is_default) || availableModels[0];
          setSelectedModel(defModel);
        } else {
          setSelectedModel(null);
        }
      }
    } catch (e) {
      console.error('Error fetching models:', e);
    }
  };

  const fetchTrafficFeed = async () => {
    try {
      const res = await fetch('/api/live-detection/traffic?limit=60');
      if (res.ok) {
        const data = await res.json();
        setDetections(data.detections || []);
        setAlerts(data.alerts || []);
        if (data.stats) setStats(data.stats);
        if (typeof data.is_running === 'boolean') setIsRunning(data.is_running);
      }
    } catch (e) {
      console.debug('Traffic feed poll error:', e);
    }
  };

  // 2. Control Handlers
  const handleStartCapture = async () => {
    if (!selectedModel) {
      setActionMessage({
        type: 'error',
        text: 'No detection model trained. Please navigate to Model Training and train a model based on your dataset first.'
      });
      return;
    }

    setLoading(true);
    setActionMessage(null);
    try {
      const payload = {
        interface_id: selectedInterface,
        model_path: selectedModel?.model_path,
        scaler_path: selectedModel?.scaler_path,
        encoder_path: selectedModel?.encoder_path,
        mode: 'realtime'
      };
      const res = await fetch('/api/live-detection/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setIsRunning(true);
        setActionMessage({ 
          type: 'success', 
          text: data.message || 'Real-time live packet detection started.' 
        });
      } else {
        setActionMessage({ 
          type: 'error', 
          text: data.error || 'Failed to start live capture.'
        });
      }
    } catch (e) {
      setActionMessage({ type: 'error', text: `Network error: ${e.message}` });
    } finally {
      setLoading(false);
      fetchTrafficFeed();
    }
  };

  const handleStopCapture = async () => {
    setLoading(true);
    setActionMessage(null);
    try {
      const res = await fetch('/api/live-detection/stop', { method: 'POST' });
      const data = await res.json();
      if (res.ok) {
        setIsRunning(false);
        setActionMessage({ type: 'info', text: 'Live packet capture stopped.' });
      }
    } catch (e) {
      setActionMessage({ type: 'error', text: `Stop error: ${e.message}` });
    } finally {
      setLoading(false);
      fetchTrafficFeed();
    }
  };

  const handleResetCounters = async () => {
    try {
      await fetch('/api/live-detection/reset', { method: 'POST' });
      fetchTrafficFeed();
    } catch (e) {
      console.error('Reset error:', e);
    }
  };

  const handleExportCSV = () => {
    window.open('/api/live-detection/export', '_blank');
  };

  const handleRemoveModel = async () => {
    setLoading(true);
    setActionMessage(null);
    try {
      const token = localStorage.getItem('nids_token');
      const res = await fetch('/api/live-detection/models/remove', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ model_id: 'all' })
      });
      const rawText = await res.text();
      let data = null;
      try {
        data = JSON.parse(rawText);
      } catch {
        data = null;
      }

      setModels([]);
      setSelectedModel(null);
      if (resetModelStatus) resetModelStatus();
      setIsRunning(false);
      setActionMessage({
        type: 'info',
        text: (data && data.message) || 'Active detection model removed. Please train a model on your dataset to resume detection.'
      });
    } catch (e) {
      setModels([]);
      setSelectedModel(null);
      if (resetModelStatus) resetModelStatus();
      setActionMessage({
        type: 'info',
        text: 'Active detection model unloaded.'
      });
    } finally {
      setLoading(false);
    }
  };

  // Filtered Detections
  const filteredDetections = detections.filter(d => {
    const matchesSearch = searchTerm === '' || 
      d.source_ip.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.destination_ip.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.prediction.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.protocol.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRisk = riskFilter === 'ALL' || d.risk_level === riskFilter;
    return matchesSearch && matchesRisk;
  });

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* 1. Header Banner */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-3 mb-1">
            <div className="h-9 w-9 rounded-xl bg-blue-600 text-white flex items-center justify-center shadow-xs">
              <Radio className="h-5 w-5 animate-pulse" />
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              Live Network Traffic Detection
            </h1>
            <span className={`text-[11px] font-mono font-bold px-2.5 py-0.5 rounded-full border ${
              isRunning 
                ? 'bg-emerald-50 text-emerald-700 border-emerald-300 animate-pulse'
                : 'bg-slate-100 text-slate-600 border-slate-300'
            }`}>
              ● {isRunning ? 'REAL-TIME MONITORING ACTIVE' : 'STOPPED'}
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500">
            Real-time passive packet inspection and flow classification powered strictly by your dataset-trained AI model.
          </p>
        </div>

        {/* Top Action Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          {isRunning ? (
            <button
              onClick={handleStopCapture}
              disabled={loading}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-rose-600 hover:bg-rose-700 shadow-sm transition-all cursor-pointer"
            >
              <Square className="h-3.5 w-3.5 fill-current" />
              <span>Stop Monitoring</span>
            </button>
          ) : (
            <button
              onClick={() => handleStartCapture()}
              disabled={loading}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm transition-all cursor-pointer"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              <span>Start Live Detection</span>
            </button>
          )}

          <button
            onClick={handleExportCSV}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-slate-700 bg-slate-100 border border-slate-300 hover:bg-slate-200 shadow-xs transition-all cursor-pointer"
          >
            <Download className="h-3.5 w-3.5" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Action Notification Alert */}
      {actionMessage && (
        <div className={`p-4 rounded-xl border text-xs font-medium ${
          actionMessage.type === 'error'
            ? 'bg-rose-50 text-rose-800 border-rose-200'
            : actionMessage.type === 'success'
            ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
            : 'bg-blue-50 text-blue-800 border-blue-200'
        }`}>
          <div className="flex items-start justify-between">
            <div className="space-y-1.5 flex-1 pr-4">
              <p className="font-semibold">{actionMessage.text}</p>
            </div>
            <button onClick={() => setActionMessage(null)} className="font-bold underline cursor-pointer">Dismiss</button>
          </div>
        </div>
      )}

      {/* Notice if no detection model is trained yet */}
      {!selectedModel && (
        <div className="bg-blue-50/90 rounded-2xl p-4.5 border border-blue-200 text-blue-950 flex items-start space-x-3.5 shadow-xs">
          <Info className="h-5 w-5 text-blue-600 shrink-0 mt-0.5" />
          <div className="text-xs space-y-1.5 flex-1">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="font-bold text-sm text-blue-900">No Dataset-Based Detection Model Trained Yet</p>
              {onNavigate && (
                <button
                  onClick={() => onNavigate('training')}
                  className="px-3 py-1 rounded-lg text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white shadow-xs cursor-pointer transition-all flex items-center space-x-1"
                >
                  <span>Train Model on Dataset</span>
                  <ArrowUpRight className="h-3.5 w-3.5" />
                </button>
              )}
            </div>
            <p className="text-blue-800 leading-relaxed">
              No trained detection model is currently loaded. To begin real-time packet detection and attack classification, please navigate to <strong>Model Training</strong> and train a neural network model on your selected dataset.
            </p>
          </div>
        </div>
      )}

      {/* 2. Control & Configuration HUD */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Network Adapter Selector */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm space-y-3">
          <div className="flex items-center space-x-2">
            <Wifi className="h-4 w-4 text-blue-600" />
            <h2 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Network Interface Adapter
            </h2>
          </div>
          <div>
            <select
              value={selectedInterface}
              onChange={(e) => setSelectedInterface(e.target.value)}
              disabled={isRunning}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-60"
            >
              {interfaces.map((iface) => (
                <option key={iface.id} value={iface.id}>
                  {iface.name} — {iface.ip} {iface.is_loopback ? '(Loopback)' : ''}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-center justify-between text-[11px] text-slate-500">
            <span>Discovered: {interfaces.length} adapters</span>
            <span className="font-mono text-emerald-700 font-semibold">Real-Time Packet Capture</span>
          </div>
        </div>

        {/* Dataset-Trained AI Model Card */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm space-y-3">
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-center space-x-2">
              <Cpu className={`h-4 w-4 ${selectedModel ? 'text-purple-600' : 'text-slate-400'}`} />
              <h2 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Dataset-Trained Detection Model
              </h2>
            </div>
            <div className="flex items-center space-x-2">
              {selectedModel ? (
                <>
                  <span className="font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-[10px]">
                    ✓ Dataset Model Active
                  </span>
                  <button
                    onClick={() => handleRemoveModel()}
                    disabled={loading || isRunning}
                    title="Remove this trained detection model"
                    className="inline-flex items-center space-x-1 px-2 py-0.5 rounded border border-rose-200 bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold text-[10px] transition-all cursor-pointer disabled:opacity-50"
                  >
                    <Trash2 className="h-3 w-3" />
                    <span>Remove Model</span>
                  </button>
                </>
              ) : (
                <span className="font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200 text-[10px]">
                  No Model Trained
                </span>
              )}
            </div>
          </div>

          <div>
            {selectedModel ? (
              <div className="w-full bg-slate-50 border border-purple-200 rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-800 flex items-center justify-between">
                <span>{selectedModel.name}</span>
                <span className="text-[10px] font-mono font-bold text-purple-700 bg-purple-100 px-2 py-0.5 rounded">
                  {selectedModel.dataset_type} • {selectedModel.features} Features
                </span>
              </div>
            ) : (
              <div className="w-full bg-slate-50 border border-amber-300/80 rounded-xl px-3 py-2 text-xs text-amber-900 flex items-center justify-between">
                <span className="italic text-slate-600">No dataset-trained model available</span>
                <span className="text-[10px] font-bold text-amber-700 uppercase tracking-wider bg-amber-100/80 px-1.5 py-0.5 rounded">
                  Untrained
                </span>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between text-[11px]">
            <span className="text-slate-500">
              Input Vector: {selectedModel ? `${selectedModel.features} features (${selectedModel.dataset_type})` : 'None (No active model)'}
            </span>
            {selectedModel ? (
              <span className="text-slate-500 font-mono text-[10px]">
                Trained on {selectedModel.dataset_name || selectedModel.dataset_type}
              </span>
            ) : (
              onNavigate && (
                <button
                  onClick={() => onNavigate('training')}
                  className="font-bold text-blue-600 hover:text-blue-800 underline text-[11px] cursor-pointer"
                >
                  Train Model on Dataset →
                </button>
              )
            )}
          </div>
        </div>
      </div>

      {/* 3. Live Metrics Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs">
          <p className="text-[11px] font-bold text-slate-500 uppercase">Monitored Flows</p>
          <p className="text-xl font-black text-slate-900 mt-1">{stats.total_flows.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 mt-0.5">{stats.flows_per_sec} flows/sec</p>
        </div>

        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs">
          <p className="text-[11px] font-bold text-emerald-600 uppercase">Normal Traffic</p>
          <p className="text-xl font-black text-emerald-600 mt-1">{stats.normal_flows.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 mt-0.5">
            {stats.total_flows > 0 ? `${((stats.normal_flows / stats.total_flows) * 100).toFixed(1)}%` : '0%'}
          </p>
        </div>

        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs">
          <p className="text-[11px] font-bold text-rose-600 uppercase">Threat Detections</p>
          <p className="text-xl font-black text-rose-600 mt-1">{stats.attack_flows.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 mt-0.5">
            {stats.total_flows > 0 ? `${((stats.attack_flows / stats.total_flows) * 100).toFixed(1)}%` : '0%'}
          </p>
        </div>

        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs">
          <p className="text-[11px] font-bold text-red-700 uppercase">High Risk Alerts</p>
          <p className="text-xl font-black text-red-700 mt-1">{stats.high_risk.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 mt-0.5">Conf ≥ 85%</p>
        </div>

        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs">
          <p className="text-[11px] font-bold text-slate-500 uppercase">Packet Volume</p>
          <p className="text-xl font-black text-slate-900 mt-1">{stats.total_packets.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 mt-0.5">{stats.packets_per_sec} pkts/sec</p>
        </div>

        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs">
          <p className="text-[11px] font-bold text-slate-500 uppercase">Throughput</p>
          <p className="text-xl font-black text-slate-900 mt-1">{stats.kb_per_sec} KB/s</p>
          <button 
            onClick={handleResetCounters} 
            className="text-[10px] text-blue-600 hover:underline mt-0.5"
          >
            Reset Stats
          </button>
        </div>
      </div>

      {/* 4. Traffic Feed Controls & Table */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        {/* Table Header Controls */}
        <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3">
          {/* Tab buttons */}
          <div className="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-xl">
            <button
              onClick={() => setActiveTab('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'all'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All Monitored Flows ({detections.length})
            </button>
            <button
              onClick={() => setActiveTab('alerts')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center space-x-1 ${
                activeTab === 'alerts'
                  ? 'bg-rose-600 text-white shadow-xs'
                  : 'text-rose-600 hover:bg-rose-50'
              }`}
            >
              <span>Security Alerts</span>
              {alerts.length > 0 && (
                <span className="ml-1 bg-white text-rose-600 text-[10px] px-1.5 py-0.2 rounded-full font-black">
                  {alerts.length}
                </span>
              )}
            </button>
          </div>

          {/* Search & Risk Filters */}
          <div className="flex items-center space-x-2 w-full sm:w-auto">
            <div className="relative flex-1 sm:w-48">
              <Search className="h-3.5 w-3.5 text-slate-400 absolute left-2.5 top-2.5" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search IP, type, proto..."
                className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-medium text-slate-700 focus:outline-none"
            >
              <option value="ALL">All Risk Levels</option>
              <option value="HIGH">High Risk</option>
              <option value="MEDIUM">Medium Risk</option>
              <option value="LOW">Low Risk</option>
            </select>
          </div>
        </div>

        {/* Detections Table / Alerts Feed */}
        {activeTab === 'all' ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-bold uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="py-2.5 px-3">Timestamp</th>
                  <th className="py-2.5 px-3">Source Endpoint</th>
                  <th className="py-2.5 px-3">Destination Endpoint</th>
                  <th className="py-2.5 px-3">Proto</th>
                  <th className="py-2.5 px-3">Duration</th>
                  <th className="py-2.5 px-3">Packets / Bytes</th>
                  <th className="py-2.5 px-3">Classification</th>
                  <th className="py-2.5 px-3">Confidence</th>
                  <th className="py-2.5 px-3 text-right">Risk Level</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {filteredDetections.length === 0 ? (
                  <tr>
                    <td colSpan="9" className="py-8 text-center text-slate-400 font-sans">
                      No network flows captured yet. Click <strong>Start Live Detection</strong> to begin real-time packet monitoring.
                    </td>
                  </tr>
                ) : (
                  filteredDetections.map((row, idx) => {
                    const isNormal = row.prediction === 'Normal' || row.prediction === 'BENIGN';
                    return (
                      <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-2 px-3 text-slate-500 text-[11px] whitespace-nowrap">
                          {row.timestamp.split(' ')[1] || row.timestamp}
                        </td>
                        <td className="py-2 px-3 text-slate-800">
                          {row.source_ip}:{row.source_port}
                        </td>
                        <td className="py-2 px-3 text-slate-800">
                          {row.destination_ip}:{row.destination_port}
                        </td>
                        <td className="py-2 px-3">
                          <span className="px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 text-[10px] font-bold font-sans">
                            {row.protocol}
                          </span>
                        </td>
                        <td className="py-2 px-3 text-slate-600 text-[11px]">
                          {row.flow_duration}s
                        </td>
                        <td className="py-2 px-3 text-slate-600 text-[11px]">
                          {row.packet_count} pkts / {(row.bytes / 1024).toFixed(1)} KB
                        </td>
                        <td className="py-2 px-3">
                          <span className={`px-2 py-0.5 rounded text-[11px] font-bold font-sans ${
                            isNormal 
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
                              : 'bg-rose-50 text-rose-700 border border-rose-300 font-black'
                          }`}>
                            {row.prediction}
                          </span>
                        </td>
                        <td className="py-2 px-3 text-slate-700 font-sans text-[11px]">
                          {(row.confidence * 100).toFixed(1)}%
                        </td>
                        <td className="py-2 px-3 text-right">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-black font-sans ${
                            row.risk_level === 'HIGH'
                              ? 'bg-red-600 text-white'
                              : row.risk_level === 'MEDIUM'
                              ? 'bg-amber-500 text-slate-950 font-bold'
                              : 'bg-slate-100 text-slate-600'
                          }`}>
                            {row.risk_level}
                          </span>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        ) : (
          /* Alerts Stream View */
          <div className="p-4 space-y-3">
            {alerts.length === 0 ? (
              <div className="py-12 text-center text-slate-400">
                <CheckCircle2 className="h-8 w-8 text-emerald-500 mx-auto mb-2" />
                <p className="font-bold text-slate-700 text-sm">Zero Active Threat Alerts</p>
                <p className="text-xs text-slate-400 mt-1">No anomalous attack flows have been identified.</p>
              </div>
            ) : (
              alerts.map((alert, idx) => (
                <div 
                  key={idx}
                  className="bg-rose-50/60 rounded-xl p-4 border border-rose-200 flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-xs"
                >
                  <div className="flex items-start space-x-3">
                    <div className="h-8 w-8 rounded-lg bg-rose-600 text-white flex items-center justify-center shrink-0 mt-0.5">
                      <ShieldAlert className="h-4 w-4" />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-black text-sm text-rose-950">
                          {alert.prediction} Threat Detected
                        </span>
                        <span className="text-[10px] font-mono font-bold bg-rose-600 text-white px-2 py-0.5 rounded">
                          {alert.risk_level} RISK
                        </span>
                      </div>
                      <p className="text-xs text-rose-900 mt-1 font-mono">
                        Source: {alert.source_ip}:{alert.source_port} ➔ Target: {alert.destination_ip}:{alert.destination_port} ({alert.protocol})
                      </p>
                      <p className="text-[11px] text-rose-700 mt-0.5">
                        Duration: {alert.flow_duration}s | Packets: {alert.packet_count} | Bytes: {alert.bytes}
                      </p>
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <p className="text-xs font-bold text-rose-900">
                      Confidence: {(alert.confidence * 100).toFixed(1)}%
                    </p>
                    <p className="text-[10px] font-mono text-slate-500 mt-0.5">
                      {alert.timestamp}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>

      {/* 5. Educational / Statistical Disclaimer Footer */}
      <div className="bg-slate-100/80 rounded-xl p-3 border border-slate-200 text-slate-600 text-[11px] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <HelpCircle className="h-4 w-4 text-slate-400 shrink-0" />
          <span>
            <strong>Zero Trust Principle:</strong> Detection results are statistical machine learning classifications and not proof of compromise. Every flagged flow should be audited alongside host and endpoint logs.
          </span>
        </div>
        <span className="font-mono text-slate-400 shrink-0 hidden md:inline-block">
          Passive Packet Capture Module v2.0
        </span>
      </div>

    </div>
  );
};
