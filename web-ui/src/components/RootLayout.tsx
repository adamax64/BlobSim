import { Box, Drawer, List, ListItem } from "@mui/material";
import { Link, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";

const pages = ['Dashboard', 'Blobs', 'Standings', 'Calendar'];

const drawerWidth = 240;

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
                    </ListItem>
                ))}
                </List>
            </Drawer>
            <Box
                component="main"
                sx={{ flexGrow: 1 }}
            >
                <Outlet />
                <TanStackRouterDevtools position="bottom-right" />
            </Box>
        </Box>
    )
}
  