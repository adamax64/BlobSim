import { useCallback, useId, useMemo } from 'react';
import { Box, Card, Typography } from '@mui/material';
import { BarChart, ChartsText, ChartsTextProps, ChartsTooltipContainer, useAxesTooltip } from '@mui/x-charts';
import { IconName } from '../../../common/IconName';
import { EliminationEventRecordDto as EventRecordDto } from '../../../../../generated/models/EliminationEventRecordDto';
import { BlobIcon } from '../../../icons/BlobIcon';
import { AppearanceType, BlobCompetitorDto } from '../../../../../generated';

interface EventBarChartProps {
  eventRecords: EventRecordDto[];
  isMobile: boolean;
}

export const EventBarChart = ({ eventRecords, isMobile }: EventBarChartProps) => {
  const chartId = useId().replace(/:/g, '');
  const getStripeColors = useCallback((record: EventRecordDto) => {
    const appearance = record.blob.appearance;
    const colors = appearance?.colors;

    if (appearance?.appearanceType === AppearanceType.Bicolor && colors && colors.length >= 2) {
      return colors.slice(0, 2);
    }

    if (appearance?.appearanceType === AppearanceType.Tricolor && colors && colors.length >= 3) {
      return colors.slice(0, 3);
    }

    return undefined;
  }, []);

  const stripePatterns = useMemo(
    () =>
      eventRecords.flatMap((record, index) => {
        const colors = getStripeColors(record);
        if (!colors) return [];

        const id = `${chartId}-blob-stripes-${index}`;
        return [
          {
            id,
            stripes: colors.map((color, stripeIndex) => ({
              color,
              key: `${id}-stripe-${stripeIndex}`,
              x: (0.2 / colors.length) * stripeIndex,
            })),
          },
        ];
      }),
    [eventRecords, getStripeColors, chartId],
  );

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
            valueFormatter: (value: BlobCompetitorDto) => JSON.stringify(value.appearance),
            tickLabelStyle: { display: 'contents' },
            colorMap: {
              colors: eventRecords.map((record, index) =>
                getStripeColors(record)
                  ? `url(#${chartId}-blob-stripes-${index})`
                  : (record.blob.appearance?.colors?.[0] ?? '#888888'),
              ),
              type: 'ordinal',
            },
          },
        ]}
        layout="horizontal"
        margin={{ top: 12, right: 16, bottom: 0, left: isMobile ? 0 : -24 }}
        xAxis={[{ position: 'top' }]}
        slots={{ tooltip: CustomTooltip, axisTickLabel: CustomAxisTickLabel(isMobile) }}
      >
        <defs>
          {stripePatterns.map(({ id, stripes }) => (
            <pattern
              key={id}
              id={id}
              width={0.2}
              height={1}
              patternUnits="objectBoundingBox"
              patternContentUnits="objectBoundingBox"
            >
              {stripes.map(({ color, key, x }) => (
                <rect key={key} x={x} y={0} width={0.2 / stripes.length} height={1} fill={color} />
              ))}
            </pattern>
          ))}
        </defs>
      </BarChart>
    </Box>
  );
};

const CustomAxisTickLabel = (isMobile: boolean) => (props: ChartsTextProps) => {
  return isMobile ? (
    props.x === 0 ? (
      <ChartsText {...props} text={props.text} />
    ) : (
      <g transform={`translate(${-30},${(typeof props.y === 'number' ? props.y : 0) - 12}) rotate(0)`}>
        <BlobIcon size={24} appearance={JSON.parse(props.text)} />
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
    'name' in (axisTooltip?.[0].axisValue ?? {})
      ? (axisTooltip?.[0].axisValue as { name: string }).name
      : String(axisTooltip?.[0].axisValue ?? '');

  const appearance = axisTooltip?.[0].axisFormattedValue ?? '{}';
  const value = Number.parseFloat(axisTooltip?.[0].seriesItems[0].formattedValue ?? '');

  return (
    <ChartsTooltipContainer>
      <Card>
        <Box padding={1} display="flex" justifyContent="space-between" width={210}>
          <IconName name={name} appearance={JSON.parse(appearance)} />
          <Typography variant="body2" align="right">
            {value > 0 ? value : '-'}
          </Typography>
        </Box>
      </Card>
    </ChartsTooltipContainer>
  );
};
