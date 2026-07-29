import { useTranslation } from 'react-i18next';
import OptionCard from '../OptionCard';
import { useState } from 'react';
import Newspaper from '@mui/icons-material/Newspaper';
import NewReleases from '@mui/icons-material/NewReleases';
import { NewsModal } from './NewsModal';
import { useNews } from '../../../context/NewsContext';

const News = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const { hasUnseenNews } = useNews();

  return (
    <>
      <OptionCard
        title={t('dashboard.news')}
        icon={Newspaper}
        onClick={() => setOpen(true)}
        badge={
          hasUnseenNews && (
            <NewReleases color='warning' fontSize='large' />
          )
        }
      />
      <NewsModal open={open} onClose={() => setOpen(false)} />
    </>
  );
};

export default News;
