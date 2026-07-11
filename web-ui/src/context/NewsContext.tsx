import { createContext, useContext } from 'react';
import { NewsApi, NewsDto } from '../../generated';
import defaultConfig from '../default-config';
import { useMutation } from '@tanstack/react-query';

type NewsContextValue = {
  newsLoading: boolean;
  news: NewsDto[] | undefined;
  refreshNews: () => void;
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

  return (
    <NewsContext.Provider value={{ news, newsLoading: isPending, refreshNews: fetchNews }}>
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
