import { useMutation } from '@tanstack/react-query';
import { CompetitionApi, EventDto, EventType } from '../../../generated';
import defaultConfig from '../../default-config';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { useCallback, useEffect } from 'react';
import { Box, Card, CircularProgress } from '@mui/material';
import { QuarteredEventFrame } from '../event-components/QuarteredEventFrame';
import { EnduranceRaceEventFrame } from '../event-components/EnduranceRaceEventFrame';

export const EventPage = () => {
  const competitionApi = new CompetitionApi(defaultConfig);

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
            No event data available
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
    }
  }, [loadingEvent, event]);

  return (
    <PageFrame>
      <PageTitleCard title={event && `${event.league.name} Season ${event.season} Round ${event.round}`} />
      {eventContent()}
    </PageFrame>
  );
};
