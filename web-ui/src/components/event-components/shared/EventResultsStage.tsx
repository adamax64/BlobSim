import { Box, CircularProgress, Typography } from '@mui/material';
import { useEffect, useMemo } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { CompetitionApi, ResultDto } from '../../../../generated';
import defaultConfig from '../../../default-config';
import { ResultsTable } from '../ResultsTable';
import { EventCardFrame } from './EventCardFrame';

type EventResultsStageProps = {
  active: boolean;
  eventId: number;
};

export const EventResultsStage = ({ active, eventId }: EventResultsStageProps) => {
  const { t } = useTranslation();
  const competitionApi = useMemo(() => new CompetitionApi(defaultConfig), []);

  const {
    data: results,
    isPending,
    mutate: loadResults,
  } = useMutation<ResultDto[], Error>({
    mutationFn: () => competitionApi.getResultsForEventRouteCompetitionResultsEventEventIdGet({ eventId }),
  });

  useEffect(() => {
    if (active) {
      loadResults();
    }
  }, [active, loadResults]);

  return (
    <EventCardFrame
      title={t('event_stage_pipeline.results.title')}
    >
      {isPending && !results ? (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight={140}>
          <CircularProgress />
        </Box>
      ) : !results || results.length === 0 ? (
        <Typography>{t('results.modal.no_results')}</Typography>
      ) : (
        <Box display="flex" justifyContent="center" width="100%">
          <Box maxWidth="400px" width="100%">
            <ResultsTable results={results} />
          </Box>
        </Box>
      )}
    </EventCardFrame>
  );
};

export default EventResultsStage;
