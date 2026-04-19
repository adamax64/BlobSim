import { useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDtoOutput } from '../../../generated';
import { RaceEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/RaceEventRecordDtoOutput';
import { getRaceDurationBySize } from '../event-components/event-utils';
import defaultConfig from '../../default-config';
import { EnduranceRaceUI } from '../event-components/endurance-race/EnduranceRaceUI';

interface ReplayEnduranceRaceFrameProps {
  event: EventDtoOutput;
  tick: number;
}

export const ReplayEnduranceRaceFrame: React.FC<ReplayEnduranceRaceFrameProps> = ({ event, tick }) => {
  const [eventRecordsCache, setEventRecordsCache] = useState<Map<number, EventRecordDto[]>>(new Map());
  const [displayedRecords, setDisplayedRecords] = useState<EventRecordDto[]>([]);
  const raceDuration = useMemo(() => getRaceDurationBySize(event.competitors.length), [event.competitors.length]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { mutate: getEventRecords, isPending } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (playbackTick: number) =>
      eventRecordsApi.getEnduranceEventRecordsEnduranceGet({
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
    <EnduranceRaceUI
      eventRecords={displayedRecords}
      tick={tick}
      raceDuration={raceDuration}
      loadingNextTick={isPending && !eventRecordsCache.has(tick)}
      isEventFinished={false}
      eventType={event.type}
    />
  );
};
