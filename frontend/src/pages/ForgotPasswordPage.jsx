import React, { useState } from 'react';
import { ArrowLeft, KeyRound, CheckCircle2, Shield, Eye, EyeOff } from 'lucide-react';

export const ForgotPasswordPage = ({ onBackToLogin }) => {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSendCode = (e) => {
    e.preventDefault();
    setStep(2);
  };

  const handleVerifyCode = (e) => {
    e.preventDefault();
    setStep(3);
  };

  const handleResetPassword = (e) => {
    e.preventDefault();
    setStep(4);
  };

  return (
    <div className="min-h-screen bg-[#f4f7fc] text-slate-900 flex flex-col justify-between selection:bg-blue-500/20 selection:text-blue-600 p-4 sm:p-6 lg:p-8">
      
      {/* Top Header */}
      <div className="max-w-7xl mx-auto w-full flex items-center justify-between pt-1">
        <button
          onClick={onBackToLogin}
          className="flex items-center space-x-2 text-xs sm:text-sm font-semibold text-slate-700 hover:text-blue-600 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Login</span>
        </button>

        <div className="flex items-center space-x-2">
          <Shield className="h-4 w-4 text-blue-600 stroke-[2.2]" />
          <span className="font-bold text-xs sm:text-sm text-slate-900">
            Zero Trust AI-Powered NIDS
          </span>
        </div>
      </div>

      {/* Main Form Card */}
      <div className="max-w-[440px] w-full mx-auto my-8">
        <div className="bg-white rounded-3xl p-7 sm:p-9 shadow-xl shadow-blue-500/5 border border-slate-200/90 space-y-6">
          
          <div className="text-center space-y-2">
            <div className="h-12 w-12 rounded-2xl bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center mx-auto shadow-xs">
              <KeyRound className="h-6 w-6" />
            </div>
            <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-3 py-0.5 rounded-full border border-blue-200 inline-block">
              SECURITY RECOVERY
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900">Credential Recovery</h2>
            <p className="text-xs text-slate-500">Zero Trust Security Identity Verification & Reset</p>
          </div>

          {step === 1 && (
            <form onSubmit={handleSendCode} className="space-y-4 text-xs font-sans text-left">
              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">Registered Academic Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="admin@jnnce.ac.in"
                  className="w-full bg-slate-50/70 border border-slate-200 focus:border-blue-500 focus:bg-white rounded-xl p-3 text-slate-900 outline-none transition-colors"
                />
              </div>
              <button
                type="submit"
                className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-xs transition-all active:scale-95"
              >
                Send Recovery Verification Code
              </button>
            </form>
          )}

          {step === 2 && (
            <form onSubmit={handleVerifyCode} className="space-y-4 text-xs font-sans text-left">
              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">Enter 6-Digit Auth Code</label>
                <input
                  type="text"
                  required
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="849201"
                  className="w-full bg-slate-50/70 border border-slate-200 focus:border-blue-500 focus:bg-white rounded-xl p-3 text-slate-900 outline-none transition-colors font-mono tracking-widest text-center text-sm font-bold"
                />
              </div>
              <button
                type="submit"
                className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-xs transition-all active:scale-95"
              >
                Verify Reset Token
              </button>
            </form>
          )}

          {step === 3 && (
            <form onSubmit={handleResetPassword} className="space-y-4 text-xs font-sans text-left">
              <div>
                <label className="block text-slate-700 font-semibold mb-1.5">New Security Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full bg-slate-50/70 border border-slate-200 focus:border-blue-500 focus:bg-white rounded-xl p-3 pr-10 text-slate-900 outline-none transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-blue-600"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
              <button
                type="submit"
                className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-xs transition-all active:scale-95"
              >
                Commit New Password
              </button>
            </form>
          )}

          {step === 4 && (
            <div className="text-center space-y-4 py-4">
              <CheckCircle2 className="h-12 w-12 text-emerald-600 mx-auto" />
              <h3 className="text-sm font-bold text-slate-900">Password Reset Successful</h3>
              <p className="text-xs text-slate-500">Your cryptographic password hash has been updated in SQLite vault.</p>
              <button
                onClick={onBackToLogin}
                className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs active:scale-95"
              >
                Return to Login
              </button>
            </div>
          )}

        </div>
      </div>

      <footer className="text-center text-[11px] text-slate-400 pb-2">
        © 2026 Zero Trust AI-Powered NIDS • Academic Phase 1 Implementation
      </footer>

    </div>
  );
};
