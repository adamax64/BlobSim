import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDtoOutput } from '../../../generated';
import { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/EliminationEventRecordDtoOutput';
import defaultConfig from '../../default-config';
import { EliminationScoringUI } from '../event-components/elimination-scoring/EliminationScoringUI';
import { useReplayTickDelay } from '../../hooks/useReplayTickDelay';

interface ReplayEliminationScoringFrameProps {
  event: EventDtoOutput;
  tick: number;
}

export const ReplayEliminationScoringFrame: React.FC<ReplayEliminationScoringFrameProps> = ({ event, tick }) => {
  const [eventRecordsCache, setEventRecordsCache] = useState<Map<number, EventRecordDto[]>>(new Map());
  const [displayedRecords, setDisplayedRecords] = useState<EventRecordDto[]>([]);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (playbackTick: number) =>
      eventRecordsApi.getEliminationEventRecordsEliminationGet({
        eventId: event.id,
        playbackTick,
      }),
    onSuccess: (data, playbackTick) => {
      setLoadingNextTick(false);
      setEventRecordsCache((prev) => new Map(prev.set(playbackTick, data)));
      setDisplayedRecords(data);
    },
  });

  useReplayTickDelay(
    tick,
    () => {
      if (!eventRecordsCache.has(tick)) {
        getEventRecords(tick);
      } else {
        setDisplayedRecords(eventRecordsCache.get(tick)!);
        setLoadingNextTick(false);
      }
    },
    setLoadingNextTick,
  );

  return (
    <EliminationScoringUI
      eventRecords={displayedRecords}
      tick={tick}
      loadingNextTick={loadingNextTick}
      isEventFinished={false}
      eventType={event.type}
    />
  );
};
