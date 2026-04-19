import { useTranslation } from 'react-i18next';
import type { ActionDto, BlobCompetitorDtoInput, EventDtoInput } from '../../../../generated';
import { ActionsApi, CompetitionApi, EventRecordsApi } from '../../../../generated';
import type { Dispatch, SetStateAction } from 'react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Alert, Snackbar } from '@mui/material';
import type { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDtoOutput';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { EliminationScoringUI } from './EliminationScoringUI';
import { useReplayState } from '../../../hooks/useReplayState';
import { EventControls } from '../shared/EventControls';

interface SnackbarState {
  message: string | null;
  severity: 'error' | 'success' | 'info' | 'warning';
  anchorOrigin: { vertical: 'top' | 'bottom'; horizontal: 'left' | 'center' | 'right' };
}

interface EliminationScoringEventFrameProps {
  event: EventDtoInput;
  setIsEventFinished: Dispatch<SetStateAction<boolean>>;
  isEventFinished: boolean;
}

export const EliminationScoringEventFrame = ({
  event,
  setIsEventFinished,
  isEventFinished,
}: EliminationScoringEventFrameProps) => {
  const { t } = useTranslation();

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarState, setSnackbarState] = useState<SnackbarState>({
    message: null,
    severity: 'error',
    anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
  });

  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.scores.length), 0));
  const { replayTick, setReplayTick } = useReplayState(event.id);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const [eventRecordsCache, setEventRecordsCache] = useState<EventRecordDto[]>([]);

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<
    EventRecordDto[],
    Error,
    { eventId: number; playbackTick?: number }
  >({
    mutationFn: ({ eventId, playbackTick }) =>
      eventRecordsApi.getEliminationEventRecordsEliminationGet({ eventId, playbackTick }),
    onSuccess: (data) => {
      setLoadingNextTick(false);
      setEventRecordsCache(data);
      return data;
    },
    onError: (error) => {
      setLoadingNextTick(false);
      setSnackbarState({
        message: error.message || t('error.generic'),
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  const { mutate: createAction } = useMutation<
    { name: string; score: number } | undefined,
    Error,
    { contenders: BlobCompetitorDtoInput[] }
  >({
    mutationFn: ({ contenders }) =>
      actionApi.eliminationActionsCreateEliminationPost({ eventId: event.id, blobCompetitorDtoInput: contenders }),
    onSuccess: (data) => {
      if (data) {
        setSnackbarState({
          message: t('elimination_event.new_record', { name: data.name, score: data.score.toFixed(3) }),
          severity: 'success',
          anchorOrigin: { vertical: 'top', horizontal: 'center' },
        });
        setSnackbarOpen(true);
      }
      setTick((prev) => prev + 1);
      setReplayTick((prev) => prev + 1);
      setLoadingNextTick(false);
      getEventRecords({ eventId: event.id });
    },
    onError: (error) => {
      setLoadingNextTick(false);
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
      competitionApi.saveEliminationCompetitionEliminationEventResultsPost({
        bodySaveEliminationCompetitionEliminationEventResultsPost: { event, eventRecords: eventRecords ?? [] },
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

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setLoadingNextTick(true);
      setTimeout(() => {
        createAction({ contenders: eventRecords.filter((record) => !record.eliminated).map((record) => record.blob) });
      }, 1000);
    }
  }, [eventRecords, isEventFinished, createAction]);

  return (
    <>
      <EventControls
        tick={tick}
        replayTick={replayTick}
        setReplayTick={setReplayTick}
        isStart={tick === 0}
        isEnd={tick >= event.actions.length - 1}
        isEventFinished={isEventFinished}
        progressButtonDisabled={loadingNextTick || replayTick < tick}
        onClickStart={progressEvent}
        onClickNext={progressEvent}
        onClickEnd={finishEvent}
      />
      <EliminationScoringUI
        eventRecords={eventRecords ?? eventRecordsCache}
        tick={replayTick}
        loadingNextTick={loadingNextTick}
        isEventFinished={isEventFinished}
        eventType={event.type}
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
