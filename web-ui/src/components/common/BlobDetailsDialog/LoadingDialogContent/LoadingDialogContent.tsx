import { Box, CircularProgress } from '@mui/material';

const LoadingDialogContent = () => {
  return (
    <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" padding={4}>
      <CircularProgress />
    </Box>
  );
};

export default LoadingDialogContent;
