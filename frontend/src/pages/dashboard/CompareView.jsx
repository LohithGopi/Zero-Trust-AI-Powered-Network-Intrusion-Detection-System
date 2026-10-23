import React, { useState, useEffect } from 'react';
import { 
  FileSpreadsheet, Layers, GitBranch, Play, CheckCircle2, 
  AlertCircle, RefreshCw, Activity, Zap, ShieldAlert, 
  Cpu, ArrowRight, BarChart3, Clock, Check, HelpCircle, Info,
  Sliders, Database, CheckSquare, Square
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { 
  apiGetAllModels, 
  apiCompareBenchmark, 
  apiCompareLive,
  apiGetDatasets 
} from '../../services/api';

export const CompareView = () => {
  const { datasets = [], toggleCompareDataset } = useAuth();
  const comparedItems = (datasets || []).filter(d => d && d.isCompared);

  // Main View Tab: 'models' (ML Model Comparison) vs 'datasets' (Dataset Matrix)
  const [activeMainTab, setActiveMainTab] = useState('models');

  // Comparison Mode for Models: 'benchmark' (Mode A) vs 'live' (Mode B)
  const [compareMode, setCompareMode] = useState('benchmark');

  // Selected Dataset for evaluation
  const [selectedDatasetId, setSelectedDatasetId] = useState('');

  // Loaded Models from Database
  const [allModels, setAllModels] = useState([]);
  const [selectedModelIds, setSelectedModelIds] = useState([]);
  const [loadingModels, setLoadingModels] = useState(false);

  // Comparison Results State
  const [isComparing, setIsComparing] = useState(false);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [comparisonError, setComparisonError] = useState('');

  // Benchmark Config
  const [testSamplesLimit, setTestSamplesLimit] = useState(1000);
  const [liveLimit, setLiveLimit] = useState(50);

  // Set default selected dataset from AuthContext
  useEffect(() => {
    if (datasets && datasets.length > 0 && !selectedDatasetId) {
      const active = datasets.find(d => d.is_selected) || datasets[0];
      if (active) setSelectedDatasetId(String(active.id));
    }
  }, [datasets]);

  // Fetch trained models on mount
  useEffect(() => {
    fetchModels();
  }, []);

  const runComparison = async (overrideMode = null, targetModelIds = null, overrideDatasetId = null) => {
    const currentMode = overrideMode || compareMode;
    const ids = (targetModelIds && targetModelIds.length > 0) ? targetModelIds : selectedModelIds;
    const dsId = overrideDatasetId !== undefined ? overrideDatasetId : selectedDatasetId;

    if (!ids || ids.length === 0) {
      setComparisonError('Please select at least one trained model to compare.');
      return;
    }

    setIsComparing(true);
    setComparisonError('');

    try {
      let res;
      if (currentMode === 'live') {
        res = await apiCompareLive({
          model_ids: ids,
          limit: Number(liveLimit) || 50
        });
      } else {
        res = await apiCompareBenchmark({
          model_ids: ids,
          dataset_id: dsId ? Number(dsId) : undefined,
          test_samples_limit: Number(testSamplesLimit) || 1000
        });
      }
      setComparisonResult(res);
    } catch (err) {
      setComparisonError(err?.message || 'Comparison evaluation failed.');
    } finally {
      setIsComparing(false);
    }
  };

  const fetchModels = async () => {
    try {
      setLoadingModels(true);
      const data = await apiGetAllModels();
      if (Array.isArray(data)) {
        setAllModels(data);
        if (data.length > 0) {
          const defaultSelected = data.slice(0, 3).map(m => m.id);
          setSelectedModelIds(defaultSelected);
          runComparison('benchmark', defaultSelected);
        }
      }
    } catch (err) {
      console.warn('Error loading models for comparison:', err);
    } finally {
      setLoadingModels(false);
    }
  };

  const handleToggleModelSelection = (id) => {
    if (selectedModelIds.includes(id)) {
      if (selectedModelIds.length === 1) return; // keep at least 1
      setSelectedModelIds(selectedModelIds.filter(mId => mId !== id));
    } else {
      setSelectedModelIds([...selectedModelIds, id]);
    }
  };

  const handleModeChange = (newMode) => {
    setCompareMode(newMode);
    setComparisonResult(null);
    if (selectedModelIds.length > 0) {
      runComparison(newMode, selectedModelIds);
    }
  };

  const handleRunComparison = async () => {
    runComparison();
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12 font-sans">
      
      {/* 1. HEADER CARD & MAIN TABS */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-mono text-purple-700 uppercase tracking-wider font-bold bg-purple-50 px-2.5 py-0.5 rounded-full border border-purple-200 inline-block">
              EVALUATION &amp; BENCHMARK SUITE
            </span>
            <span className="text-[10px] font-mono text-blue-700 uppercase tracking-wider font-bold bg-blue-50 px-2.5 py-0.5 rounded-full border border-blue-200 inline-block">
              ZERO-TRUST VERIFIED
            </span>
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 mt-1.5 tracking-tight">
            Comprehensive Model &amp; Dataset Comparison
          </h1>
          <p className="text-xs text-slate-500">
            Compare Support Vector Machine, Logistic Regression, and LSTM across held-out benchmark data or live session packet streams.
          </p>
        </div>

        {/* Primary View Switcher Tabs */}
        <div className="flex items-center bg-slate-100 p-1 rounded-xl text-xs font-bold shrink-0 self-start lg:self-auto">
          <button
            onClick={() => setActiveMainTab('models')}
            className={`px-3.5 py-2 rounded-lg transition-all cursor-pointer flex items-center space-x-1.5 ${
              activeMainTab === 'models'
                ? 'bg-white text-purple-700 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <GitBranch className="h-3.5 w-3.5" />
            <span>ML Models Comparison</span>
          </button>

          <button
            onClick={() => setActiveMainTab('datasets')}
            className={`px-3.5 py-2 rounded-lg transition-all cursor-pointer flex items-center space-x-1.5 ${
              activeMainTab === 'datasets'
                ? 'bg-white text-blue-700 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <FileSpreadsheet className="h-3.5 w-3.5" />
            <span>Dataset Specifications</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* VIEW 1: ML MODELS COMPARISON SUITE */}
      {/* ========================================================================= */}
      {activeMainTab === 'models' && (
        <div className="space-y-6">
          
          {/* Streamlined Subheader & Action Bar */}
          <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center space-x-2.5">
              <div className="p-2 bg-purple-50 text-purple-600 rounded-xl border border-purple-100">
                <BarChart3 className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-slate-900">
                  Multi-Model Comparison Suite
                </h2>
                <p className="text-xs text-slate-500">
                  Side-by-side evaluation across Support Vector Machine, Logistic Regression, and LSTM on held-out benchmark datasets or live packet streams.
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2 self-end sm:self-auto">
              <button
                onClick={() => runComparison()}
                disabled={isComparing || selectedModelIds.length === 0}
                className="px-3.5 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-bold text-xs flex items-center space-x-2 shadow-xs transition-all active:scale-95 cursor-pointer"
              >
                <RefreshCw className={`h-3.5 w-3.5 ${isComparing ? 'animate-spin' : ''}`} />
                <span>{isComparing ? 'Evaluating Models...' : 'Run Comparison'}</span>
              </button>
            </div>
          </div>

          {/* MODEL, DATASET & MODE CONFIGURATION SELECTOR */}
          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm space-y-4">
            
            {/* Top Row: Mode Switcher, Dataset Selector & Sample Limit */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-center">
              
              {/* Mode Selector (Mode A vs Mode B) */}
              <div className="lg:col-span-5 space-y-1.5">
                <label className="text-[11px] font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
                  <Activity className="h-3.5 w-3.5 text-purple-600" />
                  <span>Evaluation Mode</span>
                </label>
                <div className="grid grid-cols-2 gap-2 bg-slate-100 p-1 rounded-xl">
                  <button
                    type="button"
                    onClick={() => handleModeChange('benchmark')}
                    className={`py-2 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center space-x-1.5 cursor-pointer ${
                      compareMode === 'benchmark'
                        ? 'bg-white text-purple-700 shadow-xs border border-purple-200/60'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    <BarChart3 className="h-3.5 w-3.5" />
                    <span>Mode A: Benchmark</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => handleModeChange('live')}
                    className={`py-2 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center space-x-1.5 cursor-pointer ${
                      compareMode === 'live'
                        ? 'bg-white text-blue-700 shadow-xs border border-blue-200/60'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    <Activity className="h-3.5 w-3.5" />
                    <span>Mode B: Live Stream</span>
                  </button>
                </div>
              </div>

              {/* Dataset Selector */}
              <div className="lg:col-span-4 space-y-1.5">
                <label className="text-[11px] font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
                  <Database className="h-3.5 w-3.5 text-blue-600" />
                  <span>Evaluation Dataset</span>
                </label>
                <select
                  value={selectedDatasetId}
                  onChange={(e) => {
                    setSelectedDatasetId(e.target.value);
                    if (compareMode === 'benchmark' && selectedModelIds.length > 0) {
                      runComparison('benchmark', selectedModelIds, e.target.value);
                    }
                  }}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-medium text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 cursor-pointer"
                >
                  {datasets && datasets.length > 0 ? (
                    datasets.map((d) => (
                      <option key={d.id} value={d.id}>
                        {d.name || d.filename} ({d.dataset_type || 'NIDS'}{d.rows ? ` • ${d.rows.toLocaleString()} rows` : ''})
                      </option>
                    ))
                  ) : (
                    <option value="">Default Benchmark Dataset</option>
                  )}
                </select>
              </div>

              {/* Sample Size / Flow Count Limit */}
              <div className="lg:col-span-3 space-y-1.5">
                <label className="text-[11px] font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
                  <Sliders className="h-3.5 w-3.5 text-slate-500" />
                  <span>{compareMode === 'benchmark' ? 'Test Partition Samples' : 'Live Captured Limit'}</span>
                </label>
                {compareMode === 'benchmark' ? (
                  <select
                    value={testSamplesLimit}
                    onChange={(e) => {
                      const val = Number(e.target.value);
                      setTestSamplesLimit(val);
                      if (selectedModelIds.length > 0) {
                        runComparison('benchmark', selectedModelIds);
                      }
                    }}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-mono text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-purple-500/20 cursor-pointer"
                  >
                    <option value={500}>500 test records</option>
                    <option value={1000}>1,000 test records</option>
                    <option value={2500}>2,500 test records</option>
                    <option value={5000}>5,000 test records</option>
                    <option value={10000}>10,000 test records</option>
                    <option value={25000}>25,000 test records</option>
                    <option value={50000}>50,000 test records</option>
                  </select>
                ) : (
                  <select
                    value={liveLimit}
                    onChange={(e) => {
                      const val = Number(e.target.value);
                      setLiveLimit(val);
                      if (selectedModelIds.length > 0) {
                        runComparison('live', selectedModelIds);
                      }
                    }}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-mono text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-purple-500/20 cursor-pointer"
                  >
                    <option value={500}>500 recent live flows</option>
                    <option value={1000}>1,000 recent live flows</option>
                    <option value={2500}>2,500 recent live flows</option>
                    <option value={5000}>5,000 recent live flows</option>
                    <option value={10000}>10,000 recent live flows</option>
                    <option value={25000}>25,000 recent live flows</option>
                    <option value={50000}>50,000 recent live flows</option>
                  </select>
                )}
              </div>

            </div>

            {/* Model Multi-Select Checkboxes */}
            {allModels && allModels.length > 0 && (
              <div className="pt-3 border-t border-slate-100 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
                    <Layers className="h-3.5 w-3.5 text-purple-600" />
                    <span>Select Models to Compare ({selectedModelIds.length} of {allModels.length} selected)</span>
                  </span>
                  <div className="flex items-center space-x-2 text-[11px]">
                    <button
                      type="button"
                      onClick={() => {
                        const allIds = allModels.map(m => m.id);
                        setSelectedModelIds(allIds);
                        runComparison(compareMode, allIds);
                      }}
                      className="text-purple-600 hover:text-purple-800 font-bold hover:underline cursor-pointer"
                    >
                      Select All
                    </button>
                    <span className="text-slate-300">|</span>
                    <button
                      type="button"
                      onClick={() => {
                        const firstId = allModels.slice(0, 1).map(m => m.id);
                        setSelectedModelIds(firstId);
                        runComparison(compareMode, firstId);
                      }}
                      className="text-slate-500 hover:text-slate-800 font-medium hover:underline cursor-pointer"
                    >
                      Reset
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
                  {allModels.map((m) => {
                    const isSelected = selectedModelIds.includes(m.id);
                    return (
                      <div
                        key={m.id}
                        onClick={() => {
                          let nextIds;
                          if (isSelected) {
                            if (selectedModelIds.length === 1) return; // Keep at least 1
                            nextIds = selectedModelIds.filter(id => id !== m.id);
                          } else {
                            nextIds = [...selectedModelIds, m.id];
                          }
                          setSelectedModelIds(nextIds);
                          runComparison(compareMode, nextIds);
                        }}
                        className={`p-3 rounded-xl border text-xs cursor-pointer transition-all flex items-start space-x-3 ${
                          isSelected
                            ? 'bg-purple-50/60 border-purple-300 shadow-xs ring-1 ring-purple-400/30'
                            : 'bg-slate-50/50 border-slate-200 hover:bg-slate-100/70 opacity-75'
                        }`}
                      >
                        <div className="mt-0.5 shrink-0 text-purple-600">
                          {isSelected ? (
                            <CheckSquare className="h-4 w-4 text-purple-600" />
                          ) : (
                            <Square className="h-4 w-4 text-slate-400" />
                          )}
                        </div>
                        <div className="min-w-0 flex-1 space-y-0.5">
                          <div className="font-bold text-slate-900 truncate">{m.model_name || m.algorithm}</div>
                          <div className="text-[10px] text-slate-500 font-mono truncate">
                            {m.algorithm} • {m.dataset_name || 'Benchmark Dataset'}
                          </div>
                          {m.accuracy !== undefined && (
                            <div className="text-[10px] font-mono font-bold text-emerald-600">
                              Accuracy: {(m.accuracy * 100).toFixed(2)}%
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

          </div>

          {/* Loading State Skeleton */}
          {isComparing && !comparisonResult && (
            <div className="bg-white rounded-2xl p-12 text-center border border-slate-200/90 shadow-sm space-y-3">
              <RefreshCw className="h-8 w-8 text-purple-600 animate-spin mx-auto" />
              <h3 className="text-sm font-bold text-slate-800">Evaluating Models on Benchmark Partition...</h3>
              <p className="text-xs text-slate-500">Computing held-out test accuracy, precision, recall, F1, and confusion matrices.</p>
            </div>
          )}

          {/* No Models Available State */}
          {!loadingModels && allModels.length === 0 && (
            <div className="bg-white rounded-2xl p-12 text-center text-xs text-slate-400 border border-dashed border-slate-200 space-y-2">
              <Layers className="h-8 w-8 text-slate-400 mx-auto" />
              <p className="font-bold text-sm text-slate-800">No Trained Models Available</p>
              <p className="text-slate-500">Train models in the <strong>Model Training</strong> section to generate comparative benchmark matrices.</p>
            </div>
          )}

          {/* Error Banner */}
          {comparisonError && (
            <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center space-x-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{comparisonError}</span>
            </div>
          )}

          {/* ========================================================================= */}
          {/* RESULTS FOR MODE A: OFFLINE BENCHMARK COMPARISON */}
          {/* ========================================================================= */}
          {comparisonResult && comparisonResult.mode === 'benchmark' && (
            <div className="space-y-6">
              
              {/* Summary Winner Badges */}
              {comparisonResult.summary && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="bg-emerald-50/70 border border-emerald-200 rounded-xl p-3 text-xs space-y-1">
                    <div className="text-[10px] font-bold text-emerald-800 uppercase tracking-wider">HIGHEST ACCURACY</div>
                    <div className="font-bold text-emerald-950 truncate">{comparisonResult.summary.highest_accuracy?.name}</div>
                    <div className="text-lg font-black text-emerald-700">{((comparisonResult.summary.highest_accuracy?.value || 0) * 100).toFixed(2)}%</div>
                  </div>

                  <div className="bg-purple-50/70 border border-purple-200 rounded-xl p-3 text-xs space-y-1">
                    <div className="text-[10px] font-bold text-purple-800 uppercase tracking-wider">HIGHEST F1-SCORE</div>
                    <div className="font-bold text-purple-950 truncate">{comparisonResult.summary.highest_f1?.name}</div>
                    <div className="text-lg font-black text-purple-700">{((comparisonResult.summary.highest_f1?.value || 0) * 100).toFixed(2)}%</div>
                  </div>

                  <div className="bg-blue-50/70 border border-blue-200 rounded-xl p-3 text-xs space-y-1">
                    <div className="text-[10px] font-bold text-blue-800 uppercase tracking-wider">LOWEST FALSE POSITIVE RATE</div>
                    <div className="font-bold text-blue-950 truncate">{comparisonResult.summary.lowest_false_positive_rate?.name}</div>
                    <div className="text-lg font-black text-blue-700">{((comparisonResult.summary.lowest_false_positive_rate?.value || 0) * 100).toFixed(2)}%</div>
                  </div>

                  <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-3 text-xs space-y-1">
                    <div className="text-[10px] font-bold text-amber-800 uppercase tracking-wider">FASTEST INFERENCE</div>
                    <div className="font-bold text-amber-950 truncate">{comparisonResult.summary.lowest_inference_latency?.name}</div>
                    <div className="text-lg font-black text-amber-700">{(comparisonResult.summary.lowest_inference_latency?.value || 0).toFixed(3)} ms/sample</div>
                  </div>
                </div>
              )}

              {/* Main Comparison Matrix Table */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                  <div>
                    <h2 className="text-sm font-bold text-slate-900">
                      Standardized Evaluation Matrix (Held-Out Test Partition)
                    </h2>
                    <p className="text-xs text-slate-500">
                      Evaluated on {comparisonResult.test_samples} unseen records from {comparisonResult.dataset_name} ({comparisonResult.dataset_type}) using identical ground truth.
                    </p>
                  </div>
                  <span className="text-[11px] font-mono text-slate-400">
                    Duration: {comparisonResult.benchmark_duration_seconds}s
                  </span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                        <th className="py-2.5 px-3">Model / Algorithm</th>
                        <th className="py-2.5 px-3">Accuracy</th>
                        <th className="py-2.5 px-3">Precision</th>
                        <th className="py-2.5 px-3">Recall (Detection)</th>
                        <th className="py-2.5 px-3">F1-Score</th>
                        <th className="py-2.5 px-3">False Positive Rate</th>
                        <th className="py-2.5 px-3">Latency (ms)</th>
                        <th className="py-2.5 px-3">Throughput</th>
                        <th className="py-2.5 px-3">Size (KB)</th>
                        <th className="py-2.5 px-3">Convergence</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 font-mono">
                      {comparisonResult.models.map((m) => (
                        <tr key={m.model_id} className="hover:bg-slate-50/70 transition-colors">
                          <td className="py-3 px-3 font-sans">
                            <div className="font-bold text-slate-900">{m.model_name}</div>
                            <div className="text-[10px] text-slate-500">{m.algorithm} • {m.model_version}</div>
                          </td>
                          <td className="py-3 px-3 font-bold text-emerald-600">{(m.accuracy * 100).toFixed(2)}%</td>
                          <td className="py-3 px-3 font-bold text-blue-600">{(m.precision * 100).toFixed(2)}%</td>
                          <td className="py-3 px-3 font-bold text-indigo-600">{(m.recall * 100).toFixed(2)}%</td>
                          <td className="py-3 px-3 font-bold text-purple-600">{(m.f1_score * 100).toFixed(2)}%</td>
                          <td className="py-3 px-3 font-bold text-rose-600">{(m.false_positive_rate * 100).toFixed(2)}%</td>
                          <td className="py-3 px-3 text-slate-700">{m.prediction_latency_ms.toFixed(3)}</td>
                          <td className="py-3 px-3 text-slate-700">{m.throughput_samples_sec.toLocaleString()}/s</td>
                          <td className="py-3 px-3 text-slate-500">{m.model_size_kb} KB</td>
                          <td className="py-3 px-3 font-sans">
                            {m.converged ? (
                              <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                                Converged
                              </span>
                            ) : (
                              <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                                Warning
                              </span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Side-by-Side Confusion Matrices */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
                <h3 className="text-sm font-bold text-slate-900">
                  Side-by-Side Confusion Matrices (Normal vs Intrusion Attack)
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {comparisonResult.models.map((m) => {
                    const cm = m.confusion_matrix || [[0, 0], [0, 0]];
                    const tn = cm[0]?.[0] || 0;
                    const fp = cm[0]?.[1] || 0;
                    const fn = cm[1]?.[0] || 0;
                    const tp = cm[1]?.[1] || 0;

                    return (
                      <div key={m.model_id} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-3">
                        <div className="font-bold text-xs text-slate-900 truncate">{m.model_name}</div>
                        <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
                          <div className="p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg">
                            <div className="text-[10px] text-emerald-700 font-sans font-bold">True Negative (TN)</div>
                            <div className="text-base font-black text-emerald-800">{tn}</div>
                            <div className="text-[9px] text-slate-400 font-sans">Normal Identified</div>
                          </div>
                          <div className="p-2.5 bg-rose-50 border border-rose-200 rounded-lg">
                            <div className="text-[10px] text-rose-700 font-sans font-bold">False Positive (FP)</div>
                            <div className="text-base font-black text-rose-800">{fp}</div>
                            <div className="text-[9px] text-slate-400 font-sans">False Alarm</div>
                          </div>
                          <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg">
                            <div className="text-[10px] text-amber-700 font-sans font-bold">False Negative (FN)</div>
                            <div className="text-base font-black text-amber-800">{fn}</div>
                            <div className="text-[9px] text-slate-400 font-sans">Missed Attack</div>
                          </div>
                          <div className="p-2.5 bg-blue-50 border border-blue-200 rounded-lg">
                            <div className="text-[10px] text-blue-700 font-sans font-bold">True Positive (TP)</div>
                            <div className="text-base font-black text-blue-800">{tp}</div>
                            <div className="text-[9px] text-slate-400 font-sans">Attack Detected</div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

            </div>
          )}

          {/* ========================================================================= */}
          {/* RESULTS FOR MODE B: LIVE-SESSION COMPARISON */}
          {/* ========================================================================= */}
          {comparisonResult && comparisonResult.mode === 'live_session' && (
            ((comparisonResult?.total_flows || 0) === 0 || !comparisonResult?.models || comparisonResult.models.length === 0) ? (
              <div className="bg-white rounded-2xl p-12 text-center border border-slate-200/90 shadow-sm space-y-3">
                <Activity className="h-8 w-8 text-blue-600 mx-auto" />
                <h3 className="text-sm font-bold text-slate-800">Awaiting Live Network Traffic Capture</h3>
                <p className="text-xs text-slate-500 max-w-md mx-auto">
                  {comparisonResult.message || 'No live network packet flows have been captured yet. Start a live detection capture session or run a traffic replay to inspect multi-model live detections.'}
                </p>
              </div>
            ) : (
            <div className="space-y-6">
              
              {/* Transparency Notice */}
              <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-start space-x-3">
                <Info className="h-5 w-5 text-blue-600 shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <div className="font-bold">Ground-Truth Transparency Notice</div>
                  <p className="text-blue-800 leading-relaxed">
                    {comparisonResult.ground_truth_note} Inter-model agreement percentage, consensus classification, and alert frequency provide honest operational telemetry on unverified live traffic.
                  </p>
                </div>
              </div>

              {/* Consensus Summary KPI Bar */}
              {comparisonResult.consensus_summary && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div className="bg-white border border-slate-200 rounded-xl p-4 text-xs space-y-1">
                    <span className="text-[10px] font-bold text-slate-500 uppercase">FLOWS EVALUATED</span>
                    <div className="text-2xl font-black text-slate-900">{comparisonResult.consensus_summary.total_evaluated}</div>
                    <div className="text-[11px] text-slate-400">Captured packet flows analyzed</div>
                  </div>

                  <div className="bg-white border border-slate-200 rounded-xl p-4 text-xs space-y-1">
                    <span className="text-[10px] font-bold text-emerald-600 uppercase">UNANIMOUS AGREEMENT</span>
                    <div className="text-2xl font-black text-emerald-600">
                      {comparisonResult.consensus_summary.unanimous_rate}%
                    </div>
                    <div className="text-[11px] text-slate-400">
                      {comparisonResult.consensus_summary.unanimous_flows} of {comparisonResult.sample_flow_comparisons?.length || 0} sample flows
                    </div>
                  </div>

                  <div className="bg-white border border-slate-200 rounded-xl p-4 text-xs space-y-1">
                    <span className="text-[10px] font-bold text-purple-600 uppercase">MODELS IN CONSORTIUM</span>
                    <div className="text-2xl font-black text-purple-600">
                      {comparisonResult.consensus_summary.models_evaluated}
                    </div>
                    <div className="text-[11px] text-slate-400">Multi-model voting engine</div>
                  </div>
                </div>
              )}

              {/* Pairwise Agreement Matrix */}
              {comparisonResult.agreement_matrix && (
                <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
                  <h3 className="text-sm font-bold text-slate-900">
                    Pairwise Model Prediction Agreement Matrix (%)
                  </h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs border-collapse font-mono">
                      <thead>
                        <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-700">
                          <th className="py-2.5 px-3">Model</th>
                          {comparisonResult.models.map(m => (
                            <th key={m.model_id} className="py-2.5 px-3 text-center truncate max-w-[140px]" title={m.model_name}>
                              {m.model_name}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {comparisonResult.models.map(rowM => (
                          <tr key={rowM.model_id} className="hover:bg-slate-50/70">
                            <td className="py-2.5 px-3 font-sans font-bold text-slate-800">{rowM.model_name}</td>
                            {comparisonResult.models.map(colM => {
                              const score = comparisonResult.agreement_matrix[rowM.model_id]?.[colM.model_id];
                              const scoreVal = score !== undefined ? score : (rowM.model_id === colM.model_id ? 100 : 0);
                              return (
                                <td key={colM.model_id} className="py-2.5 px-3 text-center">
                                  <span className={`px-2 py-0.5 rounded font-bold ${
                                    scoreVal >= 95 ? 'bg-emerald-50 text-emerald-700' : scoreVal >= 85 ? 'bg-blue-50 text-blue-700' : 'bg-amber-50 text-amber-700'
                                  }`}>
                                    {scoreVal.toFixed(1)}%
                                  </span>
                                </td>
                              );
                            })}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Model Alert Breakdown in Live Session */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
                <h3 className="text-sm font-bold text-slate-900">
                  Retrospective Live Detection Behavior
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {comparisonResult.models.map((m) => (
                    <div key={m.model_id} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2 text-xs">
                      <div className="font-bold text-slate-900">{m.model_name}</div>
                      <div className="text-[10px] text-slate-500 font-mono">{m.algorithm} • {m.model_version}</div>
                      
                      <div className="space-y-1 pt-2 font-mono">
                        <div className="flex justify-between">
                          <span className="text-slate-500 font-sans">Normal Flows:</span>
                          <span className="font-bold text-emerald-600">{m.normal_count}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500 font-sans">Attack Alerts:</span>
                          <span className="font-bold text-rose-600">{m.attack_count}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500 font-sans">Alert Ratio:</span>
                          <span className="font-bold text-purple-600">{m.attack_ratio}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500 font-sans">Avg Confidence:</span>
                          <span className="font-bold text-slate-800">{(m.avg_confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500 font-sans">Replayed Latency:</span>
                          <span className="font-bold text-slate-700">{m.replayed_latency_ms.toFixed(3)} ms</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Flow-by-Flow Inspector Table */}
              {comparisonResult.sample_flow_comparisons && (
                <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
                  <h3 className="text-sm font-bold text-slate-900">
                    Flow-by-Flow Decision Inspector (Recent Captured Traffic)
                  </h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs border-collapse font-sans">
                      <thead>
                        <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                          <th className="py-2.5 px-3">Time</th>
                          <th className="py-2.5 px-3">Source → Destination</th>
                          <th className="py-2.5 px-3">Proto</th>
                          {comparisonResult.models.map(m => (
                            <th key={m.model_id} className="py-2.5 px-3 truncate max-w-[120px]">{m.model_name}</th>
                          ))}
                          <th className="py-2.5 px-3 text-center">Consensus</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                        {comparisonResult.sample_flow_comparisons.map((flow) => (
                          <tr key={flow.id} className="hover:bg-slate-50/70">
                            <td className="py-2.5 px-3 text-slate-500">{flow.timestamp}</td>
                            <td className="py-2.5 px-3 text-slate-800">{flow.src} → {flow.dst}</td>
                            <td className="py-2.5 px-3 text-slate-600">{flow.protocol}</td>
                            {comparisonResult.models.map(m => {
                              const pred = flow.predictions[String(m.model_id)] || 'Normal';
                              const isAtk = pred !== 'Normal';
                              return (
                                <td key={m.model_id} className="py-2.5 px-3">
                                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                    isAtk ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                  }`}>
                                    {pred}
                                  </span>
                                </td>
                              );
                            })}
                            <td className="py-2.5 px-3 text-center">
                              {flow.unanimous ? (
                                <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                                  ✓ Unanimous
                                </span>
                              ) : (
                                <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                                  Divided
                                </span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

            </div>
            )
          )}

        </div>
      )}

      {/* ========================================================================= */}
      {/* VIEW 2: ORIGINAL DATASET SPECIFICATIONS MATRIX */}
      {/* ========================================================================= */}
      {activeMainTab === 'datasets' && (
        <div className="space-y-6">
          <div className="flex flex-wrap items-center gap-2 font-mono text-xs">
            <span className="text-xs font-bold font-sans text-slate-700 mr-2">Toggle Datasets:</span>
            {(datasets || []).map(d => {
              const displayName = d.name || d.filename || 'dataset.csv';
              return (
                <button
                  key={d.id || displayName}
                  onClick={() => toggleCompareDataset && toggleCompareDataset(d.id)}
                  className={`px-3 py-1.5 rounded-lg font-semibold transition-all active:scale-95 border cursor-pointer ${
                    d.isCompared
                      ? 'bg-purple-600 text-white border-purple-600 shadow-xs'
                      : 'bg-white text-slate-600 border-slate-300 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  {d.isCompared ? '✓ ' : '+ '}{displayName.replace('.csv','')}
                </button>
              );
            })}
          </div>

          {comparedItems.length === 0 ? (
            <div className="bg-white p-12 text-center text-xs text-slate-400 rounded-2xl space-y-3 border border-dashed border-slate-200">
              <Layers className="h-8 w-8 text-slate-400 mx-auto" />
              <p className="font-bold text-sm text-slate-800">No Datasets Selected for Comparison</p>
              <p className="text-slate-500">Click any of the dataset buttons above to add it to the comparison matrix.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {comparedItems.map(ds => {
                const displayName = ds.name || ds.filename || 'dataset.csv';
                const dsType = ds.type || ds.dataset_type || 'Custom';
                const nameLower = (displayName + dsType).toLowerCase();
                const isNsl = nameLower.includes('nsl');
                const isUnsw = nameLower.includes('unsw');
                const isCic = nameLower.includes('cic');

                const totalRows = ds.totalRows || (isCic ? 2830743 : isUnsw ? 2540044 : 148517);
                const trainingRows = ds.trainingRows || (isNsl ? 148517 : 25000);
                const numFeatures = ds.features || (isCic ? 78 : isUnsw ? 48 : 41);
                const numClasses = ds.classes || (isCic ? 15 : isUnsw ? 10 : 5);
                const missingCount = ds.missing !== undefined ? ds.missing : (isCic ? 2886 : 0);
                const dupCount = ds.duplicates !== undefined ? ds.duplicates : (isCic ? 1012 : isUnsw ? 42 : 0);
                const purposeText = ds.purpose || (isCic ? 'High-Volume DDoS & Web Attack Identification' : isUnsw ? 'Modern Complex Network Flow Analysis' : 'Benchmark Intrusion Detection System');

                return (
                  <div 
                    key={ds.id || displayName} 
                    className={`bg-white rounded-2xl p-6 space-y-4 relative border transition-all ${
                      ds.isSelected 
                        ? 'border-2 border-blue-500 ring-4 ring-blue-500/10 shadow-md' 
                        : 'border-slate-200/90 shadow-sm'
                    }`}
                  >
                    {ds.isSelected && (
                      <span className="absolute top-4 right-4 text-[9px] font-mono font-bold bg-blue-50 text-blue-600 px-2.5 py-0.5 rounded-full border border-blue-200">
                        ACTIVE TARGET
                      </span>
                    )}

                    <div className="flex items-center space-x-2.5 border-b border-slate-100 pb-3">
                      <FileSpreadsheet className="h-5 w-5 text-blue-600 shrink-0" />
                      <h3 className="text-sm font-bold text-slate-900 truncate max-w-[220px]" title={displayName}>
                        {displayName}
                      </h3>
                    </div>

                    <div className="space-y-2 text-xs text-slate-600 font-sans">
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Dataset Standard:</span>
                        <span className="text-slate-900 font-bold">{dsType}</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Total Benchmark Rows:</span>
                        <span className="text-slate-900 font-bold font-mono">{totalRows.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Configured Training Rows:</span>
                        <span className="text-emerald-600 font-bold font-mono">{trainingRows.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Feature Count:</span>
                        <span className="text-slate-900 font-bold font-mono">{numFeatures} Features</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Classification Classes:</span>
                        <span className="text-slate-900 font-bold font-mono">{numClasses} Classes</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Missing / Inf Rows:</span>
                        <span className="text-slate-900 font-bold font-mono">{missingCount}</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Duplicate Flow Rows:</span>
                        <span className="text-slate-900 font-bold font-mono">{dupCount}</span>
                      </div>
                      <div className="pt-2">
                        <span className="text-slate-500 block mb-1">Analytical Purpose:</span>
                        <p className="text-[11px] text-slate-700 bg-slate-50 p-2.5 rounded-xl border border-slate-200/80 leading-relaxed font-sans">
                          {purposeText}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* FOOTER */}
      <footer className="text-center text-xs text-slate-500 font-medium pt-4">
        Zero-Trust Multi-Model Network Intrusion Detection System • Version 2.0
      </footer>

    </div>
  );
};
