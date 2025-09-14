import { Drawer } from '@mui/material';
import { DRAWER_WIDTH } from './constants';
import { AppSidebar } from './AppSidebar';

type MobileMenuProps = {
  isMobile: boolean;
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
};

export const MobileMenu = ({ isMobile, mobileOpen, setMobileOpen }: MobileMenuProps) => {
  if (!isMobile) {
    return null;
  }

  return (
    <nav>
      <Drawer
        variant="temporary"
        sx={{
          display: { xs: 'flex' },
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            justifyContent: 'space-between',
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
          },
        }}
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
      >
        <AppSidebar isMobile={isMobile} setMobileOpen={setMobileOpen} />
      </Drawer>
    </nav>
  );
};
