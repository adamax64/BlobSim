import { Box, BoxProps } from '@mui/material';
import { ReactNode, useEffect } from 'react';
import { LoadingOverlay } from './LoadingOverlay';
import { useCurrentPage } from '../../context/CurrentPageContext';
import { AppPage } from '../root-components/constants';

type PageFrameProps = {
  children: ReactNode;
  showLoading?: boolean;
  pageName?: AppPage;
  customPageTitle?: string;
  customFrameStyle?: BoxProps;
};

export const PageFrame = ({ children, showLoading, pageName, customPageTitle, customFrameStyle }: PageFrameProps) => {
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
    <Box display="flex" flexGrow={1} height="100%" flexDirection="column" gap={2} p={1} {...customFrameStyle}>
      {children}
      {showLoading && <LoadingOverlay />}
    </Box>
  );
};
