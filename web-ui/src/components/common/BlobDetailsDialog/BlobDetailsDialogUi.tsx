import { Dialog, Divider } from '@mui/material';
import { BlobStatsDto } from '../../../../generated';
import { useTranslation } from 'react-i18next';
import { BlobAnimated } from '../blob-visuals/BlobAnimated';
import BlobDetailsDialogContent from './BlobDetailsDialogContent/BlobDetailsDialogContent';
import LoadingDialogContent from './LoadingDialogContent/LoadingDialogContent';
import DialogTitleWithCloseButton from '../DialogTitleWithCloseButton';
interface BlobDetailsDialogUiProps {
  open: boolean;
  onClose: () => void;
  blob?: BlobStatsDto;
}

export const BlobDetailsDialogUi = ({ open, onClose, blob }: BlobDetailsDialogUiProps) => {
  const { t } = useTranslation();

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitleWithCloseButton title={blob?.name ?? t('blob_details.loading')} onClose={onClose} />
      <Divider />
      {blob ? (
        <BlobDetailsDialogContent blob={blob} blobIcon={<BlobAnimated blob={blob} size={180} />} />
      ) : (
        <LoadingDialogContent />
      )}
    </Dialog>
  );
};
