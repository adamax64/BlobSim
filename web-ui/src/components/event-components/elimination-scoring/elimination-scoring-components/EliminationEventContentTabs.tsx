import { Box, Paper, Tab, Tabs } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { EliminationEventTable } from './EliminationEventTable';
import { EventBarChart } from './EventBarChart';
import { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../../generated/models/EliminationEventRecordDtoOutput';
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
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Box sx={{ borderColor: 'divider' }}>
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
      <Box
        role="tabpanel"
        hidden={index !== 0}
        id="elimination-event-tab-table-content"
        sx={{
          flex: 1,
          overflow: 'visible',
          display: index === 0 ? 'flex' : 'none',
          flexDirection: 'column',
          paddingBottom: 2,
        }}
      >
        <EliminationEventTable eventRecords={eventRecords} isEventFinished={isEventFinished} isMobile={isMobile} />
      </Box>
      <Box
        role="tabpanel"
        hidden={index !== 1}
        id="elimination-event-tab-chart-content"
        sx={{
          flex: 1,
          overflow: 'visible',
          display: index === 1 ? 'flex' : 'none',
          paddingBottom: 2,
        }}
      >
        <EventBarChart eventRecords={eventRecords} isMobile={isMobile} />
      </Box>
    </Box>
  );
};
