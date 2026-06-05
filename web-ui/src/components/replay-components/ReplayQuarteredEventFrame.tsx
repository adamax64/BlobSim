import { useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDtoOutput } from '../../../generated';
import { QuarteredEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/QuarteredEventRecordDtoOutput';
import { getCurrentQuarter, getQuarterEnds } from '../event-components/event-utils';
import defaultConfig from '../../default-config';
import { QuarteredEventUI } from '../event-components/quartered-event/QuarteredEventUI';
import { useReplayTickDelay } from '../../hooks/useReplayTickDelay';
interface ReplayQuarteredEventFrameProps {
  event: EventDtoOutput;
  tick: number;
}

export const ReplayQuarteredEventFrame: React.FC<ReplayQuarteredEventFrameProps> = ({ event, tick }) => {
  const [eventRecordsCache, setEventRecordsCache] = useState<Map<number, EventRecordDto[]>>(new Map());
  const [displayedRecords, setDisplayedRecords] = useState<EventRecordDto[]>([]);
  const [currentBlobIndex, setCurrentBlobIndex] = useState(-1);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const quarterEnds = useMemo(
    () => getQuarterEnds(event.competitors.length, event.type),
    [event.competitors.length, event.type],
  );
  const [quarter, setQuarter] = useState(getCurrentQuarter(quarterEnds, tick));

  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (playbackTick: number) =>
      eventRecordsApi.getQuarteredEventRecordsQuarteredGet({
        eventId: event.id,
        playbackTick,
      }),
    onSuccess: (data, playbackTick) => {
      setLoadingNextTick(false);
      setQuarter(getCurrentQuarter(quarterEnds, playbackTick));
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
        setQuarter(getCurrentQuarter(quarterEnds, tick));
      }
    },
    setLoadingNextTick,
  );

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
      isPerforming={loadingNextTick}
    />
  );
};
