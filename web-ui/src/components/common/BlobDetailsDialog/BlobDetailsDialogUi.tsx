import Close from '@mui/icons-material/Close';
import { Dialog, DialogTitle, Divider, IconButton } from '@mui/material';
import { BlobStatsDto } from '../../../../generated';
import { useTranslation } from 'react-i18next';
import { BlobAnimated } from '../blob-visuals/BlobAnimated';
import BlobDetailsDialogContent from './BlobDetailsDialogContent/BlobDetailsDialogContent';
import LoadingDialogContent from './LoadingDialogContent/LoadingDialogContent';
interface BlobDetailsDialogUiProps {
  open: boolean;
  onClose: () => void;
  blob?: BlobStatsDto;
}

export const BlobDetailsDialogUi = ({ open, onClose, blob }: BlobDetailsDialogUiProps) => {
  const { t } = useTranslation();

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {blob?.name ?? t('blob_details.loading')}
        <IconButton onClick={onClose} size="small">
          <Close />
        </IconButton>
      </DialogTitle>
      <Divider />
      {blob ? (
        <BlobDetailsDialogContent blob={blob} blobIcon={<BlobAnimated blob={blob} size={180} />} />
      ) : (
        <LoadingDialogContent />
      )}
    </Dialog>
  );
};
