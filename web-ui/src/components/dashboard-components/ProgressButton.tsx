import { Fab } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useMutation } from '@tanstack/react-query';
import { SimDataApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { useSimTime } from '../../context/SimTimeContext';
import SkipNext from '@mui/icons-material/SkipNext';
import { usePolicies } from '../../context/PoliciesContext';

type ProgressButtonProps = {
  fetchNews: () => void;
  isLoadingNews: boolean;
};

export const ProgressButton = ({ fetchNews, isLoadingNews }: ProgressButtonProps) => {
  const { t } = useTranslation();
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
    progressSimulation();
  };

  return (
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
  );
};
