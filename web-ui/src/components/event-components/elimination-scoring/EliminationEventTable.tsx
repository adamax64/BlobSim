import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { useCallback } from 'react';
import { IconName } from '../../common/IconName';
import { roundToThreeDecimals } from '../event-utils';
import { useTranslation } from 'react-i18next';
import { EliminationEventRecordDto as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDto';
import { NarrowCell } from '../../common/StyledComponents';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';

interface EliminationEventTableProps {
  eventRecords: EventRecordDto[];
  isEventFinished: boolean;
  isMobile?: boolean;
}

export const EliminationEventTable = ({ eventRecords, isEventFinished, isMobile }: EliminationEventTableProps) => {
  const { t } = useTranslation();

  const getRowClass = useCallback(
    (index: number, isEliminated: boolean) => {
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
        if (isEliminated) {
          return 'row-inactive';
        }
      }
      return '';
    },
    [isEventFinished],
  );

  return (
    <TableContainer component={Paper}>
      <Table size="small">
        <TableHead>
          <TableRow>
            {isMobile ? <NarrowCell width={30}>#</NarrowCell> : <TableCell width={30}>#</TableCell>}
            <TableCell>{t('elimination_event.name')}</TableCell>
            <TableCell>{t('elimination_event.score')}</TableCell>
            <TableCell>{t('elimination_event.tick_wins')}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {eventRecords.map((record, index) => (
            <TableRow key={index} className={getRowClass(index, record.eliminated ?? false)}>
              {isMobile ? (
                <NarrowCell width={30}>{index + 1}</NarrowCell>
              ) : (
                <TableCell width={30}>{index + 1}</TableCell>
              )}
              <TableCell sx={{ display: 'flex' }}>
                <IconNameWithDetailsModal
                  blobId={record.blob.id}
                  name={record.blob.name}
                  color={record.blob.color}
                  renderFullName={!isMobile}
                />
              </TableCell>
              <TableCell>
                {!record.lastScore && record.eliminated
                  ? t('elimination_event.eliminated')
                  : (roundToThreeDecimals(record.lastScore) ?? '-')}
              </TableCell>
              <TableCell>{record.tickWins || '-'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
