import {
  Box,
  CircularProgress,
  FormControl,
  FormControlLabel,
  IconButton,
  InputAdornment,
  InputLabel,
  MenuItem,
  OutlinedInput,
  Paper,
  Select,
  SelectChangeEvent,
  Switch,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import Search from '@mui/icons-material/Search';
import { useEffect, useState } from 'react';
import { BlobStatsDto, BlobsApi, LeagueDto, LeaguesApi, TranslationsDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { BlobDetailsDialog } from '../common/BlobDetailsDialog/BlobDetailsDialog';
import { BlobsDesktopGrid } from '../blobs-components/BlobsDesktopGrid';
import { BlobsMobileCards } from '../blobs-components/BlobsMobileCards';
import { useTranslation } from 'react-i18next';
import { getLocalizedText } from '../../utils/translation-utils';

/** Sentinel value used by the league filter for "blobs without a league". */
const NO_LEAGUE_ID = -1;

interface LeagueFilterOption {
  id: number;
  translations?: TranslationsDto[];
}

export function BlobsPage() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { t, i18n } = useTranslation();
  const [nameSearch, setNameSearch] = useState<string>('');
  const [showDead, setShowDead] = useState<boolean>(false);
  const [selectedLeagueId, setSelectedLeagueId] = useState<number | ''>('');
  const [leagueOptions, setLeagueOptions] = useState<LeagueFilterOption[]>([]);
  const [selectedBlob, setSelectedBlob] = useState<BlobStatsDto | null>(null);

  const blobsApi = new BlobsApi(defaultConfig);
  const leaguesApi = new LeaguesApi(defaultConfig);

  const {
    data: blobs,
    isPending,
    mutate: getAllBlobs,
  } = useMutation<BlobStatsDto[], Error>({
    mutationFn: () =>
      blobsApi.getAllBlobsAllGet({
        nameSearch: nameSearch ? nameSearch : undefined,
        showDead,
        leagueId: selectedLeagueId === '' ? undefined : selectedLeagueId,
      }),
  });

  const {
    data: leagues,
    isPending: loadingLeagues,
    mutate: loadLeagues,
  } = useMutation<LeagueDto[], Error>({
    mutationFn: () => leaguesApi.getLeaguesWithQueueLeaguesAllWithQueueGet(),
  });

  useEffect(() => {
    loadLeagues();
  }, []);

  useEffect(() => {
    if (leagues) {
      setLeagueOptions(leagues.map((league) => ({ id: league.id, translations: league.name })));
    }
  }, [leagues]);

  useEffect(() => {
    getAllBlobs();
  }, [showDead, selectedLeagueId]);

  const getLeagueLabel = (leagueId: number) => {
    if (leagueId === NO_LEAGUE_ID) {
      return t('blobs.no_league');
    }
    const league = leagueOptions.find((l) => l.id === leagueId);
    return league ? getLocalizedText(league.translations, i18n.language) : '';
  };

  const handleLeagueChange = (event: SelectChangeEvent<number | ''>) => {
    setSelectedLeagueId(event.target.value as number | '');
  };

  return (
    <PageFrame showLoading={isPending} pageName="blobs">
      <Paper sx={{ marginBottom: 4 }}>
        <Box display="flex" gap={3} p={2} flexWrap="wrap">
          <FormControl variant="outlined">
            <InputLabel htmlFor="search-by-name">{t('blobs.search_by_name')}</InputLabel>
            <OutlinedInput
              id="search-by-name"
              type="text"
              endAdornment={
                <InputAdornment position="end">
                  <IconButton onClick={() => getAllBlobs()}>
                    <Search />
                  </IconButton>
                </InputAdornment>
              }
              value={nameSearch}
              onChange={(e) => setNameSearch(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && getAllBlobs()}
              label={t('blobs.search_by_name')}
            />
          </FormControl>
          <FormControl variant="outlined" sx={{ minWidth: 180 }}>
            <InputLabel id="league-select">{t('blobs.filter_by_league')}</InputLabel>
            <Select
              labelId="league-select"
              value={selectedLeagueId ?? ''}
              onChange={handleLeagueChange}
              label={t('blobs.filter_by_league')}
              endAdornment={
                loadingLeagues ? (
                  <InputAdornment position="end">
                    <CircularProgress size={20} />
                  </InputAdornment>
                ) : undefined
              }
            >
              <MenuItem value={''}>{t('blobs.all_leagues')}</MenuItem>
              {leagueOptions.map((league) => (
                <MenuItem key={league.id} value={league.id}>
                  {getLeagueLabel(league.id)}
                </MenuItem>
              ))}
              <MenuItem value={NO_LEAGUE_ID}>{t('blobs.no_league')}</MenuItem>
            </Select>
          </FormControl>
          <FormControlLabel
            control={<Switch value={showDead} onChange={(e) => setShowDead(e.target.checked)} />}
            label={t('blobs.show_dead')}
          />
        </Box>
        {isMobile ? (
          <BlobsMobileCards blobs={blobs} onBlobSelect={setSelectedBlob} />
        ) : (
          <BlobsDesktopGrid blobs={blobs} isPending={isPending} onBlobSelect={setSelectedBlob} />
        )}
      </Paper>
      {selectedBlob && (
        <BlobDetailsDialog open={!!selectedBlob} onClose={() => setSelectedBlob(null)} cachedBlob={selectedBlob} />
      )}
    </PageFrame>
  );
}
