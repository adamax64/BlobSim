import { useEffect, useRef, useState } from 'react';
import { CompetitionApi, LeagueDto, LeaguesApi, SeasonCompetitionDto, ResultDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { PageFrame } from '../common/PageFrame';
import {
  Box,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  useMediaQuery,
  useTheme,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Preview } from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useSimTime } from '../../context/SimTimeContext';
import { formatToShort } from '../../utils/sim-time-utils';
import { ResultsModal } from '../event-components/ResultsModal';
import { NarrowCell } from '../common/StyledComponents';

const ALL_LEAGUE = 'all';

export const ResultsPage = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { simTime, loading: simTimeLoading, refreshSimTime } = useSimTime();
  const [season, setSeason] = useState<number>(1);
  const [selectedLeague, setSelectedLeague] = useState<string>(ALL_LEAGUE);
  const [selectedCompetition, setSelectedCompetition] = useState<SeasonCompetitionDto | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const initialSeasonSet = useRef(false);

  const competitionApi = new CompetitionApi(defaultConfig);
  const leaguesApi = new LeaguesApi(defaultConfig);

  const {
    data: competitions,
    isPending: loadingCompetitions,
    mutate: loadCompetitions,
  } = useMutation<SeasonCompetitionDto[], Error, number>({
    mutationFn: (seasonId: number) =>
      competitionApi.getCompetitionsBySeasonRouteCompetitionResultsSeasonSeasonGet({ season: seasonId }),
  });

  const { data: leagues, mutate: loadLeagues } = useMutation<LeagueDto[], Error>({
    mutationFn: () => leaguesApi.getLeaguesLeaguesAllGet(),
  });

  useEffect(() => {
    if (!simTime) {
      refreshSimTime();
    }
  }, [simTime, refreshSimTime]);

  useEffect(() => {
    if (simTime && !initialSeasonSet.current) {
      setSeason(simTime.season);
      initialSeasonSet.current = true;
    }
  }, [simTime]);

  useEffect(() => {
    if (season != null) {
      loadCompetitions(season);
    }
  }, [season, loadCompetitions]);

  useEffect(() => {
    loadLeagues();
  }, [loadLeagues]);

  const seasonOptions = Array.from({ length: Math.max(0, simTime?.season ?? 0) }, (_, i) => i + 1).reverse();
  const filteredCompetitions =
    !selectedLeague || selectedLeague === ALL_LEAGUE
      ? (competitions ?? [])
      : (competitions ?? []).filter((c) => c.leagueName === selectedLeague);

  return (
    <PageFrame pageName="results">
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={2}>
            <Box display="flex" flexWrap="wrap" gap={2} alignItems="center">
              <FormControl sx={{ width: 'fit-content', minWidth: 140 }} size="small">
                <InputLabel id="results-season-label">{t('results.season')}</InputLabel>
                <Select
                  labelId="results-season-label"
                  value={season}
                  label={t('results.season')}
                  onChange={(e) => setSeason(Number(e.target.value))}
                  disabled={simTimeLoading}
                >
                  {seasonOptions.map((s) => (
                    <MenuItem key={s} value={s}>
                      {s}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl sx={{ width: 'fit-content', minWidth: 140 }} size="small">
                <InputLabel id="results-league-label">{t('results.league')}</InputLabel>
                <Select
                  labelId="results-league-label"
                  value={selectedLeague}
                  label={t('results.league')}
                  onChange={(e) => setSelectedLeague(e.target.value as string)}
                >
                  <MenuItem value={ALL_LEAGUE}>{t('results.filter_all')}</MenuItem>
                  {(leagues ?? []).map((league) => (
                    <MenuItem key={league.id} value={league.name}>
                      {league.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            {loadingCompetitions ? (
              <Box display="flex" justifyContent="center" p={2}>
                <CircularProgress />
              </Box>
            ) : (
              <TableContainer
                component={Paper}
                variant="outlined"
                sx={{ maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}
              >
                <Table size="small" stickyHeader>
                  <TableHead>
                    <TableRow>
                      <TableCell>{t('results.date')}</TableCell>
                      {isMobile ? (
                        <NarrowCell>{t('results.details')}</NarrowCell>
                      ) : (
                        <>
                          <TableCell>{t('results.league')}</TableCell>
                          <TableCell>{t('results.round')}</TableCell>
                          <TableCell>{t('results.event_type')}</TableCell>
                        </>
                      )}
                      <TableCell align="center">{t('results.actions')}</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredCompetitions.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={isMobile ? 3 : 5} align="center">
                          {t('results.no_events')}
                        </TableCell>
                      </TableRow>
                    ) : (
                      filteredCompetitions.map((row, index) => {
                        const eventTypeLabel = t(`enums.event_types.${row.eventType}`);
                        return (
                          <TableRow key={index}>
                            <TableCell>{formatToShort(row.date)}</TableCell>
                            {isMobile ? (
                              <NarrowCell>
                                {row.leagueName} · {t('results.round_short', { round: row.round })} · {eventTypeLabel}
                              </NarrowCell>
                            ) : (
                              <>
                                <TableCell>{row.leagueName}</TableCell>
                                <TableCell>{row.round}</TableCell>
                                <TableCell>{eventTypeLabel}</TableCell>
                              </>
                            )}
                            <TableCell align="center">
                              <Tooltip title={t('results.view_results')}>
                                <IconButton
                                  onClick={() => {
                                    setSelectedCompetition(row);
                                    setIsModalOpen(true);
                                  }}
                                >
                                  <Preview />
                                </IconButton>
                              </Tooltip>
                            </TableCell>
                          </TableRow>
                        );
                      })
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </Box>
        </CardContent>
      </Card>
      <ResultsModal
        eventId={selectedCompetition?.id ?? null}
        open={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedCompetition(null);
        }}
      />
    </PageFrame>
  );
};
