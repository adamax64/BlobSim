import Cake from '@mui/icons-material/Cake';
import Handyman from '@mui/icons-material/Handyman';
import WarningIcon from '@mui/icons-material/Warning';
import BatteryChargingFull from '@mui/icons-material/BatteryChargingFull';
import CleaningServices from '@mui/icons-material/CleaningServices';
import Cookie from '@mui/icons-material/Cookie';
import Extension from '@mui/icons-material/Extension';
import ChargingStation from '@mui/icons-material/ChargingStation';
import Memory from '@mui/icons-material/Memory';
import SdCard from '@mui/icons-material/SdCard';
import { Box, DialogContent, Grid, Paper, Typography } from '@mui/material';
import RetirementFocusIcon from './RetirementFocusIcon';
import StateIcon from './StateIcon';
import TraitIcon from './TraitIcon';
import { getContrastYIQ } from '../../../../utils/color-utils';
import { useTranslation } from 'react-i18next';
import { BlobStatsDto, StandingsSnippetDto, type ItemType } from '../../../../../generated';
import { IconName } from '../../IconName';
import DynamicTooltip from '../../DynamicTooltip';
import Inventory from './Inventory';
import StandingSnippetWidget from './StandingSnippetWidget';

type BlobDetailsDialogContentProps = {
  blob: BlobStatsDto;
  blobIcon: React.ReactNode;
  includeMoney?: boolean;
  includeCurrentLeague?: boolean;
  includeCurrentActivity?: boolean;
  includeInventory?: boolean;
  standingsData?: StandingsSnippetDto[];
};

const contentEntries = [
  { key: 'grandmasterTitles', value: 'blob_details.grandmaster_titles' },
  { key: 'championships', value: 'blob_details.championships' },
  { key: 'masterWins', value: 'blob_details.master_wins' },
  { key: 'masterPodiums', value: 'blob_details.master_podiums' },
  { key: 'seasonVictories', value: 'blob_details.season_victories' },
  { key: 'lesserWins', value: 'blob_details.lesser_wins' },
  { key: 'lesserPodiums', value: 'blob_details.lesser_podiums' },
] as const;

