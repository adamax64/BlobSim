import { Box, Card, Typography } from '@mui/material';
import { ChartsTooltipContainer } from '@mui/x-charts';
import { IconName } from '../../common/IconName';
import { roundToThreeDecimals } from '../event-utils';

type TooltipTrigger = 'item' | 'axis' | 'none';

export interface EventChartTooltipContentProps {
  name: string;
  color: string;
  score: number | null | undefined;
  trigger?: TooltipTrigger;
}

export const EventChartTooltipContent = ({ name, color, score, trigger }: EventChartTooltipContentProps) => {
  const rounded = roundToThreeDecimals(score);
  const display = rounded && rounded > 0 ? rounded : '-';
  return (
    <ChartsTooltipContainer trigger={trigger}>
      <Card>
        <Box padding={1} display="flex" justifyContent="space-between" width={210}>
          <IconName name={name} color={color} />
          <Typography variant="body2" align="right">
            {display}
          </Typography>
        </Box>
      </Card>
    </ChartsTooltipContainer>
  );
};
