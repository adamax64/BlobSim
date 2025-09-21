import Menu from '@mui/icons-material/Menu';
import { AppBar, Box, IconButton, Toolbar, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useCurrentPage } from '../../context/CurrentPageContext';
import { BlobIcon } from '../icons/BlobIcon';
import { AppPage } from './constants';

type TitleProps = {
  pageTitle?: string;
  currentPage: AppPage;
};

const MobileTitle = ({ pageTitle, currentPage }: TitleProps) => {
  const { t } = useTranslation();
  return (
    <Typography variant="h6" noWrap component="div">
      {pageTitle ?? t(`page_titles.${currentPage}_short`)}
    </Typography>
  );
};

const DesktopTitle = ({ currentPage, pageTitle }: TitleProps) => {
  const { t } = useTranslation();
  const blobIconColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  return (
    <Box display="flex" justifyContent="space-between" flexGrow={1}>
      <BlobIcon size={32} color={blobIconColor} />
      <Typography variant="h6" noWrap component="div">
        {pageTitle ?? t(`page_titles.${currentPage}`)}
      </Typography>
      <BlobIcon size={32} color={blobIconColor} />
    </Box>
  );
};

type AppHeaderProps = {
  isMobile: boolean;
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
};

export const AppHeader = ({ isMobile, mobileOpen, setMobileOpen }: AppHeaderProps) => {
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  const { currentPage, pageTitle } = useCurrentPage();

  const titleComponent = isMobile ? (
    <MobileTitle currentPage={currentPage} pageTitle={pageTitle} />
  ) : (
    <DesktopTitle currentPage={currentPage} pageTitle={pageTitle} />
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
              sx={{ mr: 2, display: 'inline-flex' }}
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
