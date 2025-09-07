import { useState, useEffect, useMemo } from 'react';
import { GrandmasterStandingsDTO, LeagueDto, LeaguesApi, StandingsApi, StandingsDTO } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { PageFrame } from '../common/PageFrame';
import {
  Autocomplete,
  Box,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  SelectChangeEvent,
  TextField,
} from '@mui/material';
import { PageTitleCard } from '../common/PageTitleCard';
import { StandingsTable } from '../standings/StandingsTable';
import { GrandmasterStandingsTable } from '../standings/GrandmasterStandingsTable';
import { useSimTime } from '../../context/SimTimeContext';
import { useTranslation } from 'react-i18next';

interface LeagueOption {
  id: number;
  name: string;
  level: number;
}

export function StandingsPage() {
  const [leagueOptions, setLeagueOptions] = useState<LeagueOption[]>();
  const [selectedLeague, setSelectedLeague] = useState<LeagueOption>();
  const [seasonOrEon, setSeasonOrEon] = useState<number>();
  const [isGrandmasters, setIsGrandmasters] = useState(false);
  const { t } = useTranslation();

  const { simTime, loading: loadingTime, refreshSimTime: loadSimTime } = useSimTime();

  const leaguesApi = new LeaguesApi(defaultConfig);
  const standingsApi = new StandingsApi(defaultConfig);

  const {
    data: leagues,
    isPending: loadingLeagues,
    mutate: loadLeagues,
  } = useMutation<LeagueDto[], Error>({
    mutationFn: () => leaguesApi.getLeaguesLeaguesAllGet(),
  });

  const {
    data: standings,
    isPending: loadingStandings,
    mutate: loadStandings,
  } = useMutation<StandingsDTO[], Error>({
    mutationFn: () => {
      if (selectedLeague && seasonOrEon) {
        return standingsApi.getStandingsByLeagueAndSeasonStandingsChampionshipLeagueIdSeasonGet({
          leagueId: selectedLeague.id,
          season: seasonOrEon,
        });
      }
      return Promise.reject(new Error('League or season not selected'));
    },
  });

  const {
    data: grandmasterStandings,
    isPending: loadingGrandmasterStandings,
    mutate: loadGrandmasterStandings,
  } = useMutation<GrandmasterStandingsDTO[], Error>({
    mutationFn: () => {
      if (seasonOrEon) {
        return standingsApi.getGrandmasterStandingsByEonStandingsGrandmasterStartSeasonGet({
          startSeason: (seasonOrEon - 1) * 4 + 1,
        });
      }
      return Promise.reject(new Error('Eon not selected'));
    },
  });

  useEffect(() => {
    loadLeagues();
  }, []);

  useEffect(() => {
    if (!simTime) {
      loadSimTime();
    }
  }, [simTime]);

  useEffect(() => {
    if (leagues) {
      setLeagueOptions([{ id: -1, name: t('standings.grandmasters'), level: -1 }, ...leagues]);
      setSelectedLeague(leagues[0]);
    }
  }, [leagues]);

  useEffect(() => {
    if (simTime) {
      setSeasonOrEon(isGrandmasters ? simTime.eon + 1 : simTime.season);
    }
  }, [simTime, isGrandmasters]);

  useEffect(() => {
    if (selectedLeague && seasonOrEon) {
      if (isGrandmasters || selectedLeague.id === -1) {
        loadGrandmasterStandings();
      } else {
        loadStandings();
      }
    }
  }, [selectedLeague, seasonOrEon, isGrandmasters]);

  const handleLeagueChange = (event: SelectChangeEvent<number>) => {
    const league = leagueOptions?.find((l) => l.id === event.target.value);
    setSelectedLeague(league);
    setIsGrandmasters(league?.id === -1);
  };

  const isFormLoading = useMemo(
    () => loadingLeagues || loadingTime || !selectedLeague || (!seasonOrEon && seasonOrEon !== 0),
    [loadingLeagues, loadingTime, selectedLeague],
  );

  const hasSeasonOrEonEnded = useMemo(() => {
    if (isGrandmasters) {
      return (seasonOrEon ?? 0) < (simTime?.eon ?? 0) + 1 || (simTime?.epoch ?? 0) > 30;
    }
    return (
      (seasonOrEon ?? 0) < (simTime?.season ?? 0) ||
      (standings?.[0]?.numOfRounds ?? 0) === (standings?.[0]?.results.length ?? 0)
    );
  }, [isGrandmasters, seasonOrEon, simTime, standings]);

  return (
    <PageFrame>
      <PageTitleCard title={t('standings.title')} />
      <Paper sx={{ marginBottom: 4 }}>
        {isFormLoading ? (
          <Box display="flex" justifyContent="center" p={1}>
            <CircularProgress />
          </Box>
        ) : (
          <Box display="flex" gap={2} p={2} flexDirection={{ xs: 'column', sm: 'row' }}>
            <FormControl variant="outlined" sx={{ minWidth: 210 }}>
              <InputLabel id="league-select">{t('standings.league')}</InputLabel>
              <Select
                labelId="league-select"
                value={selectedLeague?.id}
                onChange={handleLeagueChange}
                label={t('standings.league')}
              >
                {leagueOptions?.map((league) => (
                  <MenuItem key={league.id} value={league.id}>
                    {league.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Autocomplete
              value={seasonOrEon}
              onChange={(_, newValue) => setSeasonOrEon(newValue as number)}
              options={
                isGrandmasters
                  ? Array.from({ length: (simTime?.eon ?? 0) + 1 }, (_, i) => i + 1).reverse()
                  : Array.from({ length: simTime?.season ?? 0 }, (_, i) => i + 1).reverse()
              }
              getOptionLabel={(option) => option.toString()}
              renderInput={(params) => (
                <TextField {...params} label={isGrandmasters ? t('standings.eon') : t('standings.season')} />
              )}
            />
          </Box>
        )}
        {isGrandmasters ? (
          <GrandmasterStandingsTable
            loading={loadingGrandmasterStandings || isFormLoading}
            standings={grandmasterStandings ?? []}
            eon={seasonOrEon}
            hasEonEnded={hasSeasonOrEonEnded}
          />
        ) : (
          <StandingsTable
            loading={loadingStandings || isFormLoading}
            standings={standings ?? []}
            leagueName={selectedLeague?.name}
            season={seasonOrEon}
            hasSeasonEnded={hasSeasonOrEonEnded}
          />
        )}
      </Paper>
    </PageFrame>
  );
}
