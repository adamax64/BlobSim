import { NewsApi, NewsDto, NewsType } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { useCallback, useEffect, useState } from 'react';
import { NewsCard } from './NewsCard';
import { ProgressButton } from './ProgressButton';

export const NewsAndActions = () => {
  const [canContinue, setCanContinue] = useState(false);
  const [loadingSkeletonVisible, setLoadingSkeletonVisible] = useState(false);

  const newsApi = new NewsApi(defaultConfig);

  const { data: news, mutate } = useMutation<NewsDto[], Error>({
    mutationFn: () => newsApi.getNewsNewsGet(),
    onSuccess: () => {
      setLoadingSkeletonVisible(false);
    },
  });

  const fetchNews = useCallback(() => {
    setLoadingSkeletonVisible(true);
    mutate();
  }, [mutate]);

  // Fetch news on mount
  useEffect(() => {
    fetchNews();
  }, []);

  useEffect(() => {
    const isBlobInCreation = news?.some((entry) => entry.type === NewsType.BlobInCreation) ?? false;
    const isEventStarting =
      news?.some((entry) => entry.type === NewsType.EventStarted || entry.type === NewsType.OngoingEvent) ?? false;

    setCanContinue(!isBlobInCreation && !isEventStarting);
  }, [news]);

  return (
    <>
      <NewsCard news={news} loadingSkeletonVisible={loadingSkeletonVisible} fetchNews={fetchNews} />
      {canContinue ? (
        <ProgressButton
          fetchNews={fetchNews}
          setLoadingSkeletonVisible={setLoadingSkeletonVisible}
          isLoadingNews={loadingSkeletonVisible}
        />
      ) : null}
    </>
  );
};
