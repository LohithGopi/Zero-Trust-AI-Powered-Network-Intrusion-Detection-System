import React from 'react';
import { Shield, Lock, ArrowRight, GraduationCap } from 'lucide-react';

export const LandingPage = ({ onExplore, onOpenLogin, onSwitchToTrojan }) => {
  const handlePortalAccess = () => {
    if (onOpenLogin) {
      onOpenLogin();
    } else if (onExplore) {
      onExplore();
    }
  };

  return (
    <div className="min-h-screen bg-[#f4f7fc] text-slate-900 flex flex-col justify-between selection:bg-blue-500/20 selection:text-blue-600">
      
      {/* TOP NAVIGATION BAR */}
      <header className="w-full bg-white/90 backdrop-blur-md border-b border-slate-200/80 px-4 sm:px-8 py-3.5 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
          
          {/* Left: Brand / College Info */}
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-white border border-slate-200 shadow-xs p-1 flex items-center justify-center shrink-0">
              <img
                src="/jnnce_logo.png"
                alt="JNNCE Logo"
                className="h-full w-full object-contain"
              />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-xs sm:text-sm text-slate-900 tracking-tight">
                  Zero Trust AI-Powered NIDS
                </span>
                <span className="text-[9px] font-mono font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-600 border border-blue-200 shrink-0">
                  BATCH 34
                </span>
              </div>
              <p className="text-[10px] sm:text-[11px] text-slate-500 font-medium">
                JNNCE Shimoga • Dept of Information Science & Engineering
              </p>
            </div>
          </div>

          {/* Right: Academic Project Tag */}
          <div className="flex items-center space-x-2">
            <span className="hidden sm:inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-100 text-slate-700 border border-slate-200/80 text-xs font-semibold">
              <GraduationCap className="h-3.5 w-3.5 text-blue-600" />
              <span>B.E. Final Year Project (2023–2027)</span>
            </span>
          </div>

        </div>
      </header>

      {/* CENTER HERO SECTION */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-10 sm:py-16 text-center max-w-4xl mx-auto w-full">
        
        {/* Emblem Card with soft shadow */}
        <div className="mb-6 relative">
          <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-3xl bg-white p-3 border border-slate-200/90 shadow-xl shadow-blue-500/10 flex items-center justify-center mx-auto transition-transform hover:scale-105">
            <img
              src="/jnnce_logo.png"
              alt="JNNCE College Emblem"
              className="h-full w-full object-contain"
            />
          </div>
        </div>

        {/* Institution Title */}
        <div className="space-y-1.5 max-w-3xl">
          <h1 className="text-sm sm:text-base md:text-lg font-black text-slate-900 uppercase tracking-tight">
            JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING, SHIVAMOGGA
          </h1>
          <h2 className="text-xs sm:text-sm md:text-base font-extrabold text-blue-700 uppercase tracking-wide">
            DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING
          </h2>
          <p className="text-[10px] sm:text-xs text-slate-500 font-medium">
            Affiliated to Visvesvaraya Technological University (VTU), Belagavi • Approved by AICTE, New Delhi
          </p>
        </div>

        {/* Project Highlight Box */}
        <div className="mt-8 bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 sm:p-9 max-w-3xl w-full text-center space-y-3.5">
          
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-blue-50 text-blue-600 border border-blue-200 text-[10px] sm:text-xs font-bold uppercase tracking-wider">
            <Shield className="h-3.5 w-3.5" />
            <span>FINAL YEAR B.E. ACADEMIC PROJECT (2023–2027)</span>
          </div>

          <h3 className="text-xl sm:text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight leading-tight">
            Zero Trust AI-Powered Network Intrusion Detection System
          </h3>

          <p className="text-xs sm:text-sm text-slate-600 font-medium max-w-2xl mx-auto">
            Phase 1 — Dataset Preparation, Zero Trust Architecture, and AI-Based Intrusion Detection Model
          </p>
        </div>

        {/* Project Batch Tag */}
        <div className="mt-6">
          <span className="inline-flex items-center space-x-1.5 px-4 py-1 rounded-full bg-blue-50 text-blue-600 border border-blue-200 text-xs font-semibold tracking-wide">
            <GraduationCap className="h-4 w-4" />
            <span>PROJECT BATCH NO. 34</span>
          </span>
        </div>

        {/* Login to Security Portal Button */}
        <div className="mt-6">
          <button
            onClick={handlePortalAccess}
            className="px-6 py-3 text-xs sm:text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md hover:shadow-lg transition-all flex items-center space-x-2 active:scale-95"
          >
            <Lock className="h-4 w-4" />
            <span>Login to Security Portal</span>
            <ArrowRight className="h-4 w-4 ml-1" />
          </button>
        </div>

      </main>

      {/* FOOTER */}
      <footer className="py-4 text-center text-xs text-slate-500 font-medium border-t border-slate-200/60 bg-white/40">
        Department of Information Science & Engineering • Project Batch No. 34
      </footer>

    </div>
  );
};
