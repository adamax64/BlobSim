import { useTranslation } from 'react-i18next';
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
import Straighten from '@mui/icons-material/Straighten';
import ChangeHistoryIcon from '@mui/icons-material/ChangeHistory';
import AccessAlarmIcon from '@mui/icons-material/AccessAlarm';
import type { SprintEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/SprintEventRecordDtoOutput';
import { EventType } from '../../../../generated';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';
import { useCallback, useMemo } from 'react';
import { roundToOneDecimals, roundToThreeDecimals, roundToTwoDecimals } from '../event-utils';
import { DistanceProgress, NarrowCell, TickLoadingBar } from '../../common/StyledComponents';
import { EventCardFrame } from '../shared/EventCardFrame';
import { EventTable } from '../shared/EventTable';

type SprintRaceUIProps = {
  eventRecords: EventRecordDto[];
  tick: number;
  raceDuration: number;
  loadingNextTick: boolean;
  isEventFinished: boolean;
  eventType: EventType;
  isEnd: boolean;
};

export const SprintRaceUI = ({
  eventRecords,
  tick,
  raceDuration,
  loadingNextTick,
  isEventFinished,
  eventType,
  isEnd,
}: SprintRaceUIProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const getDistance = useCallback(
    (record: EventRecordDto) => {
      const currentDistance = record.distanceRecords?.[record.distanceRecords?.length - 1];
      if (currentDistance === undefined || currentDistance === null) {
        return '-';
      }
      const percentage = Math.min((currentDistance / raceDuration) * 100, 100);
      const rounded = isMobile ? roundToOneDecimals(percentage) : roundToTwoDecimals(percentage);
      return rounded !== undefined ? `${rounded}%` : '-';
    },
    [isMobile, raceDuration],
  );

  const firstNotFinishedIndex = useMemo(() => {
    const filteredIndices = eventRecords
      .map((r, index) => ({ isFinished: r.isFinished, index }))
      .filter((value) => !value.isFinished)
      .map((value) => value.index);

    return Math.min(...filteredIndices);
  }, [eventRecords]);

  const getDelta = useCallback(
    (currentRecord: EventRecordDto, otherRecord: EventRecordDto, index: number) => {
      if (index === firstNotFinishedIndex) {
        return '-';
      }
      const distance = currentRecord.distanceRecords[currentRecord.distanceRecords.length - 1];
      const otherDistance = otherRecord.distanceRecords[otherRecord.distanceRecords.length - 1];

      if (!distance || !otherDistance) {
        return '-';
      }

      return roundToThreeDecimals(otherDistance - distance);
    },
    [firstNotFinishedIndex],
  );

  const getRowClass = (previousPosition: number, currentPosition: number, isContenderFinished: boolean): string => {
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
      if (isContenderFinished) {
        return 'cell-finished';
      }
      if (previousPosition > currentPosition) {
        return 'cell-overtake';
      }
      if (currentPosition > previousPosition && tick > 0) {
        return 'cell-fell-behind';
      }
    }
    return '';
  };

  const tickDisplay = useMemo(() => {
    if (isMobile) {
      return (
        <Box display="flex" alignItems="flex-start" gap={0.5}>
          <AccessAlarmIcon fontSize="small" /> {tick} / {raceDuration}
        </Box>
      );
    } else {
      return `${t('sprint_race.tick')}: ${tick} / ${raceDuration}`;
    }
  }, [isMobile, t, tick, raceDuration]);

  return (
    <EventCardFrame eventType={eventType} tickDisplay={tickDisplay}>
      <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginBottom={2}>
        <TickLoadingBar />
      </Box>
      <EventTable>
        <TableHead>
          <TableRow>
            {isMobile ? <NarrowCell>#</NarrowCell> : <TableCell>#</TableCell>}
            <NarrowCell>{t('sprint_race.name')}</NarrowCell>
            {isMobile ? (
              <NarrowCell align="center">
                <Tooltip title={t('sprint_race.progress')}>
                  <Straighten />
                </Tooltip>
              </NarrowCell>
            ) : (
              <TableCell width="100%" align="center">
                {t('sprint_race.progress')}
              </TableCell>
            )}
            {!isMobile && <TableCell align="center">{t('sprint_race.delta_leader')}</TableCell>}
            {isMobile ? (
              <NarrowCell align="center">
                <Tooltip title={t('sprint_race.delta_time')}>
                  <>
                    <ChangeHistoryIcon />/<AccessAlarmIcon />
                  </>
                </Tooltip>
              </NarrowCell>
            ) : (
              <NarrowCell align="center">{t('sprint_race.delta_time')}</NarrowCell>
            )}
          </TableRow>
        </TableHead>
        <TableBody>
          {eventRecords.map((record, index) => (
            <TableRow
              key={index}
              className={getRowClass(record.previousPosition ?? 0, index + 1, record.isFinished ?? false)}
            >
              {isMobile ? <NarrowCell>{index + 1}</NarrowCell> : <TableCell>{index + 1}</TableCell>}
              <NarrowCell>
                <IconNameWithDetailsModal
                  blobId={record.blob.id}
                  name={record.blob.name}
                  color={record.blob.color}
                  renderFullName={!isMobile}
                />
              </NarrowCell>
              {isMobile ? (
                <NarrowCell align="center">{getDistance(record)}</NarrowCell>
              ) : (
                <NarrowCell>
                  <Box position="relative" display="flex" alignItems="center">
                    <DistanceProgress
                      variant="determinate"
                      value={Math.min(
                        ((record.distanceRecords?.[record.distanceRecords?.length - 1] ?? 0) / raceDuration) * 100,
                        100,
                      )}
                      sx={{
                        backgroundColor: getLightBackgroundColor(record.blob.color),
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: record.blob.color,
                        },
                      }}
                    />
                    <Typography
                      variant="caption"
                      sx={{
                        position: 'absolute',
                        width: '100%',
                        textAlign: 'center',
                        fontWeight: 600,
                        color: 'text.primary',
                        pointerEvents: 'none',
                      }}
                    >
                      {getDistance(record)}
                    </Typography>
                  </Box>
                </NarrowCell>
              )}
              {!isMobile && !isFinished(record) && (
                <TableCell align="center">{getDelta(record, eventRecords?.[firstNotFinishedIndex], index)}</TableCell>
              )}
              <NarrowCell align="center" colSpan={!isMobile && (isFinished(record) || isEnd) ? 2 : 1}>
                {!isFinished(record)
                  ? isEnd
                    ? 'DNF'
                    : getDelta(record, eventRecords?.[index === 0 ? 0 : index - 1], index)
                  : `${isMobile ? roundToOneDecimals(record.time) : roundToThreeDecimals(record.time)} tick`}
              </NarrowCell>
            </TableRow>
          ))}
        </TableBody>
      </EventTable>
    </EventCardFrame>
  );
};

const isFinished = (record: EventRecordDto) => {
  return record.isFinished && record.time !== undefined && record.time !== null;
};

const getLightBackgroundColor = (hex: string): string => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (!result) return hex;
  const r = parseInt(result[1], 16);
  const g = parseInt(result[2], 16);
  const b = parseInt(result[3], 16);

  // Calculate brightness using relative luminance
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;

  // If color is dark, mix with white to create a light tint
  // If color is light, mix with a bit of white to make it even lighter
  if (brightness < 128) {
    // For dark colors, mix with white (50% white, 50% color) to create a light tint
    const mixR = Math.round(r * 0.5 + 255 * 0.5);
    const mixG = Math.round(g * 0.5 + 255 * 0.5);
    const mixB = Math.round(b * 0.5 + 255 * 0.5);
    return `rgba(${mixR}, ${mixG}, ${mixB}, 0.2)`;
  } else {
    // For light colors, just use a lighter version with opacity
    return `rgba(${r}, ${g}, ${b}, 0.2)`;
  }
};
