import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Divider,
  LinearProgress,
  Paper,
  styled,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { ActionDto, ActionsApi, CompetitionApi, EventDto, EventRecordsApi } from '../../../generated';
import { translateEventType } from '../../utils/EnumTranslationUtils';
import { ProgressButton } from './ProgressButton';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { RaceEventRecordDto as EventRecordDto } from '../../../generated/models/RaceEventRecordDto';
import { getRaceDurationBySize, roundToThreeDecimals } from './EventUtils';
import defaultConfig from '../../default-config';
import { IconName } from '../common/IconName';

const TickLoadingBar = styled(LinearProgress)({
  height: 8,
  borderRadius: 10,
});

interface EnduranceRaceEventFrameProps {
  event: EventDto;
}

export const EnduranceRaceEventFrame = ({ event }: EnduranceRaceEventFrameProps) => {
  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.tick), 0));
  const [isEventFinished, setIsEventFinished] = useState(false);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const [eventRecordsCache, setEventRecordsCache] = useState<EventRecordDto[]>([]);

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const raceDuration = useMemo(() => getRaceDurationBySize(event.competitors.length), [event.competitors.length]);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const actionsApi = new ActionsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (eventId: number) => eventRecordsApi.getRaceEventRecordsRaceGet({ eventId }),
    onSuccess: (data) => {
      setLoadingNextTick(false);
      setEventRecordsCache(data);
      return data;
    },
  });

  const { mutate: createActions } = useMutation<void, Error>({
    mutationFn: () => actionsApi.raceActionsCreateRacePost({ eventId: event.id, tick: tick }),
    onSuccess: () => {
      setTick((prev) => prev + 1);
      getEventRecords(event.id);
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
    getEventRecords(event.id);
  }, [event.id]);

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setLoadingNextTick(true);
      createActions();
    }
  }, [eventRecords, isEventFinished]);

  // Add key listener for spacebar to trigger progressEvent
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' || e.key === ' ') {
        e.preventDefault();
        progressEvent();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [progressEvent]);

  const getDistance = useCallback((record: EventRecordDto) => {
    return roundToThreeDecimals(record.distanceRecords?.[record.distanceRecords?.length - 1]) ?? '-';
  }, []);

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
    <Card>
      <CardHeader title={translateEventType(event.type)} />
      <Divider />
      <CardContent>
        <ProgressButton
          isStart={(eventRecords?.[0]?.distanceRecords?.length ?? 0) === 0}
          isEnd={tick >= raceDuration}
          isEventFinished={isEventFinished}
          onClickStart={progressEvent}
          onClickNext={progressEvent}
          onClickEnd={finishEvent}
        />
        <Typography fontSize={18} fontWeight={600} paddingBottom={2}>
          Tick: {tick} / {raceDuration}
        </Typography>
        <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginBottom={2}>
          <TickLoadingBar />
        </Box>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell width={60}>#</TableCell>
                <TableCell>Name</TableCell>
                <TableCell align="center">Distance</TableCell>
                {!isMobile && <TableCell align="center">Delta leader</TableCell>}
                <TableCell align="center">Delta interval</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(eventRecords ?? eventRecordsCache).map((record, index) => (
                <TableRow key={index} className={getRowClass(record.previousPosition ?? 0, index + 1)}>
                  <TableCell padding="checkbox">{index + 1}</TableCell>
                  <TableCell>
                    <IconName name={record.blob.name} color={record.blob.color} renderFullName={!isMobile} />
                  </TableCell>
                  <TableCell align="center">{getDistance(record)}</TableCell>
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
      </CardContent>
    </Card>
  );
};
