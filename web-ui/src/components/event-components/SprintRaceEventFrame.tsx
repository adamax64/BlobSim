import {
  Box,
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
import { SprintEventRecordDto as EventRecordDto } from '../../../generated/models/SprintEventRecordDto';
import { getRaceDurationBySize, roundToThreeDecimals, roundToOneDecimals, roundToTwoDecimals } from './event-utils';
import defaultConfig from '../../default-config';
import { useAuth } from '../../context/AuthContext';
import { useTranslation } from 'react-i18next';
import Straighten from '@mui/icons-material/Straighten';
import ChangeHistoryIcon from '@mui/icons-material/ChangeHistory';
import AccessAlarmIcon from '@mui/icons-material/AccessAlarm';
import { DistanceProgress, NarrowCell, TickLoadingBar } from '../common/StyledComponents';
import { IconNameWithDetailsModal } from '../common/IconNameWithDetailsModal';
import { SnackbarState } from './snackbar-state';

interface SprintRaceEventFrameProps {
  event: EventDto;
  setIsEventFinished: Dispatch<SetStateAction<boolean>>;
  isEventFinished: boolean;
}

export const SprintRaceEventFrame: React.FC<SprintRaceEventFrameProps> = ({
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
    mutationFn: ({ eventId, isPlayback }) => eventRecordsApi.getSprintEventRecordsSprintGet({ eventId, isPlayback }),
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
      competitionApi.saveSprintCompetitionSprintEventResultsPost({
        bodySaveSprintCompetitionSprintEventResultsPost: { event, eventRecords: eventRecords ?? [] },
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
      const currentDistance = record.distanceRecords?.[record.distanceRecords?.length - 1];
      if (currentDistance === undefined || currentDistance === null) {
        return '-';
      }
      const percentage = Math.min((currentDistance / raceDuration) * 100, 100);
      const rounded = isMobile ? roundToOneDecimals(percentage) : roundToTwoDecimals(percentage);
      return rounded !== undefined ? `${rounded}%` : '-';
    },
    [isMobile, raceDuration],
  );

  const firstNotFinishedIndex = useMemo(() => {
    const records = eventRecords ?? eventRecordsCache;
    const filteredIndices = records
      .map((r, index) => ({ isFinished: r.isFinished, index }))
      .filter((value) => !value.isFinished)
      .map((value) => value.index);

    return Math.min(...filteredIndices);
  }, [eventRecords, eventRecordsCache]);

  const getDelta = useCallback(
    (currentRecord: EventRecordDto, otherRecord: EventRecordDto, index: number) => {
      if (index === firstNotFinishedIndex) {
        return '-';
      }
      const distance = currentRecord.distanceRecords[currentRecord.distanceRecords.length - 1];
      const otherDistance = otherRecord.distanceRecords[otherRecord.distanceRecords.length - 1];

      if (!distance || !otherDistance) {
        return '-';
      }

      return roundToThreeDecimals(otherDistance - distance);
    },
    [firstNotFinishedIndex],
  );

  const getRowClass = (previousPosition: number, currentPosition: number, isContenderFinished: boolean): string => {
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
      if (isContenderFinished) {
        return 'cell-finished';
      }
      if (previousPosition > currentPosition) {
        return 'cell-overtake';
      }
      if (currentPosition > previousPosition && tick > 0) {
        return 'cell-fell-behind';
      }
    }
    return '';
  };

  const isEnd = useMemo(() => {
    const records = eventRecords ?? eventRecordsCache;
    return tick >= raceDuration || (records.length > 0 && records.every((record) => record.isFinished === true));
  }, [eventRecords, eventRecordsCache, raceDuration, tick]);

  return (
    <Paper>
      <CardHeader title={t(`enums.event_types.${event.type}`)} />
      <Divider />
      <CardContent>
        {isAuthenticated && (
          <ProgressButton
            isStart={(eventRecords?.[0]?.distanceRecords?.length ?? 0) === 0}
            isEnd={isEnd}
            isEventFinished={isEventFinished}
            disabled={loadingNextTick}
            onClickStart={progressEvent}
            onClickNext={progressEvent}
            onClickEnd={finishEvent}
          />
        )}
        <Typography fontSize={18} fontWeight={600} paddingBottom={2}>
          {t('sprint_race.tick')}: {tick} / {raceDuration}
        </Typography>
        <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginBottom={2}>
          <TickLoadingBar />
        </Box>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                {isMobile ? <NarrowCell>#</NarrowCell> : <TableCell>#</TableCell>}
                <NarrowCell>{t('sprint_race.name')}</NarrowCell>
                {isMobile ? (
                  <NarrowCell align="center">
                    <Tooltip title={t('sprint_race.progress')}>
                      <Straighten />
                    </Tooltip>
                  </NarrowCell>
                ) : (
                  <TableCell width="100%" align="center">
                    {t('sprint_race.progress')}
                  </TableCell>
                )}
                {!isMobile && <TableCell align="center">{t('sprint_race.delta_leader')}</TableCell>}
                {isMobile ? (
                  <NarrowCell align="center">
                    <Tooltip title={t('sprint_race.delta_time')}>
                      <>
                        <ChangeHistoryIcon />/<AccessAlarmIcon />
                      </>
                    </Tooltip>
                  </NarrowCell>
                ) : (
                  <NarrowCell align="center">{t('sprint_race.delta_time')}</NarrowCell>
                )}
              </TableRow>
            </TableHead>
            <TableBody>
              {(eventRecords ?? eventRecordsCache).map((record, index) => (
                <TableRow
                  key={index}
                  className={getRowClass(record.previousPosition ?? 0, index + 1, record.isFinished ?? false)}
                >
                  {isMobile ? <NarrowCell>{index + 1}</NarrowCell> : <TableCell>{index + 1}</TableCell>}
                  <NarrowCell>
                    <IconNameWithDetailsModal
                      blobId={record.blob.id}
                      name={record.blob.name}
                      color={record.blob.color}
                      renderFullName={!isMobile}
                    />
                  </NarrowCell>
                  {isMobile ? (
                    <NarrowCell align="center">{getDistance(record)}</NarrowCell>
                  ) : (
                    <NarrowCell>
                      <Box position="relative" display="flex" alignItems="center">
                        <DistanceProgress
                          variant="determinate"
                          value={Math.min(
                            (record.distanceRecords?.[record.distanceRecords?.length - 1] / raceDuration) * 100,
                            100,
                          )}
                          sx={{
                            width: '100%',
                            backgroundColor: getLightBackgroundColor(record.blob.color),
                            '& .MuiLinearProgress-bar': {
                              backgroundColor: record.blob.color,
                            },
                          }}
                        />
                        <Typography
                          variant="caption"
                          sx={{
                            position: 'absolute',
                            width: '100%',
                            textAlign: 'center',
                            fontWeight: 600,
                            color: 'text.primary',
                            pointerEvents: 'none',
                          }}
                        >
                          {getDistance(record)}
                        </Typography>
                      </Box>
                    </NarrowCell>
                  )}
                  {!isMobile && !isFinished(record) && (
                    <TableCell align="center">
                      {getDelta(
                        record,
                        eventRecordsCache?.[firstNotFinishedIndex] ?? eventRecords?.[firstNotFinishedIndex],
                        index,
                      )}
                    </TableCell>
                  )}
                  <NarrowCell align="center" colSpan={!isMobile && (isFinished(record) || isEnd) ? 2 : 1}>
                    {!isFinished(record)
                      ? isEnd
                        ? 'DNF'
                        : getDelta(
                            record,
                            eventRecordsCache?.[index === 0 ? 0 : index - 1] ??
                              eventRecords?.[index === 0 ? 0 : index - 1],
                            index,
                          )
                      : `${isMobile ? roundToOneDecimals(record.time) : roundToThreeDecimals(record.time)} tick`}
                  </NarrowCell>
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

const isFinished = (record: EventRecordDto) => {
  return record.isFinished && record.time !== undefined && record.time !== null;
};

const getLightBackgroundColor = (hex: string): string => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (!result) return hex;
  const r = parseInt(result[1], 16);
  const g = parseInt(result[2], 16);
  const b = parseInt(result[3], 16);

  // Calculate brightness using relative luminance
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;

  // If color is dark, mix with white to create a light tint
  // If color is light, mix with a bit of white to make it even lighter
  if (brightness < 128) {
    // For dark colors, mix with white (50% white, 50% color) to create a light tint
    const mixR = Math.round(r * 0.5 + 255 * 0.5);
    const mixG = Math.round(g * 0.5 + 255 * 0.5);
    const mixB = Math.round(b * 0.5 + 255 * 0.5);
    return `rgba(${mixR}, ${mixG}, ${mixB}, 0.2)`;
  } else {
    // For light colors, just use a lighter version with opacity
    return `rgba(${r}, ${g}, ${b}, 0.2)`;
  }
};
