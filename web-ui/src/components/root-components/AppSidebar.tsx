import { Box, List, ListItem, Typography } from '@mui/material';
import { LanguageSwitcher } from './LanguageSwitcher';
import { useTranslation } from 'react-i18next';
import CalendarMonth from '@mui/icons-material/CalendarMonth';
import Dashboard from '@mui/icons-material/Dashboard';
import EmojiEvents from '@mui/icons-material/EmojiEvents';
import Factory from '@mui/icons-material/Factory';
import { BlobPiktogram } from '../icons/BlobPiktogram';
import { Link } from '@tanstack/react-router';
import { AppPage, MENU_ITEMS } from './constants';
import { useCurrentPage } from '../../context/CurrentPageContext';

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

type AppSidebarProps = {
  isMobile: boolean;
  setMobileOpen: (open: boolean) => void;
};

export const AppSidebar = ({ isMobile, setMobileOpen }: AppSidebarProps) => {
  const { setCurrentPage } = useCurrentPage();
  const { t } = useTranslation();

  const handleMenuItemClick = (menuItem: AppPage) => {
    setCurrentPage(menuItem);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  return (
    <>
      <List>
        {MENU_ITEMS.map((text, _) => (
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
                onClick={() => handleMenuItemClick(text)}
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
            v3.1.3
          </Typography>
        </Box>
      </Box>
    </>
  );
};
