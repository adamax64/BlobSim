import { useNews } from '../../../context/NewsContext';
import { useEffect } from 'react';
import { useCanContinue } from '../../../hooks/useCanContinue';
import { ProgressButton } from '../ProgressButton';
import { Slide, Snackbar } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { SimActionButton } from './SimActionButton';

const SimActions = () => {
  const { t } = useTranslation();
  const { news, newsLoading, refreshNews } = useNews();

  const { canContinue, isEventToday, isBlobInCreation } = useCanContinue();

  useEffect(() => {
    if (!news && !newsLoading) {
      refreshNews();
    }
  }, [news, newsLoading, refreshNews]);

  const latestNews = news?.at(0);

  return (
    <>
      <Snackbar
        open={isEventToday || isBlobInCreation}
        message={t(`enums.news_type.${latestNews?.type}`, {
          leagueName: latestNews?.leagueName,
          round: latestNews?.round,
          eventType: t(`enums.event_types.${latestNews?.eventType}`),
        })}
        slots={{ transition: (props) => <Slide {...props} direction="left" /> }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        action={<SimActionButton newsItem={latestNews} fetchNews={refreshNews} />}
      />
      {canContinue && <ProgressButton fetchNews={refreshNews} isLoadingNews={newsLoading} />}
    </>
  );
};

export default SimActions;
