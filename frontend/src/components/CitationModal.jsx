import React, { useState } from 'react';
import { GraduationCap, Copy, Check, X, FileText, BookOpen, Sparkles } from 'lucide-react';
import { cyberAudio } from '../utils/cyberAudio';

export const CitationModal = ({ isOpen, onClose }) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const bibtex = `@article{jnnce_nids_2026,
  author    = {Batch No. 34, Department of Information Science and Engineering},
  title     = {AI-Powered Zero Trust Network Intrusion Detection System (NIDS)},
  institution = {JNN College of Engineering (JNNCE), Shivamogga},
  year      = {2023--2027},
  note      = {Phase 1 Operational Architecture: LSTM Sequence Analysis with Multi-Class Intrusion Interception}
}`;

  const copyToClipboard = () => {
    cyberAudio.playClick();
    navigator.clipboard.writeText(bibtex);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
      <div className="floating-surface rounded-2xl w-full max-w-lg p-6 shadow-spatial-float border border-border/80 space-y-5">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border/40 pb-3">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-xl bg-primary/10 border border-primary/25 flex items-center justify-center text-primary">
              <GraduationCap className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-foreground">Academic Citation & Accreditation</h3>
              <p className="text-[11px] text-muted-foreground font-mono">JNNCE • Dept of ISE • Batch No. 34</p>
            </div>
          </div>
          <button 
            onClick={() => onClose(false)} 
            className="text-muted-foreground hover:text-foreground p-1 rounded-lg hover:bg-muted/40 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Institutional Accreditation Summary */}
        <div className="p-3.5 rounded-xl micro-surface space-y-2 text-xs font-mono">
          <div className="flex justify-between items-center text-[11px]">
            <span className="text-muted-foreground">College:</span>
            <span className="font-bold text-foreground">JNNCE Shivamogga</span>
          </div>
          <div className="flex justify-between items-center text-[11px]">
            <span className="text-muted-foreground">Department:</span>
            <span className="font-semibold text-foreground">Information Science & Engineering</span>
          </div>
          <div className="flex justify-between items-center text-[11px]">
            <span className="text-muted-foreground">Academic Batch:</span>
            <span className="font-bold text-primary">2023–2027 (Batch No. 34)</span>
          </div>
        </div>

        {/* BibTeX Code Snippet */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-muted-foreground font-semibold">BibTeX Citation Entry</span>
            <button
              onClick={copyToClipboard}
              className="flex items-center space-x-1.5 text-primary hover:text-primary-hover font-semibold transition-colors tactile-btn"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied to Clipboard' : 'Copy BibTeX'}</span>
            </button>
          </div>
          
          <div className="bg-[#080d16] p-3.5 rounded-xl border border-primary/20 overflow-x-auto shadow-inner">
            <pre className="text-[11px] font-mono text-cyan-300 leading-relaxed">
              {bibtex}
            </pre>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end pt-1">
          <button
            onClick={() => onClose(false)}
            className="px-4 py-2 rounded-xl micro-surface text-xs font-mono text-muted-foreground hover:text-foreground transition-colors tactile-btn"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
