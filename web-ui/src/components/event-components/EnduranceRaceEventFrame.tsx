import {
  Box,
  Card,
  CardContent,
  CardHeader,
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
} from '@mui/material';
import { EventDto, EventRecordsApi } from '../../../generated';
import { translateEventType } from '../../utils/EnumTranslationUtils';
import { ProgressButton } from './ProgressButton';
import { useCallback, useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { RaceEventRecordDto as EventRecordDto } from '../../../generated/models/RaceEventRecordDto';
import { roundToThreeDecimals } from './EventUtils';
import defaultConfig from '../../default-config';

const TickLoadingBar = styled(LinearProgress)({
  marginBottom: 14,
  height: 8,
  borderRadius: 10,
});

interface EnduranceRaceEventFrameProps {
  event: EventDto;
}

export const EnduranceRaceEventFrame = ({ event }: EnduranceRaceEventFrameProps) => {
  const [tick, setTick] = useState(0);
  const [isPerforming, setIsPerforming] = useState(false);
  const [isEventFinished, setIsEventFinished] = useState(false);
  const [loadingNextTick, setLoadingNextTick] = useState(false);

  const eventRecordsApi = new EventRecordsApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (eventId: number) => eventRecordsApi.getRaceEventRecordsRaceGet({ eventId }),
    onSuccess: (data) => {
      setIsPerforming(false);
      return data;
    },
  });

  useEffect(() => {
    getEventRecords(event.id);
  }, [event.id]);

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
    if (previousPosition > currentPosition) {
      return 'cell-overtake';
    }
    if (currentPosition > previousPosition) {
      return 'cell-fell-behind';
    }
    return '';
  };

  return (
    <Card sx={{ marginBottom: 3 }}>
      <CardHeader title={translateEventType(event.type)} />
      <CardContent>
        <ProgressButton
          isStart={tick === 0}
          isEnd={false}
          isEventFinished={isEventFinished}
          onClickStart={() => {}}
          onClickNext={() => {}}
          onClickEnd={() => {}}
        />
        <Typography fontSize={18} fontWeight={600} paddingBottom={2}>
          Tick: {tick}
        </Typography>
        <Box visibility={loadingNextTick ? 'visible' : 'hidden'}>
          <TickLoadingBar />
        </Box>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell width={60}>#</TableCell>
                <TableCell>Name</TableCell>
                <TableCell align="center">Distance</TableCell>
                <TableCell align="center">Delta leader</TableCell>
                <TableCell align="center">Delta interval</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {eventRecords?.map((record, index) => (
                <TableRow key={index} className={getRowClass(record.previousPosition ?? 0, index + 1)}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{record.blob.name}</TableCell>
                  <TableCell align="center">{getDistance(record)}</TableCell>
                  <TableCell align="center">{getDelta(record, eventRecords[0], index)}</TableCell>
                  <TableCell align="center">
                    {getDelta(record, eventRecords[index === 0 ? 0 : index - 1], index)}
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
