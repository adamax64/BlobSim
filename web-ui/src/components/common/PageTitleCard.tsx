import { Box, Card, CardHeader, Skeleton, useMediaQuery, useTheme } from '@mui/material';
import { BlobIcon } from '../icons/BlobIcon';
import { useMemo } from 'react';

interface PageTitleCardProps {
  title?: string;
  blobIconColor?: string;
  center?: boolean;
}

export function PageTitleCard({ title, blobIconColor, center }: PageTitleCardProps) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const iconColor = useMemo(
    () => blobIconColor ?? `#${Math.floor(Math.random() * 16777215).toString(16)}`,
    [blobIconColor],
  );

  return (
    <Card>
      <CardHeader
        title={
          <Box display="flex" gap={2} justifyContent={center && !isMobile ? 'space-between' : 'start'}>
            <BlobIcon size={32} color={iconColor} />
            {title || <Skeleton variant="text" width={320} />}
            {!isMobile && <BlobIcon size={32} color={iconColor} />}
          </Box>
        }
      />
    </Card>
  );
}
