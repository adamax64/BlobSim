import { useQuery } from '@tanstack/react-query';
import { NewsType, SimDataApi } from '../../generated';
import defaultConfig from '../default-config';
import { useAuth } from '../context/AuthContext';
import { useNews } from '../context/NewsContext';

export function useCanContinue() {
  const { isAuthenticated } = useAuth();
  const { news, newsLoading } = useNews();
  const simDataApi = new SimDataApi(defaultConfig);
  const { data: canProgress } = useQuery({
    queryKey: ['simData', 'canProgress', news, newsLoading],
    queryFn: () => simDataApi.canProgressSimDataCanProgressGet(),
    enabled: isAuthenticated,
  });

  const latestNews = news?.at(0);

  const isEventToday =
    latestNews && (latestNews.type === NewsType.EventStarted || latestNews.type === NewsType.OngoingEvent);

  const isBlobInCreation = latestNews && latestNews.type === NewsType.BlobInCreation;

  return { canContinue: canProgress && isAuthenticated, isEventToday, isBlobInCreation };
}
