import { Dialog, DialogContent, Divider, Skeleton, Typography } from '@mui/material';
import DialogTitleWithCloseButton from '../../common/DialogTitleWithCloseButton';
import { useTranslation } from 'react-i18next';
import { ActivityTypeDbo, BlobsApi, BlobStatsDto, ResponseError } from '../../../../generated';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import SkeletonGrid from '../blob-grid/SkeletonGrid';
import BlobGrid from '../blob-grid/BlobGrid';

type GymModalProps = {
  open: boolean;
  onClose: () => void;
};

const GymModal = ({ open, onClose }: GymModalProps) => {
  const { t } = useTranslation();
  const [catchupTrainees, setCatchupTrainees] = useState<BlobStatsDto[]>([]);
  const [regularTrainees, setRegularTrainees] = useState<BlobStatsDto[]>([]);
  const [premiumTrainees, setPremiumTrainees] = useState<BlobStatsDto[]>([]);

  const blobsApi = new BlobsApi(defaultConfig);
  const {
    mutate: fetchBlobs,
    data,
    isPending,
  } = useMutation<BlobStatsDto[]>({
    mutationFn: () =>
      blobsApi.getByActivitiesBlobsBlobsByActivitiesPost({
        blobsByActivityRequestDto: {
          activities: [
            ActivityTypeDbo.Practice,
            ActivityTypeDbo.PremiumPractice,
            ActivityTypeDbo.IntensePractice,
            ActivityTypeDbo.IntenseTraining,
          ],
        },
      }),
    onSuccess: (data) => {
      setCatchupTrainees(data.filter((blob) => blob.currentActivity === ActivityTypeDbo.IntenseTraining));
      setRegularTrainees(
        data.filter(
          (blob) =>
            blob.currentActivity === ActivityTypeDbo.Practice ||
            blob.currentActivity === ActivityTypeDbo.IntensePractice,
        ),
      );
      setPremiumTrainees(data.filter((blob) => blob.currentActivity === ActivityTypeDbo.PremiumPractice));
    },
  });

  useEffect(() => {
    if (open) {
      fetchBlobs();
    }
  }, [fetchBlobs, open]);

  const noCachedData = !catchupTrainees.length && !regularTrainees.length && !premiumTrainees.length;

  return (
    <Dialog fullWidth maxWidth="md" open={open} onClose={onClose}>
      <DialogTitleWithCloseButton title={t('gym.title')} onClose={onClose} />
      {isPending && noCachedData && <SkeletonContent />}
      {catchupTrainees.length > 0 && (
        <>
          <Divider />
          <DialogContent>
            <Typography mb={2}>{t('gym.catchup_training')}</Typography>
            <BlobGrid blobs={catchupTrainees} />
          </DialogContent>
        </>
      )}
      {regularTrainees.length > 0 && (
        <>
          <Divider />
          <DialogContent>
            <Typography mb={2}>{t('gym.practice')}</Typography>
            <BlobGrid blobs={regularTrainees} />
          </DialogContent>
        </>
      )}
      {premiumTrainees.length > 0 && (
        <>
          <Divider />
          <DialogContent>
            <Typography mb={2}>{t('gym.premium_practice')}</Typography>
            <BlobGrid blobs={premiumTrainees} />
          </DialogContent>
        </>
      )}
      {!data?.length && !isPending && (
        <>
          <Divider />
          <DialogContent>
            <Typography>{t('gym.empty')}</Typography>
          </DialogContent>
        </>
      )}
    </Dialog>
  );
};

const SkeletonContent = () => {
  return (
    <>
      <Divider />
      <DialogContent>
        <Skeleton variant="text" width="100%" sx={{ mb: 2 }} />
        <SkeletonGrid />
      </DialogContent>
    </>
  );
};

export default GymModal;
