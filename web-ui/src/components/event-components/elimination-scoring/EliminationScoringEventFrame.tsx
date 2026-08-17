import { useTranslation } from 'react-i18next';
import type { ActionDto, BlobCompetitorDto, EventDto } from '../../../../generated';
import { ActionsApi, CompetitionApi, EventRecordsApi } from '../../../../generated';
import type { Dispatch, SetStateAction } from 'react';
import { useCallback, useState } from 'react';
import type { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDtoOutput';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { EliminationScoringUI } from './EliminationScoringUI';
import { useReplayState } from '../../../hooks/useReplayState';
import { useReplayTickDelay } from '../../../hooks/useReplayTickDelay';
import { EventStagePipeline } from '../shared/EventStagePipeline';
import { useEventSnackbar } from '../shared/useEventSnackbar';
import { EventResultSnackbar } from '../shared/EventResultSnackbar';
import { useEventRecordsQuery } from '../shared/useEventRecordsQuery';
import { useFinishEventMutation } from '../shared/useFinishEventMutation';

interface EliminationScoringEventFrameProps {
  event: EventDto;
  setIsEventFinished: Dispatch<SetStateAction<boolean>>;
  isEventFinished: boolean;
}

export const EliminationScoringEventFrame = ({
  event,
  setIsEventFinished,
  isEventFinished,
}: EliminationScoringEventFrameProps) => {
  const { t } = useTranslation();

  const { snackbarOpen, snackbarState, showError, showSuccess, closeSnackbar } = useEventSnackbar();

  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.scores.length), 0));
  const { replayTick, setReplayTick, stageIndex, setStageIndex } = useReplayState(event.id);
  const [loadingNextTick, setLoadingNextTick] = useState(false);

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { eventRecords, getEventRecords } = useEventRecordsQuery<EventRecordDto>({
    fetchEventRecords: ({ eventId, playbackTick }) =>
      eventRecordsApi.getEliminationEventRecordsEliminationGet({ eventId, playbackTick }),
    onSuccess: () => setLoadingNextTick(false),
    onError: (error) => {
      setLoadingNextTick(false);
      showError(error.message || t('error.generic'));
    },
  });

  const { mutate: createAction } = useMutation<
    { name: string; score: number } | undefined,
    Error,
    { contenders: BlobCompetitorDto[] }
  >({
    mutationFn: ({ contenders }) =>
      actionApi.eliminationActionsCreateEliminationPost({ eventId: event.id, blobCompetitorDto: contenders }),
    onSuccess: (data) => {
      if (data) {
        showSuccess(t('elimination_event.new_record', { name: data.name, score: data.score.toFixed(3) }));
      }
      setTick((prev) => prev + 1);
      setReplayTick((prev) => prev + 1);
      setLoadingNextTick(false);
      getEventRecords({ eventId: event.id });
    },
    onError: (error) => {
      setLoadingNextTick(false);
      showError(error.message || t('error.generic'));
    },
  });

  const { mutate: finishEvent } = useFinishEventMutation({
    saveResults: () =>
      competitionApi.saveEliminationCompetitionEliminationEventResultsPost({
        bodySaveEliminationCompetitionEliminationEventResultsPost: { event, eventRecords: eventRecords ?? [] },
      }),
    onFinished: () => setIsEventFinished(true),
    onError: (error) => showError(error.message || t('error.generic')),
  });

  useReplayTickDelay(
    replayTick,
    () => getEventRecords({ eventId: event.id, playbackTick: replayTick }),
    setLoadingNextTick,
  );

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setLoadingNextTick(true);
      const timer = setTimeout(() => {
        createAction({ contenders: eventRecords.filter((record) => !record.eliminated).map((record) => record.blob) });
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [eventRecords, isEventFinished, createAction]);

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
          isStart: tick === 0,
          isEnd: tick >= event.actions.length - 1,
          progressButtonDisabled: loadingNextTick || replayTick < tick,
          onClickStart: progressEvent,
          onClickNext: progressEvent,
          onClickEnd: finishEvent,
        }}
        competitionContent={
          <EliminationScoringUI
            eventRecords={eventRecords}
            tick={replayTick}
            loadingNextTick={loadingNextTick}
            eventType={event.type}
          />
        }
      />
      <EventResultSnackbar open={snackbarOpen} state={snackbarState} onClose={closeSnackbar} />
    </>
  );
};
