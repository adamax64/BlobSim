import { useMutation } from '@tanstack/react-query';
import { useState } from 'react';

interface UseEventRecordsQueryOptions<T> {
  /** Fetches the event records for the given tick (or the latest, when `playbackTick` is omitted). */
  fetchEventRecords: (params: { eventId: number; playbackTick?: number }) => Promise<T[]>;
  /** Called after records are fetched, e.g. to reset a loading flag or derive extra local state. */
  onSuccess?: (data: T[], playbackTick?: number) => void;
  onError: (error: Error) => void;
}

/** Generic "fetch event records for a tick" mutation + cache, shared by all live `*EventFrame` components. */
export function useEventRecordsQuery<T>({ fetchEventRecords, onSuccess, onError }: UseEventRecordsQueryOptions<T>) {
  const [eventRecordsCache, setEventRecordsCache] = useState<T[]>([]);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<
    T[],
    Error,
    { eventId: number; playbackTick?: number }
  >({
    mutationFn: fetchEventRecords,
    onSuccess: (data, { playbackTick }) => {
      setEventRecordsCache(data);
      onSuccess?.(data, playbackTick);
    },
    onError,
  });

  return { eventRecords: eventRecords ?? eventRecordsCache, getEventRecords };
}
