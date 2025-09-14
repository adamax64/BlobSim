import { SimTimeDto } from '../../generated';

export function formatToShort(time: SimTimeDto): string {
  return `${time.season}. ${time.epoch} - ${time.cycle}`;
}
