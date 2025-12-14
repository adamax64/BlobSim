import { Box, Card, CardContent, Divider, Grid, Skeleton, Typography } from '@mui/material';
import { NewsDto } from '../../../generated';
import { NewsContent } from './NewsContent';
import { useTranslation } from 'react-i18next';
import { formatToShort } from '../../utils/sim-time-utils';

type NewsCardProps = {
  news: NewsDto[] | undefined;
  loadingSkeletonVisible: boolean;
};

export const NewsCard = ({ news, loadingSkeletonVisible }: NewsCardProps) => {
  const { t } = useTranslation();

  return (
    <Card>
      <CardContent>
        <Box display="flex" flexDirection="column" gap={1.5}>
          <Typography variant="h6">{t('dashboard.news')}</Typography>
          <Box sx={{ height: 'calc(100vh - 384px)', overflowY: 'auto' }}>
            <Grid container>
              {loadingSkeletonVisible ? (
                <NewsCardSkeleton />
              ) : news ? (
                news.map((newsItem, index) => (
                  <Grid key={index} size={12} container spacing={2}>
                    <Grid size={{ xs: 3, lg: 2, xl: 1 }} sx={{ paddingY: 1.5 }}>
                      <Typography variant="body1" textAlign="end" fontWeight="bold">
                        {formatToShort(newsItem.date)}
                      </Typography>
                    </Grid>
                    <Divider orientation="vertical" />
                    <Grid size={{ xs: 8, lg: 9, xl: 10 }} sx={{ paddingY: 1.5 }}>
                      <NewsContent newsItem={newsItem} />
                    </Grid>
                  </Grid>
                ))
              ) : (
                <NewsCardSkeleton />
              )}
            </Grid>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

const NewsCardSkeleton = () => {
  return Array.from({ length: 3 }).map((_, index) => (
    <Grid key={index} size={12} container spacing={2}>
      <Grid size={{ xs: 3, lg: 2, xl: 1 }} sx={{ paddingY: 1.5 }}>
        <Skeleton variant="rounded" height={24} />
      </Grid>
      <Divider orientation="vertical" />
      <Grid size={{ xs: 8, lg: 9, xl: 10 }} sx={{ paddingY: 1.5 }}>
        <Skeleton variant="rounded" height={120} width="80%" />
      </Grid>
    </Grid>
  ));
};
