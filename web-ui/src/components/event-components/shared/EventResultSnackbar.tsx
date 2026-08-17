import { Alert, Snackbar } from '@mui/material';
import { SnackbarState } from '../snackbar-state';

interface EventResultSnackbarProps {
  open: boolean;
  state: SnackbarState;
  onClose: () => void;
}

/** Shared snackbar rendering (new-record / error toasts) for `*EventFrame` components. */
export const EventResultSnackbar: React.FC<EventResultSnackbarProps> = ({ open, state, onClose }) => (
  <Snackbar open={open} autoHideDuration={6000} onClose={onClose} anchorOrigin={state.anchorOrigin}>
    <Alert onClose={onClose} severity={state.severity} variant="filled">
      {state.message}
    </Alert>
  </Snackbar>
);
