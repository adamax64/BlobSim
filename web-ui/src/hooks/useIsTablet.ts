import { useTheme } from '@mui/material';
import useMediaQuery from '@mui/material/useMediaQuery';

export const useIsTablet = () => {
  const theme = useTheme();
  return useMediaQuery(`${theme.breakpoints.down('md')} or (max-height:600px)`);
};
