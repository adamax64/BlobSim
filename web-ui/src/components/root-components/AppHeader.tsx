import { Menu } from '@mui/icons-material';
import { AppBar, Box, IconButton, Toolbar, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useCurrentPage } from '../../context/CurrentPageContext';
import { BlobIcon } from '../icons/BlobIcon';

type AppHeaderProps = {
  isMobile: boolean;
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
};

export const AppHeader = ({ isMobile, mobileOpen, setMobileOpen }: AppHeaderProps) => {
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  const { selectedMenuItem, pageTitle } = useCurrentPage();
  const { t } = useTranslation();

  const blobIconColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  console.log(pageTitle, selectedMenuItem);

  const titleComponent = isMobile ? (
    <Typography variant="h6" noWrap component="div">
      {t(`menu.${selectedMenuItem}`)}
    </Typography>
  ) : (
    <Box display="flex" justifyContent="space-between" flexGrow={1}>
      <BlobIcon size={32} color={blobIconColor} />
      <Typography variant="h6" noWrap component="div">
        {pageTitle ?? t(`${selectedMenuItem}.title`)}
      </Typography>
      <BlobIcon size={32} color={blobIconColor} />
    </Box>
  );

  return (
    <>
      <AppBar component="nav" color="default" elevation={1}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { xs: 'inline-flex', sm: 'none' } }}
            >
              <Menu />
            </IconButton>
          )}
          {titleComponent}
        </Toolbar>
      </AppBar>
      <Toolbar /> {/* Spacer to push content below AppBar */}
    </>
  );
};
