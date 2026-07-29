import { SimTimeDto } from '../../generated';

export function formatToShort(time: SimTimeDto): string {
  return `${time.season}. ${time.epoch} - ${time.cycle}`;
}

/**
 * Compares two sim times chronologically.
 * Returns a positive number if `a` is after `b`, negative if `a` is before `b`, 0 if equal.
 */
export function compareSimTime(a: SimTimeDto, b: SimTimeDto): number {
  return a.eon - b.eon || a.season - b.season || a.epoch - b.epoch || a.cycle - b.cycle;
}
