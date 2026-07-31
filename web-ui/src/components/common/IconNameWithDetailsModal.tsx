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
    /**
     * When viewing a replay, the id of the event being replayed, so the 'event' details dialog
     * returns standings as they stood at the time of that event instead of the current standings.
     */
    eventId?: number;
  };

export const IconNameWithDetailsModal = ({
  blobId,
  blob,
  detailsDialogVariant = 'default',
  eventId,
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
            <BlobEventDetailsDialog
              open={isDialogOpen}
              onClose={handleCloseDialog}
              blobId={blobId}
              cachedBlob={blob}
              eventId={eventId}
            />
          ) : (
            <BlobDetailsDialog open={isDialogOpen} onClose={handleCloseDialog} blobId={blobId} cachedBlob={blob} />
          )}
        </Box>
      )}
    </>
  );
};
