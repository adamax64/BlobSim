import { Box, Card, useTheme } from '@mui/material';
import { useSimTime } from '../../context/SimTimeContext';
import { useEffect } from 'react';

export function SimTimeDisplay() {
  const { simTime, refreshSimTime } = useSimTime();
  const theme = useTheme();

  useEffect(() => {
    if (!simTime) {
      refreshSimTime();
    }
  }, [refreshSimTime, simTime]);

  const isDarkMode = theme.palette.mode === 'dark';
  const colorCard = isDarkMode ? { backgroundColor: 'divider' } : undefined;

  return (
    <Box display="flex" gap={0} sx={{ fontWeight: '600' }}>
      {simTime ? (
        <>
          <Card className="p-2" sx={colorCard}>
            {simTime.season}
          </Card>
          <Box className="pe-2 pb-2 ps-1" sx={{ display: 'flex', alignItems: 'end' }}>
            .
          </Box>
          <Card className="p-2" sx={colorCard}>
            {simTime.epoch}
          </Card>
          <Box className="pe-2 pb-2 ps-2" sx={{ display: 'flex', alignItems: 'end' }}>
            -
          </Box>
          <Card className="p-2" sx={colorCard}>
            {simTime.cycle}
          </Card>{' '}
        </>
      ) : (
        'Loading...'
      )}
    </Box>
  );
}
