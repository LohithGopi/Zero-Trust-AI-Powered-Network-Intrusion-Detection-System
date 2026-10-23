import re

filepath = "frontend/src/pages/dashboard/CompareView.jsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update lucide-react imports if needed
old_imports = """import { 
  FileSpreadsheet, Layers, GitBranch, Play, CheckCircle2, 
  AlertCircle, RefreshCw, Activity, Zap, ShieldAlert, 
  Cpu, ArrowRight, BarChart3, Clock, Check, HelpCircle, Info
} from 'lucide-react';"""

new_imports = """import { 
  FileSpreadsheet, Layers, GitBranch, Play, CheckCircle2, 
  AlertCircle, RefreshCw, Activity, Zap, ShieldAlert, 
  Cpu, ArrowRight, BarChart3, Clock, Check, HelpCircle, Info,
  Sliders, Database, CheckSquare, Square
} from 'lucide-react';"""

if old_imports in content:
    content = content.replace(old_imports, new_imports)

# 2. Add selectedDatasetId state and update runComparison
old_state = """  // Comparison Mode for Models: 'benchmark' (Mode A) vs 'live' (Mode B)
  const [compareMode, setCompareMode] = useState('benchmark');

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

  // Fetch trained models on mount and automatically run benchmark comparison
  useEffect(() => {
    fetchModels();
  }, []);

  const runBenchmark = async (targetModelIds = null) => {
    const ids = (targetModelIds && targetModelIds.length > 0) ? targetModelIds : selectedModelIds;
    if (!ids || ids.length === 0) return;

    setIsComparing(true);
    setComparisonError('');

    try {
      const res = await apiCompareBenchmark({
        model_ids: ids,
        test_samples_limit: Number(testSamplesLimit) || 1000
      });
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
          runBenchmark(defaultSelected);
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

  // Run Comparison Engine
  const handleRunComparison = async () => {
    runBenchmark();
  };"""

new_state = """  // Comparison Mode for Models: 'benchmark' (Mode A) vs 'live' (Mode B)
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
  };"""

if old_state in content:
    content = content.replace(old_state, new_state)
else:
    print("Warning: old_state not matched exactly")

# 3. Insert the Model & Dataset Configuration Card in VIEW 1
old_subhead = """          {/* Streamlined Subheader & Action Bar */}
          <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center space-x-2.5">
              <div className="p-2 bg-purple-50 text-purple-600 rounded-xl border border-purple-100">
                <BarChart3 className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-slate-900">
                  Standardized Multi-Model Benchmark Comparison
                </h2>
                <p className="text-xs text-slate-500">
                  Side-by-side evaluation across Support Vector Machine, Logistic Regression, and LSTM on identical held-out test data.
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2 self-end sm:self-auto">
              <button
                onClick={() => runBenchmark()}
                disabled={isComparing}
                className="px-3.5 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-bold text-xs flex items-center space-x-2 shadow-xs transition-all active:scale-95 cursor-pointer"
              >
                <RefreshCw className={`h-3.5 w-3.5 ${isComparing ? 'animate-spin' : ''}`} />
                <span>{isComparing ? 'Evaluating Models...' : 'Refresh Benchmark'}</span>
              </button>
            </div>
          </div>"""

new_subhead = """          {/* Streamlined Subheader & Action Bar */}
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
                    <option value={25}>25 recent live flows</option>
                    <option value={50}>50 recent live flows</option>
                    <option value={100}>100 recent live flows</option>
                    <option value={200}>200 recent live flows</option>
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

          </div>"""

if old_subhead in content:
    content = content.replace(old_subhead, new_subhead)
else:
    print("Warning: old_subhead not matched exactly")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("CompareView.jsx updated successfully!")
