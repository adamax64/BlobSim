import { Gauge, gaugeClasses, useGaugeState } from '@mui/x-charts/Gauge';
import { Box, Typography, useTheme } from '@mui/material';

interface EfficiencyMeterProps {
  label: string;
  /** Efficiency as a ratio between 0 and 1 */
  value: number;
}

const RED = { r: 244, g: 67, b: 54 };
const YELLOW = { r: 255, g: 235, b: 59 };
const GREEN = { r: 76, g: 175, b: 80 };

function interpolateChannel(from: number, to: number, ratio: number): number {
  return Math.round(from + (to - from) * ratio);
}

/** Interpolates red (0) -> yellow (0.5) -> green (1) for a ratio between 0 and 1 */
function getEfficiencyColor(ratio: number): string {
  const clamped = Math.min(1, Math.max(0, ratio));
  const [from, to, localRatio] =
    clamped <= 0.5 ? [RED, YELLOW, clamped / 0.5] : [YELLOW, GREEN, (clamped - 0.5) / 0.5];

  const r = interpolateChannel(from.r, to.r, localRatio);
  const g = interpolateChannel(from.g, to.g, localRatio);
  const b = interpolateChannel(from.b, to.b, localRatio);

  return `rgb(${r}, ${g}, ${b})`;
}

function GaugePointer() {
  const { valueAngle, outerRadius, cx, cy } = useGaugeState();
  const theme = useTheme();

  if (valueAngle === null) {
    return null;
  }

  const pointerX = cx + outerRadius * Math.sin(valueAngle);
  const pointerY = cy - outerRadius * Math.cos(valueAngle);

  return (
    <g>
      <circle cx={cx} cy={cy} r={6} fill={theme.palette.text.primary} />
      <path
        d={`M ${cx} ${cy} L ${pointerX} ${pointerY}`}
        stroke={theme.palette.text.primary}
        strokeWidth={3}
        strokeLinecap="round"
      />
    </g>
  );
}

export function EfficiencyMeter({ label, value }: EfficiencyMeterProps) {
  const percentage = Math.round((value ?? 0) * 100);
  const color = getEfficiencyColor(value ?? 0);

  return (
    <Box display="flex" flexDirection="column" alignItems="center" gap={0.5}>
      <Gauge
        width={120}
        height={120}
        value={percentage}
        valueMin={0}
        valueMax={100}
        startAngle={-110}
        endAngle={110}
        text={() => ''}
        innerRadius="70%"
        sx={{
          [`& .${gaugeClasses.valueArc}`]: {
            fill: color,
          },
        }}
      >
        <GaugePointer />
      </Gauge>
      <Typography variant="body2" textAlign="center">
        {label}
      </Typography>
    </Box>
  );
}
