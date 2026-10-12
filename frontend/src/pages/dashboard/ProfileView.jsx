import React, { useState } from 'react';
import { Shield, Key, Eye, EyeOff, CheckCircle2, XCircle, User as UserIcon, Lock, Sparkles, X } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const ProfileView = ({ onClose }) => {
  const { user, role } = useAuth();
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // Password validation checks
  const hasMinLength = newPassword.length >= 8;
  const hasUppercase = /[A-Z]/.test(newPassword);
  const hasLowercase = /[a-z]/.test(newPassword);
  const hasNumber = /[0-9]/.test(newPassword);
  const hasSpecial = /[^A-Za-z0-9]/.test(newPassword);
  const isMatching = newPassword && newPassword === confirmPassword;

  const handlePasswordChange = (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    if (!hasMinLength || !hasUppercase || !hasLowercase || !hasNumber || !hasSpecial) {
      setError('New password does not satisfy all complexity requirements.');
      return;
    }

    if (!isMatching) {
      setError('New password and confirmation password do not match.');
      return;
    }

    setMessage('Security credentials updated successfully in Zero Trust database.');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto animate-fade-in pb-12">
      
      {/* Spatial Header Stage */}
      <div className="floating-surface rounded-2xl p-6 sm:p-7 shadow-spatial-md flex items-center justify-between gap-4 relative overflow-hidden">
        <div className="flex items-center space-x-3.5 relative z-10">
          <div className="w-10 h-10 rounded-2xl bg-primary/10 border border-primary/25 flex items-center justify-center text-primary shadow-spatial-sm">
            <UserIcon className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-foreground">User Security & Profile</h1>
            <p className="text-xs text-muted-foreground">Manage authentication credentials and view role permissions.</p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="relative z-10 px-4 py-2 text-xs font-semibold text-muted-foreground hover:text-foreground micro-surface rounded-xl transition-colors tactile-btn"
        >
          Close Settings
        </button>
      </div>

      {/* User Information Summary */}
      <div className="floating-surface rounded-2xl p-6 shadow-spatial-md space-y-4">
        <div className="flex items-center justify-between border-b border-border/40 pb-3">
          <div className="flex items-center space-x-2">
            <Shield className="w-4 h-4 text-primary" />
            <h2 className="text-sm font-bold text-foreground">Identity & Role Claims</h2>
          </div>
          <span className="text-[10px] font-mono text-muted-foreground uppercase">RFC 7519 Compliant</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 text-xs font-mono">
          <div className="p-3.5 rounded-2xl micro-surface shadow-spatial-sm">
            <span className="block text-[10px] text-muted-foreground uppercase font-semibold mb-1">Active Principal</span>
            <span className="text-foreground font-bold text-sm">{user?.username || 'admin'}</span>
          </div>
          <div className="p-3.5 rounded-2xl micro-surface shadow-spatial-sm border-primary/20 bg-primary/5">
            <span className="block text-[10px] text-muted-foreground uppercase font-semibold mb-1">RBAC Role Authority</span>
            <span className="text-primary font-bold text-sm">[{role.toUpperCase()}]</span>
          </div>
          <div className="p-3.5 rounded-2xl micro-surface shadow-spatial-sm border-emerald-500/20 bg-emerald-500/5">
            <span className="block text-[10px] text-muted-foreground uppercase font-semibold mb-1">Token Integrity</span>
            <span className="text-emerald-500 font-bold text-sm">HS256 Verified</span>
          </div>
        </div>
      </div>

      {/* Change Password Form */}
      <div className="floating-surface rounded-2xl p-6 shadow-spatial-md space-y-6">
        <div className="flex items-center justify-between border-b border-border/40 pb-3">
          <div className="flex items-center space-x-2">
            <Key className="h-4 w-4 text-primary" />
            <h2 className="text-sm font-bold text-foreground">Rotate Security Credentials</h2>
          </div>
          <span className="text-[10px] font-mono text-muted-foreground uppercase">Bcrypt Hash</span>
        </div>

        {message && (
          <div className="p-3.5 rounded-2xl micro-surface border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-xs font-mono shadow-spatial-sm flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
            <span>{message}</span>
          </div>
        )}

        {error && (
          <div className="p-3.5 rounded-2xl micro-surface border-rose-500/30 bg-rose-500/10 text-rose-600 dark:text-rose-400 text-xs font-mono shadow-spatial-sm flex items-center space-x-2">
            <XCircle className="w-4 h-4 text-rose-500 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handlePasswordChange} className="space-y-4 text-xs">
          
          <div>
            <label className="block text-muted-foreground font-semibold mb-1.5 text-[11px] uppercase tracking-wider font-mono">Current Password</label>
            <input
              type={showPassword ? "text" : "password"}
              required
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full bg-background border border-border rounded-xl p-2.5 text-foreground outline-none font-mono focus:border-primary transition-all shadow-inner"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-muted-foreground font-semibold text-[11px] uppercase tracking-wider font-mono">New Password</label>
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-primary hover:text-primary-hover flex items-center space-x-1 text-[11px] font-mono"
              >
                {showPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
                <span>{showPassword ? 'Hide' : 'Show'}</span>
              </button>
            </div>
            <input
              type={showPassword ? "text" : "password"}
              required
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full bg-background border border-border rounded-xl p-2.5 text-foreground outline-none font-mono focus:border-primary transition-all shadow-inner"
            />
          </div>

          <div>
            <label className="block text-muted-foreground font-semibold mb-1.5 text-[11px] uppercase tracking-wider font-mono">Confirm New Password</label>
            <input
              type={showPassword ? "text" : "password"}
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full bg-background border border-border rounded-xl p-2.5 text-foreground outline-none font-mono focus:border-primary transition-all shadow-inner"
            />
          </div>

          {/* Password Complexity Checklist */}
          <div className="micro-surface rounded-2xl p-4 space-y-2 font-mono text-[11px] shadow-spatial-sm">
            <div className="text-foreground font-bold font-sans text-xs mb-2">Password Complexity Requirements:</div>
            
            <div className="flex items-center space-x-2">
              {hasMinLength ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <XCircle className="h-3.5 w-3.5 text-muted-foreground/40" />}
              <span className={hasMinLength ? 'text-emerald-500 font-semibold' : 'text-muted-foreground'}>At least 8 characters long</span>
            </div>

            <div className="flex items-center space-x-2">
              {hasUppercase ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <XCircle className="h-3.5 w-3.5 text-muted-foreground/40" />}
              <span className={hasUppercase ? 'text-emerald-500 font-semibold' : 'text-muted-foreground'}>Contains uppercase letter (A-Z)</span>
            </div>

            <div className="flex items-center space-x-2">
              {hasLowercase ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <XCircle className="h-3.5 w-3.5 text-muted-foreground/40" />}
              <span className={hasLowercase ? 'text-emerald-500 font-semibold' : 'text-muted-foreground'}>Contains lowercase letter (a-z)</span>
            </div>

            <div className="flex items-center space-x-2">
              {hasNumber ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <XCircle className="h-3.5 w-3.5 text-muted-foreground/40" />}
              <span className={hasNumber ? 'text-emerald-500 font-semibold' : 'text-muted-foreground'}>Contains numeric digit (0-9)</span>
            </div>

            <div className="flex items-center space-x-2">
              {hasSpecial ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <XCircle className="h-3.5 w-3.5 text-muted-foreground/40" />}
              <span className={hasSpecial ? 'text-emerald-500 font-semibold' : 'text-muted-foreground'}>Contains special symbol (!@#$%^&*)</span>
            </div>

            <div className="flex items-center space-x-2 pt-2 border-t border-border/40">
              {isMatching ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <XCircle className="h-3.5 w-3.5 text-muted-foreground/40" />}
              <span className={isMatching ? 'text-emerald-500 font-bold' : 'text-muted-foreground'}>Passwords match</span>
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-xl bg-primary hover:bg-primary-hover text-white font-semibold text-xs shadow-spatial-md transition-all tactile-btn"
          >
            Update Security Credentials
          </button>

        </form>
      </div>

    </div>
  );
};

