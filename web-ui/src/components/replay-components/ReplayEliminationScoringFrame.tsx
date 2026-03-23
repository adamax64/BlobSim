import { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDtoOutput } from '../../../generated';
import { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/EliminationEventRecordDtoOutput';
import defaultConfig from '../../default-config';
import { EliminationScoringUI } from '../event-components/elimination-scoring/EliminationScoringUI';

interface ReplayEliminationScoringFrameProps {
  event: EventDtoOutput;
  tick: number;
}

export const ReplayEliminationScoringFrame: React.FC<ReplayEliminationScoringFrameProps> = ({ event, tick }) => {
  const [eventRecordsCache, setEventRecordsCache] = useState<Map<number, EventRecordDto[]>>(new Map());
  const [displayedRecords, setDisplayedRecords] = useState<EventRecordDto[]>([]);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { mutate: getEventRecords, isPending } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (playbackTick: number) =>
      eventRecordsApi.getEliminationEventRecordsEliminationGet({
        eventId: event.id,
        playbackTick,
      }),
    onSuccess: (data, playbackTick) => {
      setEventRecordsCache((prev) => new Map(prev.set(playbackTick, data)));
      setDisplayedRecords(data);
    },
  });

  useEffect(() => {
    if (!eventRecordsCache.has(tick)) {
      getEventRecords(tick);
    } else {
      // If we have cached data for this tick, update displayed records
      setDisplayedRecords(eventRecordsCache.get(tick)!);
    }
  }, [tick, eventRecordsCache, getEventRecords]);

  return (
    <EliminationScoringUI
      eventRecords={displayedRecords}
      tick={tick}
      loadingNextTick={isPending && !eventRecordsCache.has(tick)}
      isEventFinished={false}
      eventType={event.type}
    />
  );
};
