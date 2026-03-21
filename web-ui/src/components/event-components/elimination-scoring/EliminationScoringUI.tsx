import { useTranslation } from 'react-i18next';
import { Box, Typography, useMediaQuery, useTheme } from '@mui/material';
import type { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDtoOutput';
import { EventType } from '../../../../generated';
import { TickLoadingBar } from '../../common/StyledComponents';
import { EventBarChart } from './elimination-scoring-components/EventBarChart';
import { EliminationEventTable } from './elimination-scoring-components/EliminationEventTable';
import { EliminationEventContentTabs } from './elimination-scoring-components/EliminationEventContentTabs';
import { EventCardFrame } from '../shared/EventCardFrame';

type EliminationScoringUIProps = {
  eventRecords: EventRecordDto[];
  tick: number;
  loadingNextTick: boolean;
  isEventFinished: boolean;
  eventType: EventType;
};

export const EliminationScoringUI = ({
  eventRecords,
  tick,
  loadingNextTick,
  isEventFinished,
  eventType,
}: EliminationScoringUIProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <EventCardFrame eventType={eventType}>
      <Typography fontSize={18} fontWeight={600} paddingBottom={1}>
        {t('elimination_event.tick')}: {tick}
      </Typography>
      <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginBottom={isMobile ? 0 : 2}>
        <TickLoadingBar />
      </Box>
      {isMobile ? (
        <EliminationEventContentTabs
          eventRecords={eventRecords}
          isEventFinished={isEventFinished}
          isMobile={isMobile}
        />
      ) : (
        <Box display="flex" flexDirection="row">
          <Box>
            <EliminationEventTable eventRecords={eventRecords} isEventFinished={isEventFinished} isMobile={isMobile} />
          </Box>
          <Box flexGrow={1}>
            <EventBarChart eventRecords={eventRecords} isMobile={isMobile} />
          </Box>
        </Box>
      )}
    </EventCardFrame>
  );
};
