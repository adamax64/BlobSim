import { Box, Dialog, DialogContent, Divider, Typography } from '@mui/material';
import { BlobsApi, BlobStatsDto, ResponseError } from '../../../../generated';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import PoliciesPanel from './PoliciesPanel';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import DialogTitleWithCloseButton from '../../common/DialogTitleWithCloseButton';
import BlobAnimatedWithName from '../BlobAnimatedWithName';
import { useSimTime } from '../../../context/SimTimeContext';

type AdministrationModalProps = {
  open: boolean;
  onClose: () => void;
};

const AdministrationModal = ({ open, onClose }: AdministrationModalProps) => {
  const { t } = useTranslation();
  const { simTime } = useSimTime();

  const blobsApi = new BlobsApi(defaultConfig);
  const { data: grandmaster, mutate: fetchGrandmaster } = useMutation<BlobStatsDto, ResponseError>({
    mutationFn: () => blobsApi.getGrandmasterBlobsGrandmasterGet(),
  });

  useEffect(() => {
    if (simTime) {
      fetchGrandmaster();
    }
  }, [simTime, fetchGrandmaster]);

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitleWithCloseButton title={t('administration.title')} onClose={onClose} />
      <Divider />
      <DialogContent>
        <Typography variant="body1" align="center" pb={1}>
          {t('administration.grandmaster')}
        </Typography>
        <Box display="flex" justifyContent="center">
          {grandmaster && <BlobAnimatedWithName blob={grandmaster} />}
        </Box>
      </DialogContent>
      <Divider />
      <DialogContent>
        <Typography variant="h6" pb={1}>
          {t('policies.title')}
        </Typography>
        <PoliciesPanel />
      </DialogContent>
    </Dialog>
  );
};

export default AdministrationModal;
