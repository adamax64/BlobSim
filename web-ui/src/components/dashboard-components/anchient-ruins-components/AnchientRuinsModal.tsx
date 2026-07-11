import { useTranslation } from 'react-i18next';
import { ActivityTypeDbo, BlobsApi, BlobStatsDto } from '../../../../generated';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { useEffect } from 'react';
import { Dialog, DialogContent, Divider, Typography } from '@mui/material';
import DialogTitleWithCloseButton from '../../common/DialogTitleWithCloseButton';
import SkeletonContent from '../SkeletonContent';
import BlobGrid from '../blob-grid/BlobGrid';

type AnchientRuinsModalProps = {
  open: boolean;
  onClose: () => void;
};

const AnchientRuinsModal = ({ open, onClose }: AnchientRuinsModalProps) => {
  const { t } = useTranslation();
  const blobsApi = new BlobsApi(defaultConfig);
  const {
    mutate: fetchBlobs,
    data: blobs,
    isPending,
  } = useMutation<BlobStatsDto[]>({
    mutationFn: () =>
      blobsApi.getByActivitiesBlobsBlobsByActivitiesPost({
        blobsByActivityRequestDto: {
          activities: [ActivityTypeDbo.Adventure],
        },
      }),
  });

  useEffect(() => {
    if (open) {
      fetchBlobs();
    }
  }, [fetchBlobs, open]);

  return (
    <Dialog fullWidth maxWidth="md" open={open} onClose={onClose}>
      <DialogTitleWithCloseButton title={t('anchient_ruins.title')} onClose={onClose} />
      {isPending && <SkeletonContent />}
      {blobs && blobs.length > 0 && (
        <>
          <Divider />
          <DialogContent>
            <Typography mb={2}>{t('anchient_ruins.subtitle')}</Typography>
            <BlobGrid blobs={blobs} />
          </DialogContent>
        </>
      )}
      {!blobs?.length && !isPending && (
        <>
          <Divider />
          <DialogContent>
            <Typography>{t('anchient_ruins.empty')}</Typography>
          </DialogContent>
        </>
      )}
    </Dialog>
  );
};

export default AnchientRuinsModal;
