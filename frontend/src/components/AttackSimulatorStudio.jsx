import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, ShieldCheck, Play, RotateCcw, Activity, 
  Cpu, Zap, Lock, Terminal, CheckCircle2, AlertTriangle, 
  Flame, Crosshair, Sparkles
} from 'lucide-react';
import { cyberAudio } from '../utils/cyberAudio';

export const AttackSimulatorStudio = () => {
  const [selectedAttack, setSelectedAttack] = useState('SYN Flood');
  const [simState, setSimState] = useState('idle'); // 'idle' | 'analyzing' | 'blocked'
  const [activeStage, setActiveStage] = useState(0);
  const [tensorValues, setTensorValues] = useState([0.14, 0.88, 0.42, 0.05, 0.91, 0.23]);
  const [confidence, setConfidence] = useState(99.4);
  const [latencyMs, setLatencyMs] = useState(0.42);

  const attacks = [
    { id: 'SYN Flood', name: 'TCP-SYN Flood (DoS)', type: 'DoS Attack', severity: 'Critical', color: 'rose', proto: 'TCP', port: 80 },
    { id: 'PortScan', name: 'PortScan Network Recon', type: 'Probe / Recon', severity: 'High', color: 'amber', proto: 'TCP', port: 443 },
    { id: 'SSH-BruteForce', name: 'SSH Credential Brute Force', type: 'R2L Access', severity: 'High', color: 'purple', proto: 'SSH', port: 22 },
    { id: 'Botnet-C2', name: 'Botnet C2 Beaconing', type: 'Command & Control', severity: 'Critical', color: 'rose', proto: 'UDP', port: 5353 },
    { id: 'Normal-Flow', name: 'Standard HTTPS Web Traffic', type: 'Benign Flow', severity: 'Normal', color: 'emerald', proto: 'TLS', port: 443 }
  ];

  const currentAttackObj = attacks.find(a => a.id === selectedAttack) || attacks[0];

  const runSimulation = () => {
    cyberAudio.playClick();
    setSimState('analyzing');
    setActiveStage(1);

    // Randomize simulated tensor values
    setTensorValues(Array.from({ length: 6 }, () => +(Math.random() * 0.9 + 0.05).toFixed(2)));
    setLatencyMs(+(Math.random() * 0.3 + 0.35).toFixed(2));

    setTimeout(() => {
      setActiveStage(2);
      setTimeout(() => {
        setActiveStage(3);
        setTimeout(() => {
          setActiveStage(4);
          setTimeout(() => {
            setActiveStage(5);
            setSimState('blocked');
            if (currentAttackObj.severity === 'Normal') {
              cyberAudio.playVerify();
            } else {
              cyberAudio.playThreat();
            }
          }, 350);
        }, 350);
      }, 350);
    }, 350);
  };

  const resetSimulation = () => {
    cyberAudio.playClick();
    setSimState('idle');
    setActiveStage(0);
  };

  return (
    <div className="floating-surface rounded-2xl p-6 sm:p-8 shadow-spatial-lg space-y-6 relative overflow-hidden border border-border/80">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center space-x-2.5 mb-1">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping" />
            <h3 className="text-base font-bold text-foreground tracking-tight">
              Interactive Attack Ingress & Zero Trust Interceptor Sandbox
            </h3>
          </div>
          <p className="text-xs text-muted-foreground">
            Inject synthetic cyber threat vectors to test LSTM tensor classification and real-time perimeter policy enforcement.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          {simState !== 'idle' && (
            <button
              onClick={resetSimulation}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl micro-surface text-muted-foreground hover:text-foreground text-xs font-mono transition-all tactile-btn"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          )}
          <button
            onClick={runSimulation}
            disabled={simState === 'analyzing'}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold font-mono shadow-spatial-sm transition-all tactile-btn disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-white" />
            <span>{simState === 'analyzing' ? 'Intercepting Flow...' : 'Launch Threat Injection'}</span>
          </button>
        </div>
      </div>

      {/* Attack Selector Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
        {attacks.map((atk) => {
          const isSelected = selectedAttack === atk.id;
          return (
            <button
              key={atk.id}
              onClick={() => {
                cyberAudio.playClick();
                setSelectedAttack(atk.id);
                setSimState('idle');
                setActiveStage(0);
              }}
              onMouseEnter={() => cyberAudio.playHover()}
              className={`p-3 rounded-xl text-left font-mono transition-all text-xs border micro-surface ${
                isSelected
                  ? 'border-primary bg-primary/10 shadow-spatial-sm ring-1 ring-primary/40'
                  : 'hover:border-primary/40 border-border/60'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className={`text-[9px] px-1.5 py-0.2 rounded-full font-bold uppercase ${
                  atk.severity === 'Critical' ? 'bg-rose-500/20 text-rose-500' :
                  atk.severity === 'High' ? 'bg-amber-500/20 text-amber-500' :
                  'bg-emerald-500/20 text-emerald-500'
                }`}>
                  {atk.severity}
                </span>
                <span className="text-[10px] text-muted-foreground">{atk.proto}:{atk.port}</span>
              </div>
              <div className="font-bold text-foreground truncate text-[11px]">{atk.id}</div>
              <div className="text-[10px] text-muted-foreground truncate">{atk.type}</div>
            </button>
          );
        })}
      </div>

      {/* Pipeline Interception Monitor */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
        
        {/* Stages Visualization */}
        <div className="lg:col-span-8 micro-surface rounded-2xl p-4 space-y-3.5 shadow-spatial-sm">
          <div className="flex items-center justify-between text-xs font-mono border-b border-border/40 pb-2">
            <span className="text-muted-foreground font-semibold">ZERO TRUST VERIFICATION PIPELINE</span>
            <span className="text-primary">{simState.toUpperCase()}</span>
          </div>

          <div className="space-y-2.5">
            {[
              { num: '01', title: 'Device Fingerprint & Posture', desc: 'Validates TLS handshake & MAC authorization' },
              { num: '02', title: 'Identity & JWT Cryptographic Claims', desc: 'Checks non-repudiation & least-privilege token signature' },
              { num: '03', title: 'Contextual Flow Micro-Segmentation', desc: 'Applies zero-implicit-trust access firewall boundary' },
              { num: '04', title: 'LSTM Neural Threat Analysis', desc: '64-unit recurrent neural network sequence evaluation' },
              { num: '05', title: 'Enforcement & Immutable Audit Decision', desc: currentAttackObj.severity === 'Normal' ? 'Traffic Authenticated & Allowed' : 'Ingress Flow Blocked & Quarantined' }
            ].map((stg, i) => {
              const stepIndex = i + 1;
              const isPassed = activeStage >= stepIndex;
              const isCurrent = activeStage === stepIndex;

              return (
                <div 
                  key={stg.num}
                  className={`flex items-center justify-between p-2.5 rounded-xl text-xs font-mono transition-all border ${
                    isPassed 
                      ? currentAttackObj.severity === 'Normal'
                        ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-600 dark:text-emerald-400'
                        : stepIndex === 5
                        ? 'bg-rose-500/15 border-rose-500/50 text-rose-600 dark:text-rose-400 font-bold'
                        : 'bg-primary/10 border-primary/30 text-primary'
                      : 'bg-muted/20 border-border/30 text-muted-foreground opacity-60'
                  }`}
                >
                  <div className="flex items-center space-x-2.5">
                    <span className="w-6 h-6 rounded-lg bg-background/80 border border-border flex items-center justify-center font-bold text-[10px]">
                      {stg.num}
                    </span>
                    <div>
                      <div className="font-semibold text-foreground text-[11px]">{stg.title}</div>
                      <div className="text-[10px] text-muted-foreground">{stg.desc}</div>
                    </div>
                  </div>

                  <div className="text-[11px] font-bold">
                    {isPassed ? (
                      stepIndex === 5 && currentAttackObj.severity !== 'Normal' ? (
                        <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-500 flex items-center space-x-1">
                          <ShieldAlert className="w-3.5 h-3.5" />
                          <span>QUARANTINED</span>
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-500 flex items-center space-x-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>VERIFIED</span>
                        </span>
                      )
                    ) : (
                      <span className="text-[10px] text-muted-foreground">STANDBY</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Live Tensor Breakdown & Telemetry */}
        <div className="lg:col-span-4 micro-surface rounded-2xl p-4 space-y-4 shadow-spatial-sm flex flex-col justify-between">
          <div className="space-y-3">
            <div className="text-xs font-mono font-bold text-foreground border-b border-border/40 pb-2 flex items-center justify-between">
              <span>Tensor Ingestion HUD</span>
              <span className="text-[10px] text-primary">{latencyMs} ms</span>
            </div>

            {/* Simulated Tensor Features */}
            <div className="space-y-1.5 font-mono text-[10px]">
              <span className="text-muted-foreground block uppercase">Feature Vector [0..5]</span>
              <div className="grid grid-cols-3 gap-1.5">
                {tensorValues.map((val, idx) => (
                  <div key={idx} className="p-1.5 rounded-lg bg-background border border-border text-center">
                    <span className="text-[9px] text-muted-foreground block">f_{idx}</span>
                    <span className="font-bold text-cyan-400">{val}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Neural Confidence Gauge */}
            <div className="space-y-1.5 font-mono text-xs">
              <div className="flex justify-between items-center text-[11px]">
                <span className="text-muted-foreground">Neural Confidence</span>
                <span className="font-bold text-primary">{confidence}%</span>
              </div>
              <div className="w-full h-2 bg-muted/40 rounded-full overflow-hidden border border-border/40">
                <div 
                  className="h-full bg-gradient-to-r from-primary to-cyan-400 rounded-full transition-all duration-500 shadow-glow"
                  style={{ width: `${confidence}%` }}
                />
              </div>
            </div>
          </div>

          {/* Action Result Badge */}
          <div className={`p-3 rounded-xl border text-center font-mono text-xs ${
            simState === 'blocked'
              ? currentAttackObj.severity === 'Normal'
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400'
                : 'bg-rose-500/10 border-rose-500/30 text-rose-600 dark:text-rose-400'
              : 'bg-muted/20 border-border/40 text-muted-foreground'
          }`}>
            <div className="font-bold text-[11px]">
              {simState === 'blocked' 
                ? currentAttackObj.severity === 'Normal'
                  ? '✓ LEGITIMATE FLOW AUTHENTICATED'
                  : '⚠ ZERO TRUST POLICY INTERCEPTED'
                : simState === 'analyzing'
                ? '⚡ EVALUATING LSTM TENSOR FLOW...'
                : 'IDLE / AWAITING INGRESS INJECTION'}
            </div>
            <div className="text-[10px] opacity-80 mt-0.5">
              Target Vector: {currentAttackObj.name}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
