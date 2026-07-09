import { BlobsApi, BlobStatsDto, ResponseError, StandingsApi, StandingsSnippetDto } from '../../../../generated';
import { useEffect } from 'react';
import { BlobEventDetailsDialogUi } from './BlobEventDetailsDialogUi';
import defaultConfig from '../../../default-config';
import { useMutation } from '@tanstack/react-query';

type BlobEventDetailsDialogProps = {
  open: boolean;
  onClose: () => void;
  cachedBlob?: BlobStatsDto | undefined;
  blobId?: number;
};

export const BlobEventDetailsDialog = ({ open, onClose, cachedBlob, blobId }: BlobEventDetailsDialogProps) => {
  const blobsApi: BlobsApi = new BlobsApi(defaultConfig);
  const standingsApi: StandingsApi = new StandingsApi(defaultConfig);
  const { mutate: fetchBlobDetails, data: blob } = useMutation<BlobStatsDto | undefined, ResponseError>({
    mutationFn: () => (blobId ? blobsApi.getBlobBlobsBlobIdGet({ blobId }) : Promise.resolve(undefined)),
  });

  const { mutate: fetchStandingsSnippet, data: standingsData } = useMutation<
    StandingsSnippetDto[] | undefined,
    ResponseError
  >({
    mutationFn: () =>
      !blobId && !cachedBlob
        ? Promise.resolve(undefined)
        : standingsApi.getStandingsSnippetStandingsSnippetBlobIdGet({ blobId: blobId ?? cachedBlob?.id ?? 0 }),
  });

  useEffect(() => {
    if (blobId) {
      fetchBlobDetails();
    }
    fetchStandingsSnippet();
  }, [cachedBlob, blobId, fetchBlobDetails, fetchStandingsSnippet]);

  return (
    <BlobEventDetailsDialogUi open={open} onClose={onClose} blob={blob ?? cachedBlob} standingsData={standingsData} />
  );
};
