import { useTranslation } from 'react-i18next';
import type { ActionDto, BlobCompetitorDtoInput, EventDtoInput } from '../../../../generated';
import { ActionsApi, CompetitionApi, EventRecordsApi } from '../../../../generated';
import { useAuth } from '../../../context/AuthContext';
import type { Dispatch, SetStateAction } from 'react';
import { useCallback, useEffect, useState } from 'react';
import { Alert, Snackbar } from '@mui/material';
import { ProgressButton } from '../shared/ProgressButton';
import type { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDtoOutput';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { EliminationScoringUI } from './EliminationScoringUI';

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
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarState, setSnackbarState] = useState<SnackbarState>({
    message: null,
    severity: 'error',
    anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
  });

  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.scores.length), 0));
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const [eventRecordsCache, setEventRecordsCache] = useState<EventRecordDto[]>([]);

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (eventId: number) => eventRecordsApi.getEliminationEventRecordsEliminationGet({ eventId }),
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
      setLoadingNextTick(false);
      getEventRecords(event.id);
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
    getEventRecords(event.id);
  }, [event.id]);

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
      {isAuthenticated && (
        <ProgressButton
          isStart={tick === 0}
          isEnd={tick >= event.actions.length - 1}
          isEventFinished={isEventFinished}
          disabled={loadingNextTick}
          onClickStart={progressEvent}
          onClickNext={progressEvent}
          onClickEnd={finishEvent}
        />
      )}
      <EliminationScoringUI
        eventRecords={eventRecords ?? eventRecordsCache}
        tick={tick}
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
