import { BrowseGallery } from '@mui/icons-material';
import {
  Card,
  CardHeader,
  Paper,
  styled,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
} from '@mui/material';
import { useSimTime } from '../../context/SimTimeContext';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { CalendarDto } from '../../../generated';
import { EventChip } from './EventChip';

const TableCellWithBorder = styled(TableCell)(({ theme }) => ({
  borderRight: `1px solid ${theme.palette.divider}`,
  '&:last-child': {
    borderRight: 'none',
  },
}));

interface DesktopCalendarProps {
  calendar: CalendarDto[] | undefined;
}

export const DesktopCalendar: React.FC<DesktopCalendarProps> = ({ calendar }) => {
  const { t } = useTranslation();
  const { simTime, refreshSimTime } = useSimTime();

  useEffect(() => {
    if (!simTime) {
      refreshSimTime();
    }
  }, [simTime, refreshSimTime]);

  const applyCurrentClass = (cellEpoch: number, cellCycle: number): string | undefined => {
    if (cellEpoch === simTime?.epoch && cellCycle === simTime?.cycle) {
      return 'next-event';
    }
    return undefined;
  };

  return (
    <Card sx={{ padding: 2 }}>
      <CardHeader title={t('calendar.season_title', { season: calendar?.[0]?.date.season })} />
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCellWithBorder width={50}>
                <Tooltip title={t('calendar.epoch_cycle')}>
                  <BrowseGallery />
                </Tooltip>
              </TableCellWithBorder>
              <TableCellWithBorder align="center" sx={{ width: '25%' }}>
                I.
              </TableCellWithBorder>
              <TableCellWithBorder align="center" sx={{ width: '25%' }}>
                II.
              </TableCellWithBorder>
              <TableCellWithBorder align="center" sx={{ width: '25%' }}>
                III.
              </TableCellWithBorder>
              <TableCellWithBorder align="center" sx={{ width: '25%' }}>
                IV.
              </TableCellWithBorder>
            </TableRow>
          </TableHead>
          <TableBody>
            {Array.from({ length: 10 }, (_, i) => {
              let isNextSeason = false;
              let epoch = (simTime?.epoch ?? 1) - 1 + i;
              if (epoch >= 32) {
                isNextSeason = true;
                epoch = epoch % 32;
              }
              return (
                <TableRow key={i} sx={{ height: 72 }}>
                  <TableCellWithBorder align="center">{epoch}</TableCellWithBorder>
                  <TableCellWithBorder align="center" className={applyCurrentClass(epoch, 0)}>
                    {isNextSeason ? null : (
                      <EventChip
                        calendar={calendar}
                        epoch={epoch}
                        cycle={0}
                        t={t}
                        isToday={simTime?.epoch === epoch && simTime?.cycle === 0}
                      />
                    )}
                  </TableCellWithBorder>
                  <TableCellWithBorder align="center" className={applyCurrentClass(epoch, 1)}>
                    {isNextSeason ? null : (
                      <EventChip
                        calendar={calendar}
                        epoch={epoch}
                        cycle={1}
                        t={t}
                        isToday={simTime?.epoch === epoch && simTime?.cycle === 1}
                      />
                    )}
                  </TableCellWithBorder>
                  <TableCellWithBorder align="center" className={applyCurrentClass(epoch, 2)}>
                    {isNextSeason ? null : (
                      <EventChip
                        calendar={calendar}
                        epoch={epoch}
                        cycle={2}
                        t={t}
                        isToday={simTime?.epoch === epoch && simTime?.cycle === 2}
                      />
                    )}
                  </TableCellWithBorder>
                  <TableCellWithBorder align="center" className={applyCurrentClass(epoch, 3)}>
                    {isNextSeason ? null : (
                      <EventChip
                        calendar={calendar}
                        epoch={epoch}
                        cycle={3}
                        t={t}
                        isToday={simTime?.epoch === epoch && simTime?.cycle === 3}
                      />
                    )}
                  </TableCellWithBorder>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Card>
  );
};
