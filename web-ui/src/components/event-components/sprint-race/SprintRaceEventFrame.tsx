import { Snackbar, Alert } from '@mui/material';
import { ActionDto, ActionsApi, CompetitionApi, EventDtoInput, EventRecordsApi } from '../../../../generated';
import { Dispatch, SetStateAction, useCallback, useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { SprintEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/SprintEventRecordDtoOutput';
import { getRaceDurationBySize } from '../event-utils';
import defaultConfig from '../../../default-config';
import { useTranslation } from 'react-i18next';
import { SnackbarState } from '../snackbar-state';
import { SprintRaceUI } from './SprintRaceUI';
import { useReplayState } from '../../../hooks/useReplayState';
import { EventControls } from '../shared/EventControls';

interface SprintRaceEventFrameProps {
  event: EventDtoInput;
  setIsEventFinished: Dispatch<SetStateAction<boolean>>;
  isEventFinished: boolean;
}

export const SprintRaceEventFrame: React.FC<SprintRaceEventFrameProps> = ({
  event,
  setIsEventFinished,
  isEventFinished,
}) => {
  const { t } = useTranslation();

  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.scores.length), 0));
  const { replayTick, setReplayTick } = useReplayState(event.id);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const [eventRecordsCache, setEventRecordsCache] = useState<EventRecordDto[]>([]);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarState, setSnackbarState] = useState<SnackbarState>({
    message: null,
    severity: 'error',
    anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
  });

  const raceDuration = useMemo(() => getRaceDurationBySize(event.competitors.length), [event.competitors.length]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const actionsApi = new ActionsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<
    EventRecordDto[],
    Error,
    { eventId: number; playbackTick?: number }
  >({
    mutationFn: ({ eventId, playbackTick }) =>
      eventRecordsApi.getSprintEventRecordsSprintGet({ eventId, playbackTick }),
    onSuccess: (data) => {
      setLoadingNextTick(false);
      setEventRecordsCache(data);
      return data;
    },
    onError: (error) => {
      setLoadingNextTick(false);
      setSnackbarState({
        message: error.message || 'An error occurred',
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  const { mutate: createActions } = useMutation<{ name: string; score: number } | null, Error>({
    mutationFn: () => actionsApi.raceActionsCreateRacePost({ eventId: event.id, tick: tick }),
    onSuccess: (data) => {
      if (data) {
        setSnackbarState({
          message: t('race_event.new_record', { name: data.name, score: data.score.toFixed(3) }),
          severity: 'success',
          anchorOrigin: { vertical: 'top', horizontal: 'center' },
        });
        setSnackbarOpen(true);
      }
      setTick((prev) => prev + 1);
      setReplayTick((prev) => prev + 1);
      getEventRecords({ eventId: event.id });
    },
    onError: (error) => {
      setLoadingNextTick(false);
      setSnackbarState({
        message: error.message || 'An error occurred',
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  const { mutate: finishEvent } = useMutation<void, Error>({
    mutationFn: () =>
      competitionApi.saveSprintCompetitionSprintEventResultsPost({
        bodySaveSprintCompetitionSprintEventResultsPost: { event, eventRecords: eventRecords ?? [] },
      }),
    onSuccess: () => {
      setIsEventFinished(true);
    },
  });

  useEffect(() => {
    getEventRecords({ eventId: event.id, playbackTick: replayTick });
  }, [event.id, replayTick]);

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setLoadingNextTick(true);
      setTimeout(() => {
        createActions();
      }, 1000);
    }
  }, [eventRecords, isEventFinished]);

  const isEnd = useMemo(() => {
    const records = eventRecords ?? eventRecordsCache;
    return tick >= raceDuration || (records.length > 0 && records.every((record) => record.isFinished === true));
  }, [eventRecords, eventRecordsCache, raceDuration, tick]);

  return (
    <>
      <EventControls
        tick={tick}
        replayTick={replayTick}
        setReplayTick={setReplayTick}
        isStart={(eventRecords?.[0]?.distanceRecords?.length ?? 0) === 0}
        isEnd={isEnd}
        isEventFinished={isEventFinished}
        progressButtonDisabled={loadingNextTick || replayTick < tick}
        onClickStart={progressEvent}
        onClickNext={progressEvent}
        onClickEnd={finishEvent}
      />
      <SprintRaceUI
        eventRecords={eventRecords ?? eventRecordsCache}
        tick={replayTick}
        raceDuration={raceDuration}
        loadingNextTick={loadingNextTick}
        isEventFinished={isEventFinished}
        eventType={event.type}
        isEnd={isEnd}
      />
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={snackbarState.anchorOrigin}
        color="error"
      >
        <Alert onClose={() => setSnackbarOpen(false)} severity={snackbarState.severity} variant="filled">
          {snackbarState.message}
        </Alert>
      </Snackbar>
    </>
  );
};
