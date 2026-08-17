import { useTranslation } from 'react-i18next';
import { Box, IconButton, Paper, useMediaQuery, useTheme } from '@mui/material';
import type { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDtoOutput';
import { EventType } from '../../../../generated';
import { EventBarChart } from './elimination-scoring-components/EventBarChart';
import { EliminationEventTable } from './elimination-scoring-components/EliminationEventTable';
import { EventCardFrame } from '../shared/EventCardFrame';
import { useMemo, useState } from 'react';
import AccessAlarmIcon from '@mui/icons-material/AccessAlarm';
import TableChartIcon from '@mui/icons-material/TableChart';
import CloseIcon from '@mui/icons-material/Close';
import DynamicTooltip from '../../common/DynamicTooltip';

type EliminationScoringUIProps = {
  eventRecords: EventRecordDto[];
  tick: number;
  loadingNextTick: boolean;
  eventType: EventType;
  eventId?: number;
};

export const EliminationScoringUI = ({
  eventRecords,
  tick,
  loadingNextTick,
  eventType,
  eventId,
}: EliminationScoringUIProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [showTable, setShowTable] = useState(false);

  const tickDisplay = useMemo(() => {
    if (isMobile) {
      return (
        <Box display="flex" alignItems="flex-start" gap={0.5}>
          <AccessAlarmIcon fontSize="small" /> {tick}
        </Box>
      );
    } else {
      return `${t('elimination_event.tick')}: ${tick}`;
    }
  }, [isMobile, tick, t]);

  return (
    <EventCardFrame eventType={eventType} tickDisplay={tickDisplay} showLoader={loadingNextTick}>
      {isMobile ? (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, position: 'relative' }}>
          <DynamicTooltip title={showTable ? t('elimination_event.hide_table') : t('elimination_event.show_table')}>
            <IconButton
              onClick={() => setShowTable((prev) => !prev)}
              sx={{ alignSelf: 'flex-start' }}
              aria-label={showTable ? t('elimination_event.hide_table') : t('elimination_event.show_table')}
            >
              {showTable ? <CloseIcon /> : <TableChartIcon />}
            </IconButton>
          </DynamicTooltip>
          {showTable && (
            <Paper
              elevation={8}
              sx={{
                position: 'absolute',
                top: 48,
                left: 0,
                right: 0,
                zIndex: theme.zIndex.modal,
                maxHeight: '70vh',
                overflowY: 'auto',
                '&::-webkit-scrollbar': { display: 'none' },
                scrollbarWidth: 'none',
              }}
            >
              <EliminationEventTable eventRecords={eventRecords} isMobile={isMobile} eventId={eventId} />
            </Paper>
          )}
          <EventBarChart eventRecords={eventRecords} isMobile={isMobile} />
        </Box>
      ) : (
        <Box display="flex" flexDirection="row">
          <Box>
            <EliminationEventTable eventRecords={eventRecords} isMobile={isMobile} eventId={eventId} />
          </Box>
          <Box flexGrow={1}>
            <EventBarChart eventRecords={eventRecords} isMobile={isMobile} />
          </Box>
        </Box>
      )}
    </EventCardFrame>
  );
};
