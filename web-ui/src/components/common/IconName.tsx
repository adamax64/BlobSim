import { Box, Typography } from '@mui/material';
import { BlobIcon } from '../icons/BlobIcon';

interface IconNameProps {
  name: string;
  color: string;
  size?: number;
}

export function IconName({ name, color, size = 20 }: IconNameProps) {
  return (
    <Box display="flex" alignItems="center" gap={1}>
      <BlobIcon size={size} color={color} />
      <Typography variant="body2" component="span" noWrap>
        {name}
      </Typography>
    </Box>
  );
} 