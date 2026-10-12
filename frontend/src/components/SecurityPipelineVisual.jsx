import React, { useState } from 'react';
import { Shield, Key, Cpu, Lock, CheckCircle2, Sliders, Database, ArrowRight, Activity, Terminal } from 'lucide-react';

export const SecurityPipelineVisual = () => {
  const [activeStep, setActiveStep] = useState(0);

  const pipelineStages = [
    {
      step: '01',
      title: 'Device Ingestion',
      subtitle: 'Untrusted Flow Arrival',
      icon: Database,
      principle: 'Default Deny Posture',
      description: 'Raw network socket packets (TCP/UDP/ICMP) or ingested benchmark CSV flow tuples (NSL-KDD, UNSW-NB15, CIC-IDS2017) are captured at the ingress border.',
      specs: ['Durations & Flow Rates', 'Source/Destination Endpoints', 'Flag Attributes (42–78 Cols)']
    },
    {
      step: '02',
      title: 'Identity & Token Check',
      subtitle: 'Cryptographic Gate',
      icon: Key,
      principle: 'Explicit Verification',
      description: 'Zero Trust middleware validates the PyJWT HMAC-SHA256 bearer token, verifying caller identity claims and active RBAC tier (Admin vs Analyst).',
      specs: ['Stateless Token Signature', 'Bcrypt 12-Round Password Vault', 'Session Expiration Window']
    },
    {
      step: '03',
      title: 'Zero Trust Policy Rule',
      subtitle: 'Least-Privilege RBAC',
      icon: Shield,
      principle: 'Least-Privilege Enforcement',
      description: 'Route-level decorators (@require_role) strictly restrict high-impact operations (training, dataset removal) to authorized Admin roles only.',
      specs: ['Endpoint Access Matrix', 'Context Ingress Inspection', 'Role Boundary Assertion']
    },
    {
      step: '04',
      title: 'LSTM Neural Analysis',
      subtitle: 'Deep Pattern Classification',
      icon: Cpu,
      principle: 'Assume Breach & Inspect',
      description: 'Normalized flow vectors are converted into 3D tensors (Batch, 1, Features) and processed through a 64-unit Keras LSTM recurrent neural network.',
      specs: ['StandardScaler Normalization', '64 LSTM Recurrent Units', 'Dropout (rate=0.20) Regularizer']
    },
    {
      step: '05',
      title: 'Access & Telemetry Decision',
      subtitle: 'Confidence & Audit Trail',
      icon: Lock,
      principle: 'Continuous Validation',
      description: 'Softmax output produces categorical traffic probabilities (Normal, DoS, Exploits, Probe). Results are committed to the immutable SQLite audit log.',
      specs: ['97.42% Empirical Test Accuracy', 'Immutable SQLite Event Log', 'Real-Time Telemetry Dispatch']
    }
  ];

  const current = pipelineStages[activeStep];
  const Icon = current.icon;

  return (
    <div className="floating-surface rounded-2xl p-6 sm:p-8 space-y-6 relative overflow-hidden">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100 dark:border-white/5">
        <div>
          <div className="flex items-center space-x-2">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-600 dark:text-emerald-400 font-bold">
              ZERO TRUST VERIFICATION PIPELINE
            </span>
          </div>
          <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-slate-100 mt-1">
            Never Trust, Always Verify Architecture
          </h3>
        </div>

        <div className="flex items-center space-x-2 text-[10px] font-mono px-3 py-1.5 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-800">
          <Terminal className="h-3.5 w-3.5" />
          <span>END-TO-END DATA FLOW</span>
        </div>
      </div>

      {/* Spatial Step Progression Rail */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
        {pipelineStages.map((stage, idx) => {
          const StageIcon = stage.icon;
          const isActive = activeStep === idx;
          const isPassed = activeStep > idx;

          return (
            <button
              key={idx}
              onClick={() => setActiveStep(idx)}
              className={`p-3.5 rounded-xl text-left transition-all duration-200 tactile-btn flex flex-col justify-between h-28 border ${
                isActive
                  ? 'bg-blue-600 text-white border-blue-600 shadow-spatial-md ring-2 ring-blue-500/30'
                  : isPassed
                  ? 'micro-surface border-emerald-500/30 text-slate-800 dark:text-slate-200'
                  : 'micro-surface hover:border-slate-300 dark:hover:border-white/20 text-slate-700 dark:text-slate-300'
              }`}
            >
              <div className="flex items-center justify-between w-full">
                <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                  isActive ? 'bg-white/20 text-white' : 'bg-slate-100 dark:bg-white/5 text-slate-500'
                }`}>
                  {stage.step}
                </span>
                <StageIcon className={`h-4 w-4 ${isActive ? 'text-white' : isPassed ? 'text-emerald-500' : 'text-slate-400'}`} />
              </div>

              <div>
                <div className="text-xs font-bold truncate">{stage.title}</div>
                <div className={`text-[9px] truncate ${isActive ? 'text-blue-100' : 'text-slate-400 dark:text-slate-500'}`}>
                  {stage.subtitle}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Selected Step Detail Surface */}
      <div className="micro-surface rounded-xl p-5 sm:p-6 space-y-4 font-mono text-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-white/5 pb-3">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-blue-600 dark:text-blue-400 shrink-0">
              <Icon className="h-5 w-5" />
            </div>
            <div>
              <div className="font-bold text-sm text-slate-900 dark:text-slate-100 font-sans">
                Stage {current.step}: {current.title}
              </div>
              <span className="text-[10px] text-blue-600 dark:text-blue-400 font-bold uppercase tracking-wider">
                Principle: {current.principle}
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-1.5 text-emerald-600 dark:text-emerald-400 text-[10px] font-bold">
            <CheckCircle2 className="h-4 w-4 shrink-0" />
            <span>ZERO TRUST ENFORCED</span>
          </div>
        </div>

        <p className="text-xs text-slate-600 dark:text-slate-300 font-sans leading-relaxed">
          {current.description}
        </p>

        {/* Technical Sub-Specs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
          {current.specs.map((spec, i) => (
            <div key={i} className="p-2.5 rounded-lg bg-slate-50 dark:bg-[#090B0E]/60 border border-slate-200/60 dark:border-white/5 text-[10px] text-slate-600 dark:text-slate-400 flex items-center space-x-2">
              <span className="h-1.5 w-1.5 rounded-full bg-blue-500 shrink-0" />
              <span className="truncate">{spec}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};

