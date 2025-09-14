import { Box } from '@mui/material';
import { ReactNode, useEffect } from 'react';
import { LoadingOverlay } from './LoadingOverlay';
import { useCurrentPage } from '../../context/CurrentPageContext';
import { AppPage } from '../root-components/constants';

type PageFrameProps = {
  children: ReactNode;
  showLoading?: boolean;
  pageName?: AppPage;
  customPageTitle?: string;
};

export const PageFrame = ({ children, showLoading, pageName, customPageTitle }: PageFrameProps) => {
  const { setCurrentPage, setPageTitle } = useCurrentPage();

  useEffect(() => {
    if (pageName) {
      setPageTitle(undefined);
      setCurrentPage(pageName);
    }
    if (customPageTitle) {
      setPageTitle(customPageTitle);
    }
  }, [pageName, customPageTitle]);

  return (
    <Box display="flex" flexGrow={1} height="100%" flexDirection="column" gap={2} className="p-2">
      {children}
      {showLoading && <LoadingOverlay />}
    </Box>
  );
};
