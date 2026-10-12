import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { ErrorBoundary } from './components/ErrorBoundary';
import { LandingPage } from './pages/LandingPage';
import { TrojanLandingPage } from './pages/TrojanLandingPage';
import { LoginPage } from './pages/LoginPage';
import { ForgotPasswordPage } from './pages/ForgotPasswordPage';
import { DashboardApp } from './pages/DashboardApp';

const getInitialView = () => {
  if (typeof window !== 'undefined') {
    const path = window.location.pathname.toLowerCase();
    const hash = window.location.hash.toLowerCase();
    if (path === '/trojan' || hash === '#trojan') return 'trojan-landing';
    if (path === '/login' || hash === '#login') return 'login';
    if (path === '/academic' || hash === '#academic') return 'landing';
  }
  return 'landing';
};

const AppRouter = () => {
  const { isAuthenticated, resetModelStatus } = useAuth();
  const [currentView, setCurrentView] = useState(getInitialView);

  // Listen to hash changes so #trojan, #academic, #login work even without restarting Flask
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.toLowerCase();
      if (hash === '#trojan') setCurrentView('trojan-landing');
      else if (hash === '#login') setCurrentView('login');
      else if (hash === '#academic') setCurrentView('landing');
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  // If user signs in, switch to dashboard and reset model status to Untrained
  const handleSuccessLogin = () => {
    resetModelStatus();
    if (typeof window !== 'undefined') {
      window.history.replaceState({}, '', '/');
    }
    setCurrentView('dashboard');
  };

  const handleOpenLogin = () => {
    resetModelStatus();
    if (typeof window !== 'undefined') {
      window.history.replaceState({}, '', '/#login');
    }
    setCurrentView('login');
  };

  const handleBackToLanding = () => {
    resetModelStatus();
    if (typeof window !== 'undefined') {
      window.history.replaceState({}, '', '/');
    }
    setCurrentView('landing');
  };

  const handleSwitchToTrojan = () => {
    resetModelStatus();
    if (typeof window !== 'undefined') {
      window.history.replaceState({}, '', '/#trojan');
    }
    setCurrentView('trojan-landing');
  };

  if (currentView === 'login') {
    return (
      <LoginPage 
        onBackToLanding={handleBackToLanding}
        onForgotPassword={() => setCurrentView('forgot-password')}
        onSuccessLogin={handleSuccessLogin}
      />
    );
  }

  if (currentView === 'forgot-password') {
    return (
      <ForgotPasswordPage 
        onBackToLogin={() => setCurrentView('login')}
      />
    );
  }

  if (currentView === 'trojan-landing') {
    return (
      <TrojanLandingPage
        onSuccessLogin={handleSuccessLogin}
        onSwitchLanding={handleBackToLanding}
      />
    );
  }

  if (currentView === 'dashboard' || (isAuthenticated && currentView !== 'landing' && currentView !== 'trojan-landing')) {
    return (
      <DashboardApp 
        onBackToLanding={handleBackToLanding}
      />
    );
  }

  // Default: Academic Landing Page (with 1-click toggle to 3D Trojan Landing Page)
  return (
    <LandingPage 
      onExplore={handleOpenLogin}
      onOpenLogin={handleOpenLogin}
      onSwitchToTrojan={handleSwitchToTrojan}
    />
  );
};

export default function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <AppRouter />
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
