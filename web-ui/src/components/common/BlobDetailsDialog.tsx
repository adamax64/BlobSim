import { Dialog, DialogTitle, DialogContent, Box, Typography, IconButton } from '@mui/material';
import { Close } from '@mui/icons-material';
import { BlobIcon } from '../icons/BlobIcon';
import { BlobStatsDto } from '../../../generated';

interface BlobDetailsDialogProps {
  open: boolean;
  onClose: () => void;
  blob: BlobStatsDto;
}

export function BlobDetailsDialog({ open, onClose, blob }: BlobDetailsDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {blob.name}
        <IconButton onClick={onClose} size="small">
          <Close />
        </IconButton>
      </DialogTitle>
      <DialogContent>
        <Box display="flex" flexDirection="column" alignItems="center" gap={3}>
          <BlobIcon size={180} color={blob.color} />
          
          <Box display="flex" flexDirection="column" gap={2} width="100%">
            <Typography variant="body1">
              <strong>Birthdate:</strong> {blob.born}
            </Typography>
            
            {blob.debut && (
              <Typography variant="body1">
                <strong>Debut:</strong> {blob.debut}
              </Typography>
            )}
            
            {!!blob.debut ? blob.isRetired ? blob.isDead ?
            (
                <Typography variant="body1">
                    Blob is terminated
                </Typography>
            ) : (
                <Typography variant="body1">
                    Blob is retired
                </Typography>
            ) : (
            <Typography variant="body1">
              <strong>Current League:</strong> {blob.leagueName}
            </Typography>
            ) : (
                <Typography variant="body1">
                    Currently on queue
                </Typography>
            )}
            
            {blob.podiums > 0 && (
              <Typography variant="body1">
                <strong>Podiums:</strong> {blob.podiums}
              </Typography>
            )}
            
            {blob.wins > 0 && (
              <Typography variant="body1">
                <strong>Wins:</strong> {blob.wins}
              </Typography>
            )}
            
            {blob.championships > 0 && (
              <Typography variant="body1">
                <strong>Championships:</strong> {blob.championships}
              </Typography>
            )}
            
            {blob.grandmasters > 0 && (
              <Typography variant="body1">
                <strong>Grandmasters:</strong> {blob.grandmasters}
              </Typography>
            )}
          </Box>
        </Box>
      </DialogContent>
    </Dialog>
  );
}
