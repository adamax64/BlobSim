import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import OptionCard from '../OptionCard';
import Build from '@mui/icons-material/Build';
import MaintenanceModal from './MaintenanceModal';

const Maintenance = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);

  return (
    <>
      <OptionCard title={t('dashboard.options.maintenance')} icon={Build} onClick={() => setOpen(true)} />
      <MaintenanceModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default Maintenance;
