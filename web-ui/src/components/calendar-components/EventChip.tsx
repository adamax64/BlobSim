import { TFunction } from 'i18next';
import { CalendarDto } from '../../../generated';
import { Chip, Tooltip } from '@mui/material';
import { CheckCircle, PlayCircle } from '@mui/icons-material';
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

  let color: 'primary' | 'success' | 'secondary' | 'default' = 'default';
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
    default:
      color = 'default';
  }

  return (
    <Chip
      label={t('calendar.event_title', {
        leagueName: event.leagueName,
        round: event.round,
        eventType: t(`event_types.${event.eventType}`),
      })}
      color={color}
      deleteIcon={
        event.isConcluded ? (
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
    />
  );
};
