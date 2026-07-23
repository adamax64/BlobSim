import { createTheme, PaletteOptions, Theme, responsiveFontSizes } from '@mui/material/styles';
import { SeasonTemperature } from '../generated';

type Mode = 'light' | 'dark';

// background/text color shifts per season temperature, kept close in tone/luminance to the
// default palette so the fallback (no season temperature yet) does not stand out as drastically
// different: cold leans blue, neutral leans green/yellow, warm leans red/orange.
const SEASON_COLORS: Record<
  Mode,
  Record<SeasonTemperature, { backgroundDefault: string; backgroundPaper: string; textPrimary: string; textSecondary: string }>
> = {
  light: {
    [SeasonTemperature.Cold]: {
      backgroundDefault: '#f4f8fc',
      backgroundPaper: '#fafdff',
      textPrimary: 'rgba(12, 25, 42, 0.87)',
      textSecondary: 'rgba(18, 30, 46, 0.6)',
    },
    [SeasonTemperature.Neutral]: {
      backgroundDefault: '#f7faf2',
      backgroundPaper: '#fefffb',
      textPrimary: 'rgba(19, 27, 11, 0.87)',
      textSecondary: 'rgba(35, 50, 20, 0.6)',
    },
    [SeasonTemperature.Warm]: {
      backgroundDefault: '#fef7f4',
      backgroundPaper: '#fffdfc',
      textPrimary: 'rgba(27, 12, 6, 0.87)',
      textSecondary: 'rgba(30, 17, 11, 0.6)',
    },
  },
  dark: {
    [SeasonTemperature.Cold]: {
      backgroundDefault: '#0b1018',
      backgroundPaper: '#10131c',
      textPrimary: '#eaf2fb',
      textSecondary: 'rgba(234, 242, 251, 0.7)',
    },
    [SeasonTemperature.Neutral]: {
      backgroundDefault: '#10160c',
      backgroundPaper: '#12190e',
      textPrimary: '#eef5e4',
      textSecondary: 'rgba(238, 245, 228, 0.7)',
    },
    [SeasonTemperature.Warm]: {
      backgroundDefault: '#160f0a',
      backgroundPaper: '#221c17',
      textPrimary: '#fbeee6',
      textSecondary: 'rgba(251, 238, 230, 0.7)',
    },
  },
};

// Factory to create a theme for the given mode and (optional) season temperature.
// When no season temperature is provided (e.g. not loaded yet) the current default
// color palette is used as a fallback.
export function createAppTheme(mode: Mode, seasonTemperature?: SeasonTemperature) {
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
    retired: { main: '#f0f0f0', contrastText: '#7a7a7a' },
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
    retired: { main: '#3a3a3a', contrastText: '#ffffff' },
  };

  const palette: PaletteOptions = mode === 'dark' ? darkPalette : lightPalette;

  if (seasonTemperature) {
    const seasonColors = SEASON_COLORS[mode][seasonTemperature];
    palette.background = { ...palette.background, default: seasonColors.backgroundDefault, paper: seasonColors.backgroundPaper };
    palette.text = { primary: seasonColors.textPrimary, secondary: seasonColors.textSecondary };
  }

  return responsiveFontSizes(
    createTheme({
      palette,
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
              '--row-retired-bg': themePalette.retired?.main,
              '--column-active-text': themePalette.active?.contrastText,
            },
          }),
        },
      },
    }),
  );
}

export type { Mode };
