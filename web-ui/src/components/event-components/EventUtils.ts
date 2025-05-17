import { QuarteredEventRecordDto } from '../../../generated';

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

/**
 * Calculates the current competitor's index on the leaderboard
 */
export function getBlobIndex(quarterEnds: number[], tick: number, quarter: number, fieldSize: number): number {
  if (quarter === 1) {
    return tick % fieldSize;
  } else {
    const currentFieldSize = fieldSize - (quarter - 1) * getEliminations(fieldSize);
    const quarterTick = tick - quarterEnds[quarter - 2];
    return quarterTick % currentFieldSize;
  }
}

export function sortLambda(index: number) {
  return (a: QuarteredEventRecordDto, b: QuarteredEventRecordDto) =>
    (a.quarters[index].score ?? -1 > (b.quarters[index].score ?? -1)) ? -1 : 1;
}

export function roundToThreeDecimals(value?: number | null): number | undefined {
  if (value === undefined || value === null) {
    return undefined;
  }
  return Math.round(value * 1000) / 1000;
}
