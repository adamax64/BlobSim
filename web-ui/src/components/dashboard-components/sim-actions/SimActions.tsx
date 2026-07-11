import { useMutation } from '@tanstack/react-query';
import { NewsType, ResponseError, SimDataApi } from '../../../../generated';
import { useNews } from '../../../context/NewsContext';
import defaultConfig from '../../../default-config';
import { useAuth } from '../../../context/AuthContext';
import { useEffect, useMemo } from 'react';
import { ProgressButton } from '../ProgressButton';
import { Slide, Snackbar } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { SimActionButton } from './SimActionButton';

const SimActions = () => {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();
  const { news, newsLoading, refreshNews } = useNews();

  const simDataApi = new SimDataApi(defaultConfig);
  const { data: canProgress, mutate: getCanProgress } = useMutation<boolean, ResponseError>({
    mutationFn: () => simDataApi.canProgressSimDataCanProgressGet(),
  });

  useEffect(() => {
    if (!news) {
      refreshNews();
    }
    if (isAuthenticated) {
      getCanProgress();
    }
  }, [news, refreshNews, isAuthenticated]);

  const latestNews = news?.at(0);

  const isEventToday =
    latestNews && (latestNews.type === NewsType.EventStarted || latestNews.type === NewsType.OngoingEvent);

  const isBlobInCreation = latestNews && latestNews.type === NewsType.BlobInCreation;

  const canContinue = canProgress && isAuthenticated;

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
