import { TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import { useCallback } from 'react';
import { roundToThreeDecimals } from '../../event-utils';
import { useTranslation } from 'react-i18next';
import { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../../generated/models/EliminationEventRecordDtoOutput';
import { NarrowCell } from '../../../common/StyledComponents';
import { IconNameWithDetailsModal } from '../../../common/IconNameWithDetailsModal';
import { EventTable } from '../../shared/EventTable';
import SkeletonRows from '../../shared/SkeletonRows';

interface EliminationEventTableProps {
  eventRecords: EventRecordDto[];
  isMobile?: boolean;
  eventId?: number;
}

export const EliminationEventTable = ({ eventRecords, isMobile, eventId }: EliminationEventTableProps) => {
  const { t } = useTranslation();

  const getRowClass = useCallback((isEliminated: boolean) => {
    return isEliminated ? 'row-inactive' : '';
  }, []);

  return (
    <EventTable>
      <TableHead>
        <TableRow>
          {isMobile ? <NarrowCell width={30}>#</NarrowCell> : <TableCell width={30}>#</TableCell>}
          <TableCell>{t('elimination_event.name')}</TableCell>
          <TableCell>{t('elimination_event.score')}</TableCell>
          <TableCell>{t('elimination_event.tick_wins')}</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {eventRecords.length > 0 ? (
          eventRecords.map((record, index) => (
            <TableRow key={index} className={getRowClass(record.eliminated ?? false)}>
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
                  detailsDialogVariant="event"
                  eventId={eventId}
                />
              </TableCell>
              <TableCell>
                {!record.lastScore && record.eliminated
                  ? t('elimination_event.eliminated')
                  : (roundToThreeDecimals(record.lastScore) ?? '-')}
              </TableCell>
              <TableCell>{record.tickWins || '-'}</TableCell>
            </TableRow>
          ))
        ) : (
          <SkeletonRows columnCount={4} />
        )}
      </TableBody>
    </EventTable>
  );
};
