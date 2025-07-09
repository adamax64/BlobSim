import {
  Box,
  FormControl,
  FormControlLabel,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  Paper,
  Switch,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { Search } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { BlobsApi, BlobStatsDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { BlobDetailsDialog } from '../common/BlobDetailsDialog';
import { BlobsDesktopGrid } from '../blobs-components/BlobsDesktopGrid';
import { BlobsMobileCards } from '../blobs-components/BlobsMobileCards';
import { useTranslation } from 'react-i18next';

export function BlobsPage() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [nameSearch, setNameSearch] = useState<string>('');
  const [showDead, setShowDead] = useState<boolean>(false);
  const [selectedBlob, setSelectedBlob] = useState<BlobStatsDto | null>(null);
  const { t } = useTranslation();

  const blobsApi = new BlobsApi(defaultConfig);

  const {
    data: blobs,
    isPending,
    mutate: getAllBlobs,
  } = useMutation<BlobStatsDto[], Error>({
    mutationFn: () => blobsApi.getAllBlobsAllGet({ nameSearch: nameSearch ? nameSearch : undefined, showDead }),
  });

  useEffect(() => {
    getAllBlobs();
  }, [showDead]);

  return (
    <PageFrame showLoading={isPending}>
      <PageTitleCard title={t('blobs.title')} center />
      <Paper sx={{ marginBottom: 4 }}>
        <Box display="flex" gap={3} p={2}>
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
        <BlobDetailsDialog open={!!selectedBlob} onClose={() => setSelectedBlob(null)} blob={selectedBlob} />
      )}
    </PageFrame>
  );
}
