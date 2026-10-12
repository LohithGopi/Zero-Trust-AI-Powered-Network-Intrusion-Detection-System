/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#1E60D5',
          navy: '#0B1C33',
          bg: '#F8FAFC',
          card: '#FFFFFF',
          dark: '#090B0E',
          surfaceDark: '#13171F',
          surfaceLight: '#FFFFFF',
          slate: '#475569',
          border: '#E2E8F0',
          borderDark: 'rgba(255, 255, 255, 0.08)',
          success: '#10B981',
          warning: '#F59E0B',
          danger: '#EF4444',
          accent: '#3B82F6'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      boxShadow: {
        'spatial-sm': '0 2px 8px -2px rgba(15, 23, 42, 0.05), 0 1px 3px -1px rgba(15, 23, 42, 0.03)',
        'spatial-md': '0 12px 24px -6px rgba(15, 23, 42, 0.08), 0 4px 8px -2px rgba(15, 23, 42, 0.04)',
        'spatial-lg': '0 24px 48px -12px rgba(15, 23, 42, 0.12), 0 8px 16px -4px rgba(15, 23, 42, 0.06)',
        'spatial-float': '0 30px 60px -15px rgba(11, 28, 51, 0.18), 0 0 0 1px rgba(255, 255, 255, 0.08)',
        'spatial-glow': '0 0 40px -10px rgba(30, 96, 213, 0.25)',
        'spatial-threat': '0 0 30px -8px rgba(239, 68, 68, 0.3)'
      },
      animation: {
        'float-slow': 'float 6s ease-in-out infinite',
        'pulse-subtle': 'pulseSubtle 3s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        }
      }
    },
  },
  plugins: [],
}
