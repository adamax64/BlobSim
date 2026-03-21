import {
  Box,
  CircularProgress,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import type { QuarteredEventRecordDtoInput as EventRecordDto, EventType } from '../../../../generated';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';
import { roundToThreeDecimals } from '../event-utils';
import { useCallback } from 'react';
import { EventCardFrame } from '../shared/EventCardFrame';
import { EventTable } from '../shared/EventTable';

type QuarteredEventUIProps = {
  eventRecords: EventRecordDto[];
  quarter: number;
  currentBlobIndex: number;
  isPerforming: boolean;
  isEventFinished: boolean;
  eventType: EventType;
};

export const QuarteredEventUI = ({
  eventRecords,
  quarter,
  currentBlobIndex,
  isPerforming,
  isEventFinished,
  eventType,
}: QuarteredEventUIProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const highlighByQuarter = useCallback((index: number) => (quarter === index ? 'column-actual' : ''), [quarter]);

  const shouldShowQuarter = useCallback(
    (quarterNum: number) => {
      if (!isMobile) return true;

      switch (quarterNum) {
        case 1: // Q1 shows in quarters 1 and 2
          return quarter <= 2;
        case 2: // Q2 shows in quarters 1, 2 and 3
          return quarter <= 3;
        case 3: // Q3 shows in quarters 3 and 4
          return quarter >= 3;
        case 4: // Q4 shows only in quarter 4
          return quarter >= 4;
        default:
          return true;
      }
    },
    [isMobile, quarter],
  );

  const renderCellContent = useCallback(
    (record: EventRecordDto, quarterIndex: number) => {
      if (record.next && isPerforming && quarterIndex === quarter - 1) {
        return <CircularProgress size={26} />;
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
    [quarter, isPerforming, isEventFinished],
  );

  const getRowClass = useCallback(
    (record: EventRecordDto, index: number) => {
      if (isEventFinished) {
        switch (index) {
          case 0:
            return 'row-gold';
          case 1:
            return 'row-silver';
          case 2:
            return 'row-bronze';
        }
      } else {
        if (quarter <= 4 && record.eliminated) {
          return 'row-inactive';
        }
        return index === currentBlobIndex ? 'row-current' : '';
      }
    },
    [currentBlobIndex, isEventFinished, quarter],
  );

  return (
    <EventCardFrame eventType={eventType}>
      <EventTable>
        <TableHead>
          <TableRow>
            <TableCell width={30}>#</TableCell>
            <TableCell>{t('quartered_event.name')}</TableCell>
            {shouldShowQuarter(1) && (
              <TableCell align="center" className={highlighByQuarter(1)}>
                Q1
              </TableCell>
            )}
            {shouldShowQuarter(2) && (
              <TableCell align="center" className={highlighByQuarter(2)}>
                Q2
              </TableCell>
            )}
            {shouldShowQuarter(3) && (
              <TableCell align="center" className={highlighByQuarter(3)}>
                Q3
              </TableCell>
            )}
            {shouldShowQuarter(4) && (
              <TableCell align="center" className={highlighByQuarter(4)}>
                Q4
              </TableCell>
            )}
          </TableRow>
        </TableHead>
        <TableBody>
          {eventRecords.map((record, index) => (
            <TableRow key={index} className={getRowClass(record, index)}>
              <TableCell padding="checkbox" align="center">
                {index + 1}
              </TableCell>
              <TableCell sx={isMobile ? { paddingX: 1 } : {}}>
                <IconNameWithDetailsModal
                  blobId={record.blob.id}
                  name={record.blob.name}
                  color={record.blob.color}
                  renderFullName={!isMobile}
                />
              </TableCell>
              {shouldShowQuarter(1) && (
                <TableCell padding="none" align="center" className={highlighByQuarter(1)}>
                  {renderCellContent(record, 0)}
                </TableCell>
              )}
              {shouldShowQuarter(2) && (
                <TableCell padding="none" align="center" className={highlighByQuarter(2)}>
                  {renderCellContent(record, 1)}
                </TableCell>
              )}
              {shouldShowQuarter(3) && (
                <TableCell padding="none" align="center" className={highlighByQuarter(3)}>
                  {renderCellContent(record, 2)}
                </TableCell>
              )}
              {shouldShowQuarter(4) && (
                <TableCell padding="none" align="center" className={highlighByQuarter(4)}>
                  {renderCellContent(record, 3)}
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </EventTable>
    </EventCardFrame>
  );
};
