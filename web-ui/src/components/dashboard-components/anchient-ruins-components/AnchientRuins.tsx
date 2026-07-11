import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import OptionCard from '../OptionCard';
import Flood from '@mui/icons-material/Flood';
import AnchientRuinsModal from './AnchientRuinsModal';

const AnchientRuins = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);

  return (
    <>
      <OptionCard title={t('dashboard.options.anchient_ruins')} icon={Flood} onClick={() => setOpen(true)} />
      <AnchientRuinsModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default AnchientRuins;
