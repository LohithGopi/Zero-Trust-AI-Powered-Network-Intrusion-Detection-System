import React from 'react';
import { FileSpreadsheet, Layers } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const CompareView = () => {
  const { datasets = [], toggleCompareDataset } = useAuth();
  const comparedItems = (datasets || []).filter(d => d && d.isCompared);

  return (
    <div className="space-y-6 animate-fade-in pb-12 font-sans">
      
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-mono text-cyan-600 uppercase tracking-wider font-bold bg-cyan-50 px-2.5 py-0.5 rounded-full border border-cyan-200 inline-block">
            BENCHMARK MATRIX
          </span>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 mt-1.5 tracking-tight">
            NIDS Dataset Comparison Matrix
          </h1>
          <p className="text-xs text-slate-500">
            Side-by-side specification comparison across real CIC-IDS2017, UNSW-NB15, and NSL-KDD datasets.
          </p>
        </div>

        {/* Dataset Selection Toggles */}
        <div className="flex flex-wrap items-center gap-2 font-mono text-xs">
          {(datasets || []).map(d => {
            const displayName = d.name || d.filename || 'dataset.csv';
            return (
              <button
                key={d.id || displayName}
                onClick={() => toggleCompareDataset && toggleCompareDataset(d.id)}
                className={`px-3 py-1.5 rounded-lg font-semibold transition-all active:scale-95 border ${
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
      </div>

      {comparedItems.length === 0 ? (
        <div className="bg-white p-12 text-center text-xs text-slate-400 rounded-2xl space-y-3 border border-dashed border-slate-200">
          <Layers className="h-8 w-8 text-slate-400 mx-auto" />
          <p className="font-bold text-sm text-slate-800">No Datasets Selected for Comparison</p>
          <p className="text-slate-500">Click any of the dataset buttons above to add it to the comparison matrix.</p>
        </div>
      ) : (
        /* Comparison Cards Grid */
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
                    <span className="text-slate-500">Total Available Rows:</span>
                    <span className="text-slate-900 font-bold">{totalRows.toLocaleString()}</span>
                  </div>

                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Selected Training Rows:</span>
                    <span className="text-emerald-600 font-bold">{trainingRows.toLocaleString()}</span>
                  </div>

                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Total Features:</span>
                    <span className="text-slate-900 font-bold">{numFeatures}</span>
                  </div>

                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Target Classes:</span>
                    <span className="text-purple-600 font-bold">{numClasses} Classes</span>
                  </div>

                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Missing Values:</span>
                    <span className={`font-bold ${missingCount > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
                      {missingCount > 0 ? `${missingCount} Cells` : '0 (Clean)'}
                    </span>
                  </div>

                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Duplicate Records:</span>
                    <span className={`font-bold ${dupCount > 0 ? 'text-purple-600' : 'text-emerald-600'}`}>
                      {dupCount > 0 ? `${dupCount} Rows` : '0 (Unique)'}
                    </span>
                  </div>

                  <div className="pt-2">
                    <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1">
                      BENCHMARK PROFILE:
                    </span>
                    <div className="p-2.5 rounded-xl bg-blue-50/70 border border-blue-100 text-[11px] font-bold text-blue-700">
                      {purposeText}
                    </div>
                  </div>

                </div>

              </div>
            );
          })}
        </div>
      )}

      {/* Footer */}
      <footer className="text-center text-xs text-slate-500 font-medium pt-4">
        Department of Information Science & Engineering • Project Batch No. 34
      </footer>

    </div>
  );
};
