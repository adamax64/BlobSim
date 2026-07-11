import { useState } from 'react';
import { BlobStatsDto } from '../../../generated';
import { Box, Typography } from '@mui/material';
import { BlobAnimated } from '../common/blob-visuals/BlobAnimated';
import { BlobDetailsDialog } from '../common/BlobDetailsDialog/BlobDetailsDialog';

type BlobAnimatedWithNameProps = {
  blob: BlobStatsDto;
};

const BlobAnimatedWithName = ({ blob }: BlobAnimatedWithNameProps) => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Box onClick={() => setOpen(true)} sx={{ cursor: 'pointer' }}>
        <BlobAnimated blob={blob} size={180} />
        <Typography variant="body1" align="center" pt={1}>
          {blob.name}
        </Typography>
      </Box>
      <BlobDetailsDialog open={open} onClose={() => setOpen(false)} cachedBlob={blob} />
    </>
  );
};

export default BlobAnimatedWithName;
