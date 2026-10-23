import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiLogin, apiGetModelStatus, apiGetDatasets } from '../services/api';

const AuthContext = createContext(null);

// Official Benchmark Datasets matching SQLite database IDs exactly
const DEFAULT_DATASETS = [
  { 
    id: 1, 
    name: 'cicids2017_raw.csv', 
    type: 'CIC-IDS2017', 
    rows: 2830743, 
    cols: 79, 
    size: '12.4 MB', 
    status: 'Uploaded', 
    date: '2026-08-10 10:30', 
    isSelected: false, 
    isCompared: true,
    totalRows: 2830743,
    trainingRows: 25000,
    features: 22,
    classes: 15,
    missing: 0,
    duplicates: 0,
    purpose: 'High-Volume DDoS & Web Attack Identification'
  },
  { 
    id: 2, 
    name: 'unsw_nb15_raw.csv', 
    type: 'UNSW-NB15', 
    rows: 2540044, 
    cols: 49, 
    size: '15.2 MB', 
    status: 'Uploaded', 
    date: '2026-08-10 12:15', 
    isSelected: true, 
    isCompared: true,
    totalRows: 2540044,
    trainingRows: 25000,
    features: 15,
    classes: 10,
    missing: 0,
    duplicates: 0,
    purpose: 'Modern Complex Network Flow Analysis'
  },
  { 
    id: 3, 
    name: 'nsl_kdd_raw.csv', 
    type: 'NSL-KDD', 
    rows: 148517, 
    cols: 42, 
    size: '4.8 MB', 
    status: 'Uploaded', 
    date: '2026-08-10 14:20', 
    isSelected: false, 
    isCompared: true,
    totalRows: 148517,
    trainingRows: 50000,
    features: 19,
    classes: 5,
    missing: 0,
    duplicates: 0,
    purpose: 'Benchmark Intrusion Detection System'
  },
  { 
    id: 4, 
    name: 'nsl_kdd_intrusion_dataset.csv', 
    type: 'NSL-KDD', 
    rows: 148517, 
    cols: 42, 
    size: '4.8 MB', 
    status: 'Uploaded', 
    date: '2026-08-10 11:00', 
    isSelected: false, 
    isCompared: false,
    totalRows: 148517,
    trainingRows: 50000,
    features: 19,
    classes: 5,
    missing: 0,
    duplicates: 0,
    purpose: 'Benchmark Intrusion Detection System'
  }
];

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('nids_user');
    return saved ? JSON.parse(saved) : {
      username: 'admin',
      role: 'Admin',
      email: 'admin@jnnce.ac.in',
      batch: 'Batch No. 34'
    };
  });

  const [isAuthenticated, setIsAuthenticated] = useState(() => !!localStorage.getItem('nids_token'));
  const [loading, setLoading] = useState(false);

  // ── Global Dataset Collection (Synchronized with SQLite DB) ──
  const [datasets, setDatasets] = useState(() => {
    const savedDs = localStorage.getItem('nids_datasets');
    if (savedDs) {
      try {
        const parsed = JSON.parse(savedDs);
        // Ensure parsed dataset IDs match reality (id:2 must be UNSW)
        const unswEntry = parsed.find(d => (d.name || '').includes('unsw') || (d.type || '').includes('UNSW'));
        if (unswEntry && unswEntry.id === 2 && Array.isArray(parsed) && parsed.length >= 3) {
          return parsed;
        }
      } catch (err) {
        console.warn('Could not parse saved datasets, using defaults:', err);
      }
    }
    return DEFAULT_DATASETS;
  });

  // Dynamically sync datasets from backend API on mount
  useEffect(() => {
    const syncDatasetsFromBackend = async () => {
      try {
        const res = await apiGetDatasets();
        if (Array.isArray(res) && res.length > 0) {
          const mapped = res.map(d => ({
            id: d.id,
            name: d.filename,
            filename: d.filename,
            type: d.dataset_type,
            dataset_type: d.dataset_type,
            rows: d.total_rows || d.row_count,
            totalRows: d.total_rows || d.row_count,
            cols: d.col_count,
            features: d.dataset_type === 'UNSW-NB15' ? 15 : d.dataset_type === 'NSL-KDD' ? 19 : 22,
            size: `${d.file_size_mb || 0} MB`,
            status: d.upload_status || 'Uploaded',
            date: d.upload_date || '',
            isSelected: d.is_selected || false,
            isCompared: true,
            missing: d.missing_count || 0,
            duplicates: d.duplicate_count || 0,
            classes: d.num_classes || 2,
            purpose: d.dataset_type === 'UNSW-NB15' 
              ? 'Modern Complex Network Flow Analysis' 
              : d.dataset_type === 'NSL-KDD' 
              ? 'Benchmark Intrusion Detection System' 
              : 'High-Volume DDoS & Web Attack Identification'
          }));
          setDatasets(mapped);
          localStorage.setItem('nids_datasets', JSON.stringify(mapped));
        }
      } catch (e) {
        console.warn('Could not sync datasets from backend:', e);
      }
    };
    syncDatasetsFromBackend();
  }, []);

  const activeDataset = datasets.find(d => d.isSelected) || datasets.find(d => (d.type || '').includes('UNSW')) || datasets[0];

  const selectDataset = async (id) => {
    setDatasets(prev => {
      const updated = prev.map(d => ({ ...d, isSelected: d.id === id }));
      localStorage.setItem('nids_datasets', JSON.stringify(updated));
      return updated;
    });
    try {
      const token = localStorage.getItem('nids_token');
      await fetch('/api/dataset/select', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ id })
      });
    } catch (e) {
      console.warn('Dataset select sync error:', e);
    }
  };

  const toggleCompareDataset = (id) => {
    setDatasets(prev => {
      const updated = prev.map(d => (d.id === id ? { ...d, isCompared: !d.isCompared } : d));
      localStorage.setItem('nids_datasets', JSON.stringify(updated));
      return updated;
    });
  };

  const addDataset = (ds, autoSelect = true) => {
    setDatasets(prev => {
      const updated = autoSelect 
        ? prev.map(d => ({ ...d, isSelected: false }))
        : prev;
      const newList = [
        { 
          ...ds, 
          isSelected: autoSelect, 
          isCompared: true,
          missing: ds.missing !== undefined ? ds.missing : 0,
          duplicates: ds.duplicates !== undefined ? ds.duplicates : 0,
          purpose: ds.purpose || 'Custom Ingestion'
        }, 
        ...updated
      ];
      localStorage.setItem('nids_datasets', JSON.stringify(newList));
      return newList;
    });
  };

  const removeDataset = (id) => {
    setDatasets(prev => {
      const filtered = prev.filter(d => d.id !== id);
      const anySelected = filtered.some(d => d.isSelected);
      let updatedList = filtered;
      if (!anySelected && filtered.length > 0) {
        updatedList = filtered.map((d, i) => ({ ...d, isSelected: i === 0 }));
      }
      localStorage.setItem('nids_datasets', JSON.stringify(updatedList));
      return updatedList;
    });
  };

  // ── Model Training Session State (Synchronized across Admin and Analyst views) ──
  const [modelStatus, setModelStatus] = useState('Untrained');
  const [modelMetrics, setModelMetrics] = useState({
    accuracy: '0.00%',
    loss: '0.0000',
    valAccuracy: '0.00%',
    epochs: 0,
    datasetName: 'nsl_kdd_intrusion_dataset.csv',
    trainedAt: 'Pending Training'
  });

  const [trainingProgress, setTrainingProgress] = useState({
    isTraining: false,
    datasetName: 'nsl_kdd_intrusion_dataset.csv',
    currentEpoch: 0,
    totalEpochs: 10,
    accuracy: '0.00%',
    loss: '0.0000',
    statusMessage: '',
    eta: '0s'
  });

  // Background polling to keep Analyst and Admin sections in sync with backend model training
  useEffect(() => {
    let timer = null;
    const pollBackendStatus = async () => {
      try {
        const data = await apiGetModelStatus();
        if (data) {
          const isBusy = data.is_training || data.status === 'Training in progress' || data.status === 'Started' || data.status === 'Preprocessing';
          const rawAcc = data.accuracy || 0;
          const rawLoss = data.loss || 0;
          const accNum = rawAcc > 1 ? rawAcc : rawAcc * 100;
          const accStr = rawAcc > 0 ? `${accNum.toFixed(2)}%` : '0.00%';
          const lossStr = rawLoss > 0 ? rawLoss.toFixed(4) : '0.0000';
          const dsName = data.dataset_name || activeDataset?.name || activeDataset?.filename || 'nsl_kdd_intrusion_dataset.csv';

          if (isBusy) {
            setModelStatus('Training');
            setTrainingProgress({
              isTraining: true,
              datasetName: dsName,
              currentEpoch: data.current_epoch || 0,
              totalEpochs: data.total_epochs || 10,
              accuracy: accStr,
              loss: lossStr,
              statusMessage: data.message || 'Model training in progress in Admin section...',
              eta: data.estimated_time_remaining || '0s'
            });
            setModelMetrics(prev => ({
              ...prev,
              datasetName: dsName,
              accuracy: accStr,
              loss: lossStr,
              epochs: data.total_epochs || prev.epochs || 10
            }));
          } else if (data.status === 'Completed' && (modelStatus === 'Training' || modelStatus === 'Preprocessing')) {
            // Transition to Trained ONLY after active model training finishes in session
            setModelStatus('Trained');
            setTrainingProgress(prev => ({
              ...prev,
              isTraining: false,
              datasetName: dsName,
              accuracy: accStr,
              loss: lossStr,
              statusMessage: 'Model training completed successfully.'
            }));
            setModelMetrics(prev => ({
              ...prev,
              datasetName: dsName,
              accuracy: accStr,
              loss: lossStr,
              epochs: data.total_epochs || prev.epochs || 10,
              trainedAt: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }));
          } else if (modelStatus === 'Training' || modelStatus === 'Preprocessing') {
            setTrainingProgress(prev => ({ ...prev, isTraining: false }));
          }
        }
      } catch (err) {
        // Backend offline or unreachable
      }
    };

    pollBackendStatus();
    timer = setInterval(pollBackendStatus, 2000);
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [activeDataset, modelStatus]);

  const resetModelStatus = () => {
    setModelStatus('Untrained');
    setModelMetrics({
      accuracy: '0.00%',
      loss: '0.0000',
      valAccuracy: '0.00%',
      epochs: 0,
      datasetName: activeDataset?.name || 'nsl_kdd_intrusion_dataset.csv',
      trainedAt: 'Pending Training'
    });
    setTrainingProgress({
      isTraining: false,
      datasetName: activeDataset?.name || 'nsl_kdd_intrusion_dataset.csv',
      currentEpoch: 0,
      totalEpochs: 10,
      accuracy: '0.00%',
      loss: '0.0000',
      statusMessage: '',
      eta: '0s'
    });
  };

  const setTrainedModel = (metrics) => {
    setModelStatus('Trained');
    setModelMetrics(prev => ({ ...prev, ...metrics }));
    setTrainingProgress(prev => ({
      ...prev,
      isTraining: false,
      datasetName: metrics.datasetName || metrics.dataset_name || prev.datasetName,
      accuracy: metrics.accuracy || prev.accuracy,
      loss: metrics.loss || prev.loss
    }));
  };

  const login = async (username, password, selectedRole = 'Admin') => {
    setLoading(true);
    try {
      let data = null;
      try {
        data = await apiLogin(username, password);
      } catch (err) {
        console.warn('API login call fallback active:', err);
      }

      const inferredRole = selectedRole || (data && data.role) || (
        username.toLowerCase().includes('analyst') ? 'Analyst' : 'Admin'
      );

      const userObj = {
        username: (data && (data.username || (data.user && data.user.username))) || username || 'admin',
        role: (data && data.role) || inferredRole,
        email: username.includes('@') ? username : `${username}@jnnce.ac.in`,
        batch: 'Batch No. 34'
      };

      setUser(userObj);
      setIsAuthenticated(true);

      resetModelStatus();
      localStorage.removeItem('active_model');
      localStorage.removeItem('nids_models');
      localStorage.removeItem('nids_evaluation');
      localStorage.removeItem('model_metrics');
      localStorage.removeItem('model_history');

      localStorage.setItem('nids_user', JSON.stringify(userObj));
      const activeToken = (data && data.token && !selectedRole) 
        ? data.token 
        : `demo_token_${userObj.role.toLowerCase()}`;
      localStorage.setItem('nids_token', activeToken);

      return { success: true, role: userObj.role };
    } catch (err) {
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('nids_token');
    localStorage.removeItem('nids_user');
    localStorage.removeItem('active_model');
    localStorage.removeItem('nids_models');
    localStorage.removeItem('nids_evaluation');
    localStorage.removeItem('model_metrics');
    localStorage.removeItem('model_history');
    setIsAuthenticated(false);
    
    resetModelStatus();
    setUser({ username: 'admin', role: 'Admin', email: 'admin@jnnce.ac.in' });
  };

  const switchRole = (newRole) => {
    const updated = { ...user, role: newRole };
    setUser(updated);
    localStorage.setItem('nids_user', JSON.stringify(updated));
    localStorage.setItem('nids_token', `demo_token_${newRole.toLowerCase()}`);
  };

  const currentRole = user?.role || 'Admin';

  return (
    <AuthContext.Provider value={{
      user, role: currentRole, isAuthenticated, loading, login, logout, switchRole,
      // Dataset collection (persisted across logouts)
      datasets, activeDataset, selectDataset, toggleCompareDataset, addDataset, removeDataset,
      // Model training session state
      modelStatus, setModelStatus, modelMetrics, setTrainedModel, resetModelStatus, trainingProgress
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
