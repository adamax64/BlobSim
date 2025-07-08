import { Box } from '@mui/material';
import { ReactNode } from 'react';
import { LoadingOverlay } from './LoadingOverlay';

export function PageFrame({ children, showLoading }: { children: ReactNode; showLoading?: boolean }) {
  return (
    <Box display="flex" flexGrow={1} flexDirection="column" gap={2} className="p-2">
      {children}
      {showLoading && <LoadingOverlay />}
    </Box>
  );
}
