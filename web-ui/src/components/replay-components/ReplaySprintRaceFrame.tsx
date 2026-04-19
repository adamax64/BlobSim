import { useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDtoOutput } from '../../../generated';
import { SprintEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/SprintEventRecordDtoOutput';
import { getRaceDurationBySize } from '../event-components/event-utils';
import defaultConfig from '../../default-config';
import { SprintRaceUI } from '../event-components/sprint-race/SprintRaceUI';

interface ReplaySprintRaceFrameProps {
  event: EventDtoOutput;
  tick: number;
  maxTick: number;
}

export const ReplaySprintRaceFrame: React.FC<ReplaySprintRaceFrameProps> = ({ event, tick, maxTick }) => {
  const [eventRecordsCache, setEventRecordsCache] = useState<Map<number, EventRecordDto[]>>(new Map());
  const [displayedRecords, setDisplayedRecords] = useState<EventRecordDto[]>([]);
  const raceDuration = useMemo(() => getRaceDurationBySize(event.competitors.length), [event.competitors.length]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { mutate: getEventRecords, isPending } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (playbackTick: number) =>
      eventRecordsApi.getSprintEventRecordsSprintGet({
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
    <SprintRaceUI
      eventRecords={displayedRecords}
      tick={tick}
      raceDuration={raceDuration}
      loadingNextTick={isPending && !eventRecordsCache.has(tick)}
      isEventFinished={false}
      eventType={event.type}
      isEnd={tick >= maxTick}
    />
  );
};
