import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import OptionCard from '../OptionCard';
import Warehouse from '@mui/icons-material/Warehouse';
import MineModal from './MineModal';

const Mine = () => {
  const { t } = useTranslation();

  const [open, setOpen] = useState(false);

  return (
    <>
      <OptionCard title={t('dashboard.options.mine')} icon={Warehouse} onClick={() => setOpen(true)} />
      <MineModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default Mine;
