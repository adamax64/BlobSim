import { useMutation } from '@tanstack/react-query';
import { CompetitionApi, EventDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { useEffect } from 'react';

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

  return (
    <PageFrame>
      <PageTitleCard title={event && `${event.league.name} Season ${event.season} Round ${event.round}`} />
    </PageFrame>
  );
};
