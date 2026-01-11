import { Accordion, AccordionDetails, Box, Tooltip, Typography, useMediaQuery, useTheme } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Info from '@mui/icons-material/Info';
import { DefaultApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { useTranslation } from 'react-i18next';
import { useMutation } from '@tanstack/react-query';
import { Dispatch, SetStateAction, useEffect } from 'react';
import { SmallAccordionTitle } from '../common/StyledComponents';
import { TitleCountTable } from './tables/TitleCountTable';

interface TitlesTabProps {
  setLoading: Dispatch<SetStateAction<boolean>>;
}

export const TitlesTab = ({ setLoading }: TitlesTabProps) => {
  const { t } = useTranslation();

  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  const titlesApi = new DefaultApi(defaultConfig);
  const {
    data,
    isPending,
    mutate: fetchData,
  } = useMutation({
    mutationKey: ['fetch-titles-data'],
    mutationFn: () => titlesApi.getTitlesCountSummaryHallOfFameTitlesGet(),
  });

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    setLoading(isPending);
  }, [setLoading, isPending]);

  return (
    <Box display="flex" flexDirection="column">
      {isMobile ? (
        <>
          <Accordion>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.table.grandmasters')}</Typography>
            </SmallAccordionTitle>
            <TitleCountTable data={data?.grandmasters} />
          </Accordion>
          <Accordion defaultExpanded>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.table.championships')}</Typography>
            </SmallAccordionTitle>
            <TitleCountTable data={data?.championships} />
          </Accordion>
          <Accordion defaultExpanded>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.table.top_wins')}</Typography>
            </SmallAccordionTitle>
            <TitleCountTable data={data?.topWins} />
          </Accordion>
          <Accordion>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.table.top_podiums')}</Typography>
            </SmallAccordionTitle>
            <TitleCountTable data={data?.topPodiums} />
          </Accordion>
          <Accordion>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">
                {t('hall-of-fame.titles-tab.table.season_victories')}{' '}
                <Tooltip title={t('hall-of-fame.titles-tab.table.season_victory_info')} arrow>
                  <Info sx={{ fontSize: 16 }} color="info" />
                </Tooltip>
              </Typography>
            </SmallAccordionTitle>
            <TitleCountTable data={data?.seasonVictories} />
          </Accordion>
          <Accordion>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.table.lower_wins')} </Typography>
            </SmallAccordionTitle>
            <TitleCountTable data={data?.lowerWins} />
          </Accordion>
          <Accordion>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.table.lower_podiums')} </Typography>
            </SmallAccordionTitle>
            <TitleCountTable data={data?.lowerPodiums} />
          </Accordion>
        </>
      ) : (
        <>
          <Accordion defaultExpanded>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.season')}</Typography>
            </SmallAccordionTitle>
            <AccordionDetails sx={{ display: 'flex', flexDirection: 'row', flexGrow: 1, gap: 2 }}>
              <TitleCountTable data={data?.grandmasters} title={t('hall-of-fame.titles-tab.table.grandmasters')} />
              <TitleCountTable data={data?.championships} title={t('hall-of-fame.titles-tab.table.championships')} />
              <TitleCountTable
                data={data?.seasonVictories}
                title={
                  <Box display="flex" alignItems="center" gap={0.5}>
                    {t('hall-of-fame.titles-tab.table.season_victories')}
                    <Tooltip title={t('hall-of-fame.titles-tab.table.season_victory_info')} arrow>
                      <Info sx={{ fontSize: 16 }} color="info" />
                    </Tooltip>
                  </Box>
                }
              />
            </AccordionDetails>
          </Accordion>
          <Accordion defaultExpanded>
            <SmallAccordionTitle expandIcon={<ExpandMoreIcon />}>
              <Typography variant="body2">{t('hall-of-fame.titles-tab.competition')}</Typography>
            </SmallAccordionTitle>
            <AccordionDetails sx={{ display: 'flex', flexDirection: 'row', flexGrow: 1, gap: 2 }}>
              <TitleCountTable data={data?.topWins} title={t('hall-of-fame.titles-tab.table.top_wins')} />
              <TitleCountTable data={data?.topPodiums} title={t('hall-of-fame.titles-tab.table.top_podiums')} />
              <TitleCountTable data={data?.lowerWins} title={t('hall-of-fame.titles-tab.table.lower_wins')} />
              <TitleCountTable data={data?.lowerPodiums} title={t('hall-of-fame.titles-tab.table.lower_podiums')} />
            </AccordionDetails>
          </Accordion>
        </>
      )}
    </Box>
  );
};
