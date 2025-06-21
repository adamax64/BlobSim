import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { useMutation } from '@tanstack/react-query';
import { CalendarApi, CalendarDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { useEffect } from 'react';
import { formatToShort } from '../../utils/SimTimeUtils';
import { useTranslation } from 'react-i18next';

export const CalendarPage = () => {
  const calendarApi = new CalendarApi(defaultConfig);
  const { t } = useTranslation();
  const { data: calendar, mutate: loadCalendar } = useMutation<CalendarDto[], Error>({
    mutationFn: () => calendarApi.getSeasonCalendarCalendarGet(),
  });

  useEffect(() => {
    loadCalendar();
  }, []);

  return (
    <PageFrame>
      <PageTitleCard title={t('calendar.title')} />
      <TableContainer component={Paper} sx={{ padding: 2 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>{t('calendar.date')}</TableCell>
              <TableCell>{t('calendar.league')}</TableCell>
              <TableCell>{t('calendar.event_type')}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {calendar?.map((event) => (
              <TableRow
                key={JSON.stringify(event.date)}
                className={event.isCurrent ? 'current-event' : event.isNext ? 'next-event' : ''}
              >
                <TableCell>{formatToShort(event.date)}</TableCell>
                <TableCell>{event.leagueName}</TableCell>
                <TableCell>{t(`event_types.${event.eventType}`)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </PageFrame>
  );
};
