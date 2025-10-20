export type SnackbarState = {
  message: string | null;
  severity: 'error' | 'success' | 'info' | 'warning';
  anchorOrigin: { vertical: 'top' | 'bottom'; horizontal: 'left' | 'center' | 'right' };
};
