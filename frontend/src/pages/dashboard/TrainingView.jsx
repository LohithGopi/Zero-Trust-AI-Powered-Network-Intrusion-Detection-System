import React, { useState, useEffect, useRef, useMemo } from 'react';
import { 
  Sliders, Activity, Play, CheckCircle2, 
  AlertCircle, Info, RefreshCw, Terminal, Layers, ArrowRight,
  Cpu, GitBranch, History, Check, Trash2, Zap, Settings2, BarChart2,
  FolderPlus, Upload
} from 'lucide-react';
import { 
  apiTrainModel, 
  apiGetModelStatus, 
  apiGetModelReport,
  apiGetAllModels,
  apiActivateModel,
  apiDeleteModel,
  apiUploadDataset
} from '../../services/api';
import { useAuth } from '../../context/AuthContext';

export const TrainingView = ({ onNavigate }) => {
  const { 
    user, role, modelStatus, setModelStatus, 
    modelMetrics, setTrainedModel, datasets = [], 
    activeDataset, selectDataset, addDataset
  } = useAuth();

  const currentRole = role || user?.role || 'Admin';
  const isAdmin = currentRole === 'Admin';

  const safeDatasets = Array.isArray(datasets) ? datasets : [];

  // Selected Dataset State
  const initialDs = activeDataset || safeDatasets.find(d => d.isSelected) || safeDatasets[0] || null;
  const [selectedDatasetId, setSelectedDatasetId] = useState(initialDs?.id || (safeDatasets[0]?.id ?? ''));
  const currentDs = safeDatasets.find(d => String(d.id) === String(selectedDatasetId)) || initialDs || safeDatasets[0] || {};
  const dsType = currentDs?.type || currentDs?.dataset_type || 'NIDS';
  const totalAvailableRows = currentDs?.totalRows || currentDs?.rows || currentDs?.row_count || 0;

  // Model Selection (svm, logistic_regression, lstm)
  const [selectedModelType, setSelectedModelType] = useState('svm');

  const [trainingRows, setTrainingRows] = useState(
    currentDs?.trainingRows || Math.min(25000, totalAvailableRows > 0 ? totalAvailableRows : 25000)
  );

  const rowOptions = useMemo(() => {
    if (!totalAvailableRows || totalAvailableRows <= 0) {
      return [10000, 25000, 50000];
    }
    const candidates = [5000, 10000, 25000, 50000, 100000].filter(r => r < totalAvailableRows);
    return [...new Set([...candidates, totalAvailableRows])].sort((a, b) => a - b);
  }, [totalAvailableRows]);

  const [randomSeed, setRandomSeed] = useState(42);
  const [targetCol, setTargetCol] = useState(currentDs?.target_col || 'label');

  // Support Vector Machine (SVM) Specific Hyperparameters
  const [svmKernel, setSvmKernel] = useState('rbf');
  const [svmC, setSvmC] = useState('1.0');
  const [svmGamma, setSvmGamma] = useState('scale');
  const [svmClassWeight, setSvmClassWeight] = useState('balanced');
  const [svmMaxIter, setSvmMaxIter] = useState(3000);

  // Logistic Regression Specific Hyperparameters
  const [lrC, setLrC] = useState('1.0');
  const [lrPenalty, setLrPenalty] = useState('l2');
  const [lrSolver, setLrSolver] = useState('lbfgs');
  const [lrMaxIter, setLrMaxIter] = useState(500);
  const [lrClassWeight, setLrClassWeight] = useState('balanced');

  // LSTM / Neural Network Specific Hyperparameters
  const [epochs, setEpochs] = useState(10);
  const [batchSize, setBatchSize] = useState(32);
  const [learningRate, setLearningRate] = useState('0.001');

  // Confirmation Modal & Launch State
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [isLaunching, setIsLaunching] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Live Progress & Metrics
  const [runId, setRunId] = useState(modelStatus === 'Trained' ? (modelMetrics?.runId || '') : '');
  const [currentEpoch, setCurrentEpoch] = useState(modelStatus === 'Trained' ? (modelMetrics?.epochs || 0) : 0);

  // Avoid carrying over previous epoch counters when switching model type
  useEffect(() => {
    if (modelStatus !== 'Training' && !isLaunching) {
      setCurrentEpoch(0);
    }
  }, [selectedModelType]);
  const [trainLoss, setTrainLoss] = useState(modelStatus === 'Trained' && modelMetrics?.loss && modelMetrics.loss !== '0.0000' ? modelMetrics.loss : '0.0000');
  const [trainAcc, setTrainAcc] = useState(modelStatus === 'Trained' && modelMetrics?.accuracy && modelMetrics.accuracy !== '0.00%' ? modelMetrics.accuracy : '0.00%');
  const [progress, setProgress] = useState(modelStatus === 'Trained' ? 100 : 0);
  const [hoveredEpoch, setHoveredEpoch] = useState(null);
  const [hoveredEpochAcc, setHoveredEpochAcc] = useState(null);
  const [hoveredEpochLoss, setHoveredEpochLoss] = useState(null);
  const [epochHistory, setEpochHistory] = useState([]);
  const [chartMetric, setChartMetric] = useState('accuracy');
  const [stageMessage, setStageMessage] = useState('');
  const pollIntervalRef = useRef(null);

  // Model History List State
  const [modelHistoryList, setModelHistoryList] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Load Model History & Latest Status on Mount
  useEffect(() => {
    fetchModelHistory();
    fetchLatestStatus();

    return () => {
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    };
  }, []);

  // Synchronize target column & default training rows whenever selected dataset loads or changes
  useEffect(() => {
    if (currentDs?.target_col) {
      setTargetCol(currentDs.target_col);
    }
    if (currentDs?.totalRows || currentDs?.rows) {
      const tot = currentDs.totalRows || currentDs.rows;
      setTrainingRows(prev => (prev > tot ? tot : prev));
    }
  }, [currentDs?.id, currentDs?.target_col]);

  const fetchModelHistory = async () => {
    try {
      setLoadingHistory(true);
      const data = await apiGetAllModels();
      if (Array.isArray(data)) {
        setModelHistoryList(data);
      }
    } catch (err) {
      console.warn('Error fetching model history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  const formatEpochEntry = (h) => {
    const rawAcc = h.accuracy !== undefined ? h.accuracy : 0;
    const rawValAcc = h.val_accuracy !== undefined ? h.val_accuracy : null;
    const rawLoss = h.loss !== undefined ? h.loss : 0;
    const rawValLoss = h.val_loss !== undefined ? h.val_loss : null;

    const trainAccDec = rawAcc > 1 ? rawAcc / 100 : rawAcc;
    const valAccDec = (rawValAcc !== null && rawValAcc !== undefined)
      ? (rawValAcc > 1 ? rawValAcc / 100 : rawValAcc)
      : null;

    return {
      epoch: h.epoch,
      trainAccDecimal: trainAccDec,
      valAccDecimal: valAccDec,
      trainAcc: trainAccDec * 100,
      valAcc: valAccDec !== null ? valAccDec * 100 : null,
      trainLoss: rawLoss,
      valLoss: rawValLoss
    };
  };

  const startPolling = (targetRunId) => {
    if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    pollIntervalRef.current = setInterval(async () => {
      try {
        const statusData = await apiGetModelStatus();
        if (statusData) {
          if (statusData.message) setStageMessage(statusData.message);
          const ep = statusData.current_epoch || 0;
          const totalEp = statusData.total_epochs || (selectedModelType === 'lstm' ? epochs : 5);
          const rawAcc = statusData.accuracy || 0;
          const rawLoss = statusData.loss || 0;
          const accNum = rawAcc > 1 ? rawAcc : rawAcc * 100;
          const accStr = `${accNum.toFixed(2)}%`;
          const lossStr = rawLoss > 0 ? rawLoss.toFixed(4) : (rawLoss === 0 ? '0.0000' : String(rawLoss));

          setCurrentEpoch(ep);
          setTrainAcc(accStr);
          setTrainLoss(lossStr);

          // Authentic progress staging calculation
          if (statusData.stage === 'sampling') {
            setProgress(10);
          } else if (statusData.stage === 'preprocessing') {
            setProgress(25);
          } else if (statusData.stage === 'evaluating') {
            setProgress(95);
          } else if (statusData.status === 'Completed') {
            setProgress(100);
          } else if (totalEp > 0) {
            setProgress(Math.min(92, Math.max(25, Math.round(25 + (ep / totalEp) * 68))));
          }

          if (Array.isArray(statusData.epoch_history) && statusData.epoch_history.length > 0) {
            const formatted = statusData.epoch_history.map(formatEpochEntry);
            setEpochHistory(formatted);
          }

          if (statusData.status === 'Completed' && !statusData.is_training) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
            setIsLaunching(false);
            setModelStatus('Trained');
            setProgress(100);
            setCurrentEpoch(totalEp);
            setTrainAcc(accStr);
            setTrainLoss(lossStr);

            setTrainedModel({
              runId: statusData.run_id || targetRunId || runId,
              accuracy: accStr,
              loss: lossStr,
              epochs: totalEp,
              datasetName: currentDs.name || currentDs.filename,
              trainedAt: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            setSuccessMessage(`Model '${statusData.model_name || selectedModelType}' successfully trained and saved.`);
            fetchModelHistory();
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
  };

  const fetchLatestStatus = async () => {
    try {
      const statusData = await apiGetModelStatus();
      if (statusData) {
        if (statusData.is_training) {
          setIsLaunching(true);
          setModelStatus('Training');
          if (statusData.message) setStageMessage(statusData.message);
          if (Array.isArray(statusData.epoch_history) && statusData.epoch_history.length > 0) {
            const formatted = statusData.epoch_history.map(formatEpochEntry);
            setEpochHistory(formatted);
          }
          if (statusData.accuracy) {
            const accNum = statusData.accuracy > 1 ? statusData.accuracy : statusData.accuracy * 100;
            setTrainAcc(`${accNum.toFixed(2)}%`);
          }
          if (statusData.loss) {
            setTrainLoss(statusData.loss.toFixed(4));
          }
          if (statusData.current_epoch) setCurrentEpoch(statusData.current_epoch);
          if (statusData.run_id) setRunId(statusData.run_id);
          const ep = statusData.current_epoch || 0;
          const totalEp = statusData.total_epochs || targetTotalSteps;
          setProgress(Math.min(98, Math.max(10, Math.round((ep / totalEp) * 100))));
          startPolling(statusData.run_id);
        } else if (modelStatus === 'Trained') {
          if (statusData.message) setStageMessage(statusData.message);
          if (Array.isArray(statusData.epoch_history) && statusData.epoch_history.length > 0) {
            const formatted = statusData.epoch_history.map(formatEpochEntry);
            setEpochHistory(formatted);
          }
          if (statusData.accuracy) {
            const accNum = statusData.accuracy > 1 ? statusData.accuracy : statusData.accuracy * 100;
            setTrainAcc(`${accNum.toFixed(2)}%`);
          }
          if (statusData.loss) {
            setTrainLoss(statusData.loss.toFixed(4));
          }
          setProgress(100);
        }
      }
    } catch (err) {
      console.warn('Error fetching latest model status:', err);
    }
  };

  const handleDatasetChange = (newId) => {
    const targetId = Number(newId);
    setSelectedDatasetId(targetId);
    if (selectDataset) selectDataset(targetId);

    const dsObj = safeDatasets.find(d => d.id === targetId);
    if (dsObj) {
      if (dsObj.target_col) {
        setTargetCol(dsObj.target_col);
      }
      const total = dsObj.totalRows || dsObj.rows || dsObj.row_count || 0;
      if (total > 0) {
        setTrainingRows(Math.min(25000, total));
      }
    }
  };

  // Compile active hyperparameters based on selected algorithm
  const getCompiledHyperparams = () => {
    if (selectedModelType === 'svm') {
      return {
        kernel: svmKernel,
        C: parseFloat(svmC) || 1.0,
        gamma: svmGamma,
        class_weight: svmClassWeight,
        max_iter: Number(svmMaxIter) || 3000,
        random_state: Number(randomSeed)
      };
    } else if (selectedModelType === 'logistic_regression') {
      return {
        C: parseFloat(lrC) || 1.0,
        penalty: lrPenalty,
        solver: lrSolver,
        max_iter: Number(lrMaxIter),
        class_weight: lrClassWeight,
        random_state: Number(randomSeed)
      };
    } else {
      return {
        epochs: Number(epochs),
        batch_size: Number(batchSize),
        learning_rate: parseFloat(learningRate) || 0.001,
        random_state: Number(randomSeed)
      };
    }
  };

  // Start Training Request
  const handleLaunchTraining = async () => {
    setShowConfirmModal(false);
    setIsLaunching(true);
    setErrorMessage('');
    setSuccessMessage('');
    setStageMessage('Submitting training job to background thread...');
    setModelStatus('Training');
    setProgress(5);
    setCurrentEpoch(0);
    setEpochHistory([]);

    const hyperparams = getCompiledHyperparams();

    try {
      const resp = await apiTrainModel({
        model_type: selectedModelType,
        dataset_id: currentDs?.id || selectedDatasetId,
        dataset_name: currentDs?.name || currentDs?.filename,
        dataset_type: currentDs?.type || currentDs?.dataset_type || dsType,
        training_rows: Number(trainingRows),
        target_col: targetCol,
        random_seed: Number(randomSeed),
        hyperparameters: hyperparams,
        epochs: Number(epochs),
        batch_size: Number(batchSize),
        learning_rate: parseFloat(learningRate)
      });

      const newRunId = resp?.run_id || `run_${Date.now()}`;
      setRunId(newRunId);
      startPolling(newRunId);
    } catch (err) {
      setIsLaunching(false);
      setModelStatus('Untrained');
      setErrorMessage(err?.message || 'Failed to initiate model training.');
    }
  };

  const handleActivateModel = async (modelId) => {
    try {
      setErrorMessage('');
      setSuccessMessage('');
      const resp = await apiActivateModel(modelId);
      if (resp && resp.success) {
        setSuccessMessage(resp.message || 'Model activated for live detection.');
        fetchModelHistory();
      }
    } catch (err) {
      setErrorMessage(err?.message || 'Failed to activate model.');
    }
  };

  const handleDeleteModel = async (modelId) => {
    if (!window.confirm('Are you sure you want to delete this trained model and its artifacts?')) return;
    try {
      setErrorMessage('');
      const resp = await apiDeleteModel(modelId);
      if (resp && resp.success) {
        setSuccessMessage(resp.message || 'Model deleted successfully.');
        fetchModelHistory();
      }
    } catch (err) {
      setErrorMessage(err?.message || 'Failed to delete model.');
    }
  };

  const handleViewModelCurve = (m) => {
    if (m?.params_json) {
      try {
        const pj = JSON.parse(m.params_json);
        if (Array.isArray(pj.epoch_history) && pj.epoch_history.length > 0) {
          const formatted = pj.epoch_history.map(formatEpochEntry);
          setEpochHistory(formatted);
          if (m.accuracy) {
            const accNum = m.accuracy > 1 ? m.accuracy : m.accuracy * 100;
            setTrainAcc(`${accNum.toFixed(2)}%`);
          }
          if (m.loss) {
            setTrainLoss(m.loss.toFixed(4));
          }
          setSuccessMessage(`Displaying genuine training convergence curves for '${m.model_name}'.`);
          return;
        }
      } catch (e) {
        console.warn('Could not parse model params_json:', e);
      }
    }
    setErrorMessage(`No convergence epoch history recorded for '${m?.model_name || 'selected model'}'.`);
  };

  // Calculate target total steps accurately based on algorithm configuration
  const targetTotalSteps = useMemo(() => {
    if (selectedModelType === 'svm') {
      return 5;
    } else if (selectedModelType === 'logistic_regression') {
      return 5;
    } else {
      return Number(epochs) || 10;
    }
  }, [selectedModelType, epochs]);

  // Clean, strictly bounded epoch value for UI metrics
  const displayEpoch = useMemo(() => {
    if (modelStatus === 'Trained') {
      return targetTotalSteps;
    }
    if (modelStatus === 'Training' || isLaunching) {
      return Math.min(Math.max(1, currentEpoch), targetTotalSteps);
    }
    return 0;
  }, [modelStatus, isLaunching, currentEpoch, targetTotalSteps]);

  // Graph 1 Math Engine: Training vs Validation Accuracy
  const accuracyChartData = useMemo(() => {
    const W = 500;
    const H = 240;
    const padL = 48;
    const padR = 20;
    const padT = 20;
    const padB = 34;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;

    const dataPoints = Array.isArray(epochHistory) ? epochHistory : [];
    const count = dataPoints.length;
    const maxSteps = Math.max(targetTotalSteps, count || 1);

    const getX = (stepIndex) => {
      if (maxSteps <= 1) return padL + plotW / 2;
      return padL + ((stepIndex - 1) / (maxSteps - 1)) * plotW;
    };

    // Collect all valid accuracy decimals (0.0 to 1.0)
    const validAccDecimals = [];
    dataPoints.forEach(d => {
      if (typeof d.trainAccDecimal === 'number' && !isNaN(d.trainAccDecimal) && d.trainAccDecimal > 0) {
        validAccDecimals.push(d.trainAccDecimal);
      }
      if (typeof d.valAccDecimal === 'number' && !isNaN(d.valAccDecimal) && d.valAccDecimal !== null && d.valAccDecimal > 0) {
        validAccDecimals.push(d.valAccDecimal);
      }
    });

    const minAcc = validAccDecimals.length > 0 ? Math.min(...validAccDecimals) : 0.70;
    const yMinAcc = Math.max(0.0, Math.floor((minAcc - 0.05) * 10) / 10);
    const yMaxAcc = 1.0;
    const stepAcc = (yMaxAcc - yMinAcc) / 4;
    const yTicksAcc = [0, 1, 2, 3, 4].map(i => yMinAcc + i * stepAcc);

    const getY = (val) => {
      if (yMaxAcc <= yMinAcc) return padT + plotH / 2;
      const clamped = Math.min(yMaxAcc, Math.max(yMinAcc, val));
      return padT + plotH - ((clamped - yMinAcc) / (yMaxAcc - yMinAcc)) * plotH;
    };

    let trainAccPath = '';
    let trainAccArea = '';
    let valAccPath = '';
    const trainAccCoords = [];
    const valAccCoords = [];

    if (count > 0) {
      dataPoints.forEach((d, idx) => {
        const stepNum = d.epoch || (idx + 1);
        const vTrain = d.trainAccDecimal;
        if (typeof vTrain === 'number' && !isNaN(vTrain)) {
          trainAccCoords.push({ x: getX(stepNum), y: getY(vTrain), val: vTrain, epoch: stepNum, d });
        }
        const vVal = d.valAccDecimal;
        if (typeof vVal === 'number' && !isNaN(vVal) && vVal !== null) {
          valAccCoords.push({ x: getX(stepNum), y: getY(vVal), val: vVal, epoch: stepNum, d });
        }
      });

      if (trainAccCoords.length > 0) {
        trainAccPath = trainAccCoords.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`).join(' ');
        const first = trainAccCoords[0];
        const last = trainAccCoords[trainAccCoords.length - 1];
        trainAccArea = `${trainAccPath} L ${last.x.toFixed(1)} ${(padT + plotH).toFixed(1)} L ${first.x.toFixed(1)} ${(padT + plotH).toFixed(1)} Z`;
      }

      if (valAccCoords.length > 0) {
        valAccPath = valAccCoords.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`).join(' ');
      }
    }

    const xTicks = [];
    const stepX = maxSteps > 12 ? Math.ceil(maxSteps / 10) : 1;
    for (let s = 1; s <= maxSteps; s += stepX) {
      xTicks.push(s);
    }
    if (xTicks[xTicks.length - 1] !== maxSteps) {
      xTicks.push(maxSteps);
    }

    const hasVal = valAccCoords.length > 0;

    return {
      W, H, padL, padR, padT, padB, plotW, plotH,
      maxSteps, getX, getY, yTicksAcc, xTicks,
      trainAccPath, trainAccArea, valAccPath,
      trainAccCoords, valAccCoords, hasVal,
      count
    };
  }, [epochHistory, targetTotalSteps]);

  // Graph 2 Math Engine: Training vs Validation Loss
  const lossChartData = useMemo(() => {
    const W = 500;
    const H = 240;
    const padL = 48;
    const padR = 20;
    const padT = 20;
    const padB = 34;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;

    const dataPoints = Array.isArray(epochHistory) ? epochHistory : [];
    const count = dataPoints.length;
    const maxSteps = Math.max(targetTotalSteps, count || 1);

    const getX = (stepIndex) => {
      if (maxSteps <= 1) return padL + plotW / 2;
      return padL + ((stepIndex - 1) / (maxSteps - 1)) * plotW;
    };

    // Collect all valid loss numbers
    const validLosses = [];
    dataPoints.forEach(d => {
      if (typeof d.trainLoss === 'number' && !isNaN(d.trainLoss)) {
        validLosses.push(d.trainLoss);
      }
      if (typeof d.valLoss === 'number' && !isNaN(d.valLoss) && d.valLoss !== null) {
        validLosses.push(d.valLoss);
      }
    });

    const maxLossVal = validLosses.length > 0 ? Math.max(...validLosses) : 1.0;
    const yMinLoss = 0.0;
    const yMaxLoss = Math.max(0.3, Math.ceil((maxLossVal + 0.05) * 10) / 10);
    const stepLoss = (yMaxLoss - yMinLoss) / 4;
    const yTicksLoss = [0, 1, 2, 3, 4].map(i => yMinLoss + i * stepLoss);

    const getY = (val) => {
      if (yMaxLoss <= yMinLoss) return padT + plotH / 2;
      const clamped = Math.min(yMaxLoss, Math.max(yMinLoss, val));
      return padT + plotH - ((clamped - yMinLoss) / (yMaxLoss - yMinLoss)) * plotH;
    };

    let trainLossPath = '';
    let trainLossArea = '';
    let valLossPath = '';
    const trainLossCoords = [];
    const valLossCoords = [];

    if (count > 0) {
      dataPoints.forEach((d, idx) => {
        const stepNum = d.epoch || (idx + 1);
        const vTrain = d.trainLoss;
        if (typeof vTrain === 'number' && !isNaN(vTrain)) {
          trainLossCoords.push({ x: getX(stepNum), y: getY(vTrain), val: vTrain, epoch: stepNum, d });
        }
        const vVal = d.valLoss;
        if (typeof vVal === 'number' && !isNaN(vVal) && vVal !== null) {
          valLossCoords.push({ x: getX(stepNum), y: getY(vVal), val: vVal, epoch: stepNum, d });
        }
      });

      if (trainLossCoords.length > 0) {
        trainLossPath = trainLossCoords.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`).join(' ');
        const first = trainLossCoords[0];
        const last = trainLossCoords[trainLossCoords.length - 1];
        trainLossArea = `${trainLossPath} L ${last.x.toFixed(1)} ${(padT + plotH).toFixed(1)} L ${first.x.toFixed(1)} ${(padT + plotH).toFixed(1)} Z`;
      }

      if (valLossCoords.length > 0) {
        valLossPath = valLossCoords.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`).join(' ');
      }
    }

    const xTicks = [];
    const stepX = maxSteps > 12 ? Math.ceil(maxSteps / 10) : 1;
    for (let s = 1; s <= maxSteps; s += stepX) {
      xTicks.push(s);
    }
    if (xTicks[xTicks.length - 1] !== maxSteps) {
      xTicks.push(maxSteps);
    }

    const hasVal = valLossCoords.length > 0;

    return {
      W, H, padL, padR, padT, padB, plotW, plotH,
      maxSteps, getX, getY, yTicksLoss, xTicks,
      trainLossPath, trainLossArea, valLossPath,
      trainLossCoords, valLossCoords, hasVal,
      count
    };
  }, [epochHistory, targetTotalSteps]);

  return (
    <div className="space-y-6 animate-fade-in pb-12 font-sans">
      
      {/* 1. HEADER CARD */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
              Multi-Model AI Training Console
            </h1>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold inline-flex items-center space-x-1 border ${
              modelStatus === 'Trained'
                ? 'bg-emerald-50 text-emerald-600 border-emerald-200'
                : modelStatus === 'Training' || isLaunching
                ? 'bg-blue-50 text-blue-600 border-blue-200 animate-pulse'
                : 'bg-amber-50 text-amber-600 border-amber-200'
            }`}>
              {modelStatus === 'Trained' ? (
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
            Train, validate, and serialize Support Vector Machine, Logistic Regression, and LSTM Neural Networks on genuine NIDS traffic flows.
          </p>
        </div>

        <button
          onClick={() => onNavigate && onNavigate('compare')}
          className="px-4 py-2 text-xs font-semibold bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl transition-all flex items-center space-x-2 shadow-xs shrink-0 self-start md:self-auto cursor-pointer"
        >
          <GitBranch className="h-4 w-4 text-purple-600" />
          <span>Compare Models Matrix →</span>
        </button>
      </div>

      {/* Notifications */}
      {errorMessage && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-xs text-red-600 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{errorMessage}</span>
          </div>
          <button onClick={() => setErrorMessage('')} className="font-bold underline cursor-pointer">Dismiss</button>
        </div>
      )}

      {successMessage && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-700 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="h-4 w-4 shrink-0" />
            <span>{successMessage}</span>
          </div>
          <button onClick={() => setSuccessMessage('')} className="font-bold underline cursor-pointer">Dismiss</button>
        </div>
      )}

      {/* 2. TWO-COLUMN MAIN WORKSPACE */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* LEFT COLUMN: TRAINING CONFIGURATION */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-5">
          <div className="flex items-center space-x-2 border-b border-slate-100 pb-3">
            <Sliders className="h-4 w-4 text-blue-600" />
            <h2 className="text-sm font-bold text-slate-900">Algorithm &amp; Hyperparameter Setup</h2>
          </div>

          <form onSubmit={(e) => { e.preventDefault(); setShowConfirmModal(true); }} className="space-y-4 text-xs">
            
            {/* Algorithm Selector Tabs */}
            <div>
              <label className="block text-slate-700 font-semibold mb-1.5">
                Machine Learning Algorithm:
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  disabled={isLaunching || modelStatus === 'Training'}
                  onClick={() => setSelectedModelType('svm')}
                  className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer ${
                    selectedModelType === 'svm'
                      ? 'border-blue-600 bg-blue-50/70 text-blue-900 ring-2 ring-blue-500/20'
                      : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="font-bold text-[11px] flex items-center space-x-1">
                    <Layers className="h-3.5 w-3.5 text-blue-600" />
                    <span>Support Vector Mach.</span>
                  </div>
                  <div className="text-[9px] text-slate-500 mt-0.5">Kernel RBF / Dual QP</div>
                </button>

                <button
                  type="button"
                  disabled={isLaunching || modelStatus === 'Training'}
                  onClick={() => setSelectedModelType('logistic_regression')}
                  className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer ${
                    selectedModelType === 'logistic_regression'
                      ? 'border-indigo-600 bg-indigo-50/70 text-indigo-900 ring-2 ring-indigo-500/20'
                      : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="font-bold text-[11px] flex items-center space-x-1">
                    <Zap className="h-3.5 w-3.5 text-indigo-600" />
                    <span>Logistic Reg.</span>
                  </div>
                  <div className="text-[9px] text-slate-500 mt-0.5">Linear Classifier</div>
                </button>

                <button
                  type="button"
                  disabled={isLaunching || modelStatus === 'Training'}
                  onClick={() => setSelectedModelType('lstm')}
                  className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer ${
                    selectedModelType === 'lstm'
                      ? 'border-purple-600 bg-purple-50/70 text-purple-900 ring-2 ring-purple-500/20'
                      : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="font-bold text-[11px] flex items-center space-x-1">
                    <Cpu className="h-3.5 w-3.5 text-purple-600" />
                    <span>LSTM / NN</span>
                  </div>
                  <div className="text-[9px] text-slate-500 mt-0.5">Deep Learning</div>
                </button>
              </div>
            </div>

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

            {/* Target Column & Training Rows Count */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">
                  Target Label Column:
                </label>
                <input
                  type="text"
                  disabled={isLaunching || modelStatus === 'Training'}
                  value={targetCol}
                  onChange={(e) => setTargetCol(e.target.value)}
                  placeholder="e.g. label, Label, class"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">
                  Training Rows Subset:
                </label>
                <select
                  disabled={isLaunching || modelStatus === 'Training'}
                  value={trainingRows}
                  onChange={(e) => setTrainingRows(Number(e.target.value))}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-slate-900 font-medium text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  {rowOptions.map((r) => (
                    <option key={r} value={r}>
                      {r === totalAvailableRows ? `Full (${r.toLocaleString()} Rows)` : `${r.toLocaleString()} Rows Subset`}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* DYNAMIC HYPERPARAMETERS SECTION */}
            <div className="border-t border-slate-100 pt-3 space-y-3">
              <div className="flex items-center space-x-1.5 text-slate-800 font-bold">
                <Settings2 className="h-3.5 w-3.5 text-blue-600" />
                <span>
                  {(selectedModelType === 'svm') && 'Support Vector Machine Hyperparameters'}
                  {selectedModelType === 'logistic_regression' && 'Logistic Regression Hyperparameters'}
                  {selectedModelType === 'lstm' && 'LSTM / Neural Hyperparameters'}
                </span>
              </div>

              {/* 1. SUPPORT VECTOR MACHINE (SVM) FORM */}
              {(selectedModelType === 'svm') && (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Kernel Function (kernel):</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={svmKernel}
                        onChange={(e) => setSvmKernel(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value="rbf">RBF (Radial Basis Function)</option>
                        <option value="linear">Linear Kernel</option>
                        <option value="poly">Polynomial Kernel</option>
                        <option value="sigmoid">Sigmoid Kernel</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Regularization (C):</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={svmC}
                        onChange={(e) => setSvmC(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value="0.1">0.1 (Strong Regularization)</option>
                        <option value="1.0">1.0 (Standard Default)</option>
                        <option value="10.0">10.0 (High Margin Penalty)</option>
                        <option value="100.0">100.0 (Tight Boundary)</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-2">
                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Gamma:</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={svmGamma}
                        onChange={(e) => setSvmGamma(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value="scale">Scale (1 / n_feat * var)</option>
                        <option value="auto">Auto (1 / n_features)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Max Iterations:</label>
                      <input
                        type="number"
                        min="500"
                        max="10000"
                        step="500"
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={svmMaxIter}
                        onChange={(e) => setSvmMaxIter(Number(e.target.value))}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Class Weight:</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={svmClassWeight}
                        onChange={(e) => setSvmClassWeight(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value="balanced">Balanced (Recommended)</option>
                        <option value="none">None (Uniform)</option>
                      </select>
                    </div>
                  </div>

                  <div className="text-[10px] text-slate-500 bg-slate-50 p-2 rounded-lg border border-slate-100 flex items-center space-x-1.5">
                    <Info className="h-3.5 w-3.5 text-blue-500 shrink-0" />
                    <span>
                      Support Vector Machine applies non-linear kernel boundary projection and Platt probability calibration.
                    </span>
                  </div>
                </div>
              )}

              {/* 2. LOGISTIC REGRESSION FORM */}
              {selectedModelType === 'logistic_regression' && (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Inverse Regularization (C):</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={lrC}
                        onChange={(e) => setLrC(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value="0.01">0.01 (Strong L2)</option>
                        <option value="0.1">0.1</option>
                        <option value="1.0">1.0 (Standard)</option>
                        <option value="10.0">10.0 (Weak L2)</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Optimization Solver:</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={lrSolver}
                        onChange={(e) => setLrSolver(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value="lbfgs">lbfgs (Fast Quasi-Newton)</option>
                        <option value="saga">saga (Elastic/L1/L2)</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Max Iterations:</label>
                      <input
                        type="number"
                        min="50"
                        max="5000"
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={lrMaxIter}
                        onChange={(e) => setLrMaxIter(Number(e.target.value))}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      />
                    </div>

                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Class Weighting:</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={lrClassWeight}
                        onChange={(e) => setLrClassWeight(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value="balanced">Balanced</option>
                        <option value="none">None</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* 3. LSTM / NEURAL FORM */}
              {selectedModelType === 'lstm' && (
                <div className="space-y-3">
                  <div className="grid grid-cols-3 gap-2">
                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Epochs:</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={epochs}
                        onChange={(e) => setEpochs(Number(e.target.value))}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value={5}>5 Epochs</option>
                        <option value={10}>10 Epochs</option>
                        <option value={20}>20 Epochs</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Batch Size:</label>
                      <select
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={batchSize}
                        onChange={(e) => setBatchSize(Number(e.target.value))}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      >
                        <option value={16}>16</option>
                        <option value={32}>32</option>
                        <option value={64}>64</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-slate-600 font-medium mb-1">Learning Rate:</label>
                      <input
                        type="text"
                        disabled={isLaunching || modelStatus === 'Training'}
                        value={learningRate}
                        onChange={(e) => setLearningRate(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Random Seed */}
            <div className="pt-1">
              <label className="block text-slate-600 font-medium mb-1">Reproducibility Seed:</label>
              <input
                type="number"
                disabled={isLaunching || modelStatus === 'Training'}
                value={randomSeed}
                onChange={(e) => setRandomSeed(Number(e.target.value))}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-slate-900 text-xs"
              />
            </div>

            {/* Launch Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={!isAdmin || isLaunching || modelStatus === 'Training'}
                className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-xs flex items-center justify-center space-x-2 shadow-xs transition-all active:scale-95 cursor-pointer"
              >
                <Play className="h-3.5 w-3.5 fill-white" />
                <span>Configure &amp; Review Training</span>
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
                Live Training Telemetry ({dsType})
              </h2>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-[10px] font-mono text-purple-700 bg-purple-50 border border-purple-200 px-2 py-0.5 rounded-full font-bold uppercase">
                {selectedModelType.replace('_', ' ')}
              </span>
              <span className="text-[10px] font-mono text-blue-600 bg-blue-50 border border-blue-200 px-2.5 py-0.5 rounded-full font-bold">
                Run: {runId ? runId.slice(-12) : 'Standby'}
              </span>
            </div>
          </div>

          {/* Real-time Status / Stage Line */}
          <div className="flex items-center justify-between text-xs bg-slate-50 border border-slate-200/80 px-3 py-2 rounded-xl">
            <div className="flex items-center space-x-2 truncate">
              <span className={`w-2 h-2 rounded-full ${
                isLaunching || modelStatus === 'Training' ? 'bg-blue-600 animate-ping' : 'bg-emerald-500'
              }`} />
              <span className="font-semibold text-slate-800 truncate">
                {stageMessage || (modelStatus === 'Trained' ? 'Model training converged and serialized.' : 'Training pipeline ready.')}
              </span>
            </div>
            <span className="font-mono text-[11px] font-bold text-slate-500 shrink-0 ml-2">
              Epoch: {displayEpoch} / {targetTotalSteps}
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
                EPOCH
              </div>
              <div className="text-base sm:text-lg font-bold text-slate-900">
                {displayEpoch} / {targetTotalSteps}
              </div>
            </div>

            <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 space-y-1">
              <div className="text-[10px] font-bold text-orange-600 uppercase tracking-wider">
                TRAINING LOSS
              </div>
              <div className="text-base sm:text-lg font-bold text-orange-600">
                {trainLoss}
              </div>
            </div>

            <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 space-y-1">
              <div className="text-[10px] font-bold text-blue-600 uppercase tracking-wider">
                TRAIN ACCURACY
              </div>
              <div className="text-base sm:text-lg font-bold text-blue-600">
                {trainAcc}
              </div>
            </div>

          </div>

          {/* Dual Convergence Visualization: Training vs Validation Side-by-Side */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

            {/* Graph 1: Training vs Validation Accuracy */}
            <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-3 flex flex-col justify-between">
              {/* Header */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
                <div className="flex items-center space-x-2">
                  <div className="p-1.5 bg-blue-50 text-blue-600 rounded-lg border border-blue-100">
                    <Activity className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-xs sm:text-sm font-bold text-slate-900 tracking-tight">
                      Training vs Validation Accuracy
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      Convergence &amp; generalization accuracy across epochs
                    </p>
                  </div>
                </div>
                {accuracyChartData.hasVal ? (
                  <span className="text-[10px] font-mono font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
                    ✓ Train &amp; Val
                  </span>
                ) : (
                  <span className="text-[10px] font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">
                    Train Split Only
                  </span>
                )}
              </div>

              {/* SVG Canvas Container */}
              <div className="relative bg-gradient-to-b from-slate-50/70 to-slate-100/50 rounded-xl p-3 sm:p-4 flex flex-col items-center border border-slate-200/80 overflow-hidden">
                
                {/* Legends */}
                <div className="w-full flex items-center justify-between text-[11px] font-mono mb-2 px-1">
                  <div className="flex items-center space-x-1.5">
                    <span className="w-3 h-1 bg-blue-600 rounded-full" />
                    <span className="text-blue-700 font-bold text-[10.5px]">Training Acc (Blue)</span>
                  </div>
                  {accuracyChartData.hasVal ? (
                    <div className="flex items-center space-x-1.5">
                      <span className="w-3 h-1 bg-emerald-600 rounded-full border-t border-dashed" />
                      <span className="text-emerald-700 font-bold text-[10.5px]">Validation Acc (Emerald)</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-1.5 opacity-60">
                      <span className="w-3 h-0.5 bg-slate-400 rounded-full border-t border-dashed" />
                      <span className="text-slate-500 font-mono text-[10.5px]">Validation: N/A</span>
                    </div>
                  )}
                </div>

                {/* Accuracy SVG */}
                <svg viewBox={`0 0 ${accuracyChartData.W} ${accuracyChartData.H}`} className="w-full h-auto select-none overflow-visible">
                  <defs>
                    <linearGradient id="trainAccAreaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stopColor="#2563eb" stopOpacity="0.20" />
                      <stop offset="70%" stopColor="#3b82f6" stopOpacity="0.04" />
                      <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.0" />
                    </linearGradient>
                    <filter id="softGlowAcc" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="1.5" stdDeviation="2.5" floodColor="#2563eb" floodOpacity="0.25" />
                    </filter>
                    <filter id="softGlowValAcc" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="1.5" stdDeviation="2.5" floodColor="#059669" floodOpacity="0.25" />
                    </filter>
                  </defs>

                  {/* Plot Background */}
                  <rect 
                    x={accuracyChartData.padL} 
                    y={accuracyChartData.padT} 
                    width={accuracyChartData.plotW} 
                    height={accuracyChartData.plotH} 
                    fill="#ffffff" 
                    rx="6"
                    stroke="#e2e8f0" 
                    strokeWidth="1" 
                  />

                  {/* Y-Axis Grid Lines & Accuracy (%) Labels */}
                  {accuracyChartData.yTicksAcc.map((tickVal, idx) => {
                    const yPos = accuracyChartData.getY(tickVal);
                    return (
                      <g key={`yacc-${idx}`}>
                        <line 
                          x1={accuracyChartData.padL} 
                          y1={yPos} 
                          x2={accuracyChartData.padL + accuracyChartData.plotW} 
                          y2={yPos} 
                          stroke="#f1f5f9" 
                          strokeWidth="1" 
                          strokeDasharray={idx === 0 || idx === accuracyChartData.yTicksAcc.length - 1 ? "none" : "3 3"}
                        />
                        <text 
                          x={accuracyChartData.padL - 6} 
                          y={yPos + 3.5} 
                          textAnchor="end" 
                          fontSize="9" 
                          fontFamily="ui-monospace, SFMono-Regular, monospace" 
                          fill="#2563eb"
                          fontWeight="700"
                        >
                          {(tickVal * 100).toFixed(0)}%
                        </text>
                      </g>
                    );
                  })}

                  {/* Y-Axis Title: Accuracy (%) */}
                  <text
                    transform={`rotate(-90 ${accuracyChartData.padL - 32} ${accuracyChartData.padT + accuracyChartData.plotH / 2})`}
                    x={accuracyChartData.padL - 32}
                    y={accuracyChartData.padT + accuracyChartData.plotH / 2}
                    textAnchor="middle"
                    fontSize="9.5"
                    fontFamily="system-ui, -apple-system, sans-serif"
                    fontWeight="600"
                    fill="#475569"
                  >
                    Accuracy (%)
                  </text>

                  {/* X-Axis Grid Lines & Step Numbers */}
                  {accuracyChartData.xTicks.map((stepNum) => {
                    const xPos = accuracyChartData.getX(stepNum);
                    return (
                      <g key={`xtick-acc-${stepNum}`}>
                        <line 
                          x1={xPos} 
                          y1={accuracyChartData.padT} 
                          x2={xPos} 
                          y2={accuracyChartData.padT + accuracyChartData.plotH} 
                          stroke="#f8fafc" 
                          strokeWidth="1" 
                        />
                        <line 
                          x1={xPos} 
                          y1={accuracyChartData.padT + accuracyChartData.plotH} 
                          x2={xPos} 
                          y2={accuracyChartData.padT + accuracyChartData.plotH + 4} 
                          stroke="#cbd5e1" 
                          strokeWidth="1" 
                        />
                        <text 
                          x={xPos} 
                          y={accuracyChartData.padT + accuracyChartData.plotH + 16} 
                          textAnchor="middle" 
                          fontSize="9.5" 
                          fontFamily="ui-monospace, SFMono-Regular, monospace" 
                          fill="#64748b"
                          fontWeight="600"
                        >
                          {stepNum}
                        </text>
                      </g>
                    );
                  })}

                  {/* X-Axis Title: Epoch */}
                  <text 
                    x={accuracyChartData.padL + accuracyChartData.plotW / 2} 
                    y={accuracyChartData.padT + accuracyChartData.plotH + 30} 
                    textAnchor="middle" 
                    fontSize="10" 
                    fontFamily="system-ui, -apple-system, sans-serif" 
                    fontWeight="600"
                    fill="#475569"
                  >
                    Epoch
                  </text>

                  {/* Live Dynamic Curves (Simultaneously Plotted in Real Time) */}
                  {accuracyChartData.count > 0 && (
                    <>
                      {/* Area Fill under Training Accuracy */}
                      {accuracyChartData.trainAccArea && (
                        <path
                          d={accuracyChartData.trainAccArea}
                          fill="url(#trainAccAreaGrad)"
                        />
                      )}

                      {/* Validation Accuracy Line (Emerald) */}
                      {accuracyChartData.valAccPath && (
                        <path
                          d={accuracyChartData.valAccPath}
                          fill="none"
                          stroke="#059669"
                          strokeWidth="2.2"
                          strokeDasharray="4 2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          filter="url(#softGlowValAcc)"
                        />
                      )}

                      {/* Training Accuracy Line (Blue) */}
                      {accuracyChartData.trainAccPath && (
                        <path
                          d={accuracyChartData.trainAccPath}
                          fill="none"
                          stroke="#2563eb"
                          strokeWidth="2.4"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          filter="url(#softGlowAcc)"
                        />
                      )}

                      {/* Interactive Points on Validation Accuracy */}
                      {accuracyChartData.valAccCoords.map((pt, i) => (
                        <circle
                          key={`val-acc-pt-${i}`}
                          cx={pt.x}
                          cy={pt.y}
                          r={hoveredEpochAcc?.epoch === pt.epoch ? "5.5" : "3.5"}
                          fill="#059669"
                          stroke="#ffffff"
                          strokeWidth="1.8"
                          className="cursor-pointer transition-all duration-150 hover:scale-125"
                          onMouseEnter={() => setHoveredEpochAcc(pt.d)}
                          onMouseLeave={() => setHoveredEpochAcc(null)}
                        />
                      ))}

                      {/* Interactive Points on Training Accuracy */}
                      {accuracyChartData.trainAccCoords.map((pt, i) => (
                        <circle
                          key={`tr-acc-pt-${i}`}
                          cx={pt.x}
                          cy={pt.y}
                          r={hoveredEpochAcc?.epoch === pt.epoch ? "5.5" : "3.5"}
                          fill="#2563eb"
                          stroke="#ffffff"
                          strokeWidth="1.8"
                          className="cursor-pointer transition-all duration-150 hover:scale-125"
                          onMouseEnter={() => setHoveredEpochAcc(pt.d)}
                          onMouseLeave={() => setHoveredEpochAcc(null)}
                        />
                      ))}

                      {/* Live Pulsing Marker at the Active Training Frontier */}
                      {(isLaunching || modelStatus === 'Training') && accuracyChartData.trainAccCoords.length > 0 && (
                        <circle
                          cx={accuracyChartData.trainAccCoords[accuracyChartData.trainAccCoords.length - 1].x}
                          cy={accuracyChartData.trainAccCoords[accuracyChartData.trainAccCoords.length - 1].y}
                          r="7"
                          fill="none"
                          stroke="#2563eb"
                          strokeWidth="2"
                          className="animate-ping"
                          opacity="0.65"
                        />
                      )}
                    </>
                  )}

                  {/* Clean standby watermark when awaiting launch without blocking the grid */}
                  {accuracyChartData.count === 0 && (
                    <g transform={`translate(${accuracyChartData.padL + accuracyChartData.plotW / 2}, ${accuracyChartData.padT + accuracyChartData.plotH / 2})`}>
                      <text textAnchor="middle" y="-4" fontSize="11" fontWeight="600" fill="#94a3b8" fontFamily="system-ui, sans-serif">
                        Ready to Plot Live Convergence
                      </text>
                      <text textAnchor="middle" y="14" fontSize="9.5" fill="#cbd5e1" fontFamily="system-ui, sans-serif">
                        Accuracy curves update simultaneously epoch-by-epoch
                      </text>
                    </g>
                  )}
                </svg>

                {/* Hover Telemetry Tooltip */}
                {hoveredEpochAcc && (
                  <div className="absolute top-3 right-3 bg-slate-900/95 backdrop-blur-xs text-white border border-slate-700/80 rounded-xl p-2.5 text-[11px] font-mono shadow-xl pointer-events-none z-10 space-y-1 min-w-[190px]">
                    <div className="font-bold text-slate-200 border-b border-slate-800 pb-1 flex items-center justify-between gap-4">
                      <span>Epoch {hoveredEpochAcc.epoch} Accuracy</span>
                      <span className="text-[10px] text-blue-400">Step Telemetry</span>
                    </div>
                    <div className="text-blue-300 flex items-center justify-between gap-3">
                      <span>Train Accuracy:</span>
                      <span className="font-bold">{(hoveredEpochAcc.trainAccDecimal * 100).toFixed(2)}%</span>
                    </div>
                    <div className="text-emerald-300 flex items-center justify-between gap-3">
                      <span>Val Accuracy:</span>
                      <span className="font-bold">
                        {hoveredEpochAcc.valAccDecimal !== null ? `${(hoveredEpochAcc.valAccDecimal * 100).toFixed(2)}%` : 'N/A'}
                      </span>
                    </div>
                    {hoveredEpochAcc.valAccDecimal !== null && (
                      <div className="text-slate-400 border-t border-slate-800/80 pt-1 flex items-center justify-between gap-3 text-[10px]">
                        <span>Generalization Δ:</span>
                        <span className={`font-bold ${hoveredEpochAcc.valAccDecimal >= hoveredEpochAcc.trainAccDecimal ? 'text-emerald-400' : 'text-amber-400'}`}>
                          {(hoveredEpochAcc.valAccDecimal - hoveredEpochAcc.trainAccDecimal >= 0 ? '+' : '')}
                          {((hoveredEpochAcc.valAccDecimal - hoveredEpochAcc.trainAccDecimal) * 100).toFixed(2)}%
                        </span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Graph 2: Training vs Validation Loss */}
            <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/90 shadow-sm space-y-3 flex flex-col justify-between">
              {/* Header */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
                <div className="flex items-center space-x-2">
                  <div className="p-1.5 bg-orange-50 text-orange-600 rounded-lg border border-orange-100">
                    <Activity className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-xs sm:text-sm font-bold text-slate-900 tracking-tight">
                      Training vs Validation Loss
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      Cross-entropy loss minimization &amp; overfitting analysis
                    </p>
                  </div>
                </div>
                {lossChartData.hasVal ? (
                  <span className="text-[10px] font-mono font-bold text-purple-700 bg-purple-50 border border-purple-200 px-2 py-0.5 rounded-full">
                    ✓ Overfitting Monitored
                  </span>
                ) : (
                  <span className="text-[10px] font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">
                    Train Loss Only
                  </span>
                )}
              </div>

              {/* SVG Canvas Container */}
              <div className="relative bg-gradient-to-b from-slate-50/70 to-slate-100/50 rounded-xl p-3 sm:p-4 flex flex-col items-center border border-slate-200/80 overflow-hidden">
                
                {/* Legends */}
                <div className="w-full flex items-center justify-between text-[11px] font-mono mb-2 px-1">
                  <div className="flex items-center space-x-1.5">
                    <span className="w-3 h-1 bg-orange-600 rounded-full" />
                    <span className="text-orange-700 font-bold text-[10.5px]">Training Loss (Orange)</span>
                  </div>
                  {lossChartData.hasVal ? (
                    <div className="flex items-center space-x-1.5">
                      <span className="w-3 h-1 bg-purple-600 rounded-full border-t border-dashed" />
                      <span className="text-purple-700 font-bold text-[10.5px]">Validation Loss (Purple)</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-1.5 opacity-60">
                      <span className="w-3 h-0.5 bg-slate-400 rounded-full border-t border-dashed" />
                      <span className="text-slate-500 font-mono text-[10.5px]">Validation: N/A</span>
                    </div>
                  )}
                </div>

                {/* Loss SVG */}
                <svg viewBox={`0 0 ${lossChartData.W} ${lossChartData.H}`} className="w-full h-auto select-none overflow-visible">
                  <defs>
                    <linearGradient id="trainLossAreaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stopColor="#ea580c" stopOpacity="0.18" />
                      <stop offset="70%" stopColor="#f97316" stopOpacity="0.04" />
                      <stop offset="100%" stopColor="#f97316" stopOpacity="0.0" />
                    </linearGradient>
                    <filter id="softGlowLoss" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="1.5" stdDeviation="2.5" floodColor="#ea580c" floodOpacity="0.25" />
                    </filter>
                    <filter id="softGlowValLoss" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="1.5" stdDeviation="2.5" floodColor="#9333ea" floodOpacity="0.25" />
                    </filter>
                  </defs>

                  {/* Plot Background */}
                  <rect 
                    x={lossChartData.padL} 
                    y={lossChartData.padT} 
                    width={lossChartData.plotW} 
                    height={lossChartData.plotH} 
                    fill="#ffffff" 
                    rx="6"
                    stroke="#e2e8f0" 
                    strokeWidth="1" 
                  />

                  {/* Y-Axis Grid Lines & Loss Labels */}
                  {lossChartData.yTicksLoss.map((tickVal, idx) => {
                    const yPos = lossChartData.getY(tickVal);
                    return (
                      <g key={`yloss-${idx}`}>
                        <line 
                          x1={lossChartData.padL} 
                          y1={yPos} 
                          x2={lossChartData.padL + lossChartData.plotW} 
                          y2={yPos} 
                          stroke="#f1f5f9" 
                          strokeWidth="1" 
                          strokeDasharray={idx === 0 || idx === lossChartData.yTicksLoss.length - 1 ? "none" : "3 3"}
                        />
                        <text 
                          x={lossChartData.padL - 6} 
                          y={yPos + 3.5} 
                          textAnchor="end" 
                          fontSize="9" 
                          fontFamily="ui-monospace, SFMono-Regular, monospace" 
                          fill="#ea580c"
                          fontWeight="700"
                        >
                          {tickVal.toFixed(2)}
                        </text>
                      </g>
                    );
                  })}

                  {/* Y-Axis Title: Loss */}
                  <text
                    transform={`rotate(-90 ${lossChartData.padL - 32} ${lossChartData.padT + lossChartData.plotH / 2})`}
                    x={lossChartData.padL - 32}
                    y={lossChartData.padT + lossChartData.plotH / 2}
                    textAnchor="middle"
                    fontSize="9.5"
                    fontFamily="system-ui, -apple-system, sans-serif"
                    fontWeight="600"
                    fill="#475569"
                  >
                    Loss
                  </text>

                  {/* X-Axis Grid Lines & Step Numbers */}
                  {lossChartData.xTicks.map((stepNum) => {
                    const xPos = lossChartData.getX(stepNum);
                    return (
                      <g key={`xtick-loss-${stepNum}`}>
                        <line 
                          x1={xPos} 
                          y1={lossChartData.padT} 
                          x2={xPos} 
                          y2={lossChartData.padT + lossChartData.plotH} 
                          stroke="#f8fafc" 
                          strokeWidth="1" 
                        />
                        <line 
                          x1={xPos} 
                          y1={lossChartData.padT + lossChartData.plotH} 
                          x2={xPos} 
                          y2={lossChartData.padT + lossChartData.plotH + 4} 
                          stroke="#cbd5e1" 
                          strokeWidth="1" 
                        />
                        <text 
                          x={xPos} 
                          y={lossChartData.padT + lossChartData.plotH + 16} 
                          textAnchor="middle" 
                          fontSize="9.5" 
                          fontFamily="ui-monospace, SFMono-Regular, monospace" 
                          fill="#64748b"
                          fontWeight="600"
                        >
                          {stepNum}
                        </text>
                      </g>
                    );
                  })}

                  {/* X-Axis Title: Epoch */}
                  <text 
                    x={lossChartData.padL + lossChartData.plotW / 2} 
                    y={lossChartData.padT + lossChartData.plotH + 30} 
                    textAnchor="middle" 
                    fontSize="10" 
                    fontFamily="system-ui, -apple-system, sans-serif" 
                    fontWeight="600"
                    fill="#475569"
                  >
                    Epoch
                  </text>

                  {/* Live Dynamic Curves (Simultaneously Plotted in Real Time) */}
                  {lossChartData.count > 0 && (
                    <>
                      {/* Area Fill under Training Loss */}
                      {lossChartData.trainLossArea && (
                        <path
                          d={lossChartData.trainLossArea}
                          fill="url(#trainLossAreaGrad)"
                        />
                      )}

                      {/* Validation Loss Line (Purple) */}
                      {lossChartData.valLossPath && (
                        <path
                          d={lossChartData.valLossPath}
                          fill="none"
                          stroke="#9333ea"
                          strokeWidth="2.2"
                          strokeDasharray="4 2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          filter="url(#softGlowValLoss)"
                        />
                      )}

                      {/* Training Loss Line (Orange) */}
                      {lossChartData.trainLossPath && (
                        <path
                          d={lossChartData.trainLossPath}
                          fill="none"
                          stroke="#ea580c"
                          strokeWidth="2.4"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          filter="url(#softGlowLoss)"
                        />
                      )}

                      {/* Interactive Points on Validation Loss */}
                      {lossChartData.valLossCoords.map((pt, i) => (
                        <circle
                          key={`val-loss-pt-${i}`}
                          cx={pt.x}
                          cy={pt.y}
                          r={hoveredEpochLoss?.epoch === pt.epoch ? "5.5" : "3.5"}
                          fill="#9333ea"
                          stroke="#ffffff"
                          strokeWidth="1.8"
                          className="cursor-pointer transition-all duration-150 hover:scale-125"
                          onMouseEnter={() => setHoveredEpochLoss(pt.d)}
                          onMouseLeave={() => setHoveredEpochLoss(null)}
                        />
                      ))}

                      {/* Interactive Points on Training Loss */}
                      {lossChartData.trainLossCoords.map((pt, i) => (
                        <circle
                          key={`tr-loss-pt-${i}`}
                          cx={pt.x}
                          cy={pt.y}
                          r={hoveredEpochLoss?.epoch === pt.epoch ? "5.5" : "3.5"}
                          fill="#ea580c"
                          stroke="#ffffff"
                          strokeWidth="1.8"
                          className="cursor-pointer transition-all duration-150 hover:scale-125"
                          onMouseEnter={() => setHoveredEpochLoss(pt.d)}
                          onMouseLeave={() => setHoveredEpochLoss(null)}
                        />
                      ))}

                      {/* Live Pulsing Marker at the Active Training Frontier */}
                      {(isLaunching || modelStatus === 'Training') && lossChartData.trainLossCoords.length > 0 && (
                        <circle
                          cx={lossChartData.trainLossCoords[lossChartData.trainLossCoords.length - 1].x}
                          cy={lossChartData.trainLossCoords[lossChartData.trainLossCoords.length - 1].y}
                          r="7"
                          fill="none"
                          stroke="#ea580c"
                          strokeWidth="2"
                          className="animate-ping"
                          opacity="0.65"
                        />
                      )}
                    </>
                  )}

                  {/* Clean standby watermark when awaiting launch without blocking the grid */}
                  {lossChartData.count === 0 && (
                    <g transform={`translate(${lossChartData.padL + lossChartData.plotW / 2}, ${lossChartData.padT + lossChartData.plotH / 2})`}>
                      <text textAnchor="middle" y="-4" fontSize="11" fontWeight="600" fill="#94a3b8" fontFamily="system-ui, sans-serif">
                        Ready to Plot Live Convergence
                      </text>
                      <text textAnchor="middle" y="14" fontSize="9.5" fill="#cbd5e1" fontFamily="system-ui, sans-serif">
                        Loss curves update simultaneously epoch-by-epoch
                      </text>
                    </g>
                  )}
                </svg>

                {/* Hover Telemetry Tooltip */}
                {hoveredEpochLoss && (
                  <div className="absolute top-3 right-3 bg-slate-900/95 backdrop-blur-xs text-white border border-slate-700/80 rounded-xl p-2.5 text-[11px] font-mono shadow-xl pointer-events-none z-10 space-y-1 min-w-[200px]">
                    <div className="font-bold text-slate-200 border-b border-slate-800 pb-1 flex items-center justify-between gap-4">
                      <span>Epoch {hoveredEpochLoss.epoch} Loss</span>
                      <span className="text-[10px] text-orange-400">Step Telemetry</span>
                    </div>
                    <div className="text-orange-300 flex items-center justify-between gap-3">
                      <span>Train Loss:</span>
                      <span className="font-bold">{hoveredEpochLoss.trainLoss.toFixed(4)}</span>
                    </div>
                    <div className="text-purple-300 flex items-center justify-between gap-3">
                      <span>Val Loss:</span>
                      <span className="font-bold">
                        {hoveredEpochLoss.valLoss !== null ? hoveredEpochLoss.valLoss.toFixed(4) : 'N/A'}
                      </span>
                    </div>
                    {hoveredEpochLoss.valLoss !== null && (
                      <div className="text-slate-400 border-t border-slate-800/80 pt-1 flex items-center justify-between gap-3 text-[10px]">
                        <span>Overfitting Δ:</span>
                        <span className={`font-bold ${hoveredEpochLoss.valLoss - hoveredEpochLoss.trainLoss > 0.15 ? 'text-amber-400' : 'text-emerald-400'}`}>
                          {(hoveredEpochLoss.valLoss - hoveredEpochLoss.trainLoss >= 0 ? '+' : '')}
                          {(hoveredEpochLoss.valLoss - hoveredEpochLoss.trainLoss).toFixed(4)}
                          {hoveredEpochLoss.valLoss - hoveredEpochLoss.trainLoss > 0.15 ? ' (Risk)' : ' (Good)'}
                        </span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

          </div>

          {/* Terminal Sync Notice */}
          <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono bg-slate-50 p-2.5 rounded-xl border border-slate-200/80">
            <div className="flex items-center space-x-2">
              <Terminal className="h-3.5 w-3.5 text-slate-600" />
              <span>Non-blocking background thread with live socket/polling telemetry</span>
            </div>
            <span className="text-emerald-600 font-bold">● Synchronized</span>
          </div>

        </div>

      </div>

      {/* 3. TRAINED MODEL VERSIONS & HISTORY TABLE (Only included after model training) */}
      {modelStatus === 'Trained' && modelHistoryList.length > 0 && (
        <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <div className="flex items-center space-x-2">
              <History className="h-4 w-4 text-purple-600" />
              <h2 className="text-sm font-bold text-slate-900">
                Trained Machine Learning Models &amp; Active Versions
              </h2>
            </div>
            <p className="text-xs text-slate-500">
              Non-destructive model history. Select any compatible model version to activate for live network traffic intrusion detection.
            </p>
          </div>
          <button
            onClick={fetchModelHistory}
            className="px-3 py-1.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center space-x-1.5 cursor-pointer"
          >
            <RefreshCw className={`h-3 w-3 ${loadingHistory ? 'animate-spin' : ''}`} />
            <span>Refresh Models</span>
          </button>
        </div>

        {modelHistoryList.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl space-y-2">
            <Cpu className="h-6 w-6 mx-auto text-slate-300" />
            <p className="font-bold text-slate-700">No Trained Models Registered</p>
            <p>Select an algorithm above and launch training to save your first NIDS model.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse font-sans">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                  <th className="py-2.5 px-3">Algorithm</th>
                  <th className="py-2.5 px-3">Model Name / Version</th>
                  <th className="py-2.5 px-3">Dataset</th>
                  <th className="py-2.5 px-3">Accuracy</th>
                  <th className="py-2.5 px-3">F1-Score</th>
                  <th className="py-2.5 px-3">Trained At</th>
                  <th className="py-2.5 px-3 text-center">Status</th>
                  <th className="py-2.5 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {modelHistoryList.map((m) => {
                  const algoClean = (m.algorithm || '').toLowerCase();
                  const isRf = algoClean.includes('forest') || algoClean.includes('rf');
                  const isLr = algoClean.includes('logistic') || algoClean.includes('lr');
                  const badgeColor = isRf 
                    ? 'bg-blue-50 text-blue-700 border-blue-200' 
                    : isLr 
                    ? 'bg-indigo-50 text-indigo-700 border-indigo-200' 
                    : 'bg-purple-50 text-purple-700 border-purple-200';

                  return (
                    <tr key={m.id} className="hover:bg-slate-50/70 transition-colors">
                      <td className="py-3 px-3">
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${badgeColor}`}>
                          {m.algorithm || 'Neural Network'}
                        </span>
                      </td>
                      <td className="py-3 px-3 font-semibold text-slate-900">
                        <div>{m.model_name}</div>
                        <div className="text-[10px] text-slate-400 font-mono">{m.model_version || `v${m.id}`}</div>
                      </td>
                      <td className="py-3 px-3 text-slate-600">
                        {m.dataset_name || 'NIDS Dataset'}
                      </td>
                      <td className="py-3 px-3 font-mono font-bold text-emerald-600">
                        {m.accuracy ? `${(m.accuracy > 1 ? m.accuracy : m.accuracy * 100).toFixed(2)}%` : 'N/A'}
                      </td>
                      <td className="py-3 px-3 font-mono font-bold text-purple-600">
                        {m.f1_score ? `${(m.f1_score > 1 ? m.f1_score : m.f1_score * 100).toFixed(2)}%` : 'N/A'}
                      </td>
                      <td className="py-3 px-3 text-slate-500 font-mono text-[11px]">
                        {m.trained_at || 'N/A'}
                      </td>
                      <td className="py-3 px-3 text-center">
                        {m.is_active ? (
                          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                            <Check className="h-3 w-3" />
                            <span>Active in Live Detection</span>
                          </span>
                        ) : (
                          <span className="text-[10px] text-slate-400">Inactive</span>
                        )}
                      </td>
                      <td className="py-3 px-3 text-right">
                        <div className="flex items-center justify-end space-x-1.5">
                          <button
                            onClick={() => handleViewModelCurve(m)}
                            className="px-2 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-[11px] transition-colors cursor-pointer flex items-center space-x-1"
                            title="Inspect training convergence curve in Matplotlib chart"
                          >
                            <Activity className="h-3 w-3 text-blue-600" />
                            <span>Curve</span>
                          </button>
                          {!m.is_active && (
                            <button
                              onClick={() => handleActivateModel(m.id)}
                              className="px-2.5 py-1 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold text-[11px] transition-colors cursor-pointer"
                              title="Set as active model for live packet capture and detection"
                            >
                              Activate
                            </button>
                          )}
                          {isAdmin && (
                            <button
                              onClick={() => handleDeleteModel(m.id)}
                              className="p-1 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
                              title="Delete model artifact"
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
        </div>
      )}

      {/* 4. STRATIFIED SAMPLING CONFIRMATION MODAL */}
      {showConfirmModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 space-y-5 animate-scale-up">
            
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center space-x-2.5">
                <div className="p-2 rounded-xl bg-emerald-50 text-emerald-600">
                  <Play className="h-4 w-4 fill-emerald-600" />
                </div>
                <h3 className="text-base font-bold text-slate-900">
                  Confirm AI Model Training Run
                </h3>
              </div>
              <button 
                onClick={() => setShowConfirmModal(false)}
                className="text-slate-400 hover:text-slate-700 text-sm font-bold cursor-pointer"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              Verify your dataset and selected hyperparameters before dispatching computation to the background thread.
            </p>

            <div className="bg-slate-50 rounded-2xl p-4 border border-slate-200/80 space-y-2 text-xs font-mono">
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Selected Algorithm:</span>
                <span className="font-bold text-blue-700 uppercase">{selectedModelType.replace('_', ' ')}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Target Dataset:</span>
                <span className="font-bold text-slate-900">{dsType}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Target Label Column:</span>
                <span className="font-bold text-purple-700">{targetCol}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Sampled Training Rows:</span>
                <span className="font-bold text-emerald-600">{trainingRows.toLocaleString()}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200/60">
                <span className="text-slate-500">Random Seed:</span>
                <span className="font-bold text-slate-900">{randomSeed}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Hyperparameters:</span>
                <span className="font-bold text-slate-900">
                  {(selectedModelType === 'svm') && `Kernel: ${svmKernel}, C: ${svmC}`}
                  {selectedModelType === 'logistic_regression' && `C: ${lrC}, Solver: ${lrSolver}`}
                  {selectedModelType === 'lstm' && `Epochs: ${epochs}, Batch: ${batchSize}`}
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-3 pt-2">
              <button
                type="button"
                onClick={() => setShowConfirmModal(false)}
                className="flex-1 py-2.5 rounded-xl border border-slate-300 text-slate-700 font-semibold text-xs hover:bg-slate-50 transition-colors cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleLaunchTraining}
                className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-xs transition-colors flex items-center justify-center space-x-1.5 cursor-pointer"
              >
                <Play className="h-3.5 w-3.5 fill-white" />
                <span>Launch Background Training</span>
              </button>
            </div>

          </div>
        </div>
      )}

      {/* FOOTER */}
      <footer className="text-center text-xs text-slate-500 font-medium pt-4">
        Zero-Trust Multi-Model Network Intrusion Detection System • Version 2.0
      </footer>

    </div>
  );
};
