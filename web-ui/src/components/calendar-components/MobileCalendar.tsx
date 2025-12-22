import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, styled } from '@mui/material';
import { formatToShort } from '../../utils/sim-time-utils';
import { useTranslation } from 'react-i18next';
import { CalendarDto } from '../../../generated';

interface CalendarProps {
  calendar: CalendarDto[] | undefined;
}

export const MobileCalendar: React.FC<CalendarProps> = ({ calendar }) => {
  const { t } = useTranslation();

  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&.current-event, &.next-event': {
      backgroundColor: theme.palette.action.selected,
      transition: 'background-color 200ms',
    },
  }));

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
            <StyledTableRow
              key={JSON.stringify(event.date)}
              className={event.isCurrent ? 'current-event' : event.isNext ? 'next-event' : ''}
            >
              <TableCell>{formatToShort(event.date)}</TableCell>
              <TableCell>{event.leagueName ?? '-'}</TableCell>
              <TableCell>{t(`enums.event_types.${event.eventType}`, { day: event.round })}</TableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
