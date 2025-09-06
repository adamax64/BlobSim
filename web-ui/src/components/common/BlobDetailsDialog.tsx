import {
  Dialog,
  DialogTitle,
  DialogContent,
  Box,
  Typography,
  IconButton,
  Divider,
  Tooltip,
  Paper,
  Grid2,
} from '@mui/material';
import { Cake, Close, Handyman, Speed, Star } from '@mui/icons-material';
import { BlobIcon } from '../icons/BlobIcon';
import { BlobStatsDto } from '../../../generated';
import { IconName } from './IconName';
import { useTranslation } from 'react-i18next';
import { getContrastYIQ } from '../../utils/Colorutils';
import { DeadBlobIcon } from '../icons/DeadBlobIcon';

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
          {blob.isDead ? <DeadBlobIcon size={180} color={blob.color} /> : <BlobIcon size={180} color={blob.color} />}
          <Box display="flex" flexDirection="column" gap={2} width="100%">
            <Grid2 container spacing={2} width="100%">
              <Grid2 size={6}>
                <Tooltip title={t('blob_details.birthdate')} placement="top">
                  <Box display="flex" width="fit-content" gap={1}>
                    <Cake />
                    <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                      {blob.born}
                    </Typography>
                  </Box>
                </Tooltip>
              </Grid2>
              {!blob.isDead && (
                <>
                  <Grid2 size={6}>
                    <Tooltip title={t('blob_details.stats.integrity')} placement="top">
                      <Box display="flex" gap={1}>
                        <Handyman />
                        <Paper sx={{ backgroundColor: blob.integrityColor, padding: '0px 16px' }}>
                          <Typography
                            variant="body1"
                            color={getContrastYIQ(blob.integrityColor!)}
                            sx={{ transform: 'translateY(1px)' }}
                          >
                            {t(`enums.integrity_state.${blob.integrityState}`)}
                          </Typography>
                        </Paper>
                      </Box>
                    </Tooltip>
                  </Grid2>
                  <Grid2 size={6}>
                    <Tooltip title={t('blob_details.stats.strength')} placement="top">
                      <Box display="flex" gap={1}>
                        <Star />
                        <Paper sx={{ backgroundColor: blob.strengthColor, padding: '0px 16px' }}>
                          <Typography
                            variant="body1"
                            color={getContrastYIQ(blob.strengthColor!)}
                            sx={{ transform: 'translateY(1px)' }}
                          >
                            {t(`enums.strength_category.${blob.strengthCategory}`)}
                          </Typography>
                        </Paper>
                      </Box>
                    </Tooltip>
                  </Grid2>
                  <Grid2 size={6}>
                    <Tooltip title={t('blob_details.stats.speed')} placement="top">
                      <Box display="flex" gap={1}>
                        <Speed />
                        <Paper sx={{ backgroundColor: blob.speedColor, padding: '0px 16px' }}>
                          <Typography
                            variant="body1"
                            color={getContrastYIQ(blob.speedColor!)}
                            sx={{ transform: 'translateY(1px)' }}
                          >
                            {t(`enums.speed_category.${blob.speedCategory}`)}
                          </Typography>
                        </Paper>
                      </Box>
                    </Tooltip>
                  </Grid2>
                </>
              )}
              {blob.isDead && (
                <Grid2 size={6}>
                  <Tooltip title={t('blob_details.terminated')} placement="top">
                    <Box display="flex" gap={1}>
                      <Handyman />
                      <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                        {blob.terminated}
                      </Typography>
                    </Box>
                  </Tooltip>
                </Grid2>
              )}
              {blob.debut && (
                <Grid2 size={6}>
                  <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                    <strong>{t('blob_details.debut')}</strong>: {blob.debut}
                  </Typography>
                </Grid2>
              )}
              {blob.isRetired && (
                <Grid2 size={6}>
                  <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                    <strong>{t('blob_details.retired')}</strong>: {blob.contract}
                  </Typography>
                </Grid2>
              )}
              {!blob.isDead && (
                <Grid2 size={6}>
                  <Typography variant="body1">
                    <strong>{t('blob_details.money')}:</strong> {blob.money}
                  </Typography>
                </Grid2>
              )}
            </Grid2>

            {blob.parent && (
              <Typography variant="body1" component="div">
                <strong>{t('blob_details.parent')}:</strong>{' '}
                <IconName name={blob.parent.name} color={blob.parent.color} size={24} />
              </Typography>
            )}

            {!!blob.debut ? (
              !blob.isRetired && (
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
