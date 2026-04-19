import { Snackbar, Alert } from '@mui/material';
import {
  ActionsApi,
  BlobCompetitorDtoInput,
  EventDtoInput,
  EventType,
  QuarteredEventRecordDtoInput as EventRecordDto,
  CompetitionApi,
  EventRecordsApi,
} from '../../../../generated';
import { Dispatch, SetStateAction, useCallback, useEffect, useMemo, useState } from 'react';
import { getCurrentQuarter, getQuarterEnds } from '../event-utils';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { SnackbarState } from '../snackbar-state';
import { QuarteredEventUI } from './QuarteredEventUI';
import { useReplayState } from '../../../hooks/useReplayState';
import { EventControls } from '../shared/EventControls';

interface QuarteredEventFrameProps {
  event: EventDtoInput;
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
  const { replayTick, setReplayTick } = useReplayState(event.id);
  const [isPerforming, setIsPerforming] = useState(false);
  const [quarter, setQuarter] = useState(0);
  const [currentBlobIndex, setCurrentBlobIndex] = useState(-1);
  const [nextBlobIndex, setNextBlobIndex] = useState(-1);
  const [eventRecordsCache, setEventRecordsCache] = useState<EventRecordDto[]>([]);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarState, setSnackbarState] = useState<SnackbarState>({
    message: null,
    severity: 'error',
    anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
  });

  const isOneShot = useMemo(() => event.type === EventType.QuarteredOneShotScoring, [event.type]);
  const quarterEnds = useMemo(
    () => getQuarterEnds(event.competitors.length, isOneShot),
    [isOneShot, event.competitors.length],
  );

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<
    EventRecordDto[],
    Error,
    { eventId: number; playbackTick?: number }
  >({
    mutationFn: ({ eventId, playbackTick }) =>
      eventRecordsApi.getQuarteredEventRecordsQuarteredGet({ eventId, playbackTick }),
    onSuccess: (data) => {
      setIsPerforming(false);
      setEventRecordsCache(data);
      return data;
    },
    onError: (error) => {
      setIsPerforming(false);
      setSnackbarState({
        message: error.message || t('error.generic'),
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  const { mutate: createAction } = useMutation<
    { name: string; score: number } | null,
    Error,
    { contender: BlobCompetitorDtoInput }
  >({
    mutationFn: (params) =>
      actionApi.quarteredActionsCreateQuarteredPost({
        blobCompetitorDtoInput: params.contender,
        eventId: event.id,
      }),
    onSuccess: (data) => {
      if (data) {
        setSnackbarState({
          message: t('quartered_event.new_record', { name: data.name, score: data.score.toFixed(3) }),
          severity: 'success',
          anchorOrigin: { vertical: 'top', horizontal: 'center' },
        });
        setSnackbarOpen(true);
      }
      setTick((prev: number) => prev + 1);
      setReplayTick((prev) => prev + 1);
      getEventRecords({ eventId: event.id });
    },
    onError: (error) => {
      setIsPerforming(false);
      setSnackbarState({
        message: error.message || t('error.generic'),
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  const { mutate: finishEvent } = useMutation<void, Error>({
    mutationFn: () =>
      competitionApi.saveQuarteredCompetitionQuarteredEventResultsPost({
        bodySaveQuarteredCompetitionQuarteredEventResultsPost: { event, eventRecords: eventRecords ?? [] },
      }),
    onSuccess: () => {
      setIsEventFinished(true);
    },
    onError: (error) => {
      setSnackbarState({
        message: error.message || t('error.generic'),
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  useEffect(() => {
    getEventRecords({ eventId: event.id, playbackTick: replayTick });
  }, [event.id, replayTick]);

  useEffect(() => {
    setQuarter(getCurrentQuarter(quarterEnds, replayTick));
  }, [replayTick, quarterEnds]);

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
      <EventControls
        tick={tick}
        replayTick={replayTick}
        setReplayTick={setReplayTick}
        isStart={tick === 0}
        isEnd={quarter > 4}
        isEventFinished={isEventFinished}
        progressButtonDisabled={isPerforming || replayTick < tick}
        onClickStart={progressEvent}
        onClickNext={progressEvent}
        onClickEnd={finishEvent}
      />
      <QuarteredEventUI
        eventRecords={eventRecords ?? eventRecordsCache}
        quarter={quarter}
        isPerforming={isPerforming}
        isEventFinished={isEventFinished}
        eventType={event.type}
        currentBlobIndex={currentBlobIndex}
      />
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={snackbarState.anchorOrigin}
      >
        <Alert onClose={() => setSnackbarOpen(false)} severity={snackbarState.severity} variant="filled">
          {snackbarState.message}
        </Alert>
      </Snackbar>
    </>
  );
};
