import { AddCircle, Save, SkipNext, Stadium } from '@mui/icons-material';
import { AppBar, Box, Button, IconButton, Toolbar, Tooltip } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { BlobNamingDialog } from '../common/BlobNamingDialog';
import { useNavigate } from '@tanstack/react-router';
import { Dispatch, SetStateAction, useState } from 'react';
import { UseMutateFunction, useMutation } from '@tanstack/react-query';
import { NewsDto, SimDataApi, AdminApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { useSimTime } from '../../context/SimTimeContext';
import { useAuth } from '../../context/AuthContext';
import { useSnackbar } from 'notistack';

type ControlButtonsFooterProps = {
  fetchNews: UseMutateFunction<NewsDto[], Error, void, unknown>;
  setLoadingOverlayVisible: Dispatch<SetStateAction<boolean>>;
  isLoadingNews: boolean;
  canCreateBlob: boolean;
  canStartEvent: boolean;
  canContinue: boolean;
};

export const ControlButtonsFooter = ({
  fetchNews,
  setLoadingOverlayVisible,
  isLoadingNews,
  canCreateBlob,
  canStartEvent,
  canContinue,
}: ControlButtonsFooterProps) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { refreshSimTime } = useSimTime();

  const { enqueueSnackbar } = useSnackbar();

  const [open, setOpen] = useState(false);

  const simDataApi = new SimDataApi(defaultConfig);
  const adminApi = new AdminApi(defaultConfig);

  const { mutate: progressSimulation, isPending: isProgressingSimulation } = useMutation({
    mutationFn: () => simDataApi.progressSimDataSimulatePost(),
    onSuccess: () => {
      fetchNews();
      refreshSimTime();
    },
  });

  const { mutate: downloadDbDump, isPending: isDownloadingDump } = useMutation({
    mutationFn: async () => {
      try {
        const response = await adminApi.downloadDbDumpAdminDbDumpGetRaw();
        if (!response.raw.ok) {
          throw new Error(`HTTP error! status: ${response.raw.status}`);
        }
        return response.raw;
      } catch (error) {
        console.error('Database dump download failed:', error);
        throw error;
      }
    },
    onSuccess: async (response) => {
      try {
        const blob = await response.blob();
        if (blob.size === 0) {
          throw new Error('Downloaded file is empty');
        }

        // Get filename from Content-Disposition header or use default
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'bcs_database_dump.pgadmin';
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
          if (filenameMatch) {
            filename = filenameMatch[1];
          }
        }

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        enqueueSnackbar(t('dashboard.download_db_dump_success'), { variant: 'success' });
      } catch (error) {
        console.error('Error processing downloaded file:', error);
        throw error;
      }
    },
    onError: (error) => {
      console.error('Database dump download failed:', error);
      enqueueSnackbar(t('dashboard.download_db_dump_failed'), { variant: 'error' });
    },
  });

  const handleDialogClose = (update?: boolean) => {
    setOpen(false);
    if (update) {
      fetchNews();
    }
  };

  const handleProgressClick = () => {
    setLoadingOverlayVisible(true);
    progressSimulation();
  };

  return (
    <AppBar position="relative" color="default" sx={{ top: 'auto', bottom: 0 }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box display="flex" gap={1}>
          {canStartEvent && (
            <Button
              variant="contained"
              color="success"
              endIcon={<Stadium />}
              onClick={() => navigate({ to: '/event' })}
            >
              {t('dashboard.proceed_to_event')}
            </Button>
          )}
          {isAuthenticated && canCreateBlob && (
            <Button variant="contained" color="primary" endIcon={<AddCircle />} onClick={() => setOpen(true)}>
              {t('dashboard.create_new_blob')}
            </Button>
          )}
          {isAuthenticated && canContinue && (
            <Button
              variant="contained"
              color="primary"
              endIcon={<SkipNext />}
              onClick={handleProgressClick}
              disabled={isLoadingNews || isProgressingSimulation}
            >
              {t('dashboard.proceed_to_next_day')}
            </Button>
          )}
        </Box>
        {isAuthenticated && (
          <Tooltip title={t('dashboard.download_db_dump_tooltip')}>
            <IconButton color="warning" onClick={() => downloadDbDump()} disabled={isDownloadingDump}>
              <Save />
            </IconButton>
          </Tooltip>
        )}
      </Toolbar>
      {/* TODO: handle blob with parent creation */}
      <BlobNamingDialog open={open} onClose={handleDialogClose} mode="create" />
    </AppBar>
  );
};
