import { Box } from '@mui/material';
import { DRAWER_WIDTH } from './constants';
import { AppSidebar } from './AppSidebar';

type DesktopMenuProps = {
  isMobile: boolean;
};

export const DesktopMenu = ({ isMobile }: DesktopMenuProps) => {
  if (isMobile) {
    return null;
  }

  return (
    <>
      <Box
        component="nav"
        position="fixed"
        bgcolor="white"
        display="flex"
        flexDirection="column"
        height="-webkit-fill-available"
        minWidth={DRAWER_WIDTH}
        justifyContent={'space-between'}
        boxSizing={'border-box'}
        borderRight={'1px solid #e0e0e0'}
      >
        <AppSidebar isMobile={isMobile} setMobileOpen={() => {}} />
      </Box>
      <Box width={`${DRAWER_WIDTH}px`} flexShrink={0} />
    </>
  );
};
