import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useTheme,
  useMediaQuery,
  Tooltip,
  Snackbar,
  Alert,
} from '@mui/material';
import { ActionDto, ActionsApi, CompetitionApi, EventDto, EventRecordsApi } from '../../../generated';
import { ProgressButton } from './ProgressButton';
import { Dispatch, SetStateAction, useCallback, useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { RaceEventRecordDto as EventRecordDto } from '../../../generated/models/RaceEventRecordDto';
import { getRaceDurationBySize, roundToThreeDecimals, roundToOneDecimals } from './event-utils';
import defaultConfig from '../../default-config';
import { useAuth } from '../../context/AuthContext';
import { useTranslation } from 'react-i18next';
import Straighten from '@mui/icons-material/Straighten';
import { NarrowCell, TickLoadingBar } from '../common/StyledComponents';
import { IconNameWithDetailsModal } from '../common/IconNameWithDetailsModal';
import { SnackbarState } from './snackbar-state';

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
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();

  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.scores.length), 0));
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const [eventRecordsCache, setEventRecordsCache] = useState<EventRecordDto[]>([]);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarState, setSnackbarState] = useState<SnackbarState>({
    message: null,
    severity: 'error',
    anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
  });

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const raceDuration = useMemo(() => getRaceDurationBySize(event.competitors.length), [event.competitors.length]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const actionsApi = new ActionsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<
    EventRecordDto[],
    Error,
    { eventId: number; isPlayback: boolean }
  >({
    mutationFn: ({ eventId, isPlayback }) => eventRecordsApi.getRaceEventRecordsRaceGet({ eventId, isPlayback }),
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
      getEventRecords({ eventId: event.id, isPlayback: false });
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
      competitionApi.saveRaceCompetitionRaceEventResultsPost({
        bodySaveRaceCompetitionRaceEventResultsPost: { event, eventRecords: eventRecords ?? [] },
      }),
    onSuccess: () => {
      setIsEventFinished(true);
    },
  });

  useEffect(() => {
    getEventRecords({ eventId: event.id, isPlayback: true });
  }, [event.id]);

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setLoadingNextTick(true);
      setTimeout(() => {
        createActions();
      }, 1000);
    }
  }, [eventRecords, isEventFinished]);

  const getDistance = useCallback(
    (record: EventRecordDto) => {
      return isMobile
        ? (roundToOneDecimals(record.distanceRecords?.[record.distanceRecords?.length - 1]) ?? '-')
        : (roundToThreeDecimals(record.distanceRecords?.[record.distanceRecords?.length - 1]) ?? '-');
    },
    [isMobile],
  );

  const getDelta = useCallback((currentRecord: EventRecordDto, otherRecord: EventRecordDto, index: number) => {
    if (index === 0) {
      return '-';
    }
    const distance = currentRecord.distanceRecords[currentRecord.distanceRecords.length - 1];
    const otherDistance = otherRecord.distanceRecords[otherRecord.distanceRecords.length - 1];

    if (!distance || !otherDistance) {
      return '-';
    }

    return roundToThreeDecimals(otherDistance - distance);
  }, []);

  const getRowClass = (previousPosition: number, currentPosition: number): string => {
    if (isEventFinished) {
      switch (currentPosition) {
        case 1:
          return 'row-gold';
        case 2:
          return 'row-silver';
        case 3:
          return 'row-bronze';
      }
    } else {
      if (previousPosition > currentPosition) {
        return 'cell-overtake';
      }
      if (currentPosition > previousPosition && tick > 0) {
        return 'cell-fell-behind';
      }
    }
    return '';
  };

  return (
    <Paper>
      <CardHeader title={t(`enums.event_types.${event.type}`)} />
      <Divider />
      <CardContent>
        {isAuthenticated && (
          <ProgressButton
            isStart={(eventRecords?.[0]?.distanceRecords?.length ?? 0) === 0}
            isEnd={tick >= raceDuration}
            isEventFinished={isEventFinished}
            disabled={loadingNextTick}
            onClickStart={progressEvent}
            onClickNext={progressEvent}
            onClickEnd={finishEvent}
          />
        )}
        <Typography fontSize={18} fontWeight={600} paddingBottom={2}>
          {t('endurance_race.tick')}: {tick} / {raceDuration}
        </Typography>
        <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginBottom={2}>
          <TickLoadingBar />
        </Box>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                {isMobile ? <NarrowCell>#</NarrowCell> : <TableCell>#</TableCell>}
                <TableCell>{t('endurance_race.name')}</TableCell>
                {isMobile ? (
                  <NarrowCell align="center">
                    <Tooltip title={t('endurance_race.distance')}>
                      <Straighten />
                    </Tooltip>
                  </NarrowCell>
                ) : (
                  <TableCell align="center">{t('endurance_race.distance')}</TableCell>
                )}
                {!isMobile && <TableCell align="center">{t('endurance_race.delta_leader')}</TableCell>}
                <TableCell align="center">{t('endurance_race.delta_interval')}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(eventRecords ?? eventRecordsCache).map((record, index) => (
                <TableRow key={index} className={getRowClass(record.previousPosition ?? 0, index + 1)}>
                  {isMobile ? <NarrowCell>{index + 1}</NarrowCell> : <TableCell>{index + 1}</TableCell>}
                  <TableCell>
                    <IconNameWithDetailsModal
                      blobId={record.blob.id}
                      name={record.blob.name}
                      color={record.blob.color}
                      renderFullName={!isMobile}
                    />
                  </TableCell>
                  {isMobile ? (
                    <NarrowCell align="center">{getDistance(record)}</NarrowCell>
                  ) : (
                    <TableCell align="center">{getDistance(record)}</TableCell>
                  )}
                  {!isMobile && (
                    <TableCell align="center">
                      {getDelta(record, eventRecordsCache?.[0] ?? eventRecords?.[0], index)}
                    </TableCell>
                  )}
                  <TableCell align="center">
                    {getDelta(
                      record,
                      eventRecordsCache?.[index === 0 ? 0 : index - 1] ?? eventRecords?.[index === 0 ? 0 : index - 1],
                      index,
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginTop={2}>
          <TickLoadingBar />
        </Box>
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
      </CardContent>
    </Paper>
  );
};
