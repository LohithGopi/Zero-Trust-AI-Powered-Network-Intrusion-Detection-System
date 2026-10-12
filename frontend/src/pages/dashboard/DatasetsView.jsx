import React, { useState } from 'react';
import { Upload, Trash2, FileSpreadsheet, Lock, BarChart2, CheckCircle2, Plus, Database, Sparkles } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const DatasetsView = ({ onNavigate }) => {
  const { user, role, datasets = [], selectDataset, toggleCompareDataset, addDataset, removeDataset } = useAuth();
  const currentRole = role || user?.role || 'Admin';

  const canUpload = currentRole === 'Admin' || currentRole === 'Analyst';
  const canDelete = currentRole === 'Admin';

  const [showUploadModal, setShowUploadModal] = useState(false);
  const [datasetType, setDatasetType] = useState('Custom');
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadError, setUploadError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const safeDatasets = Array.isArray(datasets) ? datasets : [];
  const comparedCount = safeDatasets.filter(d => d && d.isCompared).length;

  const handleSelect = (id, name) => {
    if (!canUpload) {
      alert('Role Restriction: Only Admin and Analyst roles can select datasets for model training.');
      return;
    }
    selectDataset(id);
    setSuccessMsg(`Dataset '${name}' selected as active target for neural network training.`);
    setTimeout(() => setSuccessMsg(''), 4000);
  };

  const handleToggleCompare = (id, name, isCurrentlyCompared) => {
    toggleCompareDataset(id);
    const actionText = !isCurrentlyCompared ? 'added to' : 'removed from';
    setSuccessMsg(`Dataset '${name}' ${actionText} comparison matrix.`);
    setTimeout(() => setSuccessMsg(''), 3000);
  };

  const handleDelete = (id, name) => {
    if (!canDelete) {
      alert('Role Restriction: Only Admin role can delete datasets from system inventory.');
      return;
    }
    if (window.confirm(`Are you sure you want to delete dataset '${name}'?`)) {
      removeDataset(id);
      setSuccessMsg(`Dataset '${name}' deleted successfully.`);
      setTimeout(() => setSuccessMsg(''), 4000);
    }
  };

  const handleUploadSubmit = (e) => {
    e.preventDefault();
    setUploadError('');

    if (!selectedFile) {
      setUploadError('Please choose a valid CSV dataset file.');
      return;
    }

    if (!selectedFile.name.endsWith('.csv')) {
      setUploadError('Invalid file format. Please upload a .csv file.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target.result;
      const lines = text.split('\n').filter(l => l.trim().length > 0);
      const rowCount = Math.max(1, lines.length - 1);
      const colCount = lines[0] ? lines[0].split(',').length : 40;

      const newDs = {
        id: Date.now(),
        name: selectedFile.name,
        type: datasetType,
        rows: rowCount,
        cols: colCount,
        size: `${(selectedFile.size / (1024 * 1024)).toFixed(2)} MB`,
        status: 'Uploaded',
        date: new Date().toISOString().replace('T', ' ').substring(0, 16),
        isSelected: true,
        isCompared: true
      };
      addDataset(newDs, true);
      setShowUploadModal(false);
      setSelectedFile(null);
      setSuccessMsg(`Custom dataset '${newDs.name}' uploaded and added to comparison matrix.`);
      setTimeout(() => setSuccessMsg(''), 5000);
    };

    reader.readAsText(selectedFile.slice(0, 5000000));
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">

      {/* Role Restriction Banner */}
      {!canUpload && (
        <div className="floating-surface rounded-2xl p-4 border-amber-500/30 bg-amber-500/10 text-slate-800 dark:text-slate-200 text-xs flex items-center space-x-2 font-mono">
          <Lock className="h-4 w-4 shrink-0 text-amber-500" />
          <span>
            <strong>READ-ONLY ROLE RESTRICTION:</strong> You are authenticated as <strong>[{currentRole.toUpperCase()}]</strong>. Dataset operations require elevated RBAC permissions.
          </span>
        </div>
      )}

      {/* Header */}
      <div className="floating-surface rounded-2xl p-6 sm:p-7 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-mono text-blue-600 dark:text-blue-400 uppercase tracking-wider font-bold bg-blue-50 dark:bg-blue-950/60 px-2.5 py-0.5 rounded-full border border-blue-200 dark:border-blue-800 inline-block">
            ZERO TRUST REPOSITORY
          </span>
          <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-slate-100 mt-1.5 tracking-tight">
            Datasets Inventory
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Ingest, inspect, select active training target, and configure comparison matrix.
          </p>
        </div>

        <div className="flex items-center space-x-2.5 shrink-0">
          <button
            onClick={() => onNavigate('compare')}
            className="flex items-center space-x-2 text-xs font-semibold micro-surface hover:border-slate-300 dark:hover:border-white/20 text-slate-800 dark:text-slate-200 px-4 py-2.5 rounded-xl transition-all tactile-btn shadow-spatial-sm"
          >
            <BarChart2 className="h-4 w-4 text-blue-600 dark:text-blue-400" />
            <span>Compare Matrix ({comparedCount})</span>
          </button>

          {canUpload ? (
            <button
              onClick={() => setShowUploadModal(true)}
              className="flex items-center space-x-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 px-4 py-2.5 rounded-xl shadow-spatial-sm hover:shadow-spatial-md transition-all tactile-btn"
            >
              <Upload className="h-4 w-4" />
              <span>Upload CSV Dataset</span>
            </button>
          ) : (
            <button
              disabled
              className="flex items-center space-x-2 text-xs font-semibold text-slate-400 micro-surface px-4 py-2.5 rounded-xl cursor-not-allowed opacity-50"
            >
              <Lock className="h-4 w-4 text-slate-400" />
              <span>Upload Restricted</span>
            </button>
          )}
        </div>
      </div>

      {/* Success Notification */}
      {successMsg && (
        <div className="floating-surface rounded-2xl p-4 border-emerald-500/30 bg-emerald-50/20 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300 text-xs font-mono flex items-center space-x-2">
          <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {/* Inventory Table */}
      <div className="floating-surface rounded-2xl shadow-spatial-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs font-mono">
            <thead className="bg-slate-50 dark:bg-[#090B0E] text-slate-500 dark:text-slate-400 text-[10px] uppercase border-b border-slate-200/80 dark:border-white/5">
              <tr>
                <th className="py-3.5 px-4 font-bold">Dataset Name</th>
                <th className="py-3.5 px-4 font-bold">Standard Type</th>
                <th className="py-3.5 px-4 text-right font-bold">Available Rows</th>
                <th className="py-3.5 px-4 text-right font-bold">Training Rows</th>
                <th className="py-3.5 px-4 text-center font-bold">Features</th>
                <th className="py-3.5 px-4 text-center font-bold">File Size</th>
                <th className="py-3.5 px-4 font-bold">Status</th>
                <th className="py-3.5 px-4 text-right font-bold">RBAC Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-white/5">
              {safeDatasets.map((ds) => {
                const displayName = ds.name || ds.filename || 'dataset.csv';
                const dsType = ds.type || ds.dataset_type || 'Custom';
                
                let totalRows = ds.total_rows || ds.rows || ds.row_count || 1000;
                let trainingRows = ds.training_rows || 25000;
                if (dsType.includes('CIC')) {
                  totalRows = 2830743;
                  trainingRows = ds.training_rows || 25000;
                } else if (dsType.includes('UNSW')) {
                  totalRows = 2540044;
                  trainingRows = ds.training_rows || 25000;
                } else if (dsType.includes('NSL')) {
                  totalRows = 148517;
                  trainingRows = ds.training_rows || 148517;
                }

                const dsCols = ds.cols || ds.col_count || 42;
                const dsSize = ds.size || (ds.file_size_mb ? `${ds.file_size_mb} MB` : '0.5 MB');

                return (
                  <tr key={ds.id || displayName} className={`hover:bg-slate-50/80 dark:hover:bg-white/5 transition-colors ${ds.isSelected ? 'bg-blue-50/40 dark:bg-blue-950/20' : ''}`}>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center space-x-2.5">
                        <FileSpreadsheet className="h-4 w-4 text-blue-600 dark:text-blue-400 shrink-0" />
                        <span className="font-bold text-slate-900 dark:text-slate-100 truncate max-w-xs">{displayName}</span>
                        {ds.isSelected && (
                          <span className="text-[9px] bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 px-2 py-0.5 rounded-full font-bold whitespace-nowrap">
                            ACTIVE TARGET
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-600 dark:text-slate-400">{dsType}</td>
                    <td className="py-3.5 px-4 font-bold text-right text-slate-800 dark:text-slate-200">{totalRows.toLocaleString()}</td>
                    <td className="py-3.5 px-4 font-bold text-right text-emerald-600 dark:text-emerald-400">{trainingRows.toLocaleString()}</td>
                    <td className="py-3.5 px-4 text-center text-slate-600 dark:text-slate-400">{dsCols}</td>
                    <td className="py-3.5 px-4 text-center text-slate-600 dark:text-slate-400">{dsSize}</td>
                    <td className="py-3.5 px-4">
                      <span className="text-emerald-600 dark:text-emerald-400 font-bold">{ds.status || 'Uploaded'}</span>
                    </td>
                    <td className="py-3.5 px-4 text-right space-x-2">
                      {/* Compare Toggle */}
                      <button
                        onClick={() => handleToggleCompare(ds.id, displayName, ds.isCompared)}
                        className={`px-2.5 py-1 rounded-xl text-[11px] font-semibold transition-all tactile-btn ${
                          ds.isCompared
                            ? 'bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 border border-purple-300 dark:border-purple-800 shadow-xs'
                            : 'micro-surface text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
                        }`}
                      >
                        {ds.isCompared ? '✓ Matrix' : '+ Compare'}
                      </button>

                      {/* Target Selection */}
                      {ds.isSelected ? (
                        <button
                          disabled
                          className="px-3 py-1 rounded-xl text-[11px] font-bold bg-blue-600 text-white cursor-default shadow-spatial-sm"
                        >
                          Target Active
                        </button>
                      ) : (
                        <button
                          onClick={() => handleSelect(ds.id, displayName)}
                          className="px-3 py-1 rounded-xl text-[11px] font-semibold micro-surface text-blue-600 dark:text-blue-400 hover:border-blue-500/40 transition-colors tactile-btn"
                        >
                          Select Target
                        </button>
                      )}

                      {/* Delete Action (Admin Only) */}
                      {canDelete && (
                        <button
                          onClick={() => handleDelete(ds.id, displayName)}
                          className="p-1.5 rounded-xl text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors tactile-btn"
                          title="Delete Dataset (Admin Only)"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Floating Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-slate-950/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="floating-surface rounded-2xl max-w-md w-full p-6 sm:p-7 shadow-spatial-lg space-y-4">
            
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-3">
              <div className="flex items-center space-x-2">
                <Upload className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 font-sans">Upload Benchmark Dataset (.CSV)</h3>
              </div>
              <button onClick={() => setShowUploadModal(false)} className="text-slate-400 hover:text-slate-600 dark:hover:text-white">✕</button>
            </div>

            {uploadError && (
              <div className="p-3 rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/50 text-red-600 dark:text-red-400 text-xs font-mono">
                {uploadError}
              </div>
            )}

            <form onSubmit={handleUploadSubmit} className="space-y-4 text-xs font-mono">
              <div>
                <label className="block text-slate-700 dark:text-slate-300 mb-1 font-bold font-sans">Select CSV File:</label>
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => setSelectedFile(e.target.files[0])}
                  className="w-full p-2.5 bg-slate-50 dark:bg-[#090B0E] border border-slate-200 dark:border-white/10 rounded-xl text-xs text-slate-900 dark:text-slate-100 outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-700 dark:text-slate-300 mb-1 font-bold font-sans">Dataset Standard Category:</label>
                <select
                  value={datasetType}
                  onChange={(e) => setDatasetType(e.target.value)}
                  className="w-full p-3 bg-slate-50 dark:bg-[#090B0E] border border-slate-200 dark:border-white/10 rounded-xl text-xs text-slate-900 dark:text-slate-100 outline-none"
                >
                  <option value="NSL-KDD">NSL-KDD Standard</option>
                  <option value="UNSW-NB15">UNSW-NB15 Standard</option>
                  <option value="CICIDS2017">CICIDS2017 Standard</option>
                  <option value="Custom">Custom Intrusion Flow Dataset</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-2 pt-2 font-sans">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  className="px-4 py-2.5 rounded-xl micro-surface text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold shadow-spatial-sm transition-colors tactile-btn"
                >
                  Upload & Set Active
                </button>
              </div>
            </form>

          </div>
        </div>
      )}

    </div>
  );
};

