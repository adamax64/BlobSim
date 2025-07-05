import { Box, Button, Card, CardContent, Fab, Typography } from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import defaultConfig from '../../default-config';
import { GeneralInfosApi, News, NewsType, SimDataApi } from '../../../generated';
import { useEffect, useMemo, useState } from 'react';
import { AddCircle, SkipNext, Stadium } from '@mui/icons-material';
import { PageTitleCard } from '../common/PageTitleCard';
import { PageFrame } from '../common/PageFrame';
import { BlobNamingDialog } from '../common/BlobNamingDialog';
import { SimTimeDisplay } from '../common/SimTimeDisplay';
import { useSimTime } from '../../context/SimTimeContext';
import { LoadingOverlay } from '../common/LoadingOverlay';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

function getNewsText(news: News, t: (key: string, options?: any) => string) {
  switch (news.newsType) {
    case NewsType.Event:
      return t('dashboard.news_item.event');
    case NewsType.BlobCreatedAndNamed:
      return t('dashboard.news_item.blob_created_and_named', { blobInfo: news.blobInfo });
    case NewsType.BlobCreated:
      return t('dashboard.news_item.blob_created');
    case NewsType.SeasonStart:
      return t('dashboard.news_item.season_start');
    case NewsType.Continue:
      return t('dashboard.news_item.continue');
    case NewsType.EventEnded:
      return t('dashboard.news_item.event_ended', {
        eventName: news.eventSummary?.eventName,
        winner: news.eventSummary?.winner,
        runnerUp: news.eventSummary?.runnerUp,
        thirdPlace: news.eventSummary?.thirdPlace,
      });
  }
}

export function DashboardPage() {
  const [open, setOpen] = useState(false);
  const [loadingOverlayVisible, setLoadingOverlayVisible] = useState(false);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { t } = useTranslation();

  const { refreshSimTime, loading: simTimeLoading } = useSimTime();

  const generalApi = new GeneralInfosApi(defaultConfig);
  const {
    data: news,
    mutate: fetchNews,
    isPending: isLoadingNews,
  } = useMutation<News[], Error>({
    mutationFn: () => generalApi.getNewsGeneralInfosNewsGet(),
    onSuccess: () => {
      setLoadingOverlayVisible(false);
    },
  });

  const simDataApi = new SimDataApi(defaultConfig);
  const { mutate: progressSimulation, isPending: isProgressingSimulation } = useMutation({
    mutationFn: () => simDataApi.progressSimDataSimulatePost(),
    onSuccess: () => {
      fetchNews();
      refreshSimTime();
    },
  });

  useEffect(() => {
    fetchNews();
  }, []);

  const newsTypes: NewsType[] = useMemo(() => news?.map((newsItem) => newsItem.newsType) || [], [news]);

  function handleDialogClose(update?: boolean) {
    setOpen(false);
    if (update) {
      fetchNews();
    }
  }

  const handleProgressClick = () => {
    setLoadingOverlayVisible(true);
    progressSimulation();
  };

  return (
    <PageFrame>
      <PageTitleCard title={t('dashboard.title')} />
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">{t('dashboard.date')}</Typography>
            <SimTimeDisplay />
          </Box>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">{t('dashboard.news')}</Typography>
            {news
              ? news.map((newsItem, index) => (
                  <Box key={index} display="flex" flexDirection="column" gap={1}>
                    <Typography variant="body1">{getNewsText(newsItem, t)}</Typography>
                  </Box>
                ))
              : t('dashboard.loading')}
          </Box>
        </CardContent>
      </Card>
      <Box display="flex" gap={1}>
        {newsTypes.includes(NewsType.Event) && (
          <Button variant="contained" color="success" endIcon={<Stadium />} onClick={() => navigate({ to: '/event' })}>
            {t('dashboard.proceed_to_event')}
          </Button>
        )}
        {isAuthenticated && newsTypes.includes(NewsType.BlobCreated) && (
          <Button variant="contained" color="primary" endIcon={<AddCircle />} onClick={() => setOpen(true)}>
            {t('dashboard.create_new_blob')}
          </Button>
        )}
        {isAuthenticated &&
          (newsTypes.includes(NewsType.Continue) ||
            newsTypes.includes(NewsType.EventEnded) ||
            newsTypes.includes(NewsType.BlobCreatedAndNamed) ||
            newsTypes.includes(NewsType.SeasonStart)) && (
            <Button
              variant="contained"
              color="primary"
              endIcon={<SkipNext />}
              onClick={handleProgressClick}
              disabled={isLoadingNews || isProgressingSimulation}
            >
              {t('dashboard.proceed_to_next_day')}
            </Button>
          )}
      </Box>
      {/* TODO: handle blob with parent creation */}
      <BlobNamingDialog open={open} onClose={handleDialogClose} mode="create" />
      {(loadingOverlayVisible || simTimeLoading) && <LoadingOverlay />}
    </PageFrame>
  );
}
