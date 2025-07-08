import { Box, Drawer, List, ListItem, Typography, useTheme, useMediaQuery, Fab } from '@mui/material';
import { Link, Outlet } from '@tanstack/react-router';
import { CalendarMonth, Dashboard, EmojiEvents, Factory, Menu } from '@mui/icons-material';
import { BlobPiktogram } from './icons/BlobPiktogram';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LanguageSwitcher } from './common/LanguageSwitcher';

const pages = ['dashboard', 'blobs', 'factory', 'standings', 'calendar'];

const drawerWidth = 240;

function getMenuIcon(page: string) {
  switch (page) {
    case 'dashboard':
      return <Dashboard />;
    case 'blobs':
      return <BlobPiktogram size={24} color="#222222" />;
    case 'factory':
      return <Factory />;
    case 'standings':
      return <EmojiEvents />;
    case 'calendar':
      return <CalendarMonth />;
    default:
      return null;
  }
}

export function RootLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { t } = useTranslation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <>
      <List>
        {pages.map((text, _) => (
          <ListItem key={text}>
            <Box display="flex" gap={1} color="#222222">
              {getMenuIcon(text)}
              <Link
                key={text}
                to={`/${text}`}
                activeProps={{
                  className: 'font-bold',
                }}
                activeOptions={{ exact: true }}
                onClick={() => isMobile && setMobileOpen(false)}
              >
                {t(`menu.${text}`)}
              </Link>
            </Box>
          </ListItem>
        ))}
      </List>
      <Box>
        <LanguageSwitcher />
        <Box
          sx={{
            width: '100%',
            padding: '1rem',
            borderTop: '1px solid #e0e0e0',
            backgroundColor: 'background.paper',
          }}
        >
          <Typography variant="caption" display="block" color="text.secondary">
            © 2025 Adamax-Works
          </Typography>
          <Typography variant="caption" display="block" color="text.secondary">
            v2.6
          </Typography>
        </Box>
      </Box>
    </>
  );

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {isMobile && (
        <Box position="fixed" left={0} bottom={0} padding={2} sx={{ zIndex: 1000 }}>
          <Fab variant="circular" color="primary" aria-label="open drawer" onClick={handleDrawerToggle}>
            <Menu />
          </Fab>
        </Box>
      )}

      {/* Mobile drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: 'flex', sm: 'none' },
          '& .MuiDrawer-paper': {
            justifyContent: 'space-between',
            boxSizing: 'border-box',
            width: drawerWidth,
          },
        }}
      >
        {drawer}
      </Drawer>

      {/* Desktop drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'flex' },
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            justifyContent: 'space-between',
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        open
      >
        {drawer}
      </Drawer>

      <Box component="main" flexGrow={1} display="flex" overflow="auto" flexWrap="wrap" sx={{ padding: '0.5rem' }}>
        <Outlet />
      </Box>
    </Box>
  );
}
