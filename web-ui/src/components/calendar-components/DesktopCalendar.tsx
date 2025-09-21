import BrowseGallery from '@mui/icons-material/BrowseGallery';
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
import { useEffect, useRef } from 'react';
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
  const tableContainerRef = useRef<HTMLDivElement>(null);
  const currentEpochRowRef = useRef<HTMLTableRowElement>(null);

  useEffect(() => {
    if (!simTime) {
      refreshSimTime();
    }
  }, [simTime, refreshSimTime]);

  useEffect(() => {
    // Scroll so only one epoch is visible above the current epoch if possible
    if (currentEpochRowRef.current && tableContainerRef.current) {
      const container = tableContainerRef.current;
      const row = currentEpochRowRef.current;
      const rowHeight = row.clientHeight;
      let scrollTo;
      if (simTime?.epoch && simTime.epoch > 0) {
        // Scroll so the row above the current epoch is at the top
        scrollTo = row.offsetTop - container.offsetTop - rowHeight;
      } else {
        // If first epoch, align current epoch to top
        scrollTo = row.offsetTop - container.offsetTop;
      }
      container.scrollTop = scrollTo;
    }
  }, [simTime]);

  const applyCurrentClass = (cellEpoch: number, cellCycle: number): string | undefined => {
    if (cellEpoch === simTime?.epoch && cellCycle === simTime?.cycle) {
      return 'next-event';
    }
    return undefined;
  };

  return (
    <Card sx={{ padding: 2 }}>
      <CardHeader title={t('calendar.season_title', { season: calendar?.[0]?.date.season })} />
      <TableContainer
        component={Paper}
        ref={tableContainerRef}
        sx={{ maxHeight: 'calc(100vh - 208px)', overflowY: 'auto' }}
      >
        <Table stickyHeader>
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
            {Array.from({ length: 32 }, (_, i) => {
              const epoch = i;
              const isCurrentEpoch = simTime?.epoch === epoch;
              return (
                <TableRow key={i} sx={{ height: 72 }} ref={isCurrentEpoch ? currentEpochRowRef : undefined}>
                  <TableCellWithBorder align="center">{epoch}</TableCellWithBorder>
                  {[0, 1, 2, 3].map((cycle) => (
                    <TableCellWithBorder
                      key={cycle}
                      align="center"
                      width="25%"
                      className={applyCurrentClass(epoch, cycle)}
                    >
                      <EventChip
                        calendar={calendar}
                        epoch={epoch}
                        cycle={cycle}
                        t={t}
                        isToday={simTime?.epoch === epoch && simTime?.cycle === cycle}
                      />
                    </TableCellWithBorder>
                  ))}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Card>
  );
};
