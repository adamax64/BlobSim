import { AppBar, Box, Button, Toolbar } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { BlobNamingDialog } from '../common/BlobNamingDialog';
import { useNavigate } from '@tanstack/react-router';
import { Dispatch, SetStateAction, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { SimDataApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { useSimTime } from '../../context/SimTimeContext';
import { useAuth } from '../../context/AuthContext';
import Stadium from '@mui/icons-material/Stadium';
import AddCircle from '@mui/icons-material/AddCircle';
import SkipNext from '@mui/icons-material/SkipNext';
import { usePolicies } from '../../context/PoliciesContext';

type ControlButtonsFooterProps = {
  fetchNews: () => void;
  setLoadingSkeletonVisible: Dispatch<SetStateAction<boolean>>;
  isLoadingNews: boolean;
  canCreateBlob: boolean;
  canStartEvent: boolean;
  canContinue: boolean;
};

export const ControlButtonsFooter = ({
  fetchNews,
  setLoadingSkeletonVisible,
  isLoadingNews,
  canCreateBlob,
  canStartEvent,
  canContinue,
}: ControlButtonsFooterProps) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { refreshSimTime } = useSimTime();
  const { refreshPolicies } = usePolicies();

  const [open, setOpen] = useState(false);

  const simDataApi = new SimDataApi(defaultConfig);
  const { mutate: progressSimulation, isPending: isProgressingSimulation } = useMutation({
    mutationFn: () => simDataApi.progressSimDataSimulatePost(),
    onSuccess: () => {
      fetchNews();
      refreshSimTime();
      refreshPolicies();
    },
  });

  const handleDialogClose = (update?: boolean) => {
    setOpen(false);
    if (update) {
      fetchNews();
    }
  };

  const handleProgressClick = () => {
    setLoadingSkeletonVisible(true);
    progressSimulation();
  };

  return (
    <AppBar position="relative" color="default" sx={{ top: 'auto', bottom: 0 }}>
      <Toolbar>
        <Box display="flex" gap={1}>
          {canStartEvent && (
            <Button
              variant="contained"
              color="success"
              endIcon={<Stadium />}
              onClick={() => navigate({ to: '/event' })}
            >
              {t('dashboard.proceed_to_event')}
            </Button>
          )}
          {isAuthenticated && canCreateBlob && (
            <Button variant="contained" color="primary" endIcon={<AddCircle />} onClick={() => setOpen(true)}>
              {t('dashboard.create_new_blob')}
            </Button>
          )}
          {isAuthenticated && canContinue && (
            <Button
              variant="contained"
              color="primary"
              endIcon={<SkipNext />}
              onClick={handleProgressClick}
              disabled={isLoadingNews || isProgressingSimulation}
            >
              {t('dashboard.proceed_to_next_day')}
            </Button>
          )}
        </Box>
      </Toolbar>
      {/* TODO: handle blob with parent creation */}
      <BlobNamingDialog open={open} onClose={handleDialogClose} mode="create" />
    </AppBar>
  );
};
