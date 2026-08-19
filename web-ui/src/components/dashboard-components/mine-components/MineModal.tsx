import { useTranslation } from 'react-i18next';
import { ActivityTypeDbo, BlobsApi, BlobStatsDto, MineWinnerDto, SimDataApi } from '../../../../generated';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import {
  Accordion,
  AccordionDetails,
  Box,
  Dialog,
  DialogContent,
  Divider,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import DialogTitleWithCloseButton from '../../common/DialogTitleWithCloseButton';
import SkeletonContent from '../SkeletonContent';
import BlobGrid from '../blob-grid/BlobGrid';
import MineWinnersTable from './MineWinnersTable';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { SmallAccordionTitle } from '../../common/StyledComponents';

type MineModalProps = {
  open: boolean;
  onClose: () => void;
};

const MineModal = ({ open, onClose }: MineModalProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isTabletOrMobile = useMediaQuery(`${theme.breakpoints.down('md')} or (max-height:600px)`);
  const [winnersExpanded, setWinnersExpanded] = useState<boolean>(true);

  const blobsApi = new BlobsApi(defaultConfig);
  const {
    mutate: fetchBlobs,
    data: blobs,
    isPending,
  } = useMutation<BlobStatsDto[]>({
    mutationFn: () =>
      blobsApi.getByActivitiesBlobsBlobsByActivitiesPost({
        blobsByActivityRequestDto: {
          activities: [ActivityTypeDbo.Mining],
        },
      }),
  });

  const simDataApi = new SimDataApi(defaultConfig);
  const {
    mutate: fetchMineWinners,
    data: mineWinnersData,
    isPending: isWinnersPending,
  } = useMutation<MineWinnerDto[]>({
    mutationFn: async () => {
      const dto = await simDataApi.getMineWinnersEndpointSimDataMineWinnersGet();
      return dto.winners;
    },
  });

  useEffect(() => {
    if (open) {
      fetchBlobs();
      fetchMineWinners();
    }
  }, [fetchBlobs, fetchMineWinners, open]);

  const winners = mineWinnersData ?? [];

  const winnersSection = (
    <>
      {!isTabletOrMobile && (
        <Typography variant="subtitle1" mb={1}>
          {t('mine.winners.title')}
        </Typography>
      )}
      {isWinnersPending && <Typography>{t('mine.winners.loading')}</Typography>}
      {!isWinnersPending && winners.length === 0 && <Typography>{t('mine.winners.empty')}</Typography>}
      {winners.length > 0 && <MineWinnersTable winners={winners} />}
    </>
  );

  const blobsSection = (
    <>
      {isPending && <SkeletonContent />}
      {blobs && blobs.length > 0 && (
        <>
          <Typography mb={2}>{t('mine.subtitle')}</Typography>
          <BlobGrid blobs={blobs} />
        </>
      )}
      {!blobs?.length && !isPending && <Typography>{t('mine.empty')}</Typography>}
    </>
  );

  return (
    <Dialog fullWidth maxWidth="lg" open={open} onClose={onClose}>
      <DialogTitleWithCloseButton title={t('mine.title')} onClose={onClose} />
      <DialogContent sx={{ p: 0 }}>
        {isTabletOrMobile ? (
          <Box>
            <Box mr={2} ml={2}>
              <Accordion expanded={winnersExpanded} onChange={(_, expanded) => setWinnersExpanded(expanded)}>
                <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
                  <Typography>{t('mine.winners.title')}</Typography>
                </SmallAccordionTitle>
                <AccordionDetails>{winnersSection}</AccordionDetails>
              </Accordion>
            </Box>
            <Divider />
            <DialogContent>{blobsSection}</DialogContent>
          </Box>
        ) : (
          <Box display="flex" gap={2} alignItems="flex-start" p={3}>
            <Box flex={2}>{blobsSection}</Box>
            <Divider orientation="vertical" flexItem />
            <Box flex={1} minWidth={260}>
              {winnersSection}
            </Box>
          </Box>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default MineModal;
