import { NewsApi, NewsDto, NewsType } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { Dispatch, SetStateAction, useEffect, useState } from 'react';
import { NewsCard } from './NewsCard';
import { ControlButtonsFooter } from './ControlButtonsFooter';

type NewsAndFooterProps = {
  setLoadingOverlayVisible: Dispatch<SetStateAction<boolean>>;
};

export const NewsAndFooter = ({ setLoadingOverlayVisible }: NewsAndFooterProps) => {
  const [canCreateBlob, setCanCreateBlob] = useState(false);
  const [canStartEvent, setCanStartEvent] = useState(false);
  const [canContinue, setCanContinue] = useState(false);

  const newsApi = new NewsApi(defaultConfig);
  const {
    data: news,
    mutate: fetchNews,
    isPending: isLoadingNews,
  } = useMutation<NewsDto[], Error>({
    mutationFn: () => newsApi.getNewsNewsGet(),
    onSuccess: () => {
      setLoadingOverlayVisible(false);
    },
  });

  useEffect(() => {
    if (isLoadingNews) {
      setLoadingOverlayVisible(true);
    }
  }, [isLoadingNews]);

  useEffect(() => {
    fetchNews();
  }, []);

  useEffect(() => {
    const isBlobInCreation = news?.some((entry) => entry.type === NewsType.BlobInCreation) ?? false;
    const isEventStarting =
      news?.some((entry) => entry.type === NewsType.EventStarted || entry.type === NewsType.OngoingEvent) ?? false;

    setCanCreateBlob(isBlobInCreation);
    setCanStartEvent(isEventStarting);
    setCanContinue(!isBlobInCreation && !isEventStarting);
  }, [news]);

  return (
    <>
      <NewsCard news={news} />
      <ControlButtonsFooter
        fetchNews={fetchNews}
        setLoadingOverlayVisible={setLoadingOverlayVisible}
        isLoadingNews={isLoadingNews}
        canCreateBlob={canCreateBlob}
        canStartEvent={canStartEvent}
        canContinue={canContinue}
      />
    </>
  );
};
