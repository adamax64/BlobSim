import { useTranslation } from 'react-i18next';
import OptionCard from '../OptionCard';
import FitnessCenter from '@mui/icons-material/FitnessCenter';
import { useState } from 'react';
import GymModal from './GymModal';

const Gym = () => {
  const { t } = useTranslation();

  const [open, setOpen] = useState(false);

  return (
    <>
      <OptionCard title={t('dashboard.options.gym')} icon={FitnessCenter} onClick={() => setOpen(true)} />
      <GymModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default Gym;
