import { Badge, Box, Card, CardContent, Grid, Typography } from '@mui/material';
import { BlobStatsDto } from '../../../generated';
import { BlobState } from '../../utils/blob-state-utils';
import { BlobIcon } from '../icons/BlobIcon';
import { useTranslation } from 'react-i18next';
import { BlobStateBadge } from '../common/BlobStateBadge';

interface BlobsMobileCardsProps {
  blobs: BlobStatsDto[] | undefined;
  onBlobSelect: (blob: BlobStatsDto) => void;
}

export function BlobsMobileCards({ blobs, onBlobSelect }: BlobsMobileCardsProps) {
  const { t } = useTranslation();

  const getCardClass = (blob: BlobStatsDto) => {
    if (blob.isDead) {
      return BlobState.DEAD;
    }
    if (blob.isRetired) {
      return BlobState.RETIRED;
    }
    return '';
  };

  return (
    <Box sx={{ p: 2 }}>
      <Grid container spacing={2}>
        {blobs?.map((blob) => (
          <Grid item xs={12} key={blob.name}>
            <Card
              onClick={() => onBlobSelect(blob)}
              sx={{
                cursor: 'pointer',
                '&:hover': {
                  boxShadow: 3,
                  transform: 'scale(1.01)',
                  transition: 'transform 0.2s ease-in-out',
                },
              }}
            >
              <CardContent className={getCardClass(blob)}>
                <Box display="flex" alignItems="center" gap={2}>
                  <Box paddingX={1}>
                    <BlobIcon size={72} color={blob.color} />
                  </Box>
                  <Box>
                    <BlobStateBadge atRisk={blob.atRisk} isRookie={blob.isRookie} size="medium">
                      <Typography variant="h6" component="div">
                        {blob.name}
                      </Typography>
                    </BlobStateBadge>
                    <Typography variant="body2" color="text.secondary">
                      {t('blobs_grid.born')}: {blob.born}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {t('blobs_grid.league')}: {blob.leagueName}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
