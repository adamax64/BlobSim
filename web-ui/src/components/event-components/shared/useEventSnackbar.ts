import { useCallback, useState } from 'react';
import { SnackbarState } from '../snackbar-state';

const BOTTOM_CENTER = { vertical: 'bottom', horizontal: 'center' } as const;
const TOP_CENTER = { vertical: 'top', horizontal: 'center' } as const;

/** Shared snackbar state + show/close helpers reused by all live `*EventFrame` components. */
export const useEventSnackbar = () => {
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarState, setSnackbarState] = useState<SnackbarState>({
    message: null,
    severity: 'error',
    anchorOrigin: BOTTOM_CENTER,
  });

  const showError = useCallback((message: string) => {
    setSnackbarState({ message, severity: 'error', anchorOrigin: BOTTOM_CENTER });
    setSnackbarOpen(true);
  }, []);

  const showSuccess = useCallback((message: string) => {
    setSnackbarState({ message, severity: 'success', anchorOrigin: TOP_CENTER });
    setSnackbarOpen(true);
  }, []);

  const closeSnackbar = useCallback(() => setSnackbarOpen(false), []);

  return { snackbarOpen, snackbarState, showError, showSuccess, closeSnackbar };
};
