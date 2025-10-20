import { Box, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { IconNameWithDetailsModal } from './IconNameWithDetailsModal';
import { BlobStatsDto } from '../../../generated';

type InlineTranslatedBlobProps = {
  translationKey: string;
  blob?: BlobStatsDto;
  interpolationKey?: string; // the key used in the translation (e.g. 'blobName' or 'grandmaster')
  marker?: string;
  otherInterpolations?: Record<string, string | number>;
};

export const InlineTranslatedBlob = ({
  translationKey,
  blob,
  interpolationKey = 'blobName',
  marker = '%%BLOB_NAME%%',
  otherInterpolations = {},
}: InlineTranslatedBlobProps) => {
  const { t } = useTranslation();

  const blobComponent = blob && (
    <Box component="span" display="inline-flex" px="2px" sx={{ verticalAlign: 'text-bottom' }}>
      <IconNameWithDetailsModal blob={blob} name={blob?.name ?? ''} color={blob?.color ?? '#888888'} />
    </Box>
  );

  const translated = t(translationKey, { [interpolationKey]: marker, ...otherInterpolations });
  const parts = translated.split(marker);

  return (
    <Box component="span" display="inline" whiteSpace="pre-line">
      <Typography component="span" variant="body1" sx={{ verticalAlign: 'middle' }}>
        {parts[0]}
      </Typography>
      {blobComponent}
      <Typography component="span" variant="body1" sx={{ verticalAlign: 'middle' }}>
        {parts[1]}
      </Typography>
    </Box>
  );
};

export default InlineTranslatedBlob;
