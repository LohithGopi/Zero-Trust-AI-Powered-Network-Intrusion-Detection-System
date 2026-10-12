import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext(null);

export const ThemeProvider = ({ children }) => {
  const [themeMode, setThemeMode] = useState(() => {
    return localStorage.getItem('nids_theme_mode') || 'light';
  });

  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const applyTheme = () => {
      let darkActive = false;
      if (themeMode === 'dark') {
        darkActive = true;
      } else if (themeMode === 'light') {
        darkActive = false;
      } else {
        darkActive = mediaQuery.matches;
      }

      setIsDark(darkActive);

      if (darkActive) {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
      } else {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
      }
    };

    applyTheme();
    localStorage.setItem('nids_theme_mode', themeMode);

    const listener = (e) => {
      if (themeMode === 'system') {
        applyTheme();
      }
    };

    mediaQuery.addEventListener('change', listener);
    return () => mediaQuery.removeEventListener('change', listener);
  }, [themeMode]);

  const toggleTheme = () => {
    if (themeMode === 'system') setThemeMode('dark');
    else if (themeMode === 'dark') setThemeMode('light');
    else setThemeMode('system');
  };

  return (
    <ThemeContext.Provider value={{ themeMode, setThemeMode, toggleTheme, isDark }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};
