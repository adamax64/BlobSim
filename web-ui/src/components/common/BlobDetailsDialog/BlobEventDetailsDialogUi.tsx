import { Dialog, Divider } from '@mui/material';
import { BlobStatsDto, StandingsSnippetDto, Element } from '../../../../generated';
import { useTranslation } from 'react-i18next';
import LoadingDialogContent from './LoadingDialogContent/LoadingDialogContent';
import { BlobAnimated } from '../blob-visuals/BlobAnimated';
import BlobDetailsDialogContent from './BlobDetailsDialogContent/BlobDetailsDialogContent';
import DialogTitleWithCloseButton from '../DialogTitleWithCloseButton';
import ElementIcon from './BlobDetailsDialogContent/ElementIcon';

interface BlobEventDetailsDialogUiProps {
  open: boolean;
  onClose: () => void;
  blob?: BlobStatsDto;
  standingsData?: StandingsSnippetDto[];
}

export const BlobEventDetailsDialogUi = ({ open, onClose, blob, standingsData }: BlobEventDetailsDialogUiProps) => {
  const { t } = useTranslation();

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitleWithCloseButton
        title={blob?.name ?? t('blob_details.loading')}
        elementIcon={blob?.element && blob.element !== Element.None && <ElementIcon element={blob.element} />}
        onClose={onClose}
      />
      <Divider />
      {blob ? (
        <BlobDetailsDialogContent
          blob={blob}
          blobIcon={<BlobAnimated blob={blob} size={180} />}
          includeMoney={false}
          includeCurrentLeague={false}
          includeCurrentActivity={false}
          includeInventory={false}
          standingsData={standingsData}
        />
      ) : (
        <LoadingDialogContent />
      )}
    </Dialog>
  );
};
