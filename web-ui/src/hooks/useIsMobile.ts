import { useTheme } from '@mui/material';
import useMediaQuery from '@mui/material/useMediaQuery';

export const useIsMobile = () => {
  const theme = useTheme();
  return useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);
};
