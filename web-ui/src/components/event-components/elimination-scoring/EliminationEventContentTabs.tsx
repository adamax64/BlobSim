import { Box, Paper, Tab, Tabs } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { EliminationEventTable } from './EliminationEventTable';
import { EventBarChart } from './EventBarChart';
import { EliminationEventRecordDto as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDto';
import { useState } from 'react';

interface EliminationEventContentTabsProps {
  eventRecords: EventRecordDto[];
  isEventFinished: boolean;
  isMobile: boolean;
}

export const EliminationEventContentTabs = ({
  eventRecords,
  isEventFinished,
  isMobile,
}: EliminationEventContentTabsProps) => {
  const { t } = useTranslation();

  const [index, setIndex] = useState(0);

  return (
    <Box>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={index} onChange={(_, newValue) => setIndex(newValue)}>
          <Tab
            label={t('elimination_event.tab_table')}
            id="elimination-event-tab-table"
            aria-controls="elimination-event-tab-table-content"
          />
          <Tab
            label={t('elimination_event.tab_chart')}
            id="elimination-event-tab-chart"
            aria-controls="elimination-event-tab-chart-content"
          />
        </Tabs>
      </Box>
      <Box role="tabpanel" hidden={index !== 0} id="elimination-event-tab-table-content">
        <EliminationEventTable eventRecords={eventRecords} isEventFinished={isEventFinished} isMobile={isMobile} />
      </Box>
      <Box role="tabpanel" hidden={index !== 1} id="elimination-event-tab-chart-content" flexGrow={1}>
        <Paper>
          <Box paddingBottom={2}>
            <EventBarChart eventRecords={eventRecords} isMobile={isMobile} />
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};
