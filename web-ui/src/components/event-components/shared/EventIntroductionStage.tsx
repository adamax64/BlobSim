import { Box, Fade, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import type { EventType } from '../../../../generated';
import { EventCardFrame } from './EventCardFrame';

type EventIntroductionStageProps = {
  active: boolean;
  leagueName: string;
  season: number;
  round: number;
  eventType: EventType;
};

export const EventIntroductionStage = ({
  active,
  leagueName,
  season,
  round,
  eventType,
}: EventIntroductionStageProps) => {
  const { t } = useTranslation();

  return (
    <EventCardFrame>
      <Fade in={active} timeout={900} style={{height: '80vh'}}>
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          gap={1.5}
          height="100%"
          textAlign="center"
        >
          <Typography variant="h4" fontWeight={600}>
            {leagueName}
          </Typography>
          <Typography variant="h6" color="text.secondary">
            {t('event_stage_pipeline.introduction.season_round', { season, round })}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {t(`enums.event_types.${eventType}`)}
          </Typography>
        </Box>
      </Fade>
    </EventCardFrame>
  );
};

export default EventIntroductionStage;
