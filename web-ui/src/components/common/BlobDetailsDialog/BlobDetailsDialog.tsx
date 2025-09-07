import { BlobIcon } from '../../icons/BlobIcon';
import { BlobsApi, BlobStatsDto } from '../../../../generated';
import { DeadBlobIcon } from '../../icons/DeadBlobIcon';
import { BlobBlinkIcon } from '../../icons/BlobBlinkIcon';
import { JSX, useEffect, useState } from 'react';
import { BlobDetailsDialogUi } from './BlobDetailsDialogUi';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';

interface BlobDetailsDialogProps {
  open: boolean;
  onClose: () => void;
  cachedBlob?: BlobStatsDto | undefined;
  blobId?: number;
}

export const BlobDetailsDialog = ({ open, onClose, cachedBlob, blobId }: BlobDetailsDialogProps) => {
  const [blob, setBlob] = useState<BlobStatsDto>();
  const [blobIcon, setBlobIcon] = useState<JSX.Element>(<BlobIcon size={180} color={blob?.color ?? ''} />);

  const blobsApi: BlobsApi = new BlobsApi(defaultConfig);
  const { mutate: fetchBlobDetails } = useMutation({
    mutationFn: () => (blobId ? blobsApi.getBlobBlobsBlobIdGet({ blobId }) : Promise.resolve(undefined)),
    onSuccess: (response) => {
      if (response) {
        setBlob(response);
        setBlobIcon(<BlobIcon size={180} color={response.color} />);
      }
    },
  });

  useEffect(() => {
    if (cachedBlob) {
      setBlob(cachedBlob);
      setBlobIcon(<BlobIcon size={180} color={cachedBlob.color} />);
    } else if (blobId) {
      fetchBlobDetails();
    }
  }, [cachedBlob]);

  useEffect(() => {
    if (!blob) return;
    if (blob.isDead) {
      setBlobIcon(<DeadBlobIcon size={180} color={blob.color} />);
    } else {
      setBlobIcon(<BlobIcon size={180} color={blob.color} />);
      const interval = setInterval(() => {
        setBlobIcon(<BlobIcon size={180} color={blob.color} />);
        setTimeout(() => {
          setBlobIcon(<BlobBlinkIcon size={180} color={blob.color} />);
        }, 4000);
        setTimeout(() => {
          setBlobIcon(<BlobIcon size={180} color={blob.color} />);
        }, 4250);
        setTimeout(() => {
          setBlobIcon(<BlobBlinkIcon size={180} color={blob.color} />);
        }, 8250);
        setTimeout(() => {
          setBlobIcon(<BlobIcon size={180} color={blob.color} />);
        }, 8500);
        setTimeout(() => {
          setBlobIcon(<BlobBlinkIcon size={180} color={blob.color} />);
        }, 8750);
        setTimeout(() => {
          setBlobIcon(<BlobIcon size={180} color={blob.color} />);
        }, 9000);
      }, 9000);
      return () => clearInterval(interval);
    }
  }, [blob]);

  if (!blob) return null;

  return <BlobDetailsDialogUi open={open} onClose={onClose} blob={blob!} blobIcon={blobIcon} />;
};
