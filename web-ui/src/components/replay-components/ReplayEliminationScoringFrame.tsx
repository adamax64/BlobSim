import { useState, Dispatch, SetStateAction } from 'react';
import { useMutation } from '@tanstack/react-query';
import { EventRecordsApi, EventDto } from '../../../generated';
import { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../generated/models/EliminationEventRecordDtoOutput';
import defaultConfig from '../../default-config';
import { EliminationScoringUI } from '../event-components/elimination-scoring/EliminationScoringUI';
import { useReplayTickDelay } from '../../hooks/useReplayTickDelay';
import { EventStagePipeline } from '../event-components/shared/EventStagePipeline';

interface ReplayEliminationScoringFrameProps {
  event: EventDto;
  tick: number;
  maxTick: number | undefined;
  setCurrentTick: (tick: number | ((prev: number) => number)) => void;
  stageIndex: number;
  setStageIndex: Dispatch<SetStateAction<number>>;
  onGoBack: () => void;
}

export const ReplayEliminationScoringFrame: React.FC<ReplayEliminationScoringFrameProps> = ({
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
    <EventStagePipeline
      event={event}
      isEventFinished
      stageIndex={stageIndex}
      setStageIndex={setStageIndex}
      replayControls={{ currentTick: tick, maxTick, setCurrentTick, onGoBack }}
      competitionContent={
        <EliminationScoringUI
          eventRecords={displayedRecords}
          tick={tick}
          loadingNextTick={loadingNextTick}
          eventType={event.type}
        />
      }
    />
  );
};
