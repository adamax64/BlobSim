import { Box, useTheme, useMediaQuery } from '@mui/material';
import { Outlet } from '@tanstack/react-router';
import { useState } from 'react';
import { DesktopMenu } from './root-components/DesktopMenu';
import { MobileMenu } from './root-components/MobileMenu';
import { AppHeader } from './root-components/AppHeader';

export const RootLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  return (
    <Box display="flex" height="100vh" flexDirection="column">
      <AppHeader isMobile={isMobile} mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      <MobileMenu isMobile={isMobile} mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      <Box component="main" flexGrow={1} display="flex">
        <DesktopMenu isMobile={isMobile} />
        <Box overflow="auto" flexGrow={1}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};
