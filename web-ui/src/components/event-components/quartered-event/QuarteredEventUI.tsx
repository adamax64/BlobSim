import { Box, IconButton, Paper, useMediaQuery, useTheme } from '@mui/material';
import { useTranslation } from 'react-i18next';
import type { QuarteredEventRecordDto as EventRecordDto, EventType } from '../../../../generated';
import { useState } from 'react';
import { EventCardFrame } from '../shared/EventCardFrame';
import { QuarteredEventTable } from './quartered-event-components/QuarteredEventTable';
import { QuarteredEventChart } from './quartered-event-components/QuarteredEventChart';
import TableChartIcon from '@mui/icons-material/TableChart';
import CloseIcon from '@mui/icons-material/Close';
import DynamicTooltip from '../../common/DynamicTooltip';

type QuarteredEventUIProps = {
  eventRecords: EventRecordDto[];
  quarter: number;
  currentBlobIndex: number;
  isPerforming: boolean;
  eventType: EventType;
  eventId?: number;
};

export const QuarteredEventUI = ({
  eventRecords,
  quarter,
  currentBlobIndex,
  isPerforming,
  eventType,
  eventId,
}: QuarteredEventUIProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [showTable, setShowTable] = useState(false);

  return (
    <EventCardFrame eventType={eventType}>
      {isMobile ? (
        <Box flexDirection="column" gap={1} position="relative" height="calc(90vh - 150px)" display="flex">
          <DynamicTooltip title={showTable ? t('quartered_event.hide_table') : t('quartered_event.show_table')}>
            <IconButton
              onClick={() => setShowTable((prev) => !prev)}
              sx={{ alignSelf: 'flex-start' }}
              aria-label={showTable ? t('quartered_event.hide_table') : t('quartered_event.show_table')}
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
                overflowY: 'auto',
                '&::-webkit-scrollbar': { display: 'none' },
                scrollbarWidth: 'none',
              }}
            >
              <QuarteredEventTable
                eventRecords={eventRecords}
                quarter={quarter}
                currentBlobIndex={currentBlobIndex}
                isPerforming={isPerforming}
                isMobile={isMobile}
                eventId={eventId}
              />
            </Paper>
          )}
          <Box sx={{ flex: 1, minHeight: 0 }}>
            <QuarteredEventChart eventRecords={eventRecords} />
          </Box>
        </Box>
      ) : (
        <Box display="flex" flexDirection="row" height="calc(90vh - 150px)">
          <Box
            flex={1}
            sx={{
              overflowY: 'auto',
              '&::-webkit-scrollbar': {
                display: 'none',
              },
              scrollbarWidth: 'none',
            }}
          >
            <QuarteredEventTable
              eventRecords={eventRecords}
              quarter={quarter}
              currentBlobIndex={currentBlobIndex}
              isPerforming={isPerforming}
              isMobile={isMobile}
              eventId={eventId}
            />
          </Box>
          <Box sx={{ minWidth: 0, height: '100%' }}>
            <QuarteredEventChart eventRecords={eventRecords} />
          </Box>
        </Box>
      )}
    </EventCardFrame>
  );
};
