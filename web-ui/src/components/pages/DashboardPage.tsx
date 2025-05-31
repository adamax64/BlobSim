import { Box, Button, Card, CardContent, Typography } from '@mui/material';
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

function getNewsText(news: News) {
  switch (news.newsType) {
    case NewsType.Event:
      return 'There is a championship event today!';
    case NewsType.BlobCreatedAndNamed:
      return `A new blob called ${news.blobInfo} has been created!`;
    case NewsType.BlobCreated:
      return 'A new blob has been created!';
    case NewsType.SeasonStart:
      return 'A new season has started!';
    case NewsType.Continue:
      return 'Nothing special happening today';
    case NewsType.EventEnded:
      return `${news.eventSummary?.eventName} has ended. The top 3 are: ${news.eventSummary?.winner}, ${news.eventSummary?.runnerUp}, and ${news.eventSummary?.thirdPlace}.`;
  }
}

export function DashboardPage() {
  const [open, setOpen] = useState(false);
  const [loadingOverlayVisible, setLoadingOverlayVisible] = useState(false);

  const { refreshSimTime, loading: simTimeLoading } = useSimTime();

  const generalApi = new GeneralInfosApi(defaultConfig);
  const { data: news, mutate: fetchNews } = useMutation<News[], Error>({
    mutationFn: () => generalApi.getNewsGeneralInfosNewsGet(),
    onSuccess: () => {
      setLoadingOverlayVisible(false);
    },
  });

  const simDataApi = new SimDataApi(defaultConfig);
  const { mutate: progressSimulation } = useMutation({
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
      <PageTitleCard title="Blob Championship System - Dashboard" />
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">Date</Typography>
            <SimTimeDisplay />
          </Box>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">News</Typography>
            {news
              ? news.map((newsItem, index) => (
                  <Box key={index} display="flex" flexDirection="column" gap={1}>
                    <Typography variant="body1">{getNewsText(newsItem)}</Typography>
                  </Box>
                ))
              : 'Loading...'}
          </Box>
        </CardContent>
      </Card>
      <Box display="flex" gap={1}>
        {newsTypes.includes(NewsType.Event) && (
          <Button
            variant="contained"
            color="primary"
            endIcon={<Stadium />}
            onClick={() => (window.location.href = '/event')}
          >
            Proceed to event
          </Button>
        )}
        {newsTypes.includes(NewsType.BlobCreated) && (
          <Button variant="contained" color="primary" endIcon={<AddCircle />} onClick={() => setOpen(true)}>
            Create new Blob
          </Button>
        )}
        {(newsTypes.includes(NewsType.Continue) ||
          newsTypes.includes(NewsType.EventEnded) ||
          newsTypes.includes(NewsType.BlobCreatedAndNamed) ||
          newsTypes.includes(NewsType.SeasonStart)) && (
          <Button variant="contained" color="primary" endIcon={<SkipNext />} onClick={handleProgressClick}>
            Proceed to next day
          </Button>
        )}
      </Box>
      {/* TODO: handle blob with parent creation */}
      <BlobNamingDialog open={open} onClose={handleDialogClose} mode="create" />
      {(loadingOverlayVisible || simTimeLoading) && <LoadingOverlay />}
    </PageFrame>
  );
}
