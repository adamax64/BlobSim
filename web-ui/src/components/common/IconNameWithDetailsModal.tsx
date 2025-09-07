import { Box } from '@mui/material';
import { IconName, IconNameProps } from './IconName';
import { useState } from 'react';
import { BlobDetailsDialog } from './BlobDetailsDialog/BlobDetailsDialog';

interface IconNameWithDetailsModalProps extends IconNameProps {
  blobId: number;
}

export const IconNameWithDetailsModal = ({ blobId, ...props }: IconNameWithDetailsModalProps) => {
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
          <BlobDetailsDialog open={isDialogOpen} onClose={handleCloseDialog} blobId={blobId} />
        </Box>
      )}
    </>
  );
};
