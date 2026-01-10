import { Box, Tab, Tabs } from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ChronologyTab } from '../hall-of-fame-components/ChronologyTab';
import { TitlesTab } from '../hall-of-fame-components/TitlesTab';
import { EventsTab } from '../hall-of-fame-components/EventsTab';

export const HallOfFamePage = () => {
  const { t } = useTranslation();

  const [loading, setLoading] = useState(false);
  const [index, setIndex] = useState(0);

  return (
    <PageFrame showLoading={loading} pageName="hall-of-fame">
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={index} onChange={(_, newValue) => setIndex(newValue)}>
          <Tab
            label={t('hall-of-fame.chronology-tab.title')}
            id="hall-of-fame-tab-chronology"
            aria-controls="hall-of-fame-tab-chronology-content"
          />
          <Tab
            label={t('hall-of-fame.titles-tab.title')}
            id="hall-of-fame-tab-titles"
            aria-controls="hall-of-fame-tab-titles-content"
          />
          <Tab
            label={t('hall-of-fame.events-tab.title')}
            id="hall-of-fame-tab-events"
            aria-controls="hall-of-fame-tab-events-content"
          />
        </Tabs>
      </Box>
      <Box role="tabpanel" hidden={index !== 0} id="hall-of-fame-tab-chronology-content">
        <ChronologyTab setLoading={setLoading} />
      </Box>
      <Box role="tabpanel" hidden={index !== 1} id="hall-of-fame-tab-titles-content">
        <TitlesTab setLoading={setLoading} />
      </Box>
      <Box role="tabpanel" hidden={index !== 2} id="hall-of-fame-tab-events-content">
        <EventsTab />
      </Box>
    </PageFrame>
  );
};
