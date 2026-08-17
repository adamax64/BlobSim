import { Box, CircularProgress, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import { useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import type { QuarteredEventRecordDto as EventRecordDto } from '../../../../../generated';
import { IconNameWithDetailsModal } from '../../../common/IconNameWithDetailsModal';
import { roundToThreeDecimals } from '../../event-utils';
import { EventTable } from '../../shared/EventTable';
import SkeletonRows from '../../shared/SkeletonRows';

export interface QuarteredEventTableProps {
  eventRecords: EventRecordDto[];
  quarter: number;
  currentBlobIndex: number;
  isPerforming: boolean;
  isMobile: boolean;
  eventId?: number;
}

export const QuarteredEventTable = ({
  eventRecords,
  quarter,
  currentBlobIndex,
  isPerforming,
  isMobile,
  eventId,
}: QuarteredEventTableProps) => {
  const { t } = useTranslation();

  const highlighByQuarter = useCallback((index: number) => (quarter === index ? 'column-actual' : ''), [quarter]);

  const shouldShowQuarter = useCallback(
    (quarterNum: number) => {
      if (!isMobile) return true;

      switch (quarterNum) {
        case 1:
          return quarter <= 2;
        case 2:
          return quarter <= 3;
        case 3:
          return quarter >= 3;
        case 4:
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
    [quarter, isPerforming],
  );

  const getRowClass = useCallback(
    (record: EventRecordDto, index: number) => {
      if (quarter <= 4 && record.eliminated) {
        return 'row-inactive';
      }
      return index === currentBlobIndex ? 'row-current' : '';
    },
    [currentBlobIndex, quarter],
  );

  return (
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
        {eventRecords.length > 0 ? (
          eventRecords.map((record, index) => (
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
                  detailsDialogVariant="event"
                  eventId={eventId}
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
          ))
        ) : (
          <SkeletonRows columnCount={isMobile ? 4 : 6} />
        )}
      </TableBody>
    </EventTable>
  );
};
