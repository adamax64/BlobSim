import {
  Box,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  useTheme,
  useMediaQuery,
  Tooltip,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import type { RaceEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/RaceEventRecordDtoOutput';
import { EventType } from '../../../../generated';
import { TickLoadingBar } from '../../common/StyledComponents';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';
import Straighten from '@mui/icons-material/Straighten';
import { useCallback } from 'react';
import { roundToOneDecimals, roundToThreeDecimals } from '../event-utils';
import { NarrowCell } from '../../common/StyledComponents';
import { EventCardFrame } from '../shared/EventCardFrame';
import { EventTable } from '../shared/EventTable';

type EnduranceRaceUIProps = {
  eventRecords: EventRecordDto[];
  tick: number;
  loadingNextTick: boolean;
  isEventFinished: boolean;
  eventType: EventType;
  raceDuration: number;
};

export const EnduranceRaceUI = ({
  eventRecords,
  tick,
  loadingNextTick,
  isEventFinished,
  eventType,
  raceDuration,
}: EnduranceRaceUIProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const getDistance = useCallback(
    (record: EventRecordDto) => {
      return isMobile
        ? (roundToOneDecimals(record.distanceRecords?.[record.distanceRecords?.length - 1]) ?? '-')
        : (roundToThreeDecimals(record.distanceRecords?.[record.distanceRecords?.length - 1]) ?? '-');
    },
    [isMobile],
  );

  const getDelta = useCallback((currentRecord: EventRecordDto, otherRecord: EventRecordDto, index: number) => {
    if (index === 0) {
      return '-';
    }
    const distance = currentRecord.distanceRecords[currentRecord.distanceRecords.length - 1];
    const otherDistance = otherRecord.distanceRecords[otherRecord.distanceRecords.length - 1];

    if (!distance || !otherDistance) {
      return '-';
    }

    return roundToThreeDecimals(otherDistance - distance);
  }, []);

  const getRowClass = (previousPosition: number, currentPosition: number): string => {
    if (isEventFinished) {
      switch (currentPosition) {
        case 1:
          return 'row-gold';
        case 2:
          return 'row-silver';
        case 3:
          return 'row-bronze';
      }
    } else {
      if (previousPosition > currentPosition) {
        return 'cell-overtake';
      }
      if (currentPosition > previousPosition && tick > 0) {
        return 'cell-fell-behind';
      }
    }
    return '';
  };

  return (
    <EventCardFrame eventType={eventType}>
      <Typography fontSize={18} fontWeight={600} paddingBottom={2}>
        {t('endurance_race.tick')}: {tick} / {raceDuration}
      </Typography>
      <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginBottom={2}>
        <TickLoadingBar />
      </Box>
      <EventTable>
        <TableHead>
          <TableRow>
            {isMobile ? <NarrowCell>#</NarrowCell> : <TableCell>#</TableCell>}
            <TableCell>{t('endurance_race.name')}</TableCell>
            {isMobile ? (
              <NarrowCell align="center">
                <Tooltip title={t('endurance_race.distance')}>
                  <Straighten />
                </Tooltip>
              </NarrowCell>
            ) : (
              <TableCell align="center">{t('endurance_race.distance')}</TableCell>
            )}
            {!isMobile && <TableCell align="center">{t('endurance_race.delta_leader')}</TableCell>}
            <TableCell align="center">{t('endurance_race.delta_interval')}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {eventRecords.map((record, index) => (
            <TableRow key={index} className={getRowClass(record.previousPosition ?? 0, index + 1)}>
              {isMobile ? <NarrowCell>{index + 1}</NarrowCell> : <TableCell>{index + 1}</TableCell>}
              <TableCell>
                <IconNameWithDetailsModal
                  blobId={record.blob.id}
                  name={record.blob.name}
                  color={record.blob.color}
                  renderFullName={!isMobile}
                />
              </TableCell>
              {isMobile ? (
                <NarrowCell align="center">{getDistance(record)}</NarrowCell>
              ) : (
                <TableCell align="center">{getDistance(record)}</TableCell>
              )}
              {!isMobile && <TableCell align="center">{getDelta(record, eventRecords?.[0], index)}</TableCell>}
              <TableCell align="center">
                {getDelta(record, eventRecords?.[index === 0 ? 0 : index - 1], index)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </EventTable>
    </EventCardFrame>
  );
};
