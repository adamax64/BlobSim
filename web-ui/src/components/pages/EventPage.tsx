import { useMutation } from '@tanstack/react-query';
import { CompetitionApi, EventDto, EventType } from '../../../generated';
import defaultConfig from '../../default-config';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { useCallback, useEffect } from 'react';
import { Box, Card, CircularProgress } from '@mui/material';
import { QuarteredEventFrame } from '../event-components/QuarteredEventFrame';
import { EnduranceRaceEventFrame } from '../event-components/EnduranceRaceEventFrame';
import { useTranslation } from 'react-i18next';
import { EliminationScoringEventFrame } from '../event-components/elimination-scoring/EliminationScoringEventFrame';

export const EventPage = () => {
  const competitionApi = new CompetitionApi(defaultConfig);
  const { t } = useTranslation();

  const {
    data: event,
    isPending: loadingEvent,
    mutate: loadEvent,
  } = useMutation<EventDto, Error>({
    mutationFn: () => competitionApi.getCurrentEventCompetitionCurrentGet(),
  });

  useEffect(() => {
    loadEvent();
  }, []);

  const eventContent = useCallback(() => {
    if (loadingEvent) {
      return (
        <Card>
          <Box display="flex" justifyContent="center" alignItems="center" padding={4}>
            <CircularProgress size={48} />
          </Box>
        </Card>
      );
    }

    if (!event) {
      return (
        <Card>
          <Box display="flex" justifyContent="center" alignItems="center" padding={4}>
            {t('event.no_event_data')}
          </Box>
        </Card>
      );
    }

    switch (event.type) {
      case EventType.QuarteredTwoShotScoring:
      case EventType.QuarteredOneShotScoring:
        return <QuarteredEventFrame event={event} />;
      case EventType.EnduranceRace:
        return <EnduranceRaceEventFrame event={event} />;
      case EventType.EliminationScoring:
        return <EliminationScoringEventFrame event={event} />;
    }
  }, [loadingEvent, event]);

  return (
    <PageFrame>
      <PageTitleCard
        title={
          event &&
          t('event.title', {
            leagueName: event.league.name,
            season: event.season,
            round: event.round,
          })
        }
      />
      {eventContent()}
    </PageFrame>
  );
};
