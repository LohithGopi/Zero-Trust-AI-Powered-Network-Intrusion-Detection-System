import React, { useState, useEffect } from 'react';
import { 
  Search, Terminal, Database, Activity, Shield, Cpu, 
  Moon, Sun, Volume2, VolumeX, ArrowRight, UserCheck, 
  FileText, Sparkles, X, Command, Key, Layers
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { cyberAudio } from '../utils/cyberAudio';

export const CommandPalette = ({ isOpen, onClose, onNavigate, onSimulateAttack }) => {
  const [query, setQuery] = useState('');
  const [soundEnabled, setSoundEnabled] = useState(cyberAudio.enabled);
  const { role, user, selectDataset, datasets = [] } = useAuth();
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        onClose(!isOpen);
      }
      if (e.key === 'Escape' && isOpen) {
        onClose(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const actions = [
    {
      category: 'Navigation',
      items: [
        { id: 'nav-overview', label: 'SOC Command Center Overview', icon: Activity, action: () => { onNavigate?.('overview'); onClose(false); } },
        { id: 'nav-training', label: 'Deep Learning Model Training Studio', icon: Cpu, action: () => { onNavigate?.('training'); onClose(false); } },
        { id: 'nav-live', label: 'Live Network Traffic Detection (Passive Sniffing)', icon: Activity, action: () => { onNavigate?.('live-detection'); onClose(false); } },
        { id: 'nav-datasets', label: 'Dataset Ingestion & Repository', icon: Database, action: () => { onNavigate?.('datasets'); onClose(false); } },
        { id: 'nav-compare', label: 'Multi-Dataset Benchmark Comparison', icon: Layers, action: () => { onNavigate?.('compare'); onClose(false); } },
        { id: 'nav-model', label: 'LSTM Neural Model Specifications', icon: Terminal, action: () => { onNavigate?.('model'); onClose(false); } },
        { id: 'nav-audit', label: 'Immutable Audit Trail Stream', icon: Shield, action: () => { onNavigate?.('audit'); onClose(false); } },
        { id: 'nav-about', label: 'Technical Documentation & Architecture', icon: FileText, action: () => { onNavigate?.('about'); onClose(false); } }
      ]
    },
    {
      category: 'Simulations & Attack Interceptions',
      items: [
        { id: 'sim-syn', label: 'Simulate TCP-SYN Flood Attack Ingress', icon: Sparkles, color: 'text-rose-500', action: () => { onSimulateAttack?.('SYN Flood'); onClose(false); } },
        { id: 'sim-portscan', label: 'Simulate Network PortScan Probe', icon: Sparkles, color: 'text-amber-500', action: () => { onSimulateAttack?.('PortScan'); onClose(false); } },
        { id: 'sim-ssh', label: 'Simulate SSH Brute Force Infiltration', icon: Sparkles, color: 'text-purple-500', action: () => { onSimulateAttack?.('SSH-BruteForce'); onClose(false); } }
      ]
    },
    {
      category: 'System & Controls',
      items: [
        { 
          id: 'toggle-theme', 
          label: `Switch Theme (Current: ${theme === 'dark' ? 'Cyber Dark' : 'Clean Light'})`, 
          icon: theme === 'dark' ? Sun : Moon, 
          action: () => { toggleTheme(); onClose(false); } 
        },
        { 
          id: 'toggle-audio', 
          label: `Tactile Sound Synthesizer: ${soundEnabled ? 'Enabled' : 'Muted'}`, 
          icon: soundEnabled ? Volume2 : VolumeX, 
          action: () => { 
            const state = cyberAudio.toggle(); 
            setSoundEnabled(state); 
            if (state) cyberAudio.playVerify();
          } 
        }
      ]
    }
  ];

  const filtered = actions.map(cat => ({
    ...cat,
    items: cat.items.filter(item => item.label.toLowerCase().includes(query.toLowerCase()))
  })).filter(cat => cat.items.length > 0);

  return (
    <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-md flex items-start justify-center pt-24 p-4 animate-fade-in">
      <div 
        className="floating-surface rounded-2xl w-full max-w-xl shadow-spatial-float border border-border/80 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input Header */}
        <div className="flex items-center px-4 py-3.5 border-b border-border/60 bg-muted/20">
          <Search className="w-5 h-5 text-primary mr-3 shrink-0" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command, simulation, or search view..."
            className="w-full bg-transparent text-foreground text-sm font-mono outline-none placeholder:font-sans placeholder:text-muted-foreground"
          />
          <div className="flex items-center space-x-1.5 ml-2">
            <kbd className="px-2 py-0.5 rounded bg-muted/60 text-[10px] font-mono text-muted-foreground border border-border">ESC</kbd>
            <button 
              onClick={() => onClose(false)} 
              className="text-muted-foreground hover:text-foreground p-1 rounded-lg hover:bg-muted/40 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 space-y-4 font-sans text-xs">
          {filtered.length === 0 ? (
            <div className="py-8 text-center text-muted-foreground font-mono">
              No matching commands found for "{query}"
            </div>
          ) : (
            filtered.map((cat, idx) => (
              <div key={idx} className="space-y-1">
                <div className="px-3 py-1 text-[10px] font-mono font-bold uppercase tracking-wider text-muted-foreground">
                  {cat.category}
                </div>
                {cat.items.map(item => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.id}
                      onClick={() => {
                        cyberAudio.playClick();
                        item.action();
                      }}
                      onMouseEnter={() => cyberAudio.playHover()}
                      className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-left hover:bg-primary/10 hover:text-primary transition-all group micro-surface border-transparent"
                    >
                      <div className="flex items-center space-x-3">
                        <Icon className={`w-4 h-4 ${item.color || 'text-primary'}`} />
                        <span className="font-medium text-foreground group-hover:text-primary transition-colors">
                          {item.label}
                        </span>
                      </div>
                      <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all text-primary" />
                    </button>
                  );
                })}
              </div>
            ))
          )}
        </div>

        {/* Footer Quick Keys */}
        <div className="px-4 py-2.5 border-t border-border/40 bg-muted/30 flex items-center justify-between text-[11px] font-mono text-muted-foreground">
          <div className="flex items-center space-x-3">
            <span>↑↓ Navigate</span>
            <span>↵ Select</span>
            <span>Ctrl+K Toggle</span>
          </div>
          <span className="text-primary font-semibold">Zero Trust AI NIDS</span>
        </div>
      </div>
    </div>
  );
};
