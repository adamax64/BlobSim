import { useMutation } from '@tanstack/react-query';
import { CompetitionApi, EventDtoOutput, EventType } from '../../../generated';
import defaultConfig from '../../default-config';
import { PageFrame } from '../common/PageFrame';
import { useEffect, useMemo, useState, useCallback } from 'react';
import { Box, Card, CircularProgress } from '@mui/material';
import { useParams } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';
import { ReplaySprintRaceFrame } from '../replay-components/ReplaySprintRaceFrame';
import { ReplayEnduranceRaceFrame } from '../replay-components/ReplayEnduranceRaceFrame';
import { ReplayQuarteredEventFrame } from '../replay-components/ReplayQuarteredEventFrame';
import { ReplayEliminationScoringFrame } from '../replay-components/ReplayEliminationScoringFrame';
import { ReplayControls } from '../replay-components/ReplayControls';
import { useNavigate } from '@tanstack/react-router';

export const ReplayPage = () => {
  const { eventId } = useParams({ from: '/replay/$eventId' });
  const competitionApi = new CompetitionApi(defaultConfig);
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [currentTick, setCurrentTick] = useState(0);
  const [maxTick, setMaxTick] = useState<number | undefined>();

  const {
    data: event,
    isPending: loadingEvent,
    mutate: loadEvent,
  } = useMutation<EventDtoOutput, Error, number>({
    mutationFn: (id: number) => competitionApi.getEventByIdRouteCompetitionEventIdGet({ eventId: id }),
  });

  useEffect(() => {
    if (eventId) {
      loadEvent(Number(eventId));
    }
  }, [eventId, loadEvent]);

  useEffect(() => {
    if (eventId) {
      const storageKey = 'replay_ticks';
      const storedData = JSON.parse(localStorage.getItem(storageKey) || '[]');
      const eventEntry = storedData.find((entry: any) => entry.eventId === eventId);
      if (eventEntry) {
        setCurrentTick(eventEntry.tick);
      } else {
        setCurrentTick(0);
      }
    }
  }, [eventId]);

  useEffect(() => {
    if (event) {
      if (event.type === EventType.QuarteredOneShotScoring || event.type === EventType.QuarteredTwoShotScoring) {
        const totalActions = event.actions.reduce((sum, action) => sum + action.scores.length, 0);
        setMaxTick(totalActions);
      } else {
        const maxActionLength = Math.max(...event.actions.map((action) => action.scores.length), 0);
        setMaxTick(maxActionLength);
      }
    }
  }, [event]);

  useEffect(() => {
    if (eventId) {
      const storageKey = 'replay_ticks';
      let storedData = JSON.parse(localStorage.getItem(storageKey) || '[]');

      // Remove existing entry for this eventId if it exists
      storedData = storedData.filter((entry: any) => entry.eventId !== eventId);

      // Add new entry at the end
      storedData.push({ eventId, tick: currentTick });

      // Keep only the last 16 entries
      if (storedData.length > 16) {
        storedData = storedData.slice(-16);
      }

      localStorage.setItem(storageKey, JSON.stringify(storedData));
    }
  }, [currentTick, eventId]);

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
            {t('replay.no_event_data')}
          </Box>
        </Card>
      );
    }

    switch (event.type) {
      case EventType.QuarteredTwoShotScoring:
      case EventType.QuarteredOneShotScoring:
        return <ReplayQuarteredEventFrame event={event} tick={currentTick} />;
      case EventType.EnduranceRace:
        return <ReplayEnduranceRaceFrame event={event} tick={currentTick} />;
      case EventType.SprintRace:
        return <ReplaySprintRaceFrame event={event} tick={currentTick} maxTick={maxTick ?? 0} />;
      case EventType.EliminationScoring:
        return <ReplayEliminationScoringFrame event={event} tick={currentTick} />;
      default:
        return <div>Unknown Event Type</div>;
    }
  }, [loadingEvent, event, currentTick, t]);

  const pageTitle = useMemo(
    () =>
      event
        ? t('replay.title', { leagueName: event.league.name, season: event.season, round: event.round })
        : t('replay.title_short'),
    [event, t],
  );

  return (
    <PageFrame pageName="replay" customPageTitle={pageTitle}>
      {eventContent()}
      <ReplayControls
        currentTick={currentTick}
        maxTick={maxTick}
        setCurrentTick={setCurrentTick}
        onGoBack={() => navigate({ to: '/results' })}
      />
    </PageFrame>
  );
};
