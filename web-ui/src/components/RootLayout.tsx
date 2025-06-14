import { Box, Drawer, List, ListItem, Typography, IconButton, useTheme, useMediaQuery, Fab } from '@mui/material';
import { Link, Outlet } from '@tanstack/react-router';
import { CalendarMonth, Dashboard, EmojiEvents, Factory, Menu } from '@mui/icons-material';
import { BlobPiktogram } from './icons/BlobPiktogram';
import { useState } from 'react';

const pages = ['Dashboard', 'Blobs', 'Factory', 'Standings', 'Calendar'];

const drawerWidth = 240;

function getMenuIcon(page: string) {
  switch (page) {
    case 'Dashboard':
      return <Dashboard />;
    case 'Blobs':
      return <BlobPiktogram size={24} color="#222222" />;
    case 'Factory':
      return <Factory />;
    case 'Standings':
      return <EmojiEvents />;
    case 'Calendar':
      return <CalendarMonth />;
    default:
      return null;
  }
}

export function RootLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

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
                to={`/${text.toLowerCase()}` as string}
                activeProps={{
                  className: 'font-bold',
                }}
                activeOptions={{ exact: true }}
                onClick={() => isMobile && setMobileOpen(false)}
              >
                {text}
              </Link>
            </Box>
          </ListItem>
        ))}
      </List>
      <Box
        sx={{
          position: 'absolute',
          bottom: 0,
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
          v2.3.2
        </Typography>
      </Box>
    </>
  );

  return (
    <Box sx={{ display: 'flex' }}>
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
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': {
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
          display: { xs: 'none', sm: 'block' },
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        open
      >
        {drawer}
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, padding: '0.5rem' }}>
        <Outlet />
      </Box>
    </Box>
  );
}
