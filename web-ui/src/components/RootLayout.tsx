import { Box } from '@mui/material';
import { Outlet } from '@tanstack/react-router';
import { useState } from 'react';
import { DesktopMenu } from './root-components/DesktopMenu';
import { MobileMenu } from './root-components/MobileMenu';
import { AppHeader } from './root-components/AppHeader';
import { useIsTablet } from '../hooks/useIsTablet';

export const RootLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const isTablet = useIsTablet();

  return (
    <Box display="flex" height="100dvh" flexDirection="column">
      <AppHeader isTablet={isTablet} mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      <MobileMenu isTablet={isTablet} mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      <Box component="main" flexGrow={1} display="flex" sx={{ minHeight: 0 }}>
        <DesktopMenu isTablet={isTablet} />
        <Box overflow="auto" flexGrow={1}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};
