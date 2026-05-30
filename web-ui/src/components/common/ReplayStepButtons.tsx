import { Fab, Tooltip } from '@mui/material';
import SkipNext from '@mui/icons-material/SkipNext';
import SkipPrevious from '@mui/icons-material/SkipPrevious';
import FirstPage from '@mui/icons-material/FirstPage';
import LastPage from '@mui/icons-material/LastPage';
import ArrowBack from '@mui/icons-material/ArrowBack';
import { useTranslation } from 'react-i18next';

interface ReplayButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

export const StepBackButton: React.FC<ReplayButtonProps> = ({ onClick, disabled = false }) => {
  const { t } = useTranslation();

  return (
    <Tooltip title={t('replay.step_back')}>
      <Fab size="small" onClick={onClick} disabled={disabled}>
        <SkipPrevious />
      </Fab>
    </Tooltip>
  );
};

export const StepForwardButton: React.FC<ReplayButtonProps> = ({ onClick, disabled = false }) => {
  const { t } = useTranslation();

  return (
    <Tooltip title={t('replay.step_forward')}>
      <Fab size="small" onClick={onClick} disabled={disabled}>
        <SkipNext />
      </Fab>
    </Tooltip>
  );
};

export const JumpToStartButton: React.FC<ReplayButtonProps> = ({ onClick, disabled = false }) => {
  const { t } = useTranslation();

  return (
    <Tooltip title={t('replay.jump_to_start')}>
      <Fab size="small" onClick={onClick} disabled={disabled}>
        <FirstPage />
      </Fab>
    </Tooltip>
  );
};

export const JumpToEndButton: React.FC<ReplayButtonProps> = ({ onClick, disabled = false }) => {
  const { t } = useTranslation();

  return (
    <Tooltip title={t('replay.jump_to_end')}>
      <Fab size="small" onClick={onClick} disabled={disabled}>
        <LastPage />
      </Fab>
    </Tooltip>
  );
};

export const GoBackButton: React.FC<ReplayButtonProps> = ({ onClick, disabled = false }) => {
  const { t } = useTranslation();

  return (
    <Tooltip title={t('replay.go_back')}>
      <Fab size="small" onClick={onClick} disabled={disabled}>
        <ArrowBack />
      </Fab>
    </Tooltip>
  );
};
