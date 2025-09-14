import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { formatToShort } from '../../utils/sim-time-utils';
import { useTranslation } from 'react-i18next';
import { CalendarDto } from '../../../generated';

interface CalendarProps {
  calendar: CalendarDto[] | undefined;
}

export const MobileCalendar: React.FC<CalendarProps> = ({ calendar }) => {
  const { t } = useTranslation();

  return (
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
              <TableCell>{t(`enums.event_types.${event.eventType}`)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
