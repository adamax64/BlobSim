import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import { EventDtoOutput as EventDto, EventType } from '../../../generated';
import { translateEventType } from '../../utils/EnumTranslationUtils';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { getCurrentQuarter, getQuarterEnds } from './EventUtils';

interface QuarteredEventPageProps {
  event: EventDto;
}

export const QuarteredEventPage = ({ event }: QuarteredEventPageProps) => {
  const [tick, setTick] = useState(0);

  const isOneShot = event.type === EventType.QuarteredOneShotScoring;

  useEffect(() => {
    setTick(event.actions.length);
  }, [event.actions.length]);

  const quarterEnds = useMemo(
    () => getQuarterEnds(event.competitors.length, isOneShot),
    [isOneShot, event.competitors.length],
  );

  const quarter = useMemo(() => getCurrentQuarter(quarterEnds, tick), [quarterEnds, tick]);

  const highlighByQuarter = useCallback((index: number) => (quarter === index ? 'column-actual' : ''), [quarter]);

  return (
    <Card>
      <CardHeader title={translateEventType(event.type)} />
      <CardContent>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
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
              {event.eventRecords.map((record, index) => (
                <TableRow key={index}>
                  <TableCell align="center">{index + 1}</TableCell>
                  <TableCell>{record.blob.name}</TableCell>
                  <TableCell align="center" className={highlighByQuarter(1)}>
                    {record.quarters[0].score ?? '-'}
                  </TableCell>
                  <TableCell align="center" className={highlighByQuarter(2)}>
                    {record.quarters[1].score ?? '-'}
                  </TableCell>
                  <TableCell align="center" className={highlighByQuarter(3)}>
                    {record.quarters[2].score ?? '-'}
                  </TableCell>
                  <TableCell align="center" className={highlighByQuarter(4)}>
                    {record.quarters[3].score ?? '-'}
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
