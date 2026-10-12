import React from 'react';
import { 
  Database, FileText, Cpu, CheckCircle2, 
  Clock, Upload, BarChart2, Play, Activity, 
  GraduationCap, AlertCircle, Info, Layers
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const OverviewView = ({ onNavigate }) => {
  const { user, role, modelStatus, modelMetrics, trainingProgress, datasets, activeDataset } = useAuth();
  const currentRole = role || user?.role || 'Admin';
  const isAdmin = currentRole === 'Admin';
  const isTrained = modelStatus === 'Trained';
  const isTraining = modelStatus === 'Training' || modelStatus === 'Preprocessing' || (trainingProgress && trainingProgress.isTraining);
  
  const uploadedCount = (datasets && datasets.length) ? datasets.length : 4;
  const activeName = activeDataset?.name || activeDataset?.filename || 'nsl_kdd_intrusion_dataset.csv';
  const activeRows = activeDataset?.rows || activeDataset?.row_count || 1010;

  const datasetUsed = trainingProgress?.datasetName || modelMetrics?.datasetName || activeName;
  const displayAcc = isTraining 
    ? (trainingProgress?.accuracy && trainingProgress.accuracy !== '0.00%' ? trainingProgress.accuracy : modelMetrics.accuracy) 
    : modelMetrics.accuracy;
  const displayLoss = isTraining 
    ? (trainingProgress?.loss && trainingProgress.loss !== '0.0000' ? trainingProgress.loss : modelMetrics.loss) 
    : modelMetrics.loss;

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      
      {/* 1. INSTITUTIONAL ACCREDITATION CARD */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="h-12 w-12 sm:h-14 sm:w-14 rounded-2xl bg-white border border-slate-200 shadow-xs p-1 flex items-center justify-center shrink-0">
            <img
              src="/jnnce_logo.png"
              alt="JNNCE Logo"
              className="h-full w-full object-contain"
            />
          </div>
          <div>
            <h2 className="text-sm sm:text-base md:text-lg font-bold text-slate-900 tracking-tight">
              Jawaharlal Nehru National College of Engineering, Shivamogga
            </h2>
            <p className="text-xs font-bold text-blue-600 uppercase tracking-wide">
              DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING
            </p>
            <p className="text-[11px] sm:text-xs text-slate-500">
              Zero Trust AI-Powered Network Intrusion Detection System
            </p>
          </div>
        </div>

        <div className="shrink-0">
          <span className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-600 border border-blue-200 text-xs font-semibold">
            <GraduationCap className="h-4 w-4" />
            <span>PROJECT BATCH NO. 34</span>
          </span>
        </div>
      </div>

      {/* 2. SECTION HEADER & ACTION CONTROLS */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-1">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
            Security Operations Dashboard
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Overview of Zero Trust NIDS datasets, model training status, and evaluation metrics.
          </p>
        </div>

        <div className="flex items-center space-x-2.5 shrink-0">
          <button
            onClick={() => onNavigate('datasets')}
            className="px-4 py-2 text-xs font-semibold bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl transition-all flex items-center space-x-2 shadow-xs active:scale-95"
          >
            <Upload className="h-3.5 w-3.5" />
            <span>Upload Dataset</span>
          </button>
          
          {isAdmin && (
            <button
              onClick={() => onNavigate('training')}
              className="px-4 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-xs transition-all flex items-center space-x-2 active:scale-95"
            >
              <Play className="h-3.5 w-3.5 fill-white" />
              <span>Train Model</span>
            </button>
          )}
        </div>
      </div>

      {/* 3. 6-METRIC TELEMETRY GRID */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5 font-sans">
        
        {/* Card 1: Uploaded Datasets */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">UPLOADED DATASETS</span>
            <Database className="h-4 w-4 text-blue-600" />
          </div>
          <div className="text-xl sm:text-2xl font-bold text-slate-900">
            {uploadedCount} Files
          </div>
          <div className="text-[10px] text-slate-500 truncate" title="Custom, NSL-KDD, UNSW-NB15, CICIDS2017">
            Custom, NSL-KDD, UNSW-NB15, CICIDS2017
          </div>
        </div>

        {/* Card 2: Active Target Dataset */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">ACTIVE DATASET</span>
            <FileText className="h-4 w-4 text-blue-600" />
          </div>
          <div className="text-xs font-bold text-slate-900 truncate" title={activeName}>
            {activeName.replace('.csv','')}
          </div>
          <div className="text-[10px] text-emerald-600 font-bold">
            {activeRows.toLocaleString()} Rows
          </div>
        </div>

        {/* Card 3: Model Status */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">MODEL STATUS</span>
            <Layers className={`h-4 w-4 ${isTrained ? 'text-emerald-500' : 'text-amber-500'}`} />
          </div>
          <div className={`text-xs font-bold flex items-center space-x-1 ${isTrained ? 'text-emerald-600' : 'text-amber-500'}`}>
            {isTrained ? <CheckCircle2 className="h-3.5 w-3.5" /> : <AlertCircle className="h-3.5 w-3.5" />}
            <span>{isTrained ? 'Trained' : 'Untrained'}</span>
          </div>
          <div className="text-[10px] text-slate-500 truncate">
            {isTrained ? 'lstm_model.keras' : 'Pending Training'}
          </div>
        </div>

        {/* Card 4: Neural Engine / Current Model */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">CURRENT MODEL</span>
            <Cpu className="h-4 w-4 text-blue-600" />
          </div>
          <div className="text-xs font-bold text-slate-900">
            LSTM Network
          </div>
          <div className="text-[10px] text-slate-500">
            TensorFlow / Keras
          </div>
        </div>

        {/* Card 5: Training Accuracy */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">TRAINING ACCURACY</span>
            <Activity className={`h-4 w-4 ${isTrained ? 'text-emerald-500' : 'text-blue-600'}`} />
          </div>
          <div className={`text-xl sm:text-2xl font-bold ${isTrained ? 'text-emerald-600' : 'text-slate-400'}`}>
            {isTrained ? modelMetrics.accuracy : '0.00%'}
          </div>
          <div className="text-[10px] text-slate-500">
            {isTrained ? 'Test Set Split' : 'Requires Training'}
          </div>
        </div>

        {/* Card 6: Last Training */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">LAST TRAINING</span>
            <Clock className="h-4 w-4 text-blue-600" />
          </div>
          <div className="text-xs font-bold text-slate-900 truncate">
            {isTrained ? `${modelMetrics.epochs || 10} Epochs` : 'None'}
          </div>
          <div className="text-[10px] text-slate-500 truncate">
            {isTrained ? modelMetrics.trainedAt : 'Pending Session'}
          </div>
        </div>

      </div>

      {/* 4. PHASE 1 WORKFLOW PROGRESSION */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900">
          PHASE 1 WORKFLOW
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3 text-center">
          {[
            { id: '01', title: 'Dataset Upload', completed: true },
            { id: '02', title: 'Dataset Validation', completed: true },
            { id: '03', title: 'Preprocessing', completed: true },
            { id: '04', title: 'Feature Engineering', completed: true },
            { id: '05', title: 'Train/Test Split', completed: true },
            { id: '06', title: 'LSTM Training', completed: isTrained },
            { id: '07', title: 'Model Evaluation', completed: isTrained },
            { id: '08', title: 'Saved Model', completed: isTrained },
          ].map((step) => (
            <div key={step.id} className="bg-slate-50/80 border border-slate-200/80 rounded-xl p-3 flex flex-col justify-between h-22 space-y-1">
              <div className="text-blue-600 font-bold text-[10px]">{step.id}</div>
              <div className="text-[11px] font-bold text-slate-800 leading-tight">{step.title}</div>
              <CheckCircle2 className={`h-3.5 w-3.5 mx-auto ${step.completed ? 'text-emerald-500' : 'text-slate-300'}`} />
            </div>
          ))}
        </div>
      </div>

      {/* 5. QUICK ACTIONS */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900">
          QUICK ACTIONS
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <button
            onClick={() => onNavigate('datasets')}
            className="bg-slate-50/80 border border-slate-200/80 hover:border-blue-500/40 hover:bg-white rounded-xl p-4 transition-all text-left group shadow-xs active:scale-98"
          >
            <Upload className="h-5 w-5 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
            <div className="text-xs font-bold text-slate-900 group-hover:text-blue-600">Dataset Repository</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Upload & manage intrusion CSV benchmarks</div>
          </button>

          <button
            onClick={() => onNavigate('compare')}
            className="bg-slate-50/80 border border-slate-200/80 hover:border-blue-500/40 hover:bg-white rounded-xl p-4 transition-all text-left group shadow-xs active:scale-98"
          >
            <BarChart2 className="h-5 w-5 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
            <div className="text-xs font-bold text-slate-900 group-hover:text-blue-600">Compare Datasets</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Side-by-side feature & row comparisons</div>
          </button>

          {isAdmin ? (
            <button
              onClick={() => onNavigate('training')}
              className="bg-slate-50/80 border border-slate-200/80 hover:border-blue-500/40 hover:bg-white rounded-xl p-4 transition-all text-left group shadow-xs active:scale-98"
            >
              <Play className="h-5 w-5 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
              <div className="text-xs font-bold text-slate-900 group-hover:text-blue-600">Model Training</div>
              <div className="text-[10px] text-slate-500 mt-0.5">Configure hyperparameters & train LSTM</div>
            </button>
          ) : (
            <button
              onClick={() => onNavigate('model-details')}
              className="bg-slate-50/80 border border-slate-200/80 hover:border-blue-500/40 hover:bg-white rounded-xl p-4 transition-all text-left group shadow-xs active:scale-98"
            >
              <Layers className="h-5 w-5 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
              <div className="text-xs font-bold text-slate-900 group-hover:text-blue-600">Model Specifications</div>
              <div className="text-[10px] text-slate-500 mt-0.5">Inspect neural layer parameters & metrics</div>
            </button>
          )}

          <button
            onClick={() => onNavigate('about')}
            className="bg-slate-50/80 border border-slate-200/80 hover:border-blue-500/40 hover:bg-white rounded-xl p-4 transition-all text-left group shadow-xs active:scale-98"
          >
            <Info className="h-5 w-5 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
            <div className="text-xs font-bold text-slate-900 group-hover:text-blue-600">About Architecture</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Zero Trust architecture & department metadata</div>
          </button>

        </div>
      </div>

    </div>
  );
};
