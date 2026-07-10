import { Drawer } from '@mui/material';
import { DRAWER_WIDTH } from './constants';
import { AppSidebar } from './AppSidebar';

type MobileMenuProps = {
  isTablet: boolean;
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
};

export const MobileMenu = ({ isTablet, mobileOpen, setMobileOpen }: MobileMenuProps) => {
  if (!isTablet) {
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
        <AppSidebar isTablet={isTablet} setMobileOpen={setMobileOpen} />
      </Drawer>
    </nav>
  );
};
