import { Box, CardContent, CardHeader, CircularProgress, Divider, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { EventType } from '../../../../generated';
import { ReactNode } from 'react';

const Loader = ({ showLoader }: { showLoader?: boolean }) => (
  <Box
    height={56}
    width={56}
    marginTop="4px"
    marginRight="8px"
    display="flex"
    justifyContent="center"
    alignItems="center"
  >
    {showLoader && <CircularProgress />}
  </Box>
);

type EventCardFrameProps = {
  eventType: EventType;
  tickDisplay?: ReactNode;
  children: React.ReactNode;
  showLoader?: boolean;
};

export const EventCardFrame = ({ eventType, tickDisplay, children, showLoader }: EventCardFrameProps) => {
  const { t } = useTranslation();
  return (
    <Paper sx={{ maxHeight: '100vh', paddingBottom: 3, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <CardHeader
        title={t(`enums.event_types.${eventType}`)}
        subheader={tickDisplay}
        action={<Loader showLoader={showLoader} />}
      />
      <Divider />
      <CardContent
        sx={{
          flex: 1,
          overflowY: 'auto',
          '&::-webkit-scrollbar': {
            display: 'none',
          },
          scrollbarWidth: 'none',
        }}
      >
        {children}
      </CardContent>
    </Paper>
  );
};
