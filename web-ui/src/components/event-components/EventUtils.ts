/**
 * Determines the number of contenders eliminated in each quarter based on the field size.
 */
export function getEliminations(fieldSize: number): number {
  return fieldSize < 15 ? Math.floor((fieldSize - 3) / 3) : Math.floor(fieldSize / 4);
}

export function getQuarterEnds(fieldSize: number, isOneshot: boolean): number[] {
  const eliminations = getEliminations(fieldSize);
  const multiplier = isOneshot ? 1 : 2;

  return [
    multiplier * fieldSize,
    multiplier * (2 * fieldSize - eliminations),
    multiplier * (3 * fieldSize - 3 * eliminations),
    multiplier * (4 * fieldSize - 6 * eliminations),
  ];
}

export function getCurrentQuarter(quarterEnds: number[], tick: number): number {
  for (let i = 0; i < quarterEnds.length; i++) {
    if (tick < quarterEnds[i]) {
      return i + 1;
    }
  }
  return 5;
}

export function roundToThreeDecimals(value?: number | null): number | undefined {
  if (value === undefined || value === null) {
    return undefined;
  }
  return Math.round(value * 1000) / 1000;
}

export function roundToOneDecimals(value?: number | null): number | undefined {
  if (value === undefined || value === null) {
    return undefined;
  }
  return Math.round(value * 10) / 10;
}

const TINY_FIELD = 5;
const SMALL_FIELD = 8;
const NEAR_HALF_FIELD = 11;
const MEDIUM_FIELD = 14;
const LARGE_FIELD = 18;
const HUGE_FIELD = 22;

export function getRaceDurationBySize(fieldSize: number): number {
  if (fieldSize >= HUGE_FIELD) return 120;
  if (fieldSize >= LARGE_FIELD) return 110;
  if (fieldSize >= MEDIUM_FIELD) return 100;
  if (fieldSize >= NEAR_HALF_FIELD) return 90;
  if (fieldSize >= SMALL_FIELD) return 75;
  if (fieldSize >= TINY_FIELD) return 60;
  return 0;
}
