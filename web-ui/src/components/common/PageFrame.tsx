import { Box } from '@mui/material';
import { ReactNode } from 'react';
import { LoadingOverlay } from './LoadingOverlay';
import { useCurrentPage } from '../../context/CurrentPageContext';

type PageFrameProps = {
  children: ReactNode;
  showLoading?: boolean;
  pageTitle?: string;
};

export const PageFrame = ({ children, showLoading, pageTitle }: PageFrameProps) => {
  const { setPageTitle } = useCurrentPage();
  if (pageTitle) {
    setPageTitle(pageTitle);
  }

  return (
    <Box display="flex" flexGrow={1} height="100%" flexDirection="column" gap={2} className="p-2">
      {children}
      {showLoading && <LoadingOverlay />}
    </Box>
  );
};
