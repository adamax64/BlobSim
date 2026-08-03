import { useEffect, useMemo } from 'react';
import { useMutation } from '@tanstack/react-query';
import { StandingsApi, StandingsDTO } from '../../../../generated';
import defaultConfig from '../../../default-config';
import { StandingsTable } from '../../standings/StandingsTable';
import { EventCardFrame } from './EventCardFrame';

type EventStandingsStageProps = {
  active: boolean;
  title: string;
  leagueId: number;
  leagueName: string;
  season: number;
  throughRound: number;
};

export const EventStandingsStage = ({
  active,
  title,
  leagueId,
  leagueName,
  season,
  throughRound,
}: EventStandingsStageProps) => {
  const standingsApi = useMemo(() => new StandingsApi(defaultConfig), []);

  const {
    data: standings,
    isPending,
    mutate: loadStandings,
  } = useMutation<StandingsDTO[], Error>({
    mutationFn: () =>
      standingsApi.getStandingsByLeagueAndSeasonStandingsChampionshipLeagueIdSeasonGet({
        leagueId,
        season,
        round: throughRound,
      }),
  });

  useEffect(() => {
    if (active) {
      loadStandings();
    }
  }, [active, loadStandings, throughRound]);

  return (
    <EventCardFrame title={title}>
      <StandingsTable
        loading={isPending && !standings}
        standings={standings ?? []}
        leagueName={leagueName}
        season={season}
      />
    </EventCardFrame>
  );
};

export default EventStandingsStage;
