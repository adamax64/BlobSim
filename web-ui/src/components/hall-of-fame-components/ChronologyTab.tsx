import { useTranslation } from 'react-i18next';
import { DefaultApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { Dispatch, SetStateAction, useEffect, useMemo } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Box } from '@mui/system';
import { Accordion, AccordionDetails, Typography, useMediaQuery, useTheme } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { GrandmasterChronologyTable } from './tables/GrandmasterChronologyTable';
import { ChampionsChronologyTable } from './tables/ChampionsChronologyTable';
import { SmallAccordionTitle } from '../common/StyledComponents';

interface ChronologyTabProps {
  setLoading: Dispatch<SetStateAction<boolean>>;
}

export const ChronologyTab = ({ setLoading }: ChronologyTabProps) => {
  const { t } = useTranslation();

  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  const chronologyApi = new DefaultApi(defaultConfig);
  const {
    data,
    isPending,
    mutate: fetchData,
  } = useMutation({
    mutationKey: ['fetch-chronology-data'],
    mutationFn: () => chronologyApi.getTitlesChronologyHallOfFameChronologyGet(),
  });

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    setLoading(isPending);
  }, [setLoading, isPending]);

  const { leagueChampions, grandmasters } = data ?? {};
  const topLeague = useMemo(() => {
    if (!leagueChampions || leagueChampions.length === 0) return null;
    return leagueChampions.find((league) => league.league.level === 1) || null;
  }, [leagueChampions]);
  const dropoutLeague = useMemo(() => {
    if (!leagueChampions || leagueChampions.length === 0) return null;
    return leagueChampions.find((league) => league.league.level === 0) || null;
  }, [leagueChampions]);
  const otherLeagues = useMemo(() => {
    if (!leagueChampions || leagueChampions.length === 0) return [];
    return leagueChampions.filter((league) => league.league.level !== 1 && league.league.level !== 0);
  }, [leagueChampions]);

  return (
    <Box display="flex" flexDirection="column">
      {isMobile ? (
        <>
          {topLeague && (
            <Accordion defaultExpanded>
              <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
                <Typography variant="body2">{topLeague.league.name}</Typography>
              </SmallAccordionTitle>
              <AccordionDetails>
                <ChampionsChronologyTable leagueChampions={topLeague} />
              </AccordionDetails>
            </Accordion>
          )}
          {grandmasters && (
            <Accordion>
              <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
                <Typography variant="body2">
                  {t('hall-of-fame.chronology-tab.table.grandmaster_table_title')}
                </Typography>
              </SmallAccordionTitle>
              <AccordionDetails>
                <GrandmasterChronologyTable grandmasters={grandmasters} />
              </AccordionDetails>
            </Accordion>
          )}
          {dropoutLeague && (
            <Accordion defaultExpanded>
              <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
                <Typography variant="body2">{dropoutLeague.league.name}</Typography>
              </SmallAccordionTitle>
              <AccordionDetails>
                <ChampionsChronologyTable leagueChampions={dropoutLeague} />
              </AccordionDetails>
            </Accordion>
          )}
          {otherLeagues.length > 0 &&
            otherLeagues.map((league) => (
              <Accordion key={league.league.id}>
                <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="body2">{league.league.name}</Typography>
                </SmallAccordionTitle>
                <AccordionDetails>
                  <ChampionsChronologyTable leagueChampions={league} />
                </AccordionDetails>
              </Accordion>
            ))}
        </>
      ) : (
        <>
          <Accordion defaultExpanded sx={{ flexGrow: 1 }}>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.chronology-tab.highlighted')}</Typography>
            </SmallAccordionTitle>
            <AccordionDetails sx={{ display: 'flex', flexDirection: 'row', flexGrow: 1, gap: 2 }}>
              {topLeague && <ChampionsChronologyTable leagueChampions={topLeague} />}
              {grandmasters && <GrandmasterChronologyTable grandmasters={grandmasters} />}
              {dropoutLeague && <ChampionsChronologyTable leagueChampions={dropoutLeague} />}
            </AccordionDetails>
          </Accordion>
          <Accordion sx={{ flexGrow: 1 }}>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.chronology-tab.other')}</Typography>
            </SmallAccordionTitle>
            <AccordionDetails sx={{ display: 'flex', flexDirection: 'row', flexGrow: 1, gap: 2 }}>
              {otherLeagues.length > 0 ? (
                otherLeagues.map((league) => (
                  <ChampionsChronologyTable key={league.league.id} leagueChampions={league} />
                ))
              ) : (
                <Typography variant="caption">{t('hall-of-fame.chronology-tab.empty')}</Typography>
              )}
            </AccordionDetails>
          </Accordion>
        </>
      )}
    </Box>
  );
};
