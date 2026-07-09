import { Box, Typography } from '@mui/material';
import { BlobIcon } from '../icons/BlobIcon';
import { useMemo } from 'react';
import { BlobStatsDto } from '../../../generated';
import { BlobStateBadge } from './BlobStateBadge';
import { DeadBlobIcon } from '../icons/DeadBlobIcon';
import { getShortName } from '../../utils/blob-name-utils';

export interface IconNameProps extends Partial<BlobStatsDto> {
  name: string;
  color: string;
  size?: number;
  renderFullName?: boolean;
}

export const IconName = ({
  name,
  color,
  atRisk,
  isRookie,
  isDead,
  size = 20,
  renderFullName = true,
}: IconNameProps) => {
  const formattedName = useMemo(() => {
    if (renderFullName) return name;

    return getShortName(name);
  }, [name, renderFullName]);

  return (
    <Box display="flex" alignItems="center" gap={1}>
      {isDead ? <DeadBlobIcon size={size} color={color} /> : <BlobIcon size={size} color={color} />}
      <BlobStateBadge atRisk={atRisk} isRookie={isRookie}>
        <Typography variant="body2" component="span" noWrap>
          {formattedName}
        </Typography>
      </BlobStateBadge>
    </Box>
  );
};
