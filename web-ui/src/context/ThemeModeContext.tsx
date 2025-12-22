import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { createAppTheme, Mode } from '../theme';

type ThemeModeContextValue = {
  mode: Mode;
  toggleMode: () => void;
  setMode: (m: Mode) => void;
};

const ThemeModeContext = createContext<ThemeModeContextValue | undefined>(undefined);

const STORAGE_KEY = 'themeMode';

export const ThemeModeProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [mode, setModeState] = useState<Mode>(() => {
    if (typeof window === 'undefined') return 'light';
    const stored = localStorage.getItem(STORAGE_KEY) as Mode | null;
    if (stored) return stored;

    // Default to browser's preferred color scheme when no stored preference
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDark ? 'dark' : 'light';
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, mode);
  }, [mode]);

  // If the user hasn't set a preference, follow system changes
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return; // user set a preference, do not auto-follow

    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e: MediaQueryListEvent) => setModeState(e.matches ? 'dark' : 'light');

    // Use the standard addEventListener/removeEventListener API only.
    // Do not fall back to legacy addListener/removeListener.
    if (typeof mq.addEventListener === 'function') {
      mq.addEventListener('change', handler as EventListener);
      return () => mq.removeEventListener('change', handler as EventListener);
    }

    // Browser does not support the standard API — do not attach a listener.
    return;
  }, []);

  const setMode = (m: Mode) => setModeState(m);
  const toggleMode = () => setModeState((prev) => (prev === 'light' ? 'dark' : 'light'));

  const theme = useMemo(() => createAppTheme(mode), [mode]);

  return (
    <ThemeModeContext.Provider value={{ mode, toggleMode, setMode }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeModeContext.Provider>
  );
};

export function useThemeMode() {
  const ctx = useContext(ThemeModeContext);
  if (!ctx) throw new Error('useThemeMode must be used within ThemeModeProvider');
  return ctx;
}
