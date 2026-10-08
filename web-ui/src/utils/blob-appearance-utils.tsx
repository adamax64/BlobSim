import { JSX } from 'react/jsx-runtime';
import { AppearanceType } from '../../generated';

// Helper function to create SVG gradient definitions for bicolor/tricolor
export const createGradientDefs = (
  appearanceType: AppearanceType | undefined,
  colors: string[] | undefined,
  params: string[] | undefined,
  gradientId: string,
): JSX.Element | null => {
  if (!colors || colors.length === 0) return null;

  if (appearanceType === AppearanceType.Solid || colors.length === 1) {
    return null; // No gradient needed for solid
  }

  const gradient_point = Number.parseInt(params?.[0] ?? '50');
  const rotation = Number.parseInt(params?.[1] ?? '0');

  if (appearanceType === AppearanceType.Bicolor && colors.length >= 2) {
    // Bicolor: two colors split by rotation
    const angle = rotation;
    const x1 = 50 + 50 * Math.cos(((angle - 90) * Math.PI) / 180);
    const y1 = 50 + 50 * Math.sin(((angle - 90) * Math.PI) / 180);
    const x2 = 50 + 50 * Math.cos(((angle + 90) * Math.PI) / 180);
    const y2 = 50 + 50 * Math.sin(((angle + 90) * Math.PI) / 180);

    return (
      <defs key={`${gradientId}-defs`}>
        <linearGradient id={gradientId} x1={`${x1}%`} y1={`${y1}%`} x2={`${x2}%`} y2={`${y2}%`}>
          <stop offset="0%" stopColor={colors[0]} />
          <stop offset={`${gradient_point}%`} stopColor={colors[0]} />
          <stop offset={`${gradient_point + 1}%`} stopColor={colors[1]} />
          <stop offset="100%" stopColor={colors[1]} />
        </linearGradient>
      </defs>
    );
  }

  if (appearanceType === AppearanceType.Tricolor && colors.length >= 3) {
    const defaults = [100 / 3, (100 * 2) / 3];
    const switchPoints = [0, 1]
      .map((index) => {
        const point = Number.parseInt(params?.[index] ?? '');
        return Number.isFinite(point) ? Math.min(Math.max(point, 0), 100) : defaults[index];
      })
      .sort((left, right) => left - right);
    const switchPoint1 = switchPoints[0];
    const switchPoint2 = switchPoints[1];
    const parsedAngle = Number.parseInt(params?.[2] ?? '');
    const angle = Number.isFinite(parsedAngle) ? parsedAngle : 0;
    const x1 = 50 + 50 * Math.cos(((angle - 90) * Math.PI) / 180);
    const y1 = 50 + 50 * Math.sin(((angle - 90) * Math.PI) / 180);
    const x2 = 50 + 50 * Math.cos(((angle + 90) * Math.PI) / 180);
    const y2 = 50 + 50 * Math.sin(((angle + 90) * Math.PI) / 180);

    return (
      <defs key={`${gradientId}-defs`}>
        <linearGradient id={gradientId} x1={`${x1}%`} y1={`${y1}%`} x2={`${x2}%`} y2={`${y2}%`}>
          <stop offset="0%" stopColor={colors[0]} />
          <stop offset={`${switchPoint1}%`} stopColor={colors[0]} />
          <stop offset={`${switchPoint1 + 1}%`} stopColor={colors[1]} />
          <stop offset={`${switchPoint2}%`} stopColor={colors[1]} />
          <stop offset={`${switchPoint2 + 1}%`} stopColor={colors[2]} />
          <stop offset="100%" stopColor={colors[2]} />
        </linearGradient>
      </defs>
    );
  }

  return null;
};

// Helper to get the fill value (color or gradient URL)
export const getFillValue = (
  appearanceType: AppearanceType | undefined,
  colors: string[] | undefined,
  gradientId: string,
): string => {
  if (!colors || colors.length === 0) return '#888888';
  if (appearanceType === AppearanceType.Solid || colors.length === 1) {
    return colors[0];
  }
  return `url(#${gradientId})`;
};
