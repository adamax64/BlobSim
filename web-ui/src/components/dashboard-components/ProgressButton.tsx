import { Fab } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { Dispatch, SetStateAction } from 'react';
import { useMutation } from '@tanstack/react-query';
import { SimDataApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { useSimTime } from '../../context/SimTimeContext';
import { useAuth } from '../../context/AuthContext';
import SkipNext from '@mui/icons-material/SkipNext';
import { usePolicies } from '../../context/PoliciesContext';

type ProgressButtonProps = {
  fetchNews: () => void;
  setLoadingSkeletonVisible: Dispatch<SetStateAction<boolean>>;
  isLoadingNews: boolean;
};

export const ProgressButton = ({ fetchNews, setLoadingSkeletonVisible, isLoadingNews }: ProgressButtonProps) => {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();
  const { refreshSimTime } = useSimTime();
  const { refreshPolicies } = usePolicies();

  const simDataApi = new SimDataApi(defaultConfig);

  const { mutate: progressSimulation, isPending: isProgressingSimulation } = useMutation({
    mutationFn: () => simDataApi.progressSimDataSimulatePost(),
    onSuccess: () => {
      fetchNews();
      refreshSimTime();
      refreshPolicies();
    },
  });

  const handleProgressClick = () => {
    setLoadingSkeletonVisible(true);
    progressSimulation();
  };

  return (
    <>
      {isAuthenticated && (
        <Fab
          sx={{ position: 'fixed', bottom: 0, right: 0, margin: 2, zIndex: 1000 }}
          variant="extended"
          color="primary"
          size="small"
          onClick={handleProgressClick}
          disabled={isLoadingNews || isProgressingSimulation}
        >
          {t('dashboard.proceed_to_next_day')}
          <SkipNext />
        </Fab>
      )}
    </>
  );
};
