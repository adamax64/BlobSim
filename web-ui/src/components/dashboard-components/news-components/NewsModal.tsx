import { Box, Dialog, DialogContent, Divider, Grid, Skeleton, Typography } from '@mui/material';
import { NewsContent } from './NewsContent';
import { useTranslation } from 'react-i18next';
import { formatToShort } from '../../../utils/sim-time-utils';
import { useNews } from '../../../context/NewsContext';
import DialogTitleWithCloseButton from '../../common/DialogTitleWithCloseButton';

type NewsModalProps = {
  open: boolean;
  onClose: () => void;
};

export const NewsModal = ({ open, onClose }: NewsModalProps) => {
  const { t } = useTranslation();
  const { news, newsLoading: loadingSkeletonVisible } = useNews();

  return (
    <Dialog maxWidth="md" open={open} onClose={onClose}>
      <DialogTitleWithCloseButton title={t('dashboard.news')} onClose={onClose} />
      <Divider />
      <DialogContent>
        <Box display="flex" flexDirection="column" gap={1.5}>
          <Box sx={{ overflowY: 'auto' }}>
            <Grid container>
              {loadingSkeletonVisible ? (
                <NewsCardSkeleton />
              ) : news ? (
                news.map((newsItem, index) => (
                  <Grid key={index} size={12} container spacing={2}>
                    <Grid size={{ xs: 3, md: 2, xl: 2 }} sx={{ paddingY: 1.5 }}>
                      <Typography variant="body1" textAlign="end" fontWeight="bold">
                        {formatToShort(newsItem.date)}
                      </Typography>
                    </Grid>
                    <Divider orientation="vertical" />
                    <Grid size={{ xs: 8, md: 9, xl: 9 }} sx={{ paddingY: 1.5 }}>
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
      </DialogContent>
    </Dialog>
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
