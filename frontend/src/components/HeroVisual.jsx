import React from 'react';
import { Shield, Cpu, Lock, Activity, Radio, CheckCircle2, AlertOctagon, Terminal } from 'lucide-react';

export const HeroVisual = () => {
  return (
    <div className="relative w-full rounded-2xl floating-surface p-6 sm:p-8 overflow-hidden">
      
      {/* Background Subtle Depth Atmosphere */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_20%,rgba(30,96,213,0.1),transparent_60%)] pointer-events-none" />
      
      {/* Top Telemetry Header Rail */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-white/5 mb-6 text-xs font-mono">
        <div className="flex items-center space-x-2">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-slate-600 dark:text-slate-400 font-bold">STATE: REAL-TIME CONTINUOUS INSPECTION</span>
        </div>
        <div className="text-[10px] text-blue-600 dark:text-blue-400 font-bold px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800">
          LSTM RECURRENT INFERENCE
        </div>
      </div>

      {/* Layered Visual Composition */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs mb-6">
        
        {/* Layer 1: Ingress & Verification */}
        <div className="micro-surface rounded-xl p-4 space-y-3 relative group">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-bold">STAGE 01</span>
            <Radio className="h-4 w-4 text-blue-500 animate-pulse" />
          </div>
          <div>
            <div className="font-bold text-slate-900 dark:text-slate-100 font-sans">Network Ingress</div>
            <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">TCP/UDP Flow Stream</div>
          </div>
          <div className="p-2 rounded bg-slate-100 dark:bg-white/5 text-[10px] text-slate-600 dark:text-slate-400">
            Rate: <strong>1,420 pkts/s</strong>
          </div>
        </div>

        {/* Layer 2: Zero Trust Policy Gateway */}
        <div className="micro-surface rounded-xl p-4 space-y-3 border-blue-500/30 bg-blue-50/20 dark:bg-blue-950/20">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-blue-600 dark:text-blue-400 uppercase font-bold">STAGE 02</span>
            <Shield className="h-4 w-4 text-blue-600 dark:text-blue-400" />
          </div>
          <div>
            <div className="font-bold text-slate-900 dark:text-slate-100 font-sans">Zero Trust Gateway</div>
            <div className="text-[11px] text-blue-600 dark:text-blue-400 mt-0.5">JWT HMAC-SHA256</div>
          </div>
          <div className="p-2 rounded bg-blue-100/60 dark:bg-blue-900/30 text-[10px] text-blue-800 dark:text-blue-300 font-bold">
            Status: <strong>Never Trust, Verify</strong>
          </div>
        </div>

        {/* Layer 3: LSTM AI Classification */}
        <div className="micro-surface rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-emerald-600 dark:text-emerald-400 uppercase font-bold">STAGE 03</span>
            <Cpu className="h-4 w-4 text-emerald-500" />
          </div>
          <div>
            <div className="font-bold text-slate-900 dark:text-slate-100 font-sans">LSTM Intelligence</div>
            <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-0.5">64-Unit Recurrent Model</div>
          </div>
          <div className="p-2 rounded bg-emerald-50 dark:bg-emerald-950/40 text-[10px] text-emerald-700 dark:text-emerald-300 font-bold">
            Accuracy: <strong>97.42% Empirical</strong>
          </div>
        </div>

      </div>

      {/* Floating Active Threat Telemetry Card */}
      <div className="micro-surface rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 font-mono text-xs">
        <div className="flex items-center space-x-3">
          <div className="h-9 w-9 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold shrink-0">
            <CheckCircle2 className="h-5 w-5" />
          </div>
          <div>
            <div className="font-bold text-slate-900 dark:text-slate-100 font-sans">Continuous Spatial Threat Sentinel</div>
            <div className="text-[10px] text-slate-500 dark:text-slate-400">
              Zero Trust RBAC Enforcement • Bcrypt Hash Vault • SQLite Audit Log
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <div className="text-right">
            <div className="text-[9px] uppercase text-slate-400 font-bold">Neural Confidence</div>
            <div className="text-sm font-bold text-blue-600 dark:text-blue-400">98.4%</div>
          </div>
          <span className="px-2.5 py-1 rounded-lg text-[10px] font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30">
            FLOW VERIFIED
          </span>
        </div>
      </div>

    </div>
  );
};

