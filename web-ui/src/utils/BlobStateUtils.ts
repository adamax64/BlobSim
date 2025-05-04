export enum BlobState {
  AT_RISK = 'row-at-risk',
  DEAD = 'row-dead',
  RETIRED = 'row-retired',
  FIRST = 'row-gold',
  SECOND = 'row-silver',
  THIRD = 'row-bronze',
}

export function getClassNameForBlobState(state: BlobState): string {
  switch (state) {
    case BlobState.AT_RISK:
      return 'row-at-risk';
    case BlobState.DEAD:
      return 'row-dead';
    case BlobState.RETIRED:
      return 'row-retired';
    case BlobState.FIRST:
      return 'row-gold';
    case BlobState.SECOND:
      return 'row-silver';
    case BlobState.THIRD:
      return 'row-bronze';
    default:
      return '';
  }
}
