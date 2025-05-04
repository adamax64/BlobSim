import { Box, Button, Card, CardContent, Typography } from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import defaultConfig from '../../default-config';
import { GeneralInfosApi, News, NewsType } from '../../../generated';
import { useEffect, useMemo, useState } from 'react';
import { AddCircle, SkipNext, Stadium } from '@mui/icons-material';
import { PageTitleCard } from '../common/PageTitleCard';
import { PageFrame } from '../common/PageFrame';
import { BlobNamingDialog } from '../common/BlobNamingDialog';
import { SimTimeDisplay } from '../common/SimTimeDisplay';

function getNewsText(news: News) {
  switch (news.newsType) {
    case NewsType.Event:
      return 'There is a championship event today!';
    case NewsType.BlobCreatedAndNamed:
      return `A new blob called ${news.additionalInfo} has been created!`;
    case NewsType.BlobCreated:
      return 'A new blob has been created!';
    case NewsType.SeasonStart:
      return 'A new season has started!';
    case NewsType.Continue:
      return 'Nothing special happening today';
  }
}

export function DashboardPage() {
  const [open, setOpen] = useState(false);

  const generalApi = new GeneralInfosApi(defaultConfig);
  const { data: news, mutate: fetchNews } = useMutation<News[], Error>({
    mutationFn: () => generalApi.getNewsGeneralInfosNewsGet(),
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
          <Button variant="contained" color="primary" endIcon={<Stadium />}>
            Proceed to event
          </Button>
        )}
        {newsTypes.includes(NewsType.BlobCreated) && (
          <Button variant="contained" color="primary" endIcon={<AddCircle />} onClick={() => setOpen(true)}>
            Create new Blob
          </Button>
        )}
        {newsTypes.includes(NewsType.Continue) && (
          <Button variant="contained" color="primary" endIcon={<SkipNext />}>
            Proceed to next day
          </Button>
        )}
      </Box>
      <BlobNamingDialog open={open} onClose={handleDialogClose} mode="create" />
    </PageFrame>
  );
}
