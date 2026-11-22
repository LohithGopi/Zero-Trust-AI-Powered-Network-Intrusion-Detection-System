import React, { useState } from 'react';
import { Lock, ArrowLeft, Key, Shield, Info, CheckCircle2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LoginPage = ({ onBackToLanding, onSuccessLogin }) => {
  const { login } = useAuth();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [selectedRole, setSelectedRole] = useState('Admin');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showResetNotice, setShowResetNotice] = useState(false);

  const handleRoleSelect = (roleName) => {
    setSelectedRole(roleName);
    if (roleName === 'Admin') {
      setUsername('admin');
      setPassword('admin123');
    } else {
      setUsername('analyst');
      setPassword('analyst123');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password, selectedRole);
      onSuccessLogin();
    } catch (err) {
      setError(err?.message || 'Invalid username or password credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f4f7fc] text-slate-900 flex flex-col justify-between selection:bg-blue-500/20 selection:text-blue-600 p-4 sm:p-6 lg:p-8">
      
      {/* Top Header */}
      <div className="max-w-7xl mx-auto w-full flex items-center justify-between pt-1">
        <button
          onClick={onBackToLanding}
          className="flex items-center space-x-2 text-xs sm:text-sm font-semibold text-slate-700 hover:text-blue-600 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Home Page</span>
        </button>

        <div className="flex items-center space-x-2">
          <Shield className="h-4 w-4 text-blue-600 stroke-[2.2]" />
          <span className="font-bold text-xs sm:text-sm text-slate-900">
            Zero Trust AI-Powered NIDS
          </span>
        </div>
      </div>

      {/* Main Login Card */}
      <div className="max-w-[440px] w-full mx-auto my-8">
        <div className="bg-white rounded-3xl p-7 sm:p-9 shadow-xl shadow-blue-500/5 border border-slate-200/90 space-y-6">
          
          {/* Header icon and text */}
          <div className="text-center space-y-2">
            <div className="h-12 w-12 rounded-2xl bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center mx-auto shadow-xs">
              <Lock className="h-6 w-6" />
            </div>
            <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-3 py-0.5 rounded-full border border-blue-200 inline-block">
              SECURITY PORTAL
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900">
              Sign In to Account
            </h2>
            <p className="text-xs text-slate-500">
              Select role and enter your credentials to authenticate.
            </p>
          </div>

          {/* Role Toggle Selector */}
          <div className="grid grid-cols-2 gap-1.5 bg-slate-100 p-1.5 rounded-xl border border-slate-200/80 text-xs font-semibold">
            {['Admin', 'Analyst'].map((role) => (
              <button
                key={role}
                type="button"
                onClick={() => handleRoleSelect(role)}
                className={`py-2 rounded-lg transition-all text-center ${
                  selectedRole === role
                    ? 'bg-white text-blue-600 font-bold shadow-xs'
                    : 'text-slate-500 hover:text-slate-900'
                }`}
              >
                {role}
              </button>
            ))}
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Username / Email
              </label>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50/70 text-xs text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium"
                placeholder="Enter username"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-semibold text-slate-700">
                  Password
                </label>
                <button
                  type="button"
                  onClick={() => setShowResetNotice(!showResetNotice)}
                  className="text-xs text-blue-600 hover:underline font-medium"
                >
                  Forgot Password?
                </button>
              </div>

              {showResetNotice && (
                <div className="mb-3 p-3 rounded-xl bg-blue-50 border border-blue-200 text-xs text-slate-700 space-y-1 animate-fade-in text-left">
                  <div className="flex items-center space-x-1.5 font-bold text-blue-800">
                    <Info className="h-4 w-4 shrink-0 text-blue-600" />
                    <span>Zero Trust Policy (NIST SP 800-207)</span>
                  </div>
                  <p className="text-[11px] text-slate-600 leading-relaxed">
                    Public self-service credential resets are disabled to prevent account takeover. Please use the pre-configured Evaluator credentials below to test the platform.
                  </p>
                </div>
              )}

              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50/70 text-xs text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-xs text-red-600">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center justify-center space-x-2 shadow-xs transition-all active:scale-95 disabled:opacity-50"
            >
              <Key className="h-4 w-4" />
              <span>{loading ? 'Authenticating...' : 'Authenticate & Access Portal'}</span>
            </button>
          </form>

          {/* Quick Evaluator / Demo Credentials Card */}
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/90 space-y-2 text-left">
            <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono">
              <span className="font-semibold text-slate-700 flex items-center space-x-1.5">
                <Key className="h-3.5 w-3.5 text-blue-600" />
                <span>EVALUATOR & DEMO ACCESS</span>
              </span>
              <span className="text-[10px] text-emerald-600 font-bold bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                READY TO TEST
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => handleRoleSelect('Admin')}
                className={`p-2.5 rounded-xl border text-left transition-all ${
                  selectedRole === 'Admin'
                    ? 'bg-white border-blue-500 shadow-xs ring-1 ring-blue-500/20'
                    : 'bg-white/60 border-slate-200 hover:bg-white'
                }`}
              >
                <div className="font-bold text-slate-900 text-xs flex items-center justify-between">
                  <span>Admin Role</span>
                  <span className="text-[9px] font-mono font-bold text-purple-700 bg-purple-50 px-1 rounded">FULL</span>
                </div>
                <div className="text-[11px] font-mono text-slate-500 mt-1">
                  admin / admin123
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleRoleSelect('Analyst')}
                className={`p-2.5 rounded-xl border text-left transition-all ${
                  selectedRole === 'Analyst'
                    ? 'bg-white border-blue-500 shadow-xs ring-1 ring-blue-500/20'
                    : 'bg-white/60 border-slate-200 hover:bg-white'
                }`}
              >
                <div className="font-bold text-slate-900 text-xs flex items-center justify-between">
                  <span>Analyst Role</span>
                  <span className="text-[9px] font-mono font-bold text-blue-700 bg-blue-50 px-1 rounded">READ</span>
                </div>
                <div className="text-[11px] font-mono text-slate-500 mt-1">
                  analyst / analyst123
                </div>
              </button>
            </div>
            <p className="text-[10px] text-slate-400 text-center">
              Click either role card above to auto-fill credentials.
            </p>
          </div>

          {/* Role Status Tag */}
          <div className="text-center pt-2 border-t border-slate-100">
            <span className="text-xs font-mono text-slate-500">
              Active Selection:{' '}
              <span className="font-bold text-blue-600">{selectedRole} Tier</span>
            </span>
          </div>

        </div>
      </div>

      {/* Footer */}
      <footer className="text-center font-mono text-[11px] text-slate-400 pb-2">
        © 2026 Zero Trust AI-Powered NIDS • Academic Phase 1 Implementation
      </footer>

    </div>
  );
};
