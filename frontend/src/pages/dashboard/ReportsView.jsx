import React, { useState, useEffect } from 'react';
import { BarChart2, CheckCircle2, FileText, Download, ShieldCheck, Activity, AlertCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { apiGetModelReport } from '../../services/api';

export const ReportsView = () => {
  const { modelStatus, modelMetrics } = useAuth();
  const isTrained = modelStatus === 'Trained';

  const [reportData, setReportData] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);

  useEffect(() => {
    const fetchReport = async () => {
      if (isTrained) {
        setLoadingReport(true);
        try {
          const data = await apiGetModelReport();
          if (data && !data.error) {
            setReportData(data);
          }
        } catch (err) {
          console.warn('Could not load report JSON from backend:', err);
        } finally {
          setLoadingReport(false);
        }
      }
    };
    fetchReport();
  }, [isTrained]);

  const classes = reportData?.classes || ['Normal', 'DoS', 'Exploits', 'Generic', 'Fuzzers', 'Reconnaissance'];
  const confusionMatrix = reportData?.confusion_matrix || null;

  const accDisplay = reportData?.accuracy ? `${(reportData.accuracy * 100).toFixed(2)}%` : modelMetrics.accuracy;
  const precDisplay = reportData?.precision ? `${(reportData.precision * 100).toFixed(2)}%` : '0.00%';
  const recDisplay = reportData?.recall ? `${(reportData.recall * 100).toFixed(2)}%` : '0.00%';
  const f1Display = reportData?.f1_score ? `${(reportData.f1_score * 100).toFixed(2)}%` : '0.00%';
  const lossDisplay = modelMetrics.loss !== '0.0000' ? modelMetrics.loss : (reportData?.loss ? reportData.loss.toFixed(4) : '0.0000');

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-[#15191C] border border-[#E2E8F0] dark:border-[#252A2E] rounded-2xl p-6 shadow-sm">
        <div>
          <div className="flex items-center space-x-3">
            <h1 className="text-xl font-bold text-[#172033] dark:text-[#F3F4F1]">Model Evaluation Report</h1>
            <span className={`text-xs font-mono font-bold px-2.5 py-0.5 rounded-full border ${
              isTrained
                ? 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800'
                : 'bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800'
            }`}>
              {isTrained ? '✓ Trained Session' : '⚠ Pending Session Training'}
            </span>
          </div>
          <p className="text-xs text-[#475569] dark:text-[#9FA6A8] mt-1">
            Detailed evaluation metrics, loss values, and multi-class confusion matrix from held-out evaluation dataset.
          </p>
        </div>

        {isTrained ? (
          <button 
            onClick={() => window.print()}
            className="flex items-center space-x-2 text-xs font-semibold text-white bg-[#1769E0] hover:bg-[#0F3B68] px-4 py-2.5 rounded-xl shadow-md transition-colors"
          >
            <Download className="h-4 w-4" />
            <span>Export Report PDF</span>
          </button>
        ) : (
          <button 
            disabled
            className="flex items-center space-x-2 text-xs font-semibold text-slate-400 bg-slate-100 dark:bg-[#0B0D0F] border border-slate-200 dark:border-[#252A2E] px-4 py-2.5 rounded-xl cursor-not-allowed"
          >
            <AlertCircle className="h-4 w-4 text-slate-400" />
            <span>Export Pending Training</span>
          </button>
        )}
      </div>

      {/* Untrained Session Notice Banner */}
      {!isTrained && (
        <div className="p-5 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-300 text-xs font-mono space-y-2">
          <div className="flex items-center space-x-2 text-sm font-bold text-amber-800 dark:text-amber-300">
            <AlertCircle className="h-5 w-5 text-amber-600 shrink-0" />
            <span>MODEL PENDING TRAINING</span>
          </div>
          <p className="leading-relaxed">
            {role === 'Admin' ? (
              <>The model status is currently <strong>Untrained</strong> for this session. Go to the <strong>Model Training</strong> tab and click <strong>Start Model Training</strong> to execute the training pipeline and generate evaluation metrics.</>
            ) : (
              <>The model status is currently <strong>Untrained</strong>. Model training is executed in the Admin section.</>
            )}
          </p>
        </div>
      )}

      {/* Key Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        
        <div className="bg-white dark:bg-[#15191C] border border-[#E2E8F0] dark:border-[#252A2E] rounded-xl p-4 shadow-sm">
          <span className="text-[10px] font-mono text-[#475569] dark:text-[#9FA6A8] uppercase block mb-1">Accuracy</span>
          <div className={`text-2xl font-bold font-mono ${isTrained ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-400'}`}>
            {isTrained ? accDisplay : '0.00%'}
          </div>
          <span className="text-[10px] text-[#475569] dark:text-[#9FA6A8] mt-1 block">Test Dataset Split</span>
        </div>

        <div className="bg-white dark:bg-[#15191C] border border-[#E2E8F0] dark:border-[#252A2E] rounded-xl p-4 shadow-sm">
          <span className="text-[10px] font-mono text-[#475569] dark:text-[#9FA6A8] uppercase block mb-1">Loss</span>
          <div className={`text-2xl font-bold font-mono ${isTrained ? 'text-red-600 dark:text-red-400' : 'text-slate-400'}`}>
            {isTrained ? lossDisplay : '0.0000'}
          </div>
          <span className="text-[10px] text-[#475569] dark:text-[#9FA6A8] mt-1 block">Crossentropy</span>
        </div>

        <div className="bg-white dark:bg-[#15191C] border border-[#E2E8F0] dark:border-[#252A2E] rounded-xl p-4 shadow-sm">
          <span className="text-[10px] font-mono text-[#475569] dark:text-[#9FA6A8] uppercase block mb-1">Precision</span>
          <div className={`text-2xl font-bold font-mono ${isTrained ? 'text-[#1769E0]' : 'text-slate-400'}`}>
            {isTrained ? precDisplay : '0.00%'}
          </div>
          <span className="text-[10px] text-[#475569] dark:text-[#9FA6A8] mt-1 block">Weighted Precision</span>
        </div>

        <div className="bg-white dark:bg-[#15191C] border border-[#E2E8F0] dark:border-[#252A2E] rounded-xl p-4 shadow-sm">
          <span className="text-[10px] font-mono text-[#475569] dark:text-[#9FA6A8] uppercase block mb-1">Recall</span>
          <div className={`text-2xl font-bold font-mono ${isTrained ? 'text-purple-600 dark:text-purple-400' : 'text-slate-400'}`}>
            {isTrained ? recDisplay : '0.00%'}
          </div>
          <span className="text-[10px] text-[#475569] dark:text-[#9FA6A8] mt-1 block">Sensitivity / Detection Rate</span>
        </div>

        <div className="bg-white dark:bg-[#15191C] border border-[#E2E8F0] dark:border-[#252A2E] rounded-xl p-4 shadow-sm col-span-2 md:col-span-1">
          <span className="text-[10px] font-mono text-[#475569] dark:text-[#9FA6A8] uppercase block mb-1">F1-Score</span>
          <div className={`text-2xl font-bold font-mono ${isTrained ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400'}`}>
            {isTrained ? f1Display : '0.00%'}
          </div>
          <span className="text-[10px] text-[#475569] dark:text-[#9FA6A8] mt-1 block">Harmonic Mean</span>
        </div>

      </div>

      {/* Confusion Matrix Section */}
      <div className="bg-white dark:bg-[#15191C] border border-[#E2E8F0] dark:border-[#252A2E] rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 dark:border-[#252A2E] pb-3">
          <div className="flex items-center space-x-2">
            <BarChart2 className="h-4 w-4 text-[#1769E0]" />
            <h2 className="text-sm font-bold text-[#172033] dark:text-[#F3F4F1]">
              Confusion Matrix Heatmap ({classes.length}-Class Target Categories)
            </h2>
          </div>
          <span className="text-xs font-mono text-[#475569] dark:text-[#9FA6A8]">
            Actual vs. Predicted Traffic
          </span>
        </div>

        {!isTrained || !confusionMatrix ? (
          <div className="h-48 flex flex-col items-center justify-center text-xs font-mono text-[#475569] dark:text-[#9FA6A8] bg-[#F5F7FA] dark:bg-[#0B0D0F] rounded-xl border border-[#E2E8F0] dark:border-[#252A2E] p-4 text-center">
            <AlertCircle className="h-6 w-6 text-slate-400 mb-2" />
            <span>Confusion Matrix will be computed and displayed after completing a model training run.</span>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-center text-xs font-mono border-collapse">
              <thead>
                <tr>
                  <th className="p-2 text-left bg-[#F5F7FA] dark:bg-[#0B0D0F] text-[#475569] dark:text-[#9FA6A8] border border-[#E2E8F0] dark:border-[#252A2E]">
                    Actual \ Predicted
                  </th>
                  {classes.map((cls) => (
                    <th key={cls} className="p-2 bg-[#F5F7FA] dark:bg-[#0B0D0F] text-[#172033] dark:text-[#F3F4F1] border border-[#E2E8F0] dark:border-[#252A2E]">
                      {cls}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {confusionMatrix.map((row, rIdx) => (
                  <tr key={rIdx}>
                    <td className="p-2 font-bold text-left bg-[#F5F7FA] dark:bg-[#0B0D0F] text-[#172033] dark:text-[#F3F4F1] border border-[#E2E8F0] dark:border-[#252A2E]">
                      {classes[rIdx] || `Class ${rIdx}`}
                    </td>
                    {row.map((val, cIdx) => {
                      const isDiagonal = rIdx === cIdx;
                      return (
                        <td 
                          key={cIdx} 
                          className={`p-2.5 border border-[#E2E8F0] dark:border-[#252A2E] font-bold ${
                            isDiagonal 
                              ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300' 
                              : val > 0 
                              ? 'bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-300' 
                              : 'text-slate-400'
                          }`}
                        >
                          {val}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
};
