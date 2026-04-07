import { Box, Button, Card, CardContent, Typography, Switch, FormControlLabel, IconButton } from '@mui/material';
import { PageFrame } from '../common/PageFrame';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import { AdminApi, Configuration } from '../../../generated';
import defaultConfig from '../../default-config';
import { useSnackbar } from 'notistack';
import DownloadIcon from '@mui/icons-material/Download';
import CloseIcon from '@mui/icons-material/Close';
import { useMutation } from '@tanstack/react-query';
import { useEffect } from 'react';

export function AdminPage() {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const snackbarOptions = {
    autoHideDuration: 5000,
    action: (key: any) => (
      <IconButton color="inherit" size="small" onClick={() => closeSnackbar(key)}>
        <CloseIcon />
      </IconButton>
    ),
  };

  const adminApi = new AdminApi(defaultConfig);

  // Query to get cronjobs status
  const {
    data: cronjobsData,
    isPending: cronjobsLoading,
    mutate: getCronjobsEnabled,
  } = useMutation({
    mutationFn: async () => adminApi.getCronjobsEnabledAdminCronjobsEnabledGet(),
    onError: (error) => {
      console.error('Failed to fetch cronjobs status:', error);
      enqueueSnackbar(t('admin.cronjobs_fetch_failed'), { variant: 'error', ...snackbarOptions });
    },
  });

  // Mutation to toggle cronjobs
  const { isPending: cronjobsToggleLoading, mutate: setCronjobsEnabled } = useMutation({
    mutationFn: async (enabled: boolean) => adminApi.setCronjobsEnabledAdminCronjobsEnabledPost({ enabled }),
    onSuccess: (data) => {
      enqueueSnackbar(data.enabled ? t('admin.cronjobs_enabled_success') : t('admin.cronjobs_disabled_success'), {
        variant: 'success',
        ...snackbarOptions,
      });
      getCronjobsEnabled(); // Refresh status after toggle
    },
    onError: (error, _) => {
      console.error('Failed to toggle cronjobs:', error);
      enqueueSnackbar(t('admin.cronjobs_toggle_failed'), { variant: 'error', ...snackbarOptions });
    },
  });

  const handleCronjobsToggle = (enabled: boolean) => {
    setCronjobsEnabled(enabled);
  };

  const handleDownloadDump = async () => {
    if (!isAuthenticated) {
      enqueueSnackbar(t('admin.not_authenticated'), { variant: 'error', ...snackbarOptions });
      return;
    }

    try {
      const token = localStorage.getItem('adminToken');
      const config = new Configuration({
        basePath: defaultConfig.basePath,
        headers: { Authorization: `Bearer ${token}` },
      });
      const adminApi = new AdminApi(config);

      // Trigger download
      const response = await adminApi.downloadDatabaseDumpAdminDbDumpGetRaw();

      // Create a blob from the response
      const blob = await response.raw.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;

      // Get filename from Content-Disposition header or fallback to dated filename
      const contentDisposition = response.raw.headers.get('content-disposition');
      let filename = 'database_dump.sql';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=([^;]+)/);
        if (filenameMatch) {
          filename = filenameMatch[1].replace(/"/g, '');
        }
      }
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      enqueueSnackbar(t('admin.download_success'), { variant: 'success', ...snackbarOptions });
    } catch (error) {
      console.error('Download failed:', error);
      enqueueSnackbar(t('admin.download_failed'), { variant: 'error', ...snackbarOptions });
    }
  };

  useEffect(() => {
    getCronjobsEnabled();
  }, [getCronjobsEnabled]);

  return (
    <PageFrame pageName="admin">
      <Box display="flex" flexDirection="column" gap={2}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {t('admin.database_management')}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {t('admin.database_dump_description')}
            </Typography>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={handleDownloadDump}
              disabled={!isAuthenticated}
            >
              {t('admin.download_database_dump')}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {t('admin.cronjobs_management')}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {t('admin.cronjobs_description')}
            </Typography>
            <FormControlLabel
              control={
                <Switch
                  checked={cronjobsData?.enabled ?? false}
                  onChange={(e) => handleCronjobsToggle(e.target.checked)}
                  disabled={!isAuthenticated || cronjobsToggleLoading}
                  color="primary"
                />
              }
              label={
                cronjobsLoading
                  ? t('admin.loading')
                  : (cronjobsData?.enabled ?? false)
                    ? t('admin.cronjobs_enabled')
                    : t('admin.cronjobs_disabled')
              }
            />
          </CardContent>
        </Card>
      </Box>
    </PageFrame>
  );
}
