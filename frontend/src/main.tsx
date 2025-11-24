import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Initialize theme before React renders
function initializeTheme() {
  const stored = localStorage.getItem('theme') as 'light' | 'dark' | 'system' | null;
  const root = document.documentElement;
  
  if (stored === 'dark') {
    root.classList.add('dark');
  } else if (stored === 'light') {
    root.classList.remove('dark');
  } else {
    // system or no preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }
}

initializeTheme();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

