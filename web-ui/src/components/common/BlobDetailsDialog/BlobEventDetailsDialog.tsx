import { BlobsApi, BlobStatsDto } from '../../../../generated';
import { useEffect, useState } from 'react';
import { BlobEventDetailsDialogUi } from './BlobEventDetailsDialogUi';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';

interface BlobEventDetailsDialogProps {
  open: boolean;
  onClose: () => void;
  cachedBlob?: BlobStatsDto | undefined;
  blobId?: number;
}

export const BlobEventDetailsDialog = ({ open, onClose, cachedBlob, blobId }: BlobEventDetailsDialogProps) => {
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
  }, [cachedBlob, blobId, fetchBlobDetails]);

  return <BlobEventDetailsDialogUi open={open} onClose={onClose} blob={blob} />;
};
