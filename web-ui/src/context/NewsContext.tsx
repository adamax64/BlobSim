import { createContext, useContext, useState } from 'react';
import { NewsApi, NewsDto, SimTimeDto } from '../../generated';
import defaultConfig from '../default-config';
import { useMutation } from '@tanstack/react-query';
import { compareSimTime } from '../utils/sim-time-utils';

const STORAGE_KEY = 'lastViewedNewsDate';

type NewsContextValue = {
  newsLoading: boolean;
  news: NewsDto[] | undefined;
  refreshNews: () => void;
  hasUnseenNews: boolean;
  markNewsAsViewed: () => void;
};

export const NewsContext = createContext<NewsContextValue | undefined>(undefined);

export const NewsProvider = ({ children }: { children: React.ReactNode }) => {
  const newsApi = new NewsApi(defaultConfig);

  const {
    data: news,
    mutate: fetchNews,
    isPending,
  } = useMutation<NewsDto[], Error>({
    mutationFn: () => newsApi.getNewsNewsGet(),
  });

  const [lastViewedNewsDate, setLastViewedNewsDate] = useState<SimTimeDto | undefined>(() => {
    if (typeof window === 'undefined') return undefined;
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? (JSON.parse(stored) as SimTimeDto) : undefined;
  });

  const latestNewsDate = news?.at(0)?.date;
  const hasUnseenNews = !!latestNewsDate && (!lastViewedNewsDate || compareSimTime(latestNewsDate, lastViewedNewsDate) > 0);

  const markNewsAsViewed = () => {
    if (!latestNewsDate) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(latestNewsDate));
    setLastViewedNewsDate(latestNewsDate);
  };

  return (
    <NewsContext.Provider
      value={{
        news,
        newsLoading: isPending,
        refreshNews: fetchNews,
        hasUnseenNews,
        markNewsAsViewed,
      }}
    >
      {children}
    </NewsContext.Provider>
  );
};

export const useNews = () => {
  const context = useContext(NewsContext);

  if (!context) {
    throw new Error('NewsContext must be used within a NewsProvider');
  }
  return context;
};
