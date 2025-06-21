import { Dialog, DialogTitle, DialogContent, Box, Typography, IconButton, Divider } from '@mui/material';
import { Close } from '@mui/icons-material';
import { BlobIcon } from '../icons/BlobIcon';
import { BlobStatsDto } from '../../../generated';
import { IconName } from './IconName';
import { useTranslation } from 'react-i18next';

interface BlobDetailsDialogProps {
  open: boolean;
  onClose: () => void;
  blob: BlobStatsDto;
}

export function BlobDetailsDialog({ open, onClose, blob }: BlobDetailsDialogProps) {
  const { t } = useTranslation();
  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {blob.name}
        <IconButton onClick={onClose} size="small">
          <Close />
        </IconButton>
      </DialogTitle>
      <Divider />
      <DialogContent>
        <Box display="flex" flexDirection="column" alignItems="center" gap={3}>
          <BlobIcon size={180} color={blob.color} />

          <Box display="flex" flexDirection="column" gap={2} width="100%">
            <Typography variant="body1">
              <strong>{t('blob_details.birthdate')}:</strong> {blob.born}
            </Typography>

            {blob.parent && (
              <Typography variant="body1" component="div">
                <strong>{t('blob_details.parent')}:</strong>{' '}
                <IconName name={blob.parent.name} color={blob.parent.color} size={24} />
              </Typography>
            )}

            {blob.debut && (
              <Typography variant="body1">
                <strong>{t('blob_details.debut')}:</strong> {blob.debut}
              </Typography>
            )}

            {!!blob.debut ? (
              blob.isRetired ? (
                blob.isDead ? (
                  <Typography variant="body1">{t('blob_details.terminated')}</Typography>
                ) : (
                  <Typography variant="body1">{t('blob_details.retired')}</Typography>
                )
              ) : (
                <Typography variant="body1">
                  <strong>{t('blob_details.current_league')}:</strong> {blob.leagueName}
                </Typography>
              )
            ) : (
              <Typography variant="body1">{t('blob_details.on_queue')}</Typography>
            )}

            {blob.podiums > 0 && (
              <Typography variant="body1">
                <strong>{t('blob_details.podiums')}:</strong> {blob.podiums}
              </Typography>
            )}

            {blob.wins > 0 && (
              <Typography variant="body1">
                <strong>{t('blob_details.wins')}:</strong> {blob.wins}
              </Typography>
            )}

            {blob.championships > 0 && (
              <Typography variant="body1">
                <strong>{t('blob_details.championships')}:</strong> {blob.championships}
              </Typography>
            )}

            {blob.grandmasters > 0 && (
              <Typography variant="body1">
                <strong>{t('blob_details.grandmasters')}:</strong> {blob.grandmasters}
              </Typography>
            )}
          </Box>
        </Box>
      </DialogContent>
    </Dialog>
  );
}
