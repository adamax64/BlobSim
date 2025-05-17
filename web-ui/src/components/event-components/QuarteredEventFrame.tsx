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
} from '@mui/material';
import {
  ActionsApi,
  BlobCompetitorDto,
  EventDto,
  EventRecordsApi,
  EventType,
  QuarteredEventRecordDto as EventRecordDto,
} from '../../../generated';
import { translateEventType } from '../../utils/EnumTranslationUtils';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { getCurrentQuarter, getBlobIndex, getQuarterEnds, roundToThreeDecimals } from './EventUtils';
import { ProgressButton } from './ProgressButton';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';

interface QuarteredEventFrameProps {
  event: EventDto;
}

export const QuarteredEventFrame = ({ event }: QuarteredEventFrameProps) => {
  const [tick, setTick] = useState(event.actions.length);
  const [isPerforming, setIsPerforming] = useState(false);
  const [isEventFinished, setIsEventFinished] = useState(false);
  const [quarter, setQuarter] = useState(0);
  const [currentBlobIndex, setCurrentBlobIndex] = useState(-1);
  const [nextBlobIndex, setNextBlobIndex] = useState(-1);

  const isOneShot = useMemo(() => event.type === EventType.QuarteredOneShotScoring, [event.type]);
  const quarterEnds = useMemo(
    () => getQuarterEnds(event.competitors.length, isOneShot),
    [isOneShot, event.competitors.length],
  );

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<EventRecordDto[], Error>({
    mutationFn: () => eventRecordsApi.getByEventEventRecordsGet({ eventId: event.id }),
    onSuccess: () => setIsPerforming(false),
  });

  const { mutate: createAction } = useMutation<number, Error, { contender: BlobCompetitorDto }>({
    mutationFn: (params) =>
      actionApi.createActionActionsCreatePost({
        blobCompetitorDto: params.contender,
        tick,
        eventId: event.id,
      }),
    onSuccess: (_) => {
      setTick((prev) => prev + 1);
      getEventRecords();
    },
  });

  useEffect(() => {
    getEventRecords();
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
      createAction({ contender: eventRecords[nextBlobIndex].blob });
    }
  }, [createAction, eventRecords, nextBlobIndex]);

  const renderCellContent = useCallback(
    (record: EventRecordDto, quarterIndex: number) => {
      if (record.next && isPerforming && quarterIndex === quarter - 1) {
        return <CircularProgress />;
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
    [quarter, isPerforming],
  );

  return (
    <Card>
      <CardHeader title={translateEventType(event.type)} />
      <CardContent>
        <Box paddingBottom={2}>
          <ProgressButton
            isStart={tick === 0}
            isEnd={quarter > 4}
            onClickStart={progressEvent}
            onClickNext={progressEvent}
            onClickEnd={() => setIsEventFinished(true)}
          />
        </Box>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow className={currentBlobIndex === 0 ? 'disable-border-bottom' : ''}>
                <TableCell align="center" width={60}>
                  #
                </TableCell>
                <TableCell>Name</TableCell>
                <TableCell align="center" className={highlighByQuarter(1)}>
                  Q1
                </TableCell>
                <TableCell align="center" className={highlighByQuarter(2)}>
                  Q2
                </TableCell>
                <TableCell align="center" className={highlighByQuarter(3)}>
                  Q3
                </TableCell>
                <TableCell align="center" className={highlighByQuarter(4)}>
                  Q4
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {eventRecords?.map((record, index) => (
                <TableRow
                  key={index}
                  className={
                    index === currentBlobIndex
                      ? 'row-current'
                      : index === currentBlobIndex - 1
                        ? 'disable-border-bottom'
                        : ''
                  }
                >
                  <TableCell align="center">{index + 1}</TableCell>
                  <TableCell>{record.blob.name}</TableCell>
                  <TableCell padding="none" align="center" className={highlighByQuarter(1)}>
                    {renderCellContent(record, 0)}
                  </TableCell>
                  <TableCell padding="none" align="center" className={highlighByQuarter(2)}>
                    {renderCellContent(record, 1)}
                  </TableCell>
                  <TableCell padding="none" align="center" className={highlighByQuarter(3)}>
                    {renderCellContent(record, 2)}
                  </TableCell>
                  <TableCell padding="none" align="center" className={highlighByQuarter(4)}>
                    {renderCellContent(record, 3)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
};
