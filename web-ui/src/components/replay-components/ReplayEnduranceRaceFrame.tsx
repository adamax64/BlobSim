import { useMemo, useState, Dispatch, SetStateAction } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDto } from '../../../generated';
import { RaceEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/RaceEventRecordDtoOutput';
import { getRaceDurationBySize } from '../event-components/event-utils';
import defaultConfig from '../../default-config';
import { EnduranceRaceUI } from '../event-components/endurance-race/EnduranceRaceUI';
import { useReplayTickDelay } from '../../hooks/useReplayTickDelay';
import { EventStagePipeline } from '../event-components/shared/EventStagePipeline';

interface ReplayEnduranceRaceFrameProps {
  event: EventDto;
  tick: number;
  maxTick: number | undefined;
  setCurrentTick: (tick: number | ((prev: number) => number)) => void;
  stageIndex: number;
  setStageIndex: Dispatch<SetStateAction<number>>;
  onGoBack: () => void;
}

export const ReplayEnduranceRaceFrame: React.FC<ReplayEnduranceRaceFrameProps> = ({
  event,
  tick,
  maxTick,
  setCurrentTick,
  stageIndex,
  setStageIndex,
  onGoBack,
}) => {
  const [eventRecordsCache, setEventRecordsCache] = useState<Map<number, EventRecordDto[]>>(new Map());
  const [displayedRecords, setDisplayedRecords] = useState<EventRecordDto[]>([]);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const raceDuration = useMemo(() => getRaceDurationBySize(event.competitors.length), [event.competitors.length]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (playbackTick: number) =>
      eventRecordsApi.getEnduranceEventRecordsEnduranceGet({
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
    <EventStagePipeline
      event={event}
      isEventFinished
      stageIndex={stageIndex}
      setStageIndex={setStageIndex}
      replayControls={{ currentTick: tick, maxTick, setCurrentTick, onGoBack }}
      competitionContent={
        <EnduranceRaceUI
          eventRecords={displayedRecords}
          tick={tick}
          raceDuration={raceDuration}
          loadingNextTick={loadingNextTick}
          eventType={event.type}
          eventId={event.id}
        />
      }
    />
  );
};
