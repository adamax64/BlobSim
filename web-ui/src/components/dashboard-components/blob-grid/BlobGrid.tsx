import { Grid } from '@mui/material';
import { BlobStatsDto } from '../../../../generated';
import BlobAnimatedWithName from '../BlobAnimatedWithName';
import { useMemo } from 'react';

export const BLOB_GRID_CELL_SIZE = { xs: 12, sm: 6, md: 4, lg: 3 };

type BlobGridProps = {
  blobs: BlobStatsDto[];
};

const BlobGrid = ({ blobs }: BlobGridProps) => {
  const cellSize = useMemo(
    () => ({
      xs: BLOB_GRID_CELL_SIZE.xs,
      sm: Math.max(BLOB_GRID_CELL_SIZE.sm, 12 / blobs.length),
      md: Math.max(BLOB_GRID_CELL_SIZE.md, 12 / blobs.length),
      lg: Math.max(BLOB_GRID_CELL_SIZE.lg, 12 / blobs.length),
    }),
    [blobs.length],
  );
  return (
    <Grid container spacing={2}>
      {blobs.map((blob) => (
        <Grid size={cellSize} display="flex" justifyContent="center">
          <BlobAnimatedWithName blob={blob} />
        </Grid>
      ))}
    </Grid>
  );
};

export default BlobGrid;