const BlobDetailsDialogContent = ({
  blob,
  blobIcon,
  includeMoney = true,
  includeCurrentLeague = true,
  includeCurrentActivity = true,
  includeInventory = true,
  standingsData,
}: BlobDetailsDialogContentProps) => {
  const { t } = useTranslation();

  const rankingEntries = contentEntries
    .filter((entry) => {
      const value = blob[entry.key as keyof BlobStatsDto];
      return typeof value === 'number' && value > 0;
    })
    .splice(0, 3) // Limit to 3 entries
    .reverse(); // Reverse to show the lowest ranking first

  const innerGridSize = standingsData ? 6 : 12;
  const innerGridCellSize = standingsData ? 12 : 6;

  return (
    <DialogContent>
      <Box display="flex" flexDirection="column" alignItems="center">
        <Box display="flex" flexDirection="column" alignItems="center" width="100%">
          <Box display="flex" width="100%">
            <Box display="flex" width="100%">
              {blob.states.map((state) => (
                <StateIcon key={state.type} state={state} />
              ))}
            </Box>
            <Box display="flex" width="100%" justifyContent="flex-end">
              {blob.traits.map((trait) => (
                <TraitIcon key={trait} trait={trait} />
              ))}
            </Box>
          </Box>
          {blobIcon}
        </Box>
        <Box display="flex" flexDirection="column" gap={1.5} width="100%">
          {blob.inventory.length > 0 && includeInventory && <Inventory inventory={blob.inventory} />}

          <Grid container spacing={1.5} width="100%">
            <Grid size={6}>
              <DynamicTooltip title={t('blob_details.birthdate')} placement="top">
                <Box display="flex" width="fit-content" gap={1}>
                  <Cake />
                  <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                    {blob.born}
                  </Typography>
                </Box>
              </DynamicTooltip>
            </Grid>
            {!blob.isDead && (
              <>
                <Grid size={6}>
                  <DynamicTooltip title={t('blob_details.stats.integrity')} placement="top">
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
                  </DynamicTooltip>
                </Grid>
              </>
            )}
            {blob.isDead && (
              <Grid size={6}>
                <DynamicTooltip title={t('blob_details.terminated')} placement="top">
                  <Box display="flex" gap={1}>
                    <Handyman />
                    <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                      {blob.terminated}
                    </Typography>
                  </Box>
                </DynamicTooltip>
              </Grid>
            )}
            <Grid container size={innerGridSize} spacing={1.5}>
              {blob.debut && (
                <Grid size={6}>
                  <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                    <strong>{t('blob_details.debut')}</strong>: {blob.debut}
                  </Typography>
                </Grid>
              )}
              {blob.isRetired && (
                <Grid size={innerGridCellSize}>
                  <Typography variant="body1" sx={{ transform: 'translateY(2px)' }}>
                    <strong>{t('blob_details.retired')}</strong>: {blob.contract}
                  </Typography>
                </Grid>
              )}
              {!blob.isDead && includeMoney && (
                <Grid size={innerGridCellSize}>
                  <Typography variant="body1">
                    <strong>{t('blob_details.money')}:</strong> {blob.money}
                  </Typography>
                </Grid>
              )}
              {blob.retirementFocus && (
                <Grid size={innerGridCellSize}>
                  <Box display="flex" gap={1} alignItems="center">
                    <Typography variant="body1">
                      <strong>{t('blob_details.retirement_focus')}:</strong>
                    </Typography>
                    <RetirementFocusIcon retirementFocus={blob.retirementFocus} />
                  </Box>
                </Grid>
              )}
              {blob.parent && (
                <Grid size={12}>
                  <Typography variant="body1" component="div">
                    <strong>{t('blob_details.parent')}:</strong>{' '}
                    <IconName name={blob.parent.name} color={blob.parent.color} size={24} />
                  </Typography>
                </Grid>
              )}

              {!!blob.debut ? (
                !blob.isRetired && (
                  <>
                    {includeCurrentLeague && (
                      <Grid size={12}>
                        <Typography variant="body1">
                          <strong>{t('blob_details.current_league')}:</strong> {blob.leagueName}
                        </Typography>
                      </Grid>
                    )}
                    <Grid size={innerGridCellSize}>
                      <Box display="flex" gap={0.75} alignItems="center">
                        <Typography variant="body1">
                          <strong>{t('blob_details.contract')}:</strong> {blob.contract}
                        </Typography>
                        {blob.atRisk && (
                          <DynamicTooltip title={t('blob_details.contract_ending')}>
                            <WarningIcon fontSize="small" color="warning" />
                          </DynamicTooltip>
                        )}
                      </Box>
                    </Grid>
                    {blob.currentStandingsPosition && !standingsData && (
                      <Grid size={6}>
                        <Typography variant="body1">
                          <strong>{t('blob_details.standings')}:</strong> {blob.currentStandingsPosition}
                        </Typography>
                      </Grid>
                    )}
                  </>
                )
              ) : (
                <Grid size={12}>
                  <Typography variant="body1">{t('blob_details.on_queue')}</Typography>
                </Grid>
              )}
            </Grid>
            {standingsData && (
              <Grid size={6}>
                <StandingSnippetWidget standingsData={standingsData} />
              </Grid>
            )}
          </Grid>

          {rankingEntries.length > 0 && (
            <>
              {rankingEntries.map((entry) => {
                const value = blob[entry.key as keyof BlobStatsDto];
                return (
                  <Typography key={entry.key} variant="body1">
                    <strong>{t(entry.value)}:</strong> {typeof value === 'number' ? value : '-'}
                  </Typography>
                );
              })}
            </>
          )}

          {!blob.isDead && includeCurrentActivity && blob.currentActivity && (
            <Typography variant="body1">
              <strong>{t('blob_details.current_activity')}:</strong> {t(`enums.activity_type.${blob.currentActivity}`)}
            </Typography>
          )}
        </Box>
      </Box>
    </DialogContent>
  );
};

export default BlobDetailsDialogContent;
