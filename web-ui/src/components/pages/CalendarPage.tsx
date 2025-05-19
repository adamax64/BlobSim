import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { useMutation } from '@tanstack/react-query';
import { CalendarApi, CalendarDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { useCallback, useEffect } from 'react';
import { useSimTime } from '../../context/SimTimeContext';
import { formatToShort } from '../../utils/SimTimeUtils';
import { translateEventType } from '../../utils/EnumTranslationUtils';

export const CalendarPage = () => {
  const { simTime } = useSimTime();

  const calendarApi = new CalendarApi(defaultConfig);
  const { data: calendar, mutate: loadCalendar } = useMutation<CalendarDto[], Error>({
    mutationFn: () => calendarApi.getSeasonCalendarCalendarGet(),
  });

  useEffect(() => {
    loadCalendar();
  }, []);

  return (
    <PageFrame>
      <PageTitleCard title="Blob Championship System - Season Calendar" />
      <TableContainer component={Paper} sx={{ padding: 2 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>League</TableCell>
              <TableCell>Event Type</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {calendar?.map((event) => (
              <TableRow className={event.isCurrent ? 'current-event' : event.isNext ? 'next-event' : ''}>
                <TableCell>{formatToShort(event.date)}</TableCell>
                <TableCell>{event.leagueName}</TableCell>
                <TableCell>{translateEventType(event.eventType)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </PageFrame>
  );
};
