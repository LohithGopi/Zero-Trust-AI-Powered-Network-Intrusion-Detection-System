import React, { useState } from 'react';
import { Sidebar } from '../components/Sidebar';
import { CommandPalette } from '../components/CommandPalette';
import { CitationModal } from '../components/CitationModal';
import { OverviewView } from './dashboard/OverviewView';
import { DatasetsView } from './dashboard/DatasetsView';
import { CompareView } from './dashboard/CompareView';
import { TrainingView } from './dashboard/TrainingView';
import { ModelDetailsView } from './dashboard/ModelDetailsView';
import { AuditLogsView } from './dashboard/AuditLogsView';
import { ProfileView } from './dashboard/ProfileView';
import { AboutView } from './dashboard/AboutView';
import { LiveDetectionView } from './dashboard/LiveDetectionView';
import { useAuth } from '../context/AuthContext';
import { Activity, Radio, Cpu, Sparkles } from 'lucide-react';

export const DashboardApp = ({ onBackToLanding }) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [showProfile, setShowProfile] = useState(false);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [isCitationOpen, setIsCitationOpen] = useState(false);
  const { user, role, modelStatus, modelMetrics, trainingProgress, logout } = useAuth();
  const isAdmin = (role || user?.role) === 'Admin';
  const isTraining = modelStatus === 'Training' || modelStatus === 'Preprocessing' || (trainingProgress && trainingProgress.isTraining);
  const activeDatasetName = trainingProgress?.datasetName || modelMetrics?.datasetName || 'nsl_kdd_intrusion_dataset.csv';
  const displayAcc = trainingProgress?.accuracy && trainingProgress.accuracy !== '0.00%' ? trainingProgress.accuracy : modelMetrics.accuracy;
  const displayLoss = trainingProgress?.loss && trainingProgress.loss !== '0.0000' ? trainingProgress.loss : modelMetrics.loss;

  const handleLogout = () => {
    logout();
    if (onBackToLanding) {
      onBackToLanding();
    }
  };

  const renderActiveView = () => {
    if (showProfile) {
      return <ProfileView onClose={() => setShowProfile(false)} />;
    }

    switch (activeTab) {
      case 'dashboard':
        return <OverviewView onNavigate={setActiveTab} />;
      case 'datasets':
        return <DatasetsView onNavigate={setActiveTab} />;
      case 'compare':
        return <CompareView />;
      case 'training':
        return isAdmin ? <TrainingView onNavigate={setActiveTab} /> : <OverviewView onNavigate={setActiveTab} />;
      case 'model-details':
        return <ModelDetailsView onNavigate={setActiveTab} />;
      case 'live-detection':
        return <LiveDetectionView onNavigate={setActiveTab} />;
      case 'audit-logs':
        return <AuditLogsView />;
      case 'about':
        return <AboutView />;
      default:
        return <OverviewView onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 flex flex-col transition-colors duration-200">
      
      {/* Top Navigation Bar */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={(tab) => { setShowProfile(false); setActiveTab(tab); }} 
        onLogout={handleLogout}
        onOpenProfile={() => setShowProfile(true)}
        onOpenCommandPalette={setIsCommandPaletteOpen}
        onOpenCitation={setIsCitationOpen}
      />

      {/* Global Interactive Command Palette HUD (Ctrl+K) */}
      <CommandPalette 
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onNavigate={(tab) => {
          setShowProfile(false);
          setActiveTab(tab);
        }}
      />

      {/* Academic Citation & Accreditation Modal */}
      <CitationModal
        isOpen={isCitationOpen}
        onClose={() => setIsCitationOpen(false)}
      />

      {/* Global Analyst Live Training HUD */}
      {!isAdmin && isTraining && (
        <div className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 mt-4">
          <div className="bg-amber-500/10 rounded-2xl p-4 border-2 border-amber-500/40 text-slate-900 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-sm">
            <div className="flex items-center space-x-3">
              <div className="h-9 w-9 rounded-xl bg-amber-500 text-slate-950 flex items-center justify-center font-bold shrink-0 shadow-sm animate-pulse">
                <Cpu className="h-5 w-5" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-[10px] font-mono font-bold bg-amber-500 text-slate-950 px-2 py-0.5 rounded uppercase">
                    ⚡ LIVE ADMIN TRAINING
                  </span>
                  <span className="text-xs font-mono font-bold truncate">
                    Dataset: {activeDatasetName}
                  </span>
                </div>
                <div className="text-xs text-slate-600 font-sans mt-0.5">
                  Epoch {trainingProgress?.currentEpoch || 0} of {trainingProgress?.totalEpochs || 10} • Recurrent weights recalculating
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-3 font-mono text-xs shrink-0 self-end sm:self-auto">
              <div className="p-2 rounded-xl bg-white border border-slate-200">
                <span className="text-[9px] text-slate-400 block">TRAINING ACC</span>
                <span className="font-bold text-emerald-600">{displayAcc}</span>
              </div>
              <div className="p-2 rounded-xl bg-white border border-slate-200">
                <span className="text-[9px] text-slate-400 block">TRAINING LOSS</span>
                <span className="font-bold text-amber-600">{displayLoss}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Workspace Stage */}
      <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
        {renderActiveView()}
      </main>

      {/* Footer */}
      <footer className="py-4 border-t border-slate-200/80 text-center text-xs text-slate-500 font-sans">
        Department of Information Science & Engineering • Project Batch No. 34
      </footer>

    </div>
  );
};

