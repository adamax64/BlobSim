import { Grid, Skeleton } from '@mui/material';
import { BLOB_GRID_CELL_SIZE } from './BlobGrid';

const SkeletonGrid = () => {
  return (
    <Grid container spacing={2}>
      {Array.from({ length: 4 }).map((_, index) => (
        <Grid key={index} size={BLOB_GRID_CELL_SIZE} display="flex" justifyContent="center">
          <Skeleton variant="circular" width={180} height={180} />
        </Grid>
      ))}
    </Grid>
  );
};

export default SkeletonGrid;
