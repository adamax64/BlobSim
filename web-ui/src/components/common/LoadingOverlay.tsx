import { Box, CircularProgress } from '@mui/material';

export const LoadingOverlay = () => {
  return (
    <Box
      position="fixed"
      top={0}
      left={0}
      right={0}
      bottom={0}
      display="flex"
      justifyContent="center"
      alignItems="center"
      bgcolor="rgba(255, 255, 255, 0.8)"
      zIndex={1000}
    >
      <CircularProgress />
    </Box>
  );
};
