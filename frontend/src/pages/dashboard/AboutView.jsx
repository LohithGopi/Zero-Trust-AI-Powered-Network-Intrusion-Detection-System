import React from 'react';
import { 
  ShieldCheck, GitBranch, CheckCircle2, 
  AlertCircle, GraduationCap, Cpu
} from 'lucide-react';

export const AboutView = () => {
  return (
    <div className="space-y-6 animate-fade-in pb-12 font-sans">
      
      {/* HEADER BANNER */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded bg-blue-50 text-blue-600 text-[10px] font-mono font-bold border border-blue-200">
              SYSTEM DOCUMENTATION
            </span>
            <span className="px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-600 text-[10px] font-mono font-bold border border-emerald-200">
              PHASE 1 ARCHITECTURE
            </span>
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight pt-1">
            About System & Technical Architecture
          </h1>
          <p className="text-xs text-slate-500 max-w-2xl leading-relaxed">
            Comprehensive overview of Zero Trust principles, AI/ML LSTM Intrusion Detection Pipeline, and Institution Details.
          </p>
        </div>
        
        <div className="shrink-0">
          <span className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-600 border border-blue-200 text-xs font-semibold">
            <GraduationCap className="h-4 w-4" />
            <span>BATCH 2023–2027 (BATCH 34)</span>
          </span>
        </div>
      </div>

      {/* SECTION 1: PROBLEM & SOLUTION */}
      <section className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-5">
        <div className="flex items-center space-x-3 border-b border-slate-100 pb-3">
          <div className="p-2 rounded-xl bg-blue-50 text-blue-600 border border-blue-100">
            <ShieldCheck className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">
              1. Problem & Solution
            </h2>
            <p className="text-xs text-slate-500">
              Challenge in perimeter defense vs. AI-driven Zero Trust response
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {/* PROBLEM CARD */}
          <div className="p-5 rounded-2xl border border-red-200 bg-red-50/40 space-y-2.5">
            <div className="flex items-center space-x-2 text-red-600 font-bold text-xs uppercase tracking-wide">
              <AlertCircle className="h-4 w-4" />
              <span>Problem</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Traditional network security approaches may struggle to detect evolving cyber threats and provide sufficient protection for modern network environments.
            </p>
          </div>

          {/* SOLUTION CARD */}
          <div className="p-5 rounded-2xl border border-emerald-200 bg-emerald-50/40 space-y-2.5">
            <div className="flex items-center space-x-2 text-emerald-600 font-bold text-xs uppercase tracking-wide">
              <CheckCircle2 className="h-4 w-4" />
              <span>Solution</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              The proposed <strong>AI-Powered Zero Trust Network Intrusion Detection System (NIDS)</strong> combines Zero Trust security principles with an AI-based intrusion detection model. It processes network traffic datasets, performs preprocessing, and uses an LSTM-based model to identify normal and malicious network activity.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 2: HOW IT WORKS */}
      <section className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-5">
        <div className="flex items-center space-x-3 border-b border-slate-100 pb-3">
          <div className="p-2 rounded-xl bg-blue-50 text-blue-600 border border-blue-100">
            <GitBranch className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">
              2. How It Works
            </h2>
            <p className="text-xs text-slate-500">
              Step-by-step workflow of dataset ingestion, preprocessing, training, and classification
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { step: '1', title: 'Dataset Collection', desc: 'Network intrusion datasets are imported into the system.' },
            { step: '2', title: 'Data Preprocessing', desc: 'Missing values and duplicate records are identified and handled.' },
            { step: '3', title: 'Feature Processing', desc: 'Relevant network traffic features are encoded, normalized, and prepared for model training.' },
            { step: '4', title: 'Sequential Data Preparation', desc: 'Processed features are converted into sequences suitable for the LSTM model where applicable.' },
            { step: '5', title: 'AI Model Training', desc: 'The LSTM model learns patterns from the prepared network traffic data.' },
            { step: '6', title: 'Intrusion Detection', desc: 'The trained model is used to classify network traffic based on learned patterns.' }
          ].map((item) => (
            <div key={item.step} className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-2">
              <div className="flex items-center space-x-2 text-slate-900 font-bold text-xs">
                <span className="h-5 w-5 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-[10px] font-mono shrink-0">
                  {item.step}
                </span>
                <h4>{item.title}</h4>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* FOOTER */}
      <footer className="text-center text-xs text-slate-500 font-medium pt-4">
        Department of Information Science & Engineering • Project Batch No. 34
      </footer>

    </div>
  );
};
