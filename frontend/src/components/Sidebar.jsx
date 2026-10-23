import React from 'react';
import { 
  LayoutDashboard, Database, BarChart2, Cpu, Shield, 
  Info, Sun, Moon, LogOut, User as UserIcon, Radio
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export const Sidebar = ({ 
  activeTab, 
  setActiveTab, 
  onLogout, 
  onOpenProfile, 
  onOpenCommandPalette, 
  onOpenCitation 
}) => {
  const { user, role, logout } = useAuth();
  const { toggleTheme, isDark } = useTheme();
  const currentRole = role || user?.role || 'Admin';
  const isAdmin = currentRole === 'Admin';

  const handleLogoutClick = () => {
    logout();
    if (onLogout) {
      onLogout();
    }
  };

  const navItems = isAdmin ? [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'datasets', label: 'Datasets', icon: Database },
    { id: 'compare', label: 'Compare Datasets', icon: BarChart2 },
    { id: 'training', label: 'Model Training', icon: Cpu },
    { id: 'live-detection', label: 'Live Detection', icon: Radio },
    { id: 'model-details', label: 'Performance Evaluation', icon: BarChart2 },
    { id: 'audit-logs', label: 'Behavioral & Audit', icon: Shield },
    { id: 'about', label: 'About', icon: Info }
  ] : [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'datasets', label: 'Datasets', icon: Database },
    { id: 'compare', label: 'Compare Datasets', icon: BarChart2 },
    { id: 'live-detection', label: 'Live Detection', icon: Radio },
    { id: 'model-details', label: 'Performance Evaluation', icon: Cpu },
    { id: 'audit-logs', label: 'Behavioral & Audit', icon: Shield },
    { id: 'about', label: 'About', icon: Info }
  ];

  return (
    <header className="w-full bg-[#070e22] border-b border-slate-800 text-white sticky top-0 z-50 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 flex flex-wrap items-center justify-between gap-3">
        
        {/* Left: Emblem & System Name */}
        <div 
          onClick={() => setActiveTab('dashboard')}
          className="flex items-center space-x-3 cursor-pointer shrink-0"
        >
          <div className="h-7 w-7 rounded-md bg-white p-0.5 border border-slate-700 flex items-center justify-center shrink-0">
            <img
              src="/jnnce_logo.png"
              alt="JNNCE Logo"
              className="h-full w-full object-contain"
            />
          </div>

          <span className="font-extrabold text-xs sm:text-sm tracking-tight text-white">
            Zero Trust AI-Powered Network Intrusion Detection System
          </span>
          
          <span className="text-[9px] font-mono font-bold px-2 py-0.5 rounded bg-blue-600/30 text-blue-400 border border-blue-500/40 shrink-0 hidden sm:inline-block">
            BATCH NO. 34
          </span>
        </div>

        {/* Right: Controls & User Status */}
        <div className="flex items-center space-x-2.5 shrink-0">
          
          {/* RBAC Role Pill */}
          <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded ${
            isAdmin 
              ? 'bg-purple-900/60 text-purple-300 border border-purple-500/40' 
              : 'bg-blue-900/60 text-blue-300 border border-blue-500/40'
          }`}>
            [{isAdmin ? 'ADMIN' : 'ANALYST'}]
          </span>

          {/* Theme Switcher */}
          <button
            onClick={toggleTheme}
            className="p-1.5 rounded-lg text-amber-400 hover:text-amber-300 hover:bg-slate-800 transition-colors"
            title="Toggle Theme"
          >
            {isDark ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
          </button>

          {/* User badge */}
          <div className="flex items-center space-x-1.5 text-xs text-slate-200 px-2 py-1">
            <UserIcon className="h-3.5 w-3.5 text-slate-400" />
            <span className="font-medium">{user?.username || 'admin'}</span>
          </div>

          {/* Logout Button */}
          <button
            onClick={handleLogoutClick}
            className="flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-semibold text-rose-400 border border-rose-500/40 hover:bg-rose-500/20 transition-colors"
            title="Logout Session"
          >
            <LogOut className="h-3.5 w-3.5" />
            <span>Logout</span>
          </button>
        </div>

        {/* Navigation Tabs Bar */}
        <div className="w-full flex items-center space-x-1.5 overflow-x-auto pt-1 pb-0.5 no-scrollbar text-xs font-sans">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white font-bold shadow-xs'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`h-3.5 w-3.5 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

      </div>
    </header>
  );
};
