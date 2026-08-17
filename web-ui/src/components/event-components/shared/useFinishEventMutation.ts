import { useMutation } from '@tanstack/react-query';
import { useNews } from '../../../context/NewsContext';

interface UseFinishEventMutationOptions {
  /** Persists the final event results (e.g. `competitionApi.save*CompetitionPost`). */
  saveResults: () => Promise<void>;
  onFinished: () => void;
  onError?: (error: Error) => void;
}

/** Generic "save final results" mutation shared by all live `*EventFrame` components. */
export function useFinishEventMutation({ saveResults, onFinished, onError }: UseFinishEventMutationOptions) {
  const { refreshNews } = useNews();
  return useMutation<void, Error>({
    mutationFn: saveResults,
    onSuccess: () => {
      onFinished();
      refreshNews();
    },
    onError,
  });
}
