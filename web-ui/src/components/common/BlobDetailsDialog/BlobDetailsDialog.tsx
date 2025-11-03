import { BlobsApi, BlobStatsDto } from '../../../../generated';
import { useEffect, useState } from 'react';
import { BlobDetailsDialogUi } from './BlobDetailsDialogUi';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';
import { BlobAnimated } from '../blob-visuals/BlobAnimated';

interface BlobDetailsDialogProps {
  open: boolean;
  onClose: () => void;
  cachedBlob?: BlobStatsDto | undefined;
  blobId?: number;
}

export const BlobDetailsDialog = ({ open, onClose, cachedBlob, blobId }: BlobDetailsDialogProps) => {
  const [blob, setBlob] = useState<BlobStatsDto>();

  const blobsApi: BlobsApi = new BlobsApi(defaultConfig);
  const { mutate: fetchBlobDetails } = useMutation({
    mutationFn: () => (blobId ? blobsApi.getBlobBlobsBlobIdGet({ blobId }) : Promise.resolve(undefined)),
    onSuccess: (response) => {
      if (response) {
        setBlob(response);
      }
    },
  });

  useEffect(() => {
    if (cachedBlob) {
      setBlob(cachedBlob);
    } else if (blobId) {
      fetchBlobDetails();
    }
  }, [cachedBlob]);

  if (!blob) return null;

  return (
    <BlobDetailsDialogUi
      open={open}
      onClose={onClose}
      blob={blob!}
      blobIcon={<BlobAnimated blob={blob} size={180} />}
    />
  );
};
