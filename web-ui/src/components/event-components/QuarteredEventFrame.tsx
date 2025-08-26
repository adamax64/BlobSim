import {
  Box,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  useMediaQuery,
  useTheme,
  Snackbar,
  Alert,
} from '@mui/material';
import {
  ActionsApi,
  BlobCompetitorDto,
  EventDto,
  EventType,
  QuarteredEventRecordDto as EventRecordDto,
  CompetitionApi,
  EventRecordsApi,
} from '../../../generated';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { getCurrentQuarter, getQuarterEnds, roundToThreeDecimals } from './EventUtils';
import { ProgressButton } from './ProgressButton';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { IconName } from '../common/IconName';
import { useAuth } from '../../context/AuthContext';
import { useTranslation } from 'react-i18next';

type SnackbarState = {
  message: string | null;
  severity: 'error' | 'success' | 'info' | 'warning';
  anchorOrigin: { vertical: 'top' | 'bottom'; horizontal: 'left' | 'center' | 'right' };
};

interface QuarteredEventFrameProps {
  event: EventDto;
}

export const QuarteredEventFrame: React.FC<QuarteredEventFrameProps> = ({ event }) => {
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();

  const [tick, setTick] = useState(event.actions.reduce((sum, action) => sum + action.scores.length, 0));
  const [isPerforming, setIsPerforming] = useState(false);
  const [isEventFinished, setIsEventFinished] = useState(false);
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

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const isOneShot = useMemo(() => event.type === EventType.QuarteredOneShotScoring, [event.type]);
  const quarterEnds = useMemo(
    () => getQuarterEnds(event.competitors.length, isOneShot),
    [isOneShot, event.competitors.length],
  );

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (eventId: number) => eventRecordsApi.getQuarteredEventRecordsQuarteredGet({ eventId }),
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

  const { mutate: createAction } = useMutation<{ newRecord: boolean }, Error, { contender: BlobCompetitorDto }>({
    mutationFn: (params) =>
      actionApi.quarteredActionsCreateQuarteredPost({
        blobCompetitorDto: params.contender,
        eventId: event.id,
      }),
    onSuccess: (data) => {
      if (data?.newRecord) {
        setSnackbarState({
          message: t('quartered_event.new_record', { name: eventRecordsCache[currentBlobIndex]?.blob.name }),
          severity: 'success',
          anchorOrigin: { vertical: 'top', horizontal: 'center' },
        });
        setSnackbarOpen(true);
      }
      setTick((prev: number) => prev + 1);
      getEventRecords(event.id);
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
    getEventRecords(event.id);
  }, [event.id]);

  useEffect(() => {
    setQuarter(getCurrentQuarter(quarterEnds, tick));
  }, [tick, quarterEnds]);

  useEffect(() => {
    if (eventRecords) {
      setCurrentBlobIndex(eventRecords.findIndex((record) => record.current));
      setNextBlobIndex(eventRecords.findIndex((record) => record.next));
    }
  }, [eventRecords]);

  const highlighByQuarter = useCallback((index: number) => (quarter === index ? 'column-actual' : ''), [quarter]);

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setCurrentBlobIndex(nextBlobIndex);
      setIsPerforming(true);
      setTimeout(() => {
        createAction({ contender: eventRecords[nextBlobIndex].blob });
      }, 1000);
    }
  }, [createAction, eventRecords, nextBlobIndex]);

  const renderCellContent = useCallback(
    (record: EventRecordDto, quarterIndex: number) => {
      if (record.next && isPerforming && quarterIndex === quarter - 1) {
        return <CircularProgress size={26} />;
      }

      const currentScore = record.quarters[quarterIndex];

      // If someone is performing, no need to color the scores
      if (isPerforming) {
        return roundToThreeDecimals(currentScore.score) ?? '-';
      }

      const cellClasses = [];
      if (currentScore.best) {
        cellClasses.push('cell-best');
      }
      if (currentScore.personalBest) {
        cellClasses.push('cell-personal-best');
      }
      if (currentScore.latestScore) {
        cellClasses.push('cell-not-improved');
      }

      return (
        <Box className={cellClasses.join(' ')}>
          {currentScore.latestScore
            ? roundToThreeDecimals(currentScore.latestScore)
            : (roundToThreeDecimals(currentScore.score) ?? '-')}
        </Box>
      );
    },
    [quarter, isPerforming, isEventFinished],
  );

  const getRowClass = useCallback(
    (record: EventRecordDto, index: number) => {
      if (isEventFinished) {
        switch (index) {
          case 0:
            return 'row-gold';
          case 1:
            return 'row-silver';
          case 2:
            return 'row-bronze';
        }
      } else {
        if (quarter <= 4 && record.eliminated) {
          return 'row-inactive';
        }
        return index === currentBlobIndex ? 'row-current' : '';
      }
    },
    [currentBlobIndex, isEventFinished, quarter],
  );

  const shouldShowQuarter = useCallback(
    (quarterNum: number) => {
      if (!isMobile) return true;

      switch (quarterNum) {
        case 1: // Q1 shows in quarters 1 and 2
          return quarter <= 2;
        case 2: // Q2 shows in quarters 1, 2 and 3
          return quarter <= 3;
        case 3: // Q3 shows in quarters 3 and 4
          return quarter >= 3;
        case 4: // Q4 shows only in quarter 4
          return quarter >= 4;
        default:
          return true;
      }
    },
    [isMobile, quarter],
  );

  return (
    <Card>
      <CardHeader title={t(`event_types.${event.type}`)} />
      <CardContent>
        {isAuthenticated && (
          <ProgressButton
            isStart={tick === 0}
            isEnd={quarter > 4}
            isEventFinished={isEventFinished}
            disabled={isPerforming}
            onClickStart={progressEvent}
            onClickNext={progressEvent}
            onClickEnd={finishEvent}
          />
        )}
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell width={30}>#</TableCell>
                <TableCell>{t('quartered_event.name')}</TableCell>
                {shouldShowQuarter(1) && (
                  <TableCell align="center" className={highlighByQuarter(1)}>
                    Q1
                  </TableCell>
                )}
                {shouldShowQuarter(2) && (
                  <TableCell align="center" className={highlighByQuarter(2)}>
                    Q2
                  </TableCell>
                )}
                {shouldShowQuarter(3) && (
                  <TableCell align="center" className={highlighByQuarter(3)}>
                    Q3
                  </TableCell>
                )}
                {shouldShowQuarter(4) && (
                  <TableCell align="center" className={highlighByQuarter(4)}>
                    Q4
                  </TableCell>
                )}
              </TableRow>
            </TableHead>
            <TableBody>
              {(eventRecords ?? eventRecordsCache).map((record, index) => (
                <TableRow key={index} className={getRowClass(record, index)}>
                  <TableCell padding="checkbox" align="center">
                    {index + 1}
                  </TableCell>
                  <TableCell sx={isMobile ? { paddingX: 1 } : {}}>
                    <IconName name={record.blob.name} color={record.blob.color} renderFullName={!isMobile} />
                  </TableCell>
                  {shouldShowQuarter(1) && (
                    <TableCell padding="none" align="center" className={highlighByQuarter(1)}>
                      {renderCellContent(record, 0)}
                    </TableCell>
                  )}
                  {shouldShowQuarter(2) && (
                    <TableCell padding="none" align="center" className={highlighByQuarter(2)}>
                      {renderCellContent(record, 1)}
                    </TableCell>
                  )}
                  {shouldShowQuarter(3) && (
                    <TableCell padding="none" align="center" className={highlighByQuarter(3)}>
                      {renderCellContent(record, 2)}
                    </TableCell>
                  )}
                  {shouldShowQuarter(4) && (
                    <TableCell padding="none" align="center" className={highlighByQuarter(4)}>
                      {renderCellContent(record, 3)}
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
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
      </CardContent>
    </Card>
  );
};
