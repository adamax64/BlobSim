import { Box, Drawer, List, ListItem, Typography } from "@mui/material";
import { Link, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import { CalendarMonth, Dashboard, EmojiEvents, Factory } from "@mui/icons-material";
import { BlobPiktogram } from "./icons/BlobPiktogram";

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
  return (
    <Box sx={{ display: 'flex' }}>
      <Drawer
        sx={{
          flexShrink: 0,
          width: drawerWidth,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="permanent" anchor="left">
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
            v2.2
          </Typography>
        </Box>
      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, padding: "0.5rem" }}
      >
        <Outlet />
        <TanStackRouterDevtools position="bottom-right" />
      </Box>
    </Box>
  )
}
