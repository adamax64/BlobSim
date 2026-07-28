import { useTranslation } from 'react-i18next';
import { ActivityTypeDbo, BlobsApi, BlobStatsDto } from '../../../../generated';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { useEffect } from 'react';
import { Dialog, DialogContent, Divider, Typography } from '@mui/material';
import DialogTitleWithCloseButton from '../../common/DialogTitleWithCloseButton';
import SkeletonContent from '../SkeletonContent';
import BlobGrid from '../blob-grid/BlobGrid';

type MaintenanceModalProps = {
  open: boolean;
  onClose: () => void;
};

const MaintenanceModal = ({ open, onClose }: MaintenanceModalProps) => {
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
          activities: [ActivityTypeDbo.Maintenance],
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
      <DialogTitleWithCloseButton title={t('maintenance.title')} onClose={onClose} />
      {isPending && <SkeletonContent />}
      {blobs && blobs.length > 0 && (
        <>
          <Divider />
          <DialogContent>
            <Typography mb={2}>{t('maintenance.subtitle')}</Typography>
            <BlobGrid blobs={blobs} />
          </DialogContent>
        </>
      )}
      {!blobs?.length && !isPending && (
        <>
          <Divider />
          <DialogContent>
            <Typography>{t('maintenance.empty')}</Typography>
          </DialogContent>
        </>
      )}
    </Dialog>
  );
};

export default MaintenanceModal;
