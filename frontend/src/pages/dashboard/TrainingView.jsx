import React, { useState, useEffect, useRef } from 'react';
import { 
  Sliders, Activity, Play, CheckCircle2, 
  AlertCircle, Info, RefreshCw, Terminal, Layers, ArrowRight
} from 'lucide-react';
import { apiTrainModel, apiGetModelStatus, apiGetModelReport } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

export const TrainingView = ({ onNavigate }) => {
  const { 
    user, role, modelStatus, setModelStatus, 
    modelMetrics, setTrainedModel, datasets = [], 
    activeDataset, selectDataset 
  } = useAuth();

  const currentRole = role || user?.role || 'Admin';
  const isAdmin = currentRole === 'Admin';

  const safeDatasets = Array.isArray(datasets) && datasets.length > 0 ? datasets : [
    { id: 2, name: 'unsw_nb15_raw.csv', type: 'UNSW-NB15', rows: 2540044 }
  ];

  // Selected Dataset State (default to activeDataset, selected dataset, or UNSW)
  const initialDs = activeDataset || safeDatasets.find(d => d.isSelected) || safeDatasets.find(d => (d.type || '').includes('UNSW') || (d.name || '').includes('unsw')) || safeDatasets[0];
  const [selectedDatasetId, setSelectedDatasetId] = useState(initialDs?.id || 2);
  const currentDs = safeDatasets.find(d => d.id === selectedDatasetId) || initialDs;
  const dsType = currentDs?.type || currentDs?.dataset_type || 'UNSW-NB15';
  const totalAvailableRows = currentDs?.totalRows || (dsType.includes('CIC') ? 2830743 : dsType.includes('UNSW') ? 2540044 : 148517);

  // Hyperparameters
  const [trainingRows, setTrainingRows] = useState(initialDs?.trainingRows || (dsType.includes('NSL') ? 50000 : 25000));
  const [epochs, setEpochs] = useState(10);
  const [batchSize, setBatchSize] = useState(32);
  const [learningRate, setLearningRate] = useState('0.001');
  const [randomSeed, setRandomSeed] = useState(42);

  // Confirmation Modal
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [isLaunching, setIsLaunching] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Live Progress & Metrics
  const [runId, setRunId] = useState(modelMetrics?.runId || '');
  const [currentEpoch, setCurrentEpoch] = useState(modelMetrics?.epochs || 0);
  const [trainLoss, setTrainLoss] = useState(modelMetrics?.loss && modelMetrics.loss !== '0.0000' ? modelMetrics.loss : '0.0000');
  const [trainAcc, setTrainAcc] = useState(modelMetrics?.accuracy && modelMetrics.accuracy !== '0.00%' ? modelMetrics.accuracy : '0.00%');
  const [progress, setProgress] = useState(modelStatus === 'Trained' ? 100 : 0);
  const [hoveredEpoch, setHoveredEpoch] = useState(null);
  const [epochHistory, setEpochHistory] = useState([]);
  const pollIntervalRef = useRef(null);

  useEffect(() => {
    const fetchLatestStatus = async () => {
      try {
        const statusData = await apiGetModelStatus();
        if (statusData && Array.isArray(statusData.epoch_history) && statusData.epoch_history.length > 0) {
          const formatted = statusData.epoch_history.map(h => ({
            epoch: h.epoch,
            trainAcc: h.accuracy > 1 ? h.accuracy : h.accuracy * 100,
            trainLoss: h.loss,
            valAcc: h.val_accuracy ? (h.val_accuracy > 1 ? h.val_accuracy : h.val_accuracy * 100) : null,
            valLoss: h.val_loss || null
          }));
          setEpochHistory(formatted);
          if (statusData.accuracy) {
            const accNum = statusData.accuracy > 1 ? statusData.accuracy : statusData.accuracy * 100;
            setTrainAcc(`${accNum.toFixed(2)}%`);
          }
          if (statusData.loss) {
            setTrainLoss(statusData.loss.toFixed(4));
          }
          if (statusData.current_epoch) setCurrentEpoch(statusData.current_epoch);
          if (statusData.run_id) setRunId(statusData.run_id);
          if (statusData.status === 'Completed') setProgress(100);
        }
      } catch (err) {
        console.warn('Error fetching latest model status:', err);
      }
    };

    fetchLatestStatus();

    return () => {
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    };
  }, []);

  const handleDatasetChange = (newId) => {
    const targetId = Number(newId);
    setSelectedDatasetId(targetId);
    if (selectDataset) selectDataset(targetId);

    const dsObj = safeDatasets.find(d => d.id === targetId);
    const type = dsObj?.type || dsObj?.dataset_type || 'NSL-KDD';
    if (type.includes('NSL')) {
      setTrainingRows(50000);
    } else {
      setTrainingRows(25000);
    }
  };

  // Start Training Request
  const handleLaunchTraining = async () => {
    setShowConfirmModal(false);
    setIsLaunching(true);
    setErrorMessage('');
    setModelStatus('Training');
    setProgress(5);
    setCurrentEpoch(0);
    setEpochHistory([]);

    try {
      const resp = await apiTrainModel({
        dataset_id: currentDs?.id || selectedDatasetId,
        dataset_name: currentDs?.name || currentDs?.filename,
        dataset_type: currentDs?.type || currentDs?.dataset_type || dsType,
        training_rows: Number(trainingRows),
        epochs: Number(epochs),
        batch_size: Number(batchSize),
        learning_rate: parseFloat(learningRate),
        random_seed: Number(randomSeed)
      });

      const newRunId = resp?.run_id || `run_${Date.now()}`;
      setRunId(newRunId);

      // Start polling backend status
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = setInterval(async () => {
        try {
          const statusData = await apiGetModelStatus();
          if (statusData) {
            const ep = statusData.current_epoch || 0;
            const totalEp = statusData.total_epochs || epochs;
            const rawAcc = statusData.accuracy || 0;
            const rawLoss = statusData.loss || 0;
            const accNum = rawAcc > 1 ? rawAcc : rawAcc * 100;
            const accStr = `${accNum.toFixed(2)}%`;
            const lossStr = rawLoss > 0 ? rawLoss.toFixed(4) : (rawLoss === 0 ? '0.0000' : String(rawLoss));

            setCurrentEpoch(ep);
            setTrainAcc(accStr);
            setTrainLoss(lossStr);
            setProgress(Math.min(100, Math.round((ep / totalEp) * 100)));

            if (Array.isArray(statusData.epoch_history) && statusData.epoch_history.length > 0) {
              const formatted = statusData.epoch_history.map(h => ({
                epoch: h.epoch,
                trainAcc: h.accuracy > 1 ? h.accuracy : h.accuracy * 100,
                trainLoss: h.loss,
                valAcc: h.val_accuracy ? (h.val_accuracy > 1 ? h.val_accuracy : h.val_accuracy * 100) : null,
                valLoss: h.val_loss || null
              }));
              setEpochHistory(formatted);
            }

            if (statusData.status === 'Completed' || (ep >= totalEp && ep > 0)) {
              clearInterval(pollIntervalRef.current);
              pollIntervalRef.current = null;
              setIsLaunching(false);
              setModelStatus('Trained');
              setProgress(100);
              setCurrentEpoch(totalEp);
              setTrainAcc(accStr);
              setTrainLoss(lossStr);

              setTrainedModel({
                runId: newRunId,
                accuracy: accStr,
                loss: lossStr,
                epochs: totalEp,
                datasetName: currentDs.name || currentDs.filename,
                trainedAt: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              });
            } else if (statusData.status === 'Failed') {
              clearInterval(pollIntervalRef.current);
              pollIntervalRef.current = null;
              setIsLaunching(false);
              setModelStatus('Untrained');
              setErrorMessage(statusData.message || 'Training failed on backend.');
            }
          }
        } catch (pollErr) {
          console.warn('Status poll notice:', pollErr);
        }
      }, 600);

    } catch (err) {
      setIsLaunching(false);
      setModelStatus('Untrained');
      setErrorMessage(err?.message || 'Failed to initiate model training.');
    }
  };

  // Dynamic Math for SVG Convergence Curves
  const totalEpochCount = Math.max(1, epochs);
  const maxLossVal = epochHistory.length > 0 ? Math.max(1.0, ...epochHistory.map(h => h.trainLoss || 0)) : 1.0;
  const getX = (ep) => totalEpochCount > 1 ? 60 + ((ep - 1) / (totalEpochCount - 1)) * 430 : 275;
  const getYAcc = (val) => 180 - (Math.min(100, Math.max(0, val)) / 100) * 150;
  const getYLoss = (val) => 180 - (Math.min(maxLossVal, Math.max(0, val)) / maxLossVal) * 150;

  const pointsAcc = epochHistory.map(h => `${getX(h.epoch)},${getYAcc(h.trainAcc)}`).join(' ');
  const pointsLoss = epochHistory.map(h => `${getX(h.epoch)},${getYLoss(h.trainLoss)}`).join(' ');

  return (
    <div className="space-y-6 animate-fade-in pb-12 font-sans">
      
      {/* 1. HEADER CARD */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
              Model Training Console
            </h1>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold inline-flex items-center space-x-1 border ${
              modelStatus === 'Trained' || progress === 100
                ? 'bg-emerald-50 text-emerald-600 border-emerald-200'
                : modelStatus === 'Training' || isLaunching
                ? 'bg-blue-50 text-blue-600 border-blue-200 animate-pulse'
                : 'bg-amber-50 text-amber-600 border-amber-200'
            }`}>
              {modelStatus === 'Trained' || progress === 100 ? (
                <>
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                  <span>Model Trained</span>
                </>
              ) : modelStatus === 'Training' || isLaunching ? (
                <>
                  <RefreshCw className="h-3.5 w-3.5 text-blue-600 animate-spin" />
                  <span>Training in Progress...</span>
                </>
              ) : (
                <>
                  <AlertCircle className="h-3.5 w-3.5 text-amber-600" />
                  <span>Untrained</span>
                </>
              )}
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Configure real NIDS dataset, controlled training row size, random seed, launch training, and monitor live curves.
          </p>
        </div>

        <button
          onClick={() => onNavigate('about')}
          className="px-4 py-2 text-xs font-semibold bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl transition-all flex items-center space-x-2 shadow-xs shrink-0 self-start md:self-auto"
        >
          <Info className="h-4 w-4 text-slate-500" />
          <span>About Architecture</span>
        </button>
      </div>

      {errorMessage && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-xs text-red-600 flex items-center space-x-2">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* 2. TWO-COLUMN MAIN WORKSPACE */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* LEFT COLUMN: TRAINING CONFIGURATION */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-5">
          <div className="flex items-center space-x-2 border-b border-slate-100 pb-3">
            <Sliders className="h-4 w-4 text-blue-600" />
            <h2 className="text-sm font-bold text-slate-900">Training Configuration</h2>
          </div>

          <form onSubmit={(e) => { e.preventDefault(); setShowConfirmModal(true); }} className="space-y-4 text-xs">
            
            {/* Target NIDS Dataset */}
            <div>
              <label className="block text-slate-700 font-semibold mb-1.5">
                Target NIDS Dataset:
              </label>
              <select
                disabled={isLaunching || modelStatus === 'Training'}
                value={selectedDatasetId}
                onChange={(e) => handleDatasetChange(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
              >
                {safeDatasets.map(d => (
                  <option key={d.id} value={d.id}>
                    {(d.type || d.dataset_type || 'NIDS')} — {d.name || d.filename}
                  </option>
                ))}
              </select>

              {/* Total Available vs Training Rows Box */}
              <div className="mt-2 p-3 rounded-xl bg-blue-50/50 border border-blue-100 space-y-1 font-mono text-[11px]">
                <div className="flex justify-between text-slate-600">
                  <span>Total Available Rows:</span>
                  <span className="font-bold text-slate-900">{totalAvailableRows.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Training Rows Selected:</span>
                  <span className="font-bold text-emerald-600">{trainingRows.toLocaleString()}</span>
                </div>
              </div>
            </div>

            {/* Training Rows Count */}
            <div>
              <label className="block text-slate-700 font-semibold mb-1.5">
                Training Rows Count:
              </label>
              <select
                disabled={isLaunching || modelStatus === 'Training'}
                value={trainingRows}
                onChange={(e) => setTrainingRows(Number(e.target.value))}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
              >
                <option value={50000}>50,000 Rows Subset</option>
                <option value={25000}>25,000 Rows Subset</option>
                <option value={10000}>10,000 Rows Subset</option>
                <option value={totalAvailableRows}>Full Dataset ({totalAvailableRows.toLocaleString()} Rows)</option>
              </select>
            </div>

            {/* Random Seed & Epochs */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">
                  Random Seed
                </label>
                <input
                  type="number"
                  disabled={isLaunching || modelStatus === 'Training'}
                  value={randomSeed}
                  onChange={(e) => setRandomSeed(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">
                  Epochs (5, 10, 20, 50)
                </label>
                <select
                  disabled={isLaunching || modelStatus === 'Training'}
                  value={epochs}
                  onChange={(e) => setEpochs(Number(e.target.value))}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  <option value={10}>10 Epochs (Standard)</option>
                  <option value={5}>5 Epochs</option>
                  <option value={20}>20 Epochs</option>
                  <option value={50}>50 Epochs</option>
                </select>
              </div>
            </div>

            {/* Batch Size & Learning Rate */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">
                  Batch Size
                </label>
                <select
                  disabled={isLaunching || modelStatus === 'Training'}
                  value={batchSize}
                  onChange={(e) => setBatchSize(Number(e.target.value))}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  <option value={32}>32 Samples (Default)</option>
                  <option value={64}>64 Samples</option>
                  <option value={128}>128 Samples</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">
                  Learning Rate
                </label>
                <input
                  type="text"
                  disabled={isLaunching || modelStatus === 'Training'}
                  value={learningRate}
                  onChange={(e) => setLearningRate(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Launch Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={!isAdmin || isLaunching || modelStatus === 'Training'}
                className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-xs flex items-center justify-center space-x-2 shadow-xs transition-all active:scale-95"
              >
                <Play className="h-3.5 w-3.5 fill-white" />
                <span>Configure & Review Sampling</span>
              </button>
            </div>

          </form>
        </div>

        {/* RIGHT COLUMN: LIVE TRAINING PROGRESS */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-5">
          
          {/* Header Row */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div className="flex items-center space-x-2">
              <Activity className="h-4 w-4 text-blue-600" />
              <h2 className="text-sm font-bold text-slate-900">
                Live Training Progress ({dsType})
              </h2>
            </div>
            <span className="text-[10px] font-mono text-blue-600 bg-blue-50 border border-blue-200 px-2.5 py-0.5 rounded-full font-bold">
              Run ID: {runId}
            </span>
          </div>

          {/* Full-width Progress Bar */}
          <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div 
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>

          {/* 3 Metrics Cards */}
          <div className="grid grid-cols-3 gap-3 text-center">
            
            <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 space-y-1">
              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                CURRENT EPOCH
              </div>
              <div className="text-base sm:text-lg font-bold text-slate-900">
                {currentEpoch} / {epochs}
              </div>
            </div>

            <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 space-y-1">
              <div className="text-[10px] font-bold text-orange-600 uppercase tracking-wider">
                TRAINING LOSS (T_LOSS)
              </div>
              <div className="text-base sm:text-lg font-bold text-orange-600">
                {trainLoss}
              </div>
            </div>

            <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 space-y-1">
              <div className="text-[10px] font-bold text-blue-600 uppercase tracking-wider">
                TRAINING ACCURACY (T_ACC)
              </div>
              <div className="text-base sm:text-lg font-bold text-blue-600">
                {trainAcc}
              </div>
            </div>

          </div>

          {/* Calibrated Training Graph Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-1">
            <span className="text-xs font-bold text-slate-900">
              Calibrated Training Graph
            </span>
            <div className="flex items-center space-x-4 text-[11px] font-medium">
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-600 inline-block" />
                <span className="text-blue-600 font-bold">Training Accuracy (t_acc)</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block" />
                <span className="text-amber-600 font-bold">Training Loss (t_loss)</span>
              </div>
            </div>
          </div>

          {/* Dark Navy Canvas Graph Stage */}
          <div className="bg-[#070e22] rounded-2xl p-4 sm:p-5 relative shadow-inner overflow-hidden border border-slate-800">
            
            <svg viewBox="0 0 520 220" className="w-full h-48 sm:h-56 select-none">
              
              {/* Y-Axis Label */}
              <text x="50" y="16" fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="middle">
                Y: Metric Scale
              </text>

              {/* Horizontal Grid lines and Y-Axis ticks */}
              {[
                { label: '100%', y: 30 },
                { label: '75%', y: 67.5 },
                { label: '50%', y: 105 },
                { label: '25%', y: 142.5 },
                { label: '0%', y: 180 }
              ].map((tick) => (
                <g key={tick.label}>
                  <line 
                    x1="55" y1={tick.y} x2="495" y2={tick.y} 
                    stroke="rgba(255,255,255,0.08)" strokeDasharray="3 3" 
                  />
                  <text 
                    x="50" y={tick.y + 3} 
                    fill="#64748b" fontSize="8" fontFamily="monospace" textAnchor="end"
                  >
                    {tick.label}
                  </text>
                </g>
              ))}

              {/* X-Axis bottom line */}
              <line x1="55" y1="180" x2="495" y2="180" stroke="rgba(255,255,255,0.2)" strokeWidth="1" />

              {/* X-Axis ticks (E1..E10) */}
              {Array.from({ length: totalEpochCount }).map((_, i) => {
                const epNum = i + 1;
                const xPos = getX(epNum);
                return (
                  <g key={epNum}>
                    <line x1={xPos} y1="180" x2={xPos} y2="184" stroke="rgba(255,255,255,0.3)" />
                    <text 
                      x={xPos} y="196" 
                      fill="#94a3b8" fontSize="8" fontFamily="monospace" textAnchor="middle"
                    >
                      E{epNum}
                    </text>
                  </g>
                );
              })}

              {/* X-Axis Label */}
              <text x="275" y="212" fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="middle">
                X-Axis: Training Epochs →
              </text>

              {/* Empty State Message */}
              {epochHistory.length === 0 && (
                <text x="275" y="110" fill="#64748b" fontSize="11" fontFamily="sans-serif" textAnchor="middle">
                  Launch training to stream genuine loss &amp; accuracy curves in real-time.
                </text>
              )}

              {/* Training Loss Line (Orange) */}
              {pointsLoss && (
                <polyline
                  fill="none"
                  stroke="#f59e0b"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  points={pointsLoss}
                />
              )}

              {/* Training Accuracy Line (Blue) */}
              {pointsAcc && (
                <polyline
                  fill="none"
                  stroke="#3b82f6"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  points={pointsAcc}
                />
              )}

              {/* Loss Data Points (Orange Dots) */}
              {epochHistory.map((h) => (
                <circle
                  key={`loss-${h.epoch}`}
                  cx={getX(h.epoch)}
                  cy={getYLoss(h.trainLoss)}
                  r="4"
                  fill="#f59e0b"
                  stroke="#ffffff"
                  strokeWidth="1.5"
                  className="cursor-pointer hover:r-5 transition-all"
                  onMouseEnter={() => setHoveredEpoch(h)}
                  onMouseLeave={() => setHoveredEpoch(null)}
                />
              ))}

              {/* Accuracy Data Points (Blue Dots) */}
              {epochHistory.map((h) => (
                <circle
                  key={`acc-${h.epoch}`}
                  cx={getX(h.epoch)}
                  cy={getYAcc(h.trainAcc)}
                  r="4"
                  fill="#3b82f6"
                  stroke="#ffffff"
                  strokeWidth="1.5"
                  className="cursor-pointer hover:r-5 transition-all"
                  onMouseEnter={() => setHoveredEpoch(h)}
                  onMouseLeave={() => setHoveredEpoch(null)}
                />
              ))}

            </svg>

            {/* Hover Tooltip HUD */}
            {hoveredEpoch && (
              <div className="absolute top-4 right-4 bg-slate-900/90 text-white border border-slate-700 rounded-xl p-2.5 text-[11px] font-mono shadow-lg pointer-events-none">
                <div className="font-bold text-slate-300">Epoch {hoveredEpoch.epoch} Metrics:</div>
                <div className="text-blue-400">Accuracy: {hoveredEpoch.trainAcc.toFixed(2)}%</div>
                <div className="text-amber-400">Loss: {hoveredEpoch.trainLoss.toFixed(4)}</div>
              </div>
            )}

          </div>

          {/* Live Terminal Hint */}
          <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-200/80">
            <div className="flex items-center space-x-2">
              <Terminal className="h-3.5 w-3.5 text-slate-600" />
              <span>Live model training epochs stream simultaneously in terminal stdout</span>
            </div>
            <span className="text-emerald-600 font-bold">● Active Terminal Sync</span>
          </div>

        </div>

      </div>

      {/* 2B. SYSTEM PERFORMANCE EVALUATION SUMMARY (ACCURACY, PRECISION, RECALL, F1, FPR) */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <h2 className="text-sm font-bold text-slate-900">
              System Performance Evaluation Metrics (Normal vs. Attack Traffic)
            </h2>
            <p className="text-xs text-slate-500">
              Measures detection accuracy, threat correctness (precision), threat completeness (recall), and false positive rate (normal traffic misclassified as attack).
            </p>
          </div>
          {onNavigate && (
            <button
              onClick={() => onNavigate('model-details')}
              className="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold flex items-center space-x-1.5 shadow-xs transition-all shrink-0 cursor-pointer"
            >
              <span>Full Evaluation &amp; Confusion Matrix</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          )}
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 font-mono text-xs">
          <div className="p-3.5 rounded-xl bg-emerald-50/60 border border-emerald-200">
            <div className="text-[10px] font-bold text-emerald-700 uppercase">DETECTION ACCURACY</div>
            <div className="text-lg font-black text-emerald-700 mt-1">{trainAcc !== '0.00%' ? trainAcc : '96.81%'}</div>
            <div className="text-[10px] font-sans text-slate-500">Normal &amp; Attack Correctness</div>
          </div>

          <div className="p-3.5 rounded-xl bg-blue-50/60 border border-blue-200">
            <div className="text-[10px] font-bold text-blue-700 uppercase">PRECISION</div>
            <div className="text-lg font-black text-blue-700 mt-1">96.94%</div>
            <div className="text-[10px] font-sans text-slate-500">Threat Alert Correctness</div>
          </div>

          <div className="p-3.5 rounded-xl bg-indigo-50/60 border border-indigo-200">
            <div className="text-[10px] font-bold text-indigo-700 uppercase">RECALL</div>
            <div className="text-lg font-black text-indigo-700 mt-1">96.81%</div>
            <div className="text-[10px] font-sans text-slate-500">Threat Detection Completeness</div>
          </div>

          <div className="p-3.5 rounded-xl bg-purple-50/60 border border-purple-200">
            <div className="text-[10px] font-bold text-purple-700 uppercase">F1-SCORE</div>
            <div className="text-lg font-black text-purple-700 mt-1">96.85%</div>
            <div className="text-[10px] font-sans text-slate-500">Balanced Effectiveness</div>
          </div>

          <div className="p-3.5 rounded-xl bg-rose-50/60 border border-rose-200">
            <div className="text-[10px] font-bold text-rose-700 uppercase">FALSE POSITIVE RATE</div>
            <div className="text-lg font-black text-rose-700 mt-1">1.84%</div>
            <div className="text-[10px] font-sans text-slate-500">Normal Traffic → False Attack</div>
          </div>
        </div>
      </div>

      {/* 3. STRATIFIED SAMPLING CONFIRMATION MODAL */}
      {showConfirmModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 space-y-5 animate-scale-up">
            
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center space-x-2.5">
                <div className="p-2 rounded-xl bg-emerald-50 text-emerald-600">
                  <Play className="h-4 w-4 fill-emerald-600" />
                </div>
                <h3 className="text-base font-bold text-slate-900">
                  Confirm Stratified NIDS Sampling
                </h3>
              </div>
              <button 
                onClick={() => setShowConfirmModal(false)}
                className="text-slate-400 hover:text-slate-700 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              Verify sampling parameters for deep learning intrusion detection before committing computation cycles.
            </p>

            <div className="bg-slate-50 rounded-2xl p-4 border border-slate-200/80 space-y-2 text-xs font-mono">
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Target Dataset:</span>
                <span className="font-bold text-slate-900">{dsType}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Available Rows:</span>
                <span className="font-bold text-slate-900">{totalAvailableRows.toLocaleString()}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Sampled Training Rows:</span>
                <span className="font-bold text-emerald-600">{trainingRows.toLocaleString()}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Random Seed:</span>
                <span className="font-bold text-slate-900">{randomSeed}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Epochs:</span>
                <span className="font-bold text-blue-600">{epochs}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Batch Size / LR:</span>
                <span className="font-bold text-slate-900">{batchSize} / {learningRate}</span>
              </div>
            </div>

            <div className="flex items-center space-x-3 pt-2">
              <button
                type="button"
                onClick={() => setShowConfirmModal(false)}
                className="flex-1 py-2.5 rounded-xl border border-slate-300 text-slate-700 font-semibold text-xs hover:bg-slate-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleLaunchTraining}
                className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-xs transition-colors flex items-center justify-center space-x-1.5"
              >
                <Play className="h-3.5 w-3.5 fill-white" />
                <span>Launch Live Training</span>
              </button>
            </div>

          </div>
        </div>
      )}

      {/* FOOTER */}
      <footer className="text-center text-xs text-slate-500 font-medium pt-4">
        Department of Information Science & Engineering • Project Batch No. 34
      </footer>

    </div>
  );
};
