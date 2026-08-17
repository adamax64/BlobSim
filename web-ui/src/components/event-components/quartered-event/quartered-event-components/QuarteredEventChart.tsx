import { Box } from '@mui/material';
import { ScatterChart, ScatterMarkerProps, useItemTooltip } from '@mui/x-charts';
import { useEffect, useRef, useState } from 'react';
import { useMemo } from 'react';
import { BlobIcon } from '../../../icons/BlobIcon';
import { roundToThreeDecimals } from '../../event-utils';
import { EventChartTooltipContent } from '../../shared/EventChartTooltipContent';
import type { QuarteredEventRecordDto as EventRecordDto } from '../../../../../generated';

interface QuarteredEventChartPoint {
  x: number;
  y: number;
  color: string;
  name: string;
  justScored: boolean;
}

interface QuarteredEventChartScore {
  y: number;
  color: string;
  name: string;
  justScored: boolean;
}

export interface QuarteredEventChartProps {
  eventRecords: EventRecordDto[];
}

const MIN_HEIGHT = 240;
const SCORE_OVERLAP_THRESHOLD = 0.5;
const X_SPREAD = 0.15;

export const QuarteredEventChart = ({ eventRecords }: QuarteredEventChartProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [measuredHeight, setMeasuredHeight] = useState(MIN_HEIGHT);

  useEffect(() => {
    const element = containerRef.current;
    if (!element) {
      return;
    }
    const observer = new ResizeObserver((entries) => {
      const entryHeight = entries[0]?.contentRect.height ?? 0;
      setMeasuredHeight(Math.max(entryHeight, MIN_HEIGHT));
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  const points = useMemo<QuarteredEventChartScore[]>(
    () =>
      eventRecords
        .map((record) => {
          let score: number | undefined;
          let justScored = false;
          for (let q = 0; q < record.quarters.length; q += 1) {
            const quarterScore = record.quarters[q];
            const value = quarterScore.latestScore ?? quarterScore.score;
            justScored = record.current ?? false;
            if (value != null) {
              score = value;
            }
          }
          if (score == null) {
            return null;
          }
          return {
            y: score ?? 0,
            color: record.blob.color,
            name: record.blob.name,
            justScored,
          };
        })
        .filter((point): point is QuarteredEventChartScore => point !== null),
    [eventRecords],
  );

  const pointsWithX = useMemo<QuarteredEventChartPoint[]>(() => {
    const sorted = [...points].sort((a, b) => a.y - b.y);
    const result: QuarteredEventChartPoint[] = [];
    for (let i = 0; i < sorted.length; i++) {
      const overlaps = result.filter((p) => Math.abs(p.y - sorted[i].y) < SCORE_OVERLAP_THRESHOLD);
      const offsetIndex = overlaps.length;
      const x = 1 + offsetIndex * X_SPREAD;
      result.push({ ...sorted[i], x });
    }
    return result;
  }, [points]);

  const isEmpty = pointsWithX.length === 0;

  const series = useMemo(
    () => [
      {
        type: 'scatter' as const,
        data: isEmpty
          ? [{ x: 0, y: 0, id: 'empty' }]
          : pointsWithX.map((point) => ({ x: point.x, y: point.y, id: point.name })),
        markerSize: 20,
      },
    ],
    [pointsWithX, isEmpty],
  );

  const yDomain = useMemo<[number, number]>(() => {
    const scores = pointsWithX.map((point) => point.y).filter((value) => Number.isFinite(value));
    if (scores.length === 0) {
      return [0, 1];
    }
    const min = Math.min(...scores);
    const max = Math.max(...scores);
    const padding = max - min === 0 ? Math.max(max * 0.1, 0.1) : (max - min) * 0.15;
    return [0, max + padding];
  }, [pointsWithX]);

  const xMax = useMemo(() => {
    if (pointsWithX.length === 0) {
      return 1;
    }
    return Math.max(...pointsWithX.map((p) => p.x)) + X_SPREAD;
  }, [pointsWithX]);

  return (
    <Box ref={containerRef} sx={{ height: '100%', width: '100%', minHeight: MIN_HEIGHT }}>
      <ScatterChart
        series={series}
        height={measuredHeight}
        hideLegend
        margin={{ top: 16, right: 24, bottom: 8, left: 24 }}
        yAxis={[
          {
            min: yDomain[0],
            max: yDomain[1],
            valueFormatter: (value: number) => String(roundToThreeDecimals(value) ?? ''),
          },
        ]}
        xAxis={[
          {
            min: 0,
            max: isEmpty ? 1 : xMax,
            disableTicks: true,
            tickLabelStyle: { display: 'none' },
          },
        ]}
        slots={{ marker: isEmpty ? InvisibleScatterMarker : BlobScatterMarker, tooltip: ScatterTooltip }}
        slotProps={{
          marker: { points: pointsWithX } as unknown as ScatterMarkerProps,
          tooltip: { points: pointsWithX, trigger: 'item' as const } as unknown as Record<string, unknown>,
        }}
      />
    </Box>
  );
};

interface BlobScatterMarkerProps extends ScatterMarkerProps {
  points?: QuarteredEventChartPoint[];
}

const InvisibleScatterMarker = () => null;

const BlobScatterMarker = (props: BlobScatterMarkerProps) => {
  const { points, x, y, isHighlighted, dataIndex } = props;
  const point = points?.[dataIndex];
  if (!point) {
    return null;
  }
  const size = isHighlighted ? 28 : point.justScored ? 26 : 20;
  return (
    <g transform={`translate(${x},${y})`}>
      <foreignObject x={-size / 2} y={-size / 2} width={size} height={size} style={{ overflow: 'visible' }}>
        <div style={{ width: size, height: size, pointerEvents: 'none' }}>
          <BlobIcon size={size} color={point.color} />
        </div>
      </foreignObject>
    </g>
  );
};

interface ScatterTooltipProps {
  points?: QuarteredEventChartPoint[];
  trigger?: 'item' | 'axis' | 'none';
}

const ScatterTooltip = ({ points, trigger }: ScatterTooltipProps) => {
  const tooltip = useItemTooltip<'scatter'>();
  if (!tooltip) {
    return null;
  }
  const dataIndex = tooltip.identifier.dataIndex;
  const point = points?.[dataIndex];
  if (!point) {
    return null;
  }
  return <EventChartTooltipContent name={point.name} color={point.color} score={point.y} trigger={trigger} />;
};
