import { Accordion, AccordionDetails, Box, Typography, useMediaQuery, useTheme } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Dispatch, SetStateAction, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { DefaultApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { WinsByEventTypeTable } from './tables/WinsByEventTypeTable';
import { RecordsByLeagueTable } from './tables/RecordsByEventTable';
import { SmallAccordionTitle } from '../common/StyledComponents';

interface EventsTabProps {
  setLoading: Dispatch<SetStateAction<boolean>>;
}

export const EventsTab = ({ setLoading }: EventsTabProps) => {
  const { t } = useTranslation();

  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  const recordsApi = new DefaultApi(defaultConfig);
  const {
    data,
    isPending,
    mutate: fetchData,
  } = useMutation({
    mutationKey: ['fetch-records-data'],
    mutationFn: () => recordsApi.getRecordsByEventTypeHallOfFameRecordsByEventGet(),
  });

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    setLoading(isPending);
  }, [setLoading, isPending]);

  const { recordsByLeague, winsByEvent } = data ?? {};

  return isMobile ? (
    <Box display="flex" flexDirection="column">
      <Accordion defaultExpanded>
        <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
          <Typography variant="body2">{t('hall-of-fame.events-tab.wins_by_event')}</Typography>
        </SmallAccordionTitle>
        <AccordionDetails>
          <WinsByEventTypeTable data={winsByEvent} />
        </AccordionDetails>
      </Accordion>
      {recordsByLeague &&
        recordsByLeague.map((records) => (
          <Accordion defaultExpanded={records.league.level === 1} key={records.league.level}>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{records.league.name}</Typography>
            </SmallAccordionTitle>
            <AccordionDetails>
              <RecordsByLeagueTable data={records.records} />
            </AccordionDetails>
          </Accordion>
        ))}
    </Box>
  ) : (
    <Box display="flex" flexDirection="row" gap={1}>
      <Box display="flex" flexDirection="column" width="50%">
        {recordsByLeague &&
          recordsByLeague.map((records) => (
            <Accordion defaultExpanded={records.league.level === 1} key={records.league.level}>
              <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
                <Typography variant="body2">{records.league.name}</Typography>
              </SmallAccordionTitle>
              <AccordionDetails>
                <RecordsByLeagueTable data={records.records} />
              </AccordionDetails>
            </Accordion>
          ))}
      </Box>
      <Box width="50%">
        <WinsByEventTypeTable data={winsByEvent} title={t('hall-of-fame.events-tab.wins_by_event')} />
      </Box>
    </Box>
  );
};
