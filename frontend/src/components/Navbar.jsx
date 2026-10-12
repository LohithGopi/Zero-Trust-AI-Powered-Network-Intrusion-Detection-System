import React, { useState } from 'react';
import { 
  Shield, Lock, ArrowUpRight, Cpu, Layers, Activity, 
  Search, Volume2, VolumeX, GraduationCap, Command
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { Sun, Moon, Monitor } from 'lucide-react';
import { cyberAudio } from '../utils/cyberAudio';

export const Navbar = ({ onOpenLogin, onOpenCommandPalette, onOpenCitation }) => {
  const { themeMode, toggleTheme, isDark } = useTheme();
  const [audioActive, setAudioActive] = useState(cyberAudio.enabled);

  const handleToggleAudio = () => {
    const newState = cyberAudio.toggle();
    setAudioActive(newState);
    if (newState) cyberAudio.playVerify();
  };

  return (
    <div className="sticky top-4 z-50 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
      <nav className="floating-dock rounded-2xl px-4 sm:px-6 py-3 flex items-center justify-between shadow-spatial-md">
        
        {/* Brand & Identity */}
        <a 
          href="#hero" 
          onMouseEnter={() => cyberAudio.playHover()}
          onClick={() => cyberAudio.playClick()}
          className="flex items-center space-x-3 group"
        >
          <div className="relative">
            <img
              src="/jnnce_logo.png"
              alt="JNNCE Logo"
              className="h-8 w-8 sm:h-9 sm:w-9 object-contain bg-white rounded-xl p-0.5 border border-border shadow-spatial-sm transition-transform group-hover:scale-105"
            />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-emerald-500 border-2 border-background animate-pulse" />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-xs sm:text-sm tracking-tight text-foreground">
                Zero Trust AI NIDS
              </span>
              <span className="text-[9px] font-mono font-bold px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/25 hidden md:inline-block">
                BATCH 34
              </span>
            </div>
            <span className="text-[10px] text-muted-foreground font-mono hidden sm:block">
              JNNCE Shivamogga • Dept of ISE
            </span>
          </div>
        </a>

        {/* Anchor Links */}
        <div className="hidden lg:flex items-center space-x-1 font-mono text-xs">
          {[
            { href: '#topology', label: 'Topology' },
            { href: '#zero-trust', label: 'Zero Trust' },
            { href: '#threat-detection', label: 'Threat Studio' },
            { href: '#architecture', label: 'Architecture' },
            { href: '#capabilities', label: 'Capabilities' }
          ].map((link) => (
            <a 
              key={link.href}
              href={link.href}
              onMouseEnter={() => cyberAudio.playHover()}
              onClick={() => cyberAudio.playClick()}
              className="px-3 py-1.5 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted/40 transition-colors"
            >
              {link.label}
            </a>
          ))}
        </div>

        {/* Right CTA & Interactive Controls */}
        <div className="flex items-center space-x-2 sm:space-x-2.5">
          
          {/* Quick Search / Command Palette Pill */}
          <button
            onClick={() => {
              cyberAudio.playClick();
              onOpenCommandPalette?.(true);
            }}
            onMouseEnter={() => cyberAudio.playHover()}
            className="hidden sm:flex items-center space-x-2 px-3 py-1.5 rounded-xl micro-surface hover:border-primary/40 text-muted-foreground hover:text-foreground text-xs font-mono transition-all tactile-btn"
            title="Open Command Palette (Ctrl+K)"
          >
            <Search className="w-3.5 h-3.5 text-primary" />
            <span className="text-[11px]">Command</span>
            <kbd className="px-1.5 py-0.2 rounded bg-muted/60 text-[9px] border border-border">Ctrl+K</kbd>
          </button>

          {/* Academic Citation Trigger */}
          <button
            onClick={() => {
              cyberAudio.playClick();
              onOpenCitation?.(true);
            }}
            onMouseEnter={() => cyberAudio.playHover()}
            title="Academic Citation & Accreditation"
            className="p-2 rounded-xl micro-surface hover:border-primary/40 text-muted-foreground hover:text-foreground transition-colors tactile-btn"
          >
            <GraduationCap className="h-4 w-4 text-primary" />
          </button>

          {/* Tactile Audio Toggle */}
          <button
            onClick={handleToggleAudio}
            title={`Synthesized Audio Feedback: ${audioActive ? 'Active' : 'Muted'}`}
            className="p-2 rounded-xl micro-surface hover:border-primary/40 text-muted-foreground hover:text-foreground transition-colors tactile-btn"
          >
            {audioActive ? (
              <Volume2 className="h-4 w-4 text-emerald-500" />
            ) : (
              <VolumeX className="h-4 w-4 text-muted-foreground" />
            )}
          </button>

          {/* Theme Toggle Button */}
          <button
            onClick={() => {
              cyberAudio.playClick();
              toggleTheme();
            }}
            onMouseEnter={() => cyberAudio.playHover()}
            title={`Theme Mode: ${themeMode.toUpperCase()}`}
            className="p-2 rounded-xl micro-surface hover:border-primary/40 text-muted-foreground hover:text-foreground transition-colors tactile-btn"
          >
            {themeMode === 'system' ? (
              <Monitor className="h-4 w-4 text-primary" />
            ) : isDark ? (
              <Moon className="h-4 w-4 text-cyan-400" />
            ) : (
              <Sun className="h-4 w-4 text-amber-500" />
            )}
          </button>

          {/* Launch Platform Button */}
          <button
            onClick={() => {
              cyberAudio.playClick();
              onOpenLogin();
            }}
            onMouseEnter={() => cyberAudio.playHover()}
            className="px-4 py-2 text-xs font-bold text-white bg-primary hover:bg-primary-hover rounded-xl shadow-spatial-sm hover:shadow-spatial-md transition-all flex items-center space-x-1.5 tactile-btn"
          >
            <Lock className="h-3.5 w-3.5" />
            <span>Launch Platform</span>
            <ArrowUpRight className="h-3.5 w-3.5 hidden sm:inline" />
          </button>
        </div>

      </nav>
    </div>
  );
};


