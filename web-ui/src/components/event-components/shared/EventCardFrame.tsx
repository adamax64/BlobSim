import { CardContent, CardHeader, Divider, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { EventType } from '../../../../generated';
import { ReactNode } from 'react';

type EventCardFrameProps = {
  eventType: EventType;
  tickDisplay?: ReactNode;
  children: React.ReactNode;
};

export const EventCardFrame = ({ eventType, tickDisplay, children }: EventCardFrameProps) => {
  const { t } = useTranslation();
  return (
    <Paper sx={{ maxHeight: '100vh', paddingBottom: 3, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <CardHeader title={t(`enums.event_types.${eventType}`)} subheader={tickDisplay} />
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
