import { useTranslation } from 'react-i18next';
import OptionCard from '../OptionCard';
import { useState } from 'react';
import Newspaper from '@mui/icons-material/Newspaper';
import { NewsModal } from './NewsModal';

const News = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);

  return (
    <>
      <OptionCard title={t('dashboard.news')} icon={Newspaper} onClick={() => setOpen(true)} />
      <NewsModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default News;
