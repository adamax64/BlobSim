import '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Palette {
    gold: Palette['primary'];
    silver: Palette['primary'];
    bronze: Palette['primary'];
  }
  interface PaletteOptions {
    gold?: PaletteOptions['primary'];
    silver?: PaletteOptions['primary'];
    bronze?: PaletteOptions['primary'];
  }
}
