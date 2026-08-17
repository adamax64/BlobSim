import { ActionDto, ActionsApi, CompetitionApi, EventDto, EventRecordsApi } from '../../../../generated';
import { Dispatch, SetStateAction, useCallback, useMemo, useState } from 'react';
import { RaceEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/RaceEventRecordDtoOutput';
import { getRaceDurationBySize } from '../event-utils';
import defaultConfig from '../../../default-config';
import { useTranslation } from 'react-i18next';
import { EnduranceRaceUI } from './EnduranceRaceUI';
import { useReplayState } from '../../../hooks/useReplayState';
import { useReplayTickDelay } from '../../../hooks/useReplayTickDelay';
import { EventStagePipeline } from '../shared/EventStagePipeline';
import { useEventSnackbar } from '../shared/useEventSnackbar';
import { EventResultSnackbar } from '../shared/EventResultSnackbar';
import { useEventRecordsQuery } from '../shared/useEventRecordsQuery';
import { useFinishEventMutation } from '../shared/useFinishEventMutation';
import { useMutation } from '@tanstack/react-query';

interface EnduranceRaceEventFrameProps {
  event: EventDto;
  setIsEventFinished: Dispatch<SetStateAction<boolean>>;
  isEventFinished: boolean;
}

export const EnduranceRaceEventFrame: React.FC<EnduranceRaceEventFrameProps> = ({
  event,
  setIsEventFinished,
  isEventFinished,
}) => {
  const { t } = useTranslation();

  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.scores.length), 0));
  const { replayTick, setReplayTick, stageIndex, setStageIndex } = useReplayState(event.id);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const { snackbarOpen, snackbarState, showError, showSuccess, closeSnackbar } = useEventSnackbar();

  const raceDuration = useMemo(() => getRaceDurationBySize(event.competitors.length), [event.competitors.length]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const actionsApi = new ActionsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { eventRecords, getEventRecords } = useEventRecordsQuery<EventRecordDto>({
    fetchEventRecords: ({ eventId, playbackTick }) =>
      eventRecordsApi.getEnduranceEventRecordsEnduranceGet({ eventId, playbackTick }),
    onSuccess: () => setLoadingNextTick(false),
    onError: (error) => {
      setLoadingNextTick(false);
      showError(error.message || t('error.generic'));
    },
  });

  const { mutate: createActions } = useMutation<{ name: string; score: number } | null, Error>({
    mutationFn: () => actionsApi.raceActionsCreateRacePost({ eventId: event.id, tick: tick }),
    onSuccess: (data) => {
      if (data) {
        showSuccess(t('race_event.new_record', { name: data.name, score: data.score.toFixed(3) }));
      }
      setTick((prev) => prev + 1);
      setReplayTick((prev) => prev + 1);
      getEventRecords({ eventId: event.id });
    },
    onError: (error) => {
      setLoadingNextTick(false);
      showError(error.message || t('error.generic'));
    },
  });

  const { mutate: finishEvent } = useFinishEventMutation({
    saveResults: () =>
      competitionApi.saveEnduranceCompetitionEnduranceEventResultsPost({
        bodySaveEnduranceCompetitionEnduranceEventResultsPost: { event, eventRecords: eventRecords ?? [] },
      }),
    onFinished: () => setIsEventFinished(true),
  });

  useReplayTickDelay(
    replayTick,
    () => getEventRecords({ eventId: event.id, playbackTick: replayTick }),
    setLoadingNextTick,
  );

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setLoadingNextTick(true);
      setTimeout(() => {
        createActions();
      }, 1000);
    }
  }, [eventRecords, isEventFinished]);

  return (
    <>
      <EventStagePipeline
        event={event}
        isEventFinished={isEventFinished}
        stageIndex={stageIndex}
        setStageIndex={setStageIndex}
        eventControls={{
          tick,
          replayTick,
          setReplayTick,
          isStart: (eventRecords?.[0]?.distanceRecords?.length ?? 0) === 0,
          isEnd: tick >= raceDuration,
          progressButtonDisabled: loadingNextTick || replayTick < tick,
          onClickStart: progressEvent,
          onClickNext: progressEvent,
          onClickEnd: finishEvent,
        }}
        competitionContent={
          <EnduranceRaceUI
            eventRecords={eventRecords}
            tick={replayTick}
            loadingNextTick={loadingNextTick}
            eventType={event.type}
            raceDuration={raceDuration}
          />
        }
      />
      <EventResultSnackbar open={snackbarOpen} state={snackbarState} onClose={closeSnackbar} />
    </>
  );
};
