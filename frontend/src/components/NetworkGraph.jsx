import React, { useState } from 'react';
import { Network, Shield, Cpu, Server, Lock, AlertTriangle, CheckCircle2, Activity, Radio, ArrowUpRight } from 'lucide-react';

export const NetworkGraph = () => {
  const [selectedNode, setSelectedNode] = useState(null);
  const [threatMode, setThreatMode] = useState(false);

  const nodes = [
    { id: 'client-1', name: 'Edge Client A', ip: '192.168.1.104', type: 'endpoint', status: 'trusted', x: 70, y: 70, flows: '142 pkt/s' },
    { id: 'client-2', name: 'Edge Client B', ip: '192.168.1.189', type: 'endpoint', status: threatMode ? 'threat' : 'trusted', x: 70, y: 210, flows: threatMode ? '4,890 pkt/s' : '98 pkt/s' },
    { id: 'gateway', name: 'Zero Trust Gateway', ip: '10.0.0.1', type: 'gateway', status: 'verified', x: 230, y: 140, flows: '6,120 pkt/s' },
    { id: 'lstm', name: 'LSTM Neural Classifier', ip: '10.0.0.50', type: 'ai', status: 'active', x: 390, y: 140, flows: '64-Unit Recurrent' },
    { id: 'policy', name: 'Enforcement Sentinel', ip: '10.0.0.99', type: 'policy', status: threatMode ? 'alert' : 'clean', x: 530, y: 70, flows: threatMode ? 'BLOCK RULE APPLIED' : 'Allow 99.8%' },
    { id: 'database', name: 'Secure Internal Core', ip: '172.16.0.12', type: 'core', status: 'secured', x: 530, y: 210, flows: 'Encrypted SHA-256' },
  ];

  const activeNodeData = nodes.find(n => n.id === selectedNode) || nodes[2];

  return (
    <div className="floating-surface rounded-2xl p-6 sm:p-8 space-y-6 relative overflow-hidden">
      
      {/* Background Spatial Grid & Radial Glow */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(30,96,213,0.08),transparent_70%)] pointer-events-none" />
      
      {/* Topology Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10 pb-4 border-b border-slate-100 dark:border-white/5">
        <div>
          <div className="flex items-center space-x-2">
            <span className="h-2 w-2 rounded-full bg-blue-500 animate-pulse" />
            <span className="text-[10px] font-mono uppercase tracking-wider text-blue-600 dark:text-blue-400 font-bold">
              LIVING NETWORK TOPOLOGY
            </span>
          </div>
          <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-slate-100 mt-1">
            Zero Trust Dynamic Traffic & Threat Map
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Click any node or toggle threat mode to inspect live packet routes and neural verification states.
          </p>
        </div>

        {/* Threat Mode Simulator Toggle */}
        <div className="flex items-center space-x-3 shrink-0">
          <button
            onClick={() => setThreatMode(!threatMode)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold flex items-center space-x-2 transition-all tactile-btn ${
              threatMode
                ? 'bg-red-500 text-white shadow-spatial-threat ring-2 ring-red-500/30'
                : 'micro-surface text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400'
            }`}
          >
            <AlertTriangle className="h-3.5 w-3.5" />
            <span>{threatMode ? '⚡ Threat Mode Active' : 'Simulate Intrusion'}</span>
          </button>
        </div>
      </div>

      {/* 3D SVG Topology Canvas */}
      <div className="relative z-10 bg-slate-50 dark:bg-[#090B0E]/80 border border-slate-200/80 dark:border-white/5 rounded-xl p-4 overflow-x-auto shadow-inner">
        <svg viewBox="0 0 620 280" className="w-full min-w-[580px] h-64 select-none">
          
          <defs>
            <linearGradient id="normalFlow" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#10B981" stopOpacity="0.8" />
            </linearGradient>
            <linearGradient id="threatFlow" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#EF4444" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#F59E0B" stopOpacity="0.6" />
            </linearGradient>
          </defs>

          {/* Connection Links */}
          <line x1="70" y1="70" x2="230" y2="140" stroke="#3B82F6" strokeWidth="2" strokeDasharray="4 4" className="opacity-60" />
          <line x1="70" y1="210" x2="230" y2="140" stroke={threatMode ? '#EF4444' : '#3B82F6'} strokeWidth={threatMode ? "3" : "2"} strokeDasharray={threatMode ? "none" : "4 4"} className={threatMode ? "opacity-100" : "opacity-60"} />
          <line x1="230" y1="140" x2="390" y2="140" stroke="url(#normalFlow)" strokeWidth="3" />
          <line x1="390" y1="140" x2="530" y2="70" stroke={threatMode ? '#EF4444' : '#10B981'} strokeWidth="2" strokeDasharray={threatMode ? "none" : "3 3"} />
          <line x1="390" y1="140" x2="530" y2="210" stroke="#10B981" strokeWidth="2" />

          {/* Animated Flow Packets */}
          <circle r="4" fill="#3B82F6">
            <animateMotion path="M 70 70 L 230 140" dur="2s" repeatCount="indefinite" />
          </circle>
          
          {threatMode ? (
            <circle r="5" fill="#EF4444">
              <animateMotion path="M 70 210 L 230 140" dur="1s" repeatCount="indefinite" />
            </circle>
          ) : (
            <circle r="4" fill="#3B82F6">
              <animateMotion path="M 70 210 L 230 140" dur="2.4s" repeatCount="indefinite" />
            </circle>
          )}

          <circle r="4" fill="#10B981">
            <animateMotion path="M 230 140 L 390 140" dur="1.5s" repeatCount="indefinite" />
          </circle>

          {/* Interactive Topology Nodes */}
          {nodes.map((node) => {
            const isSelected = selectedNode === node.id;
            const isThreat = node.status === 'threat' || (threatMode && node.id === 'policy');

            return (
              <g 
                key={node.id} 
                className="cursor-pointer transition-transform duration-200"
                onClick={() => setSelectedNode(node.id)}
                transform={`translate(${node.x}, ${node.y})`}
              >
                {/* Node Outer Ring / Radar */}
                <circle
                  r={isThreat ? 28 : 24}
                  fill={isThreat ? 'rgba(239, 68, 68, 0.15)' : 'rgba(59, 130, 246, 0.08)'}
                  stroke={isThreat ? '#EF4444' : isSelected ? '#3B82F6' : 'rgba(148, 163, 184, 0.4)'}
                  strokeWidth={isSelected || isThreat ? 2.5 : 1.5}
                />

                {/* Node Center Badge */}
                <circle
                  r="16"
                  fill={isThreat ? '#EF4444' : node.type === 'ai' ? '#10B981' : node.type === 'gateway' ? '#1E60D5' : '#0F172A'}
                  className="shadow-md"
                />

                {/* Label Text */}
                <text 
                  y="40" 
                  textAnchor="middle" 
                  className="text-[10px] font-mono font-bold fill-slate-800 dark:fill-slate-200"
                >
                  {node.name}
                </text>
                <text 
                  y="52" 
                  textAnchor="middle" 
                  className="text-[8px] font-mono fill-slate-400 dark:fill-slate-500"
                >
                  {node.ip}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Contextual Spatial Inspection HUD */}
      <div className="relative z-10 micro-surface rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 font-mono text-xs">
        <div className="flex items-center space-x-3">
          <div className={`h-9 w-9 rounded-lg flex items-center justify-center font-bold shrink-0 ${
            activeNodeData.status === 'threat' 
              ? 'bg-red-500/10 text-red-500 border border-red-500/30' 
              : 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/30'
          }`}>
            {activeNodeData.type === 'ai' ? <Cpu className="h-5 w-5" /> : activeNodeData.type === 'gateway' ? <Shield className="h-5 w-5" /> : <Server className="h-5 w-5" />}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-900 dark:text-slate-100">{activeNodeData.name}</span>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400">
                {activeNodeData.ip}
              </span>
            </div>
            <span className="text-[11px] text-slate-500 dark:text-slate-400 block mt-0.5">
              Live Telemetry: {activeNodeData.flows}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          <span className={`px-2.5 py-1 rounded-lg text-[10px] font-bold border ${
            activeNodeData.status === 'threat'
              ? 'bg-red-500/10 text-red-500 border-red-500/30 animate-pulse'
              : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
          }`}>
            {activeNodeData.status === 'threat' ? '⚠ MALICIOUS FLOW ISOLATED' : '✓ ZERO TRUST VERIFIED'}
          </span>
        </div>
      </div>

    </div>
  );
};

