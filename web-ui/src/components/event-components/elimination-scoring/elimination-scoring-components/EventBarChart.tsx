import { Box } from '@mui/material';
import { BarChart, ChartsText, ChartsTextProps, useAxesTooltip } from '@mui/x-charts';
import { EliminationEventRecordDtoOutput as EventRecordDto } from '../../../../../generated/models/EliminationEventRecordDtoOutput';
import { BlobIcon } from '../../../icons/BlobIcon';
import { BlobCompetitorDto } from '../../../../../generated';
import { EventChartTooltipContent } from '../../shared/EventChartTooltipContent';

interface EventBarChartProps {
  eventRecords: EventRecordDto[];
  isMobile: boolean;
}

export const EventBarChart = ({ eventRecords, isMobile }: EventBarChartProps) => {
  return (
    <Box
      sx={{
        width: '100%',
        height: '100%',
      }}
    >
      <BarChart
        height={33 * (eventRecords?.length ?? 0) + 35}
        series={[
          {
            data: eventRecords.map((record) => record.lastScore ?? 0),
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
        margin={{ top: 12, right: 16, bottom: 0, left: isMobile ? 0 : -24 }}
        xAxis={[{ position: 'top' }]}
        slots={{ tooltip: CustomTooltip, axisTickLabel: CustomAxisTickLabel(isMobile) }}
      />
    </Box>
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

  return <EventChartTooltipContent name={name} color={color} score={Number.isFinite(value) ? value : null} />;
};
