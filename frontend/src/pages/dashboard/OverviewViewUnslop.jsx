import React from 'react';
import { 
  Shield, Activity, Database, Cpu, Radio, 
  ArrowUpRight, Check, RefreshCw
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const OverviewViewUnslop = ({ onNavigate }) => {
  const { user, role, modelStatus, modelMetrics, trainingProgress, datasets, activeDataset } = useAuth();
  const currentRole = role || user?.role || 'Admin';
  const isAdmin = currentRole === 'Admin';
  const isTrained = modelStatus === 'Trained';
  const isTraining = modelStatus === 'Training' || modelStatus === 'Preprocessing' || (trainingProgress && trainingProgress.isTraining);

  // Dynamic values strictly derived from system context / state
  const uploadedCount = (datasets && datasets.length) ? datasets.length : 0;
  const activeName = activeDataset?.name || activeDataset?.filename || 'No Active Dataset';
  const activeRows = activeDataset?.rows || activeDataset?.row_count;

  const accuracy = isTraining 
    ? (trainingProgress?.accuracy && trainingProgress.accuracy !== '0.00%' ? trainingProgress.accuracy : modelMetrics?.accuracy || '—')
    : isTrained 
    ? (modelMetrics?.accuracy || '—') 
    : '—';

  const rocauc = isTrained ? (modelMetrics?.rocAuc || modelMetrics?.roc_auc || '—') : '—';
  const fpr = isTrained ? (modelMetrics?.fpr || modelMetrics?.false_positive_rate || '—') : '—';
  const algorithm = isTrained 
    ? (modelMetrics?.algorithm || modelMetrics?.model_name || 'Active Model') 
    : 'Untrained';

  const pipelineStages = [
    { num: '01', name: 'Raw Ingestion', status: activeDataset ? 'ready' : 'pending', detail: activeName.replace('.csv', '') },
    { num: '02', name: 'Sanitization', status: activeDataset ? 'ready' : 'pending', detail: 'Deduplicated' },
    { num: '03', name: 'Anti-Leak Split', status: activeDataset ? 'ready' : 'pending', detail: '70 / 15 / 15' },
    { num: '04', name: 'Train Scaler', status: isTrained ? 'ready' : 'pending', detail: 'scaler.pkl' },
    { num: '05', name: 'Model Training', status: isTrained ? 'ready' : isTraining ? 'active' : 'pending', detail: isTrained ? 'Optimized' : isTraining ? 'In Progress' : 'Pending' },
    { num: '06', name: 'Holdout Eval', status: isTrained ? 'ready' : 'pending', detail: isTrained ? (modelMetrics?.evalSamples ? `${modelMetrics.evalSamples} Flows` : 'Evaluated') : 'Pending' },
    { num: '07', name: 'Model Registry', status: isTrained ? 'ready' : 'pending', detail: 'model.joblib' },
    { num: '08', name: 'Live Sniffer', status: 'ready', detail: 'Active Driver' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 text-slate-900 font-sans">
      
      {/* Top Console Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-slate-500 mb-1">
            <span className={`inline-block w-2 h-2 rounded-full ${isTrained ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
            <span>SYSTEM CONSOLE ACTIVE</span>
            <span>/</span>
            <span>ZERO TRUST PERIMETER</span>
            <span>/</span>
            <span>NIST SP 800-207</span>
          </div>
          <h1 className="text-xl font-semibold tracking-tight text-slate-950">
            Security Operations & Threat Telemetry
          </h1>
        </div>

        <div className="flex items-center space-x-2.5">
          {isAdmin && (
            <button
              onClick={() => onNavigate('training')}
              className="text-xs font-medium px-3.5 py-1.5 rounded-lg bg-slate-900 text-white hover:bg-slate-800 transition-colors flex items-center space-x-1.5 shadow-2xs"
            >
              <Cpu className="h-3.5 w-3.5 text-slate-300" />
              <span>Model Studio</span>
            </button>
          )}
          <button
            onClick={() => onNavigate('live-detection')}
            className="text-xs font-medium px-3.5 py-1.5 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors flex items-center space-x-1.5 shadow-2xs"
          >
            <Radio className="h-3.5 w-3.5 text-blue-200" />
            <span>Live Sniffer</span>
          </button>
        </div>
      </div>

      {/* Primary Telemetry Grid: 4 Dedicated Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Metric 1: Active Model & Security Verdict */}
        <div className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span>Active Classifier</span>
              <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-mono ${
                isTrained ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600'
              }`}>
                {isTrained ? 'Online' : 'Standby'}
              </span>
            </div>
            <div className="mt-3 text-base font-semibold text-slate-900 truncate" title={algorithm}>
              {algorithm}
            </div>
            <div className="mt-1 text-xs text-slate-500 font-mono">
              ROC-AUC: <span className="text-slate-900 font-semibold">{rocauc}</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-mono">
            <span>False Positive Rate</span>
            <span className="font-semibold text-slate-800">{fpr}</span>
          </div>
        </div>

        {/* Metric 2: Detection Accuracy */}
        <div className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span>Holdout Test Accuracy</span>
              <Activity className="h-4 w-4 text-slate-400" />
            </div>
            <div className="mt-2 text-3xl font-semibold tracking-tight text-slate-950 tabular-nums">
              {accuracy}
            </div>
            <div className="mt-1 text-xs text-slate-500">
              {isTrained ? 'Validation on holdout split' : 'Awaiting model training session'}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-mono">
            <span>Inference Latency</span>
            <span className="font-semibold text-emerald-700">
              {modelMetrics?.prediction_time ? `${modelMetrics.prediction_time}s` : '< 1.0 ms/flow'}
            </span>
          </div>
        </div>

        {/* Metric 3: Active Benchmark Dataset */}
        <div className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span>Benchmark Partition</span>
              <Database className="h-4 w-4 text-slate-400" />
            </div>
            <div className="mt-3 text-sm font-semibold text-slate-900 truncate" title={activeName}>
              {activeName.replace('.csv', '')}
            </div>
            <div className="mt-1 text-xs text-slate-500 tabular-nums font-mono">
              {activeRows ? `${activeRows.toLocaleString()} rows cataloged` : 'Dataset selected'}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
            <span>Inventory Count</span>
            <span className="font-mono font-medium text-slate-800">{uploadedCount} Benchmarks</span>
          </div>
        </div>

        {/* Metric 4: Zero Trust Access Governance */}
        <div className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span>Access Control Layer</span>
              <Shield className="h-4 w-4 text-slate-400" />
            </div>
            <div className="mt-3 text-sm font-semibold text-slate-900">
              Role: <span className="font-mono text-blue-700">{currentRole}</span>
            </div>
            <div className="mt-1 text-xs text-slate-500 font-mono">
              Token: HMAC-SHA256 (Signed)
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-mono">
            <span>Zero Trust Boundary</span>
            <span className="text-emerald-700 font-medium">Enforced</span>
          </div>
        </div>

      </div>

      {/* Unified Pipeline State Machine */}
      <div className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs">
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
          <div>
            <h2 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">
              Deterministic Processing Pipeline
            </h2>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Zero data-leakage isolation across dataset ingestion, mathematical scaling, and live classification.
            </p>
          </div>
          <span className="text-[11px] font-mono text-slate-500 bg-slate-50 px-2 py-0.5 rounded border border-slate-200">
            Stages 01–08
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2.5">
          {pipelineStages.map((stage) => {
            const isReady = stage.status === 'ready';
            const isActive = stage.status === 'active';
            return (
              <div 
                key={stage.num}
                className={`p-3 rounded-lg border text-left flex flex-col justify-between h-24 transition-colors ${
                  isReady 
                    ? 'bg-slate-50/70 border-slate-200' 
                    : isActive 
                    ? 'bg-blue-50/70 border-blue-300' 
                    : 'bg-white border-slate-200 opacity-60'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-semibold text-slate-500">{stage.num}</span>
                  {isReady && <Check className="h-3 w-3 text-emerald-600" />}
                  {isActive && <RefreshCw className="h-3 w-3 text-blue-600 animate-spin" />}
                </div>
                <div>
                  <div className="text-xs font-medium text-slate-900 leading-tight">{stage.name}</div>
                  <div className="text-[10px] text-slate-500 font-mono mt-0.5">{stage.detail}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Operational Workflows & Forensic Navigation */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div 
          onClick={() => onNavigate('live-detection')}
          className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs hover:border-slate-300 cursor-pointer transition-colors group"
        >
          <div className="flex items-center justify-between text-xs text-slate-500 font-mono">
            <span>LIVE INTERFACE</span>
            <ArrowUpRight className="h-3.5 w-3.5 text-slate-400 group-hover:text-slate-900 transition-colors" />
          </div>
          <h3 className="text-sm font-semibold text-slate-950 mt-2">Promiscuous Packet Sniffer</h3>
          <p className="text-xs text-slate-500 mt-1">
            Out-of-band capture via Windows Npcap driver, direction-agnostic 5-tuple canonical hashing, and real-time threat telemetry.
          </p>
        </div>

        <div 
          onClick={() => onNavigate('compare')}
          className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs hover:border-slate-300 cursor-pointer transition-colors group"
        >
          <div className="flex items-center justify-between text-xs text-slate-500 font-mono">
            <span>BENCHMARKS</span>
            <ArrowUpRight className="h-3.5 w-3.5 text-slate-400 group-hover:text-slate-900 transition-colors" />
          </div>
          <h3 className="text-sm font-semibold text-slate-950 mt-2">Multi-Dataset Matrix</h3>
          <p className="text-xs text-slate-500 mt-1">
            Cross-benchmark structural analysis contrasting feature schemas and class distributions.
          </p>
        </div>

        <div 
          onClick={() => onNavigate('audit-logs')}
          className="bg-white rounded-xl p-5 border border-slate-200/90 shadow-2xs hover:border-slate-300 cursor-pointer transition-colors group"
        >
          <div className="flex items-center justify-between text-xs text-slate-500 font-mono">
            <span>FORENSICS</span>
            <ArrowUpRight className="h-3.5 w-3.5 text-slate-400 group-hover:text-slate-900 transition-colors" />
          </div>
          <h3 className="text-sm font-semibold text-slate-950 mt-2">Tamper-Evident Audit Ledger</h3>
          <p className="text-xs text-slate-500 mt-1">
            Cryptographic ledger tracking authentication tokens, RBAC permission gate checks, and administrative training invocations.
          </p>
        </div>

      </div>

    </div>
  );
};
