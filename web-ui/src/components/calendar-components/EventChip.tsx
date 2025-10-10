import { TFunction } from 'i18next';
import { CalendarDto } from '../../../generated';
import { Chip, Tooltip } from '@mui/material';
import CheckCircle from '@mui/icons-material/CheckCircle';
import PlayCircle from '@mui/icons-material/PlayCircle';
import { useNavigate } from '@tanstack/react-router';

interface EventChipProps {
  calendar: CalendarDto[] | undefined;
  epoch: number;
  cycle: number;
  t: TFunction<'translation', undefined>;
  isToday: boolean;
}

export const EventChip: React.FC<EventChipProps> = ({ calendar, epoch, cycle, t, isToday }) => {
  const navigate = useNavigate();

  if (!calendar) return null;

  const event = calendar.find((e) => e.date.epoch === epoch && e.date.cycle === cycle);
  if (!event) return null;

  let color: 'primary' | 'success' | 'secondary' | 'default' | 'error' = 'default';
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
      color = 'default';
      break;
    default:
      color = 'default';
  }

  if (event.eventType === 'CATCHUP_TRAINING') {
    color = 'error';
  }

  return (
    <Chip
      label={
        event.leagueName
          ? t('calendar.event_title', {
              leagueName: event.leagueName,
              round: event.round,
              eventType: t(`enums.event_types.${event.eventType}`),
            })
          : t(`enums.event_types.${event.eventType}`, { day: event.round })
      }
      color={color}
      deleteIcon={
        // Do not render a deleteIcon for catch-up training events
        event.eventType === 'CATCHUP_TRAINING' ? (
          <></>
        ) : event.isConcluded ? (
          <CheckCircle />
        ) : isToday ? (
          <Tooltip title={t('calendar.jump_to_event')}>
            <PlayCircle />
          </Tooltip>
        ) : (
          <></>
        )
      }
      onDelete={() => {
        if (isToday) {
          navigate({
            to: '/event',
          });
        }
      }}
      sx={{
        height: 'auto',
        '& .MuiChip-label': {
          display: 'block',
          whiteSpace: 'normal',
          paddingTop: 0.5,
          paddingBottom: 0.5,
        },
      }}
    />
  );
};
