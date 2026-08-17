import {
  ActionsApi,
  BlobCompetitorDto,
  EventDto,
  QuarteredEventRecordDto as EventRecordDto,
  CompetitionApi,
  EventRecordsApi,
} from '../../../../generated';
import { Dispatch, SetStateAction, useCallback, useEffect, useMemo, useState } from 'react';
import { getCurrentQuarter, getQuarterEnds } from '../event-utils';
import defaultConfig from '../../../default-config';
import { useTranslation } from 'react-i18next';
import { QuarteredEventUI } from './QuarteredEventUI';
import { useReplayState } from '../../../hooks/useReplayState';
import { useReplayTickDelay } from '../../../hooks/useReplayTickDelay';
import { EventStagePipeline } from '../shared/EventStagePipeline';
import { useEventSnackbar } from '../shared/useEventSnackbar';
import { EventResultSnackbar } from '../shared/EventResultSnackbar';
import { useEventRecordsQuery } from '../shared/useEventRecordsQuery';
import { useFinishEventMutation } from '../shared/useFinishEventMutation';
import { useMutation } from '@tanstack/react-query';

interface QuarteredEventFrameProps {
  event: EventDto;
  setIsEventFinished: Dispatch<SetStateAction<boolean>>;
  isEventFinished: boolean;
}

export const QuarteredEventFrame: React.FC<QuarteredEventFrameProps> = ({
  event,
  setIsEventFinished,
  isEventFinished,
}) => {
  const { t } = useTranslation();

  const [tick, setTick] = useState(event.actions.reduce((sum, action) => sum + action.scores.length, 0));
  const { replayTick, setReplayTick, stageIndex, setStageIndex } = useReplayState(event.id);
  const [isPerforming, setIsPerforming] = useState(false);
  const [quarter, setQuarter] = useState(0);
  const [currentBlobIndex, setCurrentBlobIndex] = useState(-1);
  const [nextBlobIndex, setNextBlobIndex] = useState(-1);
  const { snackbarOpen, snackbarState, showError, showSuccess, closeSnackbar } = useEventSnackbar();

  const quarterEnds = useMemo(
    () => getQuarterEnds(event.competitors.length, event.type),
    [event.type, event.competitors.length],
  );

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { eventRecords, getEventRecords } = useEventRecordsQuery<EventRecordDto>({
    fetchEventRecords: ({ eventId, playbackTick }) =>
      eventRecordsApi.getQuarteredEventRecordsQuarteredGet({ eventId, playbackTick }),
    onSuccess: (_data, playbackTick) => {
      setIsPerforming(false);
      setQuarter(getCurrentQuarter(quarterEnds, playbackTick ?? tick));
    },
    onError: (error) => {
      setIsPerforming(false);
      showError(error.message || t('error.generic'));
    },
  });

  const { mutate: createAction } = useMutation<
    { name: string; score: number } | null,
    Error,
    { contender: BlobCompetitorDto }
  >({
    mutationFn: (params) =>
      actionApi.quarteredActionsCreateQuarteredPost({
        blobCompetitorDto: params.contender,
        eventId: event.id,
      }),
    onSuccess: (data) => {
      if (data) {
        showSuccess(t('quartered_event.new_record', { name: data.name, score: data.score.toFixed(3) }));
      }
      setTick((prev: number) => prev + 1);
      setReplayTick((prev) => prev + 1);
      getEventRecords({ eventId: event.id });
    },
    onError: (error) => {
      setIsPerforming(false);
      showError(error.message || t('error.generic'));
    },
  });

  const { mutate: finishEvent } = useFinishEventMutation({
    saveResults: () =>
      competitionApi.saveQuarteredCompetitionQuarteredEventResultsPost({
        bodySaveQuarteredCompetitionQuarteredEventResultsPost: { event, eventRecords: eventRecords ?? [] },
      }),
    onFinished: () => setIsEventFinished(true),
    onError: (error) => showError(error.message || t('error.generic')),
  });

  useReplayTickDelay(
    replayTick,
    () => getEventRecords({ eventId: event.id, playbackTick: replayTick }),
    setIsPerforming,
  );

  useEffect(() => {
    if (eventRecords) {
      setCurrentBlobIndex(eventRecords.findIndex((record) => record.current));
      setNextBlobIndex(eventRecords.findIndex((record) => record.next));
    }
  }, [eventRecords]);

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setCurrentBlobIndex(nextBlobIndex);
      setIsPerforming(true);
      setTimeout(() => {
        createAction({ contender: eventRecords[nextBlobIndex].blob });
      }, 1000);
    }
  }, [createAction, eventRecords, nextBlobIndex]);

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
          isEnd: quarter > 4,
          progressButtonDisabled: isPerforming || replayTick < tick,
          onClickStart: progressEvent,
          onClickNext: progressEvent,
          onClickEnd: finishEvent,
        }}
        competitionContent={
          <QuarteredEventUI
            eventRecords={eventRecords}
            quarter={quarter}
            isPerforming={isPerforming}
            eventType={event.type}
            currentBlobIndex={currentBlobIndex}
          />
        }
      />
      <EventResultSnackbar open={snackbarOpen} state={snackbarState} onClose={closeSnackbar} />
    </>
  );
};
