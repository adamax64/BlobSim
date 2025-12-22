import { Box, Card, CardContent, Typography } from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { SimTimeDisplay } from '../common/SimTimeDisplay';
import { useSimTime } from '../../context/SimTimeContext';
import { useTranslation } from 'react-i18next';
import { NewsAndFooter } from '../dashboard-components/NewsAndFooter';
import PoliciesPanel from '../dashboard-components/PoliciesPanel';
import { usePolicies } from '../../context/PoliciesContext';

export function DashboardPage() {
  const { t } = useTranslation();

  const { loading: simTimeLoading } = useSimTime();
  const { policiesLoading } = usePolicies();

  return (
    <PageFrame showLoading={simTimeLoading || policiesLoading} pageName="dashboard">
      <Box gap={2} display="flex">
        <Card sx={{ flexGrow: 1 }}>
          <CardContent>
            <Box display="flex" flexDirection="column" gap={1}>
              <Typography variant="h6">{t('dashboard.date')}</Typography>
              <SimTimeDisplay />
            </Box>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Box display="flex" flexDirection="column" gap={1} alignItems={{ xs: 'center', xl: 'flex-start' }}>
              <Typography variant="h6">{t('policies.title')}</Typography>
              <PoliciesPanel />
            </Box>
          </CardContent>
        </Card>
      </Box>
      <NewsAndFooter />
    </PageFrame>
  );
}
