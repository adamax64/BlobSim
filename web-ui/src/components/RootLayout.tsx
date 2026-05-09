import { Box } from '@mui/material';
import { Outlet } from '@tanstack/react-router';
import { useState } from 'react';
import { DesktopMenu } from './root-components/DesktopMenu';
import { MobileMenu } from './root-components/MobileMenu';
import { AppHeader } from './root-components/AppHeader';
import { useIsMobile } from '../hooks/useIsMobile';

export const RootLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const isMobile = useIsMobile();

  return (
    <Box display="flex" height="100dvh" flexDirection="column">
      <AppHeader isMobile={isMobile} mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      <MobileMenu isMobile={isMobile} mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      <Box component="main" flexGrow={1} display="flex" sx={{ minHeight: 0 }}>
        <DesktopMenu isMobile={isMobile} />
        <Box overflow="auto" flexGrow={1}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};
