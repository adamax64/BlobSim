import AccountBalance from '@mui/icons-material/AccountBalance';
import OptionCard from '../OptionCard';
import { useState } from 'react';
import AdministrationModal from './AdministrationModal';
import { useTranslation } from 'react-i18next';

const Administration = () => {
  const {t} = useTranslation()
  const [open, setOpen] = useState(false);

  return (
    <>
      <OptionCard title={t('dashboard.options.administration')} icon={AccountBalance} onClick={() => setOpen(true)} />
      <AdministrationModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default Administration;
