import { Box, Card, Typography } from '@mui/material';
import {
  BarChart,
  ChartsText,
  ChartsTextProps,
  ChartsTooltipContainer,
  useAxesTooltip,
  UseAxisTooltipReturnValue,
} from '@mui/x-charts';
import { IconName } from '../../common/IconName';
import { EliminationEventRecordDto as EventRecordDto } from '../../../../generated/models/EliminationEventRecordDto';
import { BlobIcon } from '../../icons/BlobIcon';
import { BlobCompetitorDto } from '../../../../generated';
import { CartesianChartSeriesType } from '@mui/x-charts/internals';

interface EventBarChartProps {
  eventRecords: EventRecordDto[];
  isMobile: boolean;
}

export const EventBarChart = ({ eventRecords, isMobile }: EventBarChartProps) => {
  return (
    <BarChart
      height={33 * (eventRecords?.length ?? 0) + 35}
      series={[
        {
          data: eventRecords.map((record) => (record.eliminated ? 0 : (record.lastScore ?? 0))),
        },
      ]}
      yAxis={[
        {
          data: eventRecords.map((record) => record.blob),
          valueFormatter: (value: BlobCompetitorDto) => value.color,
          tickLabelStyle: { display: 'contents' },
          colorMap: {
            colors: eventRecords.map((record) => record.blob.color),
            type: 'ordinal',
          },
        },
      ]}
      layout="horizontal"
      margin={{ top: 12, right: 16, bottom: 0, left: 0 }}
      xAxis={[{ position: 'top' }]}
      slots={{ tooltip: CustomTooltip, axisTickLabel: CustomAxisTickLabel(isMobile) }}
    />
  );
};

const CustomAxisTickLabel = (isMobile: boolean) => (props: ChartsTextProps) => {
  return isMobile ? (
    props.x === 0 ? (
      <ChartsText {...props} text={props.text} />
    ) : (
      <g transform={`translate(${-30},${(typeof props.y === 'number' ? props.y : 0) - 12}) rotate(0)`}>
        <BlobIcon size={24} color={props.text} />
      </g>
    )
  ) : (
    <ChartsText {...props} text={props.x === 0 ? props.text : ''} />
  );
};

const CustomTooltip = () => {
  const axisTooltip = useAxesTooltip();

  // We may specify the axisValue as object even though the type is specified otherwise in useAxesTooltip
  // so we need to handle this case as well
  const name =
    typeof axisTooltip?.[0].axisValue === 'object' &&
    axisTooltip?.[0].axisValue !== null &&
    'name' in axisTooltip?.[0].axisValue
      ? (axisTooltip?.[0].axisValue as { name: string }).name
      : String(axisTooltip?.[0].axisValue ?? '');

  const color = axisTooltip?.[0].seriesItems[0].color ?? '';
  const value = Number.parseFloat(axisTooltip?.[0].seriesItems[0].formattedValue ?? '');

  return (
    <ChartsTooltipContainer>
      <Card>
        <Box padding={1} display="flex" justifyContent="space-between" width={210}>
          <IconName name={name} color={color} />
          <Typography variant="body2" align="right">
            {value > 0 ? value : '-'}
          </Typography>
        </Box>
      </Card>
    </ChartsTooltipContainer>
  );
};
