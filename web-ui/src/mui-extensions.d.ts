import '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Palette {
    gold: Palette['primary'];
    silver: Palette['primary'];
    bronze: Palette['primary'];
    inactive: Palette['primary'];
    overtake: Palette['primary'];
    fellBehind: Palette['primary'];
    active: Palette['primary'];
  }
  interface PaletteOptions {
    gold?: PaletteOptions['primary'];
    silver?: PaletteOptions['primary'];
    bronze?: PaletteOptions['primary'];
    inactive?: PaletteOptions['primary'];
    overtake?: PaletteOptions['primary'];
    fellBehind?: PaletteOptions['primary'];
    active?: PaletteOptions['primary'];
  }
}
