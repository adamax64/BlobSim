import { Box, Tooltip, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { CalendarDto, EventType } from '../../../../generated';
import { useNavigate } from '@tanstack/react-router';
import CheckCircle from '@mui/icons-material/CheckCircle';
import PlayCircle from '@mui/icons-material/PlayCircle';
import ResultsModal from '../../event-components/ResultsModal';
import { useState } from 'react';

type CalendarEventContentUIProps = {
  event: CalendarDto;
  isToday: boolean;
};

export const CalendarEventContentUI: React.FC<CalendarEventContentUIProps> = ({ event, isToday }) => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [resultsModalOpen, setResultsModalOpen] = useState(false);

  const closeResultsModal = () => {
    setResultsModalOpen(false);
  };

  const handleClick = () => {
    if (event.isConcluded && event.eventId) {
      setResultsModalOpen(true);
    } else if (isToday) {
      navigate({
        to: '/event',
      });
    }
  };

  return (
    <>
      <Typography variant="caption" sx={{ fontSize: '0.8125rem' }}>
        {event.leagueName
          ? t('calendar.event_title', {
              leagueName: event.leagueName,
              round: event.round,
              eventType: t(`enums.event_types.${event.eventType}`),
            })
          : t(`enums.event_types.${event.eventType}`, { day: event.round })}
      </Typography>
      {event.eventType !== EventType.CatchupTraining && (event.isConcluded || isToday) ? (
        <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }} onClick={handleClick}>
          {event.isConcluded ? (
            <Tooltip title={t('calendar.show_results')}>
              <CheckCircle sx={{ cursor: 'pointer' }} />
            </Tooltip>
          ) : isToday ? (
            <Tooltip title={t('calendar.jump_to_event')}>
              <PlayCircle sx={{ cursor: 'pointer' }} />
            </Tooltip>
          ) : null}
        </Box>
      ) : null}
      {event.isConcluded && event.eventId && (
        <ResultsModal eventId={event.eventId} open={resultsModalOpen} onClose={closeResultsModal} />
      )}
    </>
  );
};
