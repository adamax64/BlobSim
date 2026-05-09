import { CalendarDto, EventType } from '../../../../generated';
import { CalendarEventContentUI } from './CalendarEventContentUI';
import { CalendarEventWithTooltip } from './CalendarEventWithTooltip';
import { useIsMobile } from '../../../hooks/useIsMobile';
import { Paper } from '@mui/material';

interface EventWidgetProps {
  calendar: CalendarDto[] | undefined;
  epoch: number;
  cycle: number;
  isToday: boolean;
}

export const EventWidget: React.FC<EventWidgetProps> = ({ calendar, epoch, cycle, isToday }) => {
  const isMobile = useIsMobile();

  if (!calendar) return null;

  const event = calendar.find((e) => e.date.epoch === epoch && e.date.cycle === cycle);
  if (!event) return null;

  let color: 'primary' | 'success' | 'secondary' | 'default' | 'error' | 'warning' = 'default';
  switch (event.leagueLevel) {
    case 1:
      color = 'primary';
      break;
    case 2:
      color = 'success';
      break;
    case 3:
      color = 'secondary';
      break;
    case 0:
      color = 'warning';
      break;
    default:
      color = 'default';
  }

  if (event.eventType === EventType.CatchupTraining) {
    color = 'error';
  }

  return (
    <Paper
      elevation={1}
      sx={{
        height: 'auto',
        display: 'flex',
        whiteSpace: 'normal',
        paddingTop: 0.5,
        paddingBottom: 0.5,
        paddingLeft: 1,
        paddingRight: 1,
        borderRadius: 2,
        backgroundColor: `${color}.main`,
        color: `${color}.contrastText`,
      }}
    >
      {isMobile ? (
        <CalendarEventWithTooltip event={event} isToday={isToday} />
      ) : (
        <CalendarEventContentUI event={event} isToday={isToday} />
      )}
    </Paper>
  );
};
