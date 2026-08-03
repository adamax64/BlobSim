import React, { createContext, use, useEffect, useMemo, useState } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { createAppTheme, Mode } from '../theme';
import { useWeather } from './WeatherContext';

type ThemeModeContextValue = {
  mode: Mode;
  toggleMode: () => void;
  setMode: (m: Mode) => void;
};

const ThemeModeContext = createContext<ThemeModeContextValue | undefined>(undefined);

const STORAGE_KEY = 'themeMode';

export const ThemeModeProvider: React.FC<React.PropsWithChildren<object>> = ({ children }) => {
  const [mode, setMode] = useState<Mode>(() => {
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
    const handler = (e: MediaQueryListEvent) => setMode(e.matches ? 'dark' : 'light');

    // Use the standard addEventListener/removeEventListener API only.
    // Do not fall back to legacy addListener/removeListener.
    if (typeof mq.addEventListener === 'function') {
      mq.addEventListener('change', handler as EventListener);
      return () => mq.removeEventListener('change', handler as EventListener);
    }

    // Browser does not support the standard API — do not attach a listener.
    return;
  }, []);

  const toggleMode = () => setMode((prev) => (prev === 'light' ? 'dark' : 'light'));

  const { seasonTemperature } = useWeather();
  const theme = useMemo(() => createAppTheme(mode, seasonTemperature), [mode, seasonTemperature]);

  return (
    <ThemeModeContext value={{ mode, toggleMode, setMode }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeModeContext>
  );
};

export function useThemeMode() {
  const context = use(ThemeModeContext as React.Context<ThemeModeContextValue>);
  return context;
}
