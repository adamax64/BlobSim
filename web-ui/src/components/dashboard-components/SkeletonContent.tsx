import { DialogContent, Divider, Skeleton } from '@mui/material';
import SkeletonGrid from './blob-grid/SkeletonGrid';

const SkeletonContent = () => {
  return (
    <>
      <Divider />
      <DialogContent>
        <Skeleton variant="text" width="100%" sx={{ mb: 2 }} />
        <SkeletonGrid />
      </DialogContent>
    </>
  );
};

export default SkeletonContent;
