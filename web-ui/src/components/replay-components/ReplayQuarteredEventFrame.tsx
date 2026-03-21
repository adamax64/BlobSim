import { useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDtoOutput, EventType } from '../../../generated';
import { QuarteredEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/QuarteredEventRecordDtoOutput';
import { getCurrentQuarter, getQuarterEnds } from '../event-components/event-utils';
import defaultConfig from '../../default-config';
import { QuarteredEventUI } from '../event-components/quartered-event/QuarteredEventUI';

interface ReplayQuarteredEventFrameProps {
  event: EventDtoOutput;
  tick: number;
}

export const ReplayQuarteredEventFrame: React.FC<ReplayQuarteredEventFrameProps> = ({ event, tick }) => {
  const [eventRecordsCache, setEventRecordsCache] = useState<Map<number, EventRecordDto[]>>(new Map());
  const [displayedRecords, setDisplayedRecords] = useState<EventRecordDto[]>([]);
  const [currentBlobIndex, setCurrentBlobIndex] = useState(-1);
  const isOneShot = useMemo(() => event.type === EventType.QuarteredOneShotScoring, [event.type]);
  const quarterEnds = useMemo(
    () => getQuarterEnds(event.competitors.length, isOneShot),
    [event.competitors.length, isOneShot],
  );
  const quarter = useMemo(() => getCurrentQuarter(quarterEnds, tick), [tick, quarterEnds]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { mutate: getEventRecords, isPending } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (playbackTick: number) =>
      eventRecordsApi.getQuarteredEventRecordsQuarteredGet({
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

  useEffect(() => {
    if (displayedRecords.length > 0) {
      setCurrentBlobIndex(displayedRecords.findIndex((record) => record.current));
    }
  }, [displayedRecords]);

  return (
    <QuarteredEventUI
      eventRecords={displayedRecords}
      quarter={quarter}
      isEventFinished={false}
      eventType={event.type}
      currentBlobIndex={currentBlobIndex}
      isPerforming={isPending}
    />
  );
};
