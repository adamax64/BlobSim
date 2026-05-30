import { CalendarDto, EventType } from '../../../../generated';
import Tooltip from '@mui/material/Tooltip';
import { Box, ClickAwayListener } from '@mui/material';
import { SyntheticEvent, useMemo, useState } from 'react';
import AccessAlarmIcon from '@mui/icons-material/AccessAlarm';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import RouteIcon from '@mui/icons-material/Route';
import HeightIcon from '@mui/icons-material/Height';
import SportsMmaIcon from '@mui/icons-material/SportsMma';
import SportsScoreIcon from '@mui/icons-material/SportsScore';
import { CalendarEventContentUI } from './CalendarEventContentUI';

type CalendarEventWithTooltipProps = {
  event: CalendarDto;
  isToday: boolean;
};

export const CalendarEventWithTooltip: React.FC<CalendarEventWithTooltipProps> = ({ event, isToday }) => {
  const [open, setOpen] = useState(false);

  const handleTooltipClose = (event: Event | SyntheticEvent<Element, Event>) => {
    setOpen(false);
  };

  const handleTooltipOpen = () => {
    setOpen(true);
  };

  const eventIcon = useMemo(() => {
    switch (event.eventType) {
      case EventType.QuarteredOneShotScoring:
      case EventType.QuarteredTwoShotScoring:
      case EventType.QuarteredOneShotScoringV2:
      case EventType.QuarteredTwoShotScoringV2:
        return <HeightIcon />;
      case EventType.EnduranceRace:
        return <AccessAlarmIcon />;
      case EventType.SprintRace:
        return <RouteIcon />;
      case EventType.EliminationScoring:
        return <SportsMmaIcon />;
      case EventType.CatchupTraining:
        return <FitnessCenterIcon />;
      default:
        return <SportsScoreIcon />;
    }
  }, [event.eventType]);

  return (
    <ClickAwayListener onClickAway={handleTooltipClose}>
      <Box width="100%">
        <Tooltip
          describeChild
          onClose={handleTooltipClose}
          open={open}
          disableFocusListener
          disableHoverListener
          disableTouchListener
          arrow
          title={
            <Box display="flex" gap={1}>
              <CalendarEventContentUI event={event} isToday={isToday} />
            </Box>
          }
        >
          <Box display="flex" alignItems="center" justifyContent="center" width="100%" onClick={handleTooltipOpen}>
            {eventIcon}
          </Box>
        </Tooltip>
      </Box>
    </ClickAwayListener>
  );
};
