import { Box, Card, CardContent, Grid, Typography, useTheme } from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { SimTimeDisplay } from '../common/SimTimeDisplay';
import { useSimTime } from '../../context/SimTimeContext';
import { useTranslation } from 'react-i18next';
import Administration from '../dashboard-components/administration-components/Administration';
import SimActions from '../dashboard-components/sim-actions/SimActions';
import News from '../dashboard-components/news-components/News';
import Gym from '../dashboard-components/gym-components/Gym';

const GRID_CELL_SIZE = { xs: 12, sm: 6, lg: 4 };

export function DashboardPage() {
  const { t } = useTranslation();

  const { loading: simTimeLoading } = useSimTime();

  return (
    <PageFrame showLoading={simTimeLoading} pageName="dashboard" customFrameStyle={{ p: 2 }}>
      <Box gap={2} display="flex">
        <Card sx={{ flexGrow: 1 }}>
          <CardContent>
            <Box display="flex" flexDirection="column" gap={1}>
              <Typography variant="h6">{t('dashboard.date')}</Typography>
              <SimTimeDisplay />
            </Box>
          </CardContent>
        </Card>
      </Box>
      <Grid container spacing={2}>
        <Grid size={GRID_CELL_SIZE}>
          <Administration />
        </Grid>
        <Grid size={GRID_CELL_SIZE}>
          <News />
        </Grid>
        <Grid size={GRID_CELL_SIZE}>
          <Gym />
        </Grid>
      </Grid>
      <SimActions />
    </PageFrame>
  );
}
