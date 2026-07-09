import { Box } from '@mui/material';
import { IconName, IconNameProps } from './IconName';
import { useState } from 'react';
import { BlobDetailsDialog } from './BlobDetailsDialog/BlobDetailsDialog';
import { BlobEventDetailsDialog } from './BlobDetailsDialog/BlobEventDetailsDialog';
import { BlobStatsDto } from '../../../generated/models/BlobStatsDto';

type IconNameWithDetailsModalProps = IconNameProps &
  (
    | {
        blobId: number;
        blob?: never;
      }
    | { blob?: BlobStatsDto; blobId?: never }
  ) & {
    detailsDialogVariant?: 'default' | 'event';
  };

export const IconNameWithDetailsModal = ({
  blobId,
  blob,
  detailsDialogVariant = 'default',
  ...props
}: IconNameWithDetailsModalProps) => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleOpenDialog = () => {
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
  };

  return (
    <>
      <Box onClick={handleOpenDialog} sx={{ cursor: 'pointer', display: 'inline-block' }}>
        <IconName {...props} />
      </Box>
      {isDialogOpen && (
        <Box position="static">
          {detailsDialogVariant === 'event' ? (
            <BlobEventDetailsDialog open={isDialogOpen} onClose={handleCloseDialog} blobId={blobId} cachedBlob={blob} />
          ) : (
            <BlobDetailsDialog open={isDialogOpen} onClose={handleCloseDialog} blobId={blobId} cachedBlob={blob} />
          )}
        </Box>
      )}
    </>
  );
};
