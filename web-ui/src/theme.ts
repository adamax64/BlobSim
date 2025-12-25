import { createTheme, PaletteOptions, Theme } from '@mui/material/styles';

type Mode = 'light' | 'dark';

// Factory to create a theme for the given mode
export function createAppTheme(mode: Mode) {
  const lightPalette: PaletteOptions = {
    mode: 'light',
    background: { default: '#f9f9f9' },
    gold: { main: '#ffe993', contrastText: '#8c7300' },
    silver: { main: '#d9d9d9', contrastText: '#7a7a7a' },
    inactive: { main: '#e0e0e0', contrastText: '#7a7a7a' },
    bronze: { main: '#eccfa0', contrastText: '#8c5a1e' },
    overtake: { main: '#d4f8e8', contrastText: '#007700' },
    fellBehind: { main: '#ffe6b3', contrastText: '#a65c00' },
    active: { main: '#e9f3ff', contrastText: '#1976d2' },
  };

  const darkPalette: PaletteOptions = {
    mode: 'dark',
    background: { default: '#121212' },
    gold: { main: '#5f4700', contrastText: '#ffffff' },
    silver: { main: '#3a3a3a', contrastText: '#ffffff' },
    inactive: { main: '#2a2a2a', contrastText: '#bdbdbd' },
    bronze: { main: '#5a3e22', contrastText: '#ffffff' },
    overtake: { main: '#1a3d2e', contrastText: '#4ade80' },
    fellBehind: { main: '#4a3a1f', contrastText: '#fbbf24' },
    active: { main: '#1e3a5f', contrastText: '#90caf9' },
  };

  const palette: PaletteOptions = mode === 'dark' ? darkPalette : lightPalette;

  return createTheme({
    palette,
    typography: {
      h6: { fontSize: '1.15rem' },
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: ({ palette: themePalette }: Theme) => ({
          ':root': {
            '--row-gold-bg': themePalette.gold?.main,
            '--row-gold-text': themePalette.gold?.contrastText,
            '--row-silver-bg': themePalette.silver?.main,
            '--row-silver-text': themePalette.silver?.contrastText,
            '--row-bronze-bg': themePalette.bronze?.main,
            '--row-bronze-text': themePalette.bronze?.contrastText,
            '--row-inactive-bg': themePalette.inactive?.main,
            '--row-inactive-text': themePalette.inactive?.contrastText,
            '--cell-overtake-bg': themePalette.overtake?.main,
            '--cell-overtake-text': themePalette.overtake?.contrastText,
            '--cell-fell-behind-bg': themePalette.fellBehind?.main,
            '--cell-fell-behind-text': themePalette.fellBehind?.contrastText,
            '--column-active-bg': themePalette.active?.main,
          },
        }),
      },
    },
  });
}

export type { Mode };
