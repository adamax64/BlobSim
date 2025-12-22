import { createTheme, PaletteOptions, Theme } from '@mui/material/styles';

type Mode = 'light' | 'dark';

// Factory to create a theme for the given mode
export function createAppTheme(mode: Mode) {
  const lightPalette: PaletteOptions = {
    mode: 'light',
    background: { default: '#f9f9f9' },
    gold: { main: '#ffe993', contrastText: '#8c7300' },
    silver: { main: '#d9d9d9', contrastText: '#7a7a7a' },
    bronze: { main: '#eccfa0', contrastText: '#8c5a1e' },
  };

  const darkPalette: PaletteOptions = {
    mode: 'dark',
    background: { default: '#121212' },
    gold: { main: '#5f4700', contrastText: '#ffffff' },
    silver: { main: '#3a3a3a', contrastText: '#ffffff' },
    bronze: { main: '#5a3e22', contrastText: '#ffffff' },
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
          },
        }),
      },
    },
  });
}

export type { Mode };
