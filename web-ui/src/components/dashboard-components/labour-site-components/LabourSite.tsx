import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import OptionCard from '../OptionCard';
import Hardware from '@mui/icons-material/Hardware';
import LabourSiteModal from './LabourSiteModal';

const LabourSite = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);

  return (
    <>
      <OptionCard title={t('dashboard.options.labour_site')} icon={Hardware} onClick={() => setOpen(true)} />
      <LabourSiteModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default LabourSite;
