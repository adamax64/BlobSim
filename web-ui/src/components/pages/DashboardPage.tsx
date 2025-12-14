import { Box, Card, CardContent, Typography } from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { SimTimeDisplay } from '../common/SimTimeDisplay';
import { useSimTime } from '../../context/SimTimeContext';
import { useTranslation } from 'react-i18next';
import { NewsAndFooter } from '../dashboard-components/NewsAndFooter';

export function DashboardPage() {
  const { t } = useTranslation();

  const { loading: simTimeLoading } = useSimTime();

  return (
    <PageFrame showLoading={simTimeLoading} pageName="dashboard">
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">{t('dashboard.date')}</Typography>
            <SimTimeDisplay />
          </Box>
        </CardContent>
      </Card>
      <NewsAndFooter />
    </PageFrame>
  );
}
