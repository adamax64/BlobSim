import { Box, Fab, Tooltip } from '@mui/material';
import { SkipPrevious, SkipNext, FirstPage, LastPage, ArrowBack } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { useCallback } from 'react';

interface ReplayControlsProps {
  currentTick: number;
  maxTick: number | undefined;
  setCurrentTick: (tick: number | ((prev: number) => number)) => void;
  onGoBack: () => void;
}

export const ReplayControls: React.FC<ReplayControlsProps> = ({ currentTick, maxTick, setCurrentTick, onGoBack }) => {
  const { t } = useTranslation();

  const handleStepBack = useCallback(() => {
    setCurrentTick((prev) => Math.max(0, prev - 1));
  }, [setCurrentTick]);

  const handleStepForward = useCallback(() => {
    setCurrentTick((prev) => (maxTick !== undefined ? Math.min(maxTick, prev + 1) : prev));
  }, [maxTick, setCurrentTick]);

  const handleJumpToStart = useCallback(() => {
    setCurrentTick(0);
  }, [setCurrentTick]);

  const handleJumpToEnd = useCallback(() => {
    if (maxTick !== undefined) {
      setCurrentTick(maxTick);
    }
  }, [maxTick, setCurrentTick]);

  return (
    <Box
      sx={{
        position: 'fixed',
        bottom: 16,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: 1,
        zIndex: 1000,
      }}
    >
      <Tooltip title={t('replay.go_back')}>
        <Fab size="small" onClick={onGoBack}>
          <ArrowBack />
        </Fab>
      </Tooltip>
      <Tooltip title={t('replay.jump_to_start')}>
        <Fab size="small" onClick={handleJumpToStart} disabled={currentTick <= 0}>
          <FirstPage />
        </Fab>
      </Tooltip>
      <Tooltip title={t('replay.step_back')}>
        <Fab size="small" onClick={handleStepBack} disabled={currentTick <= 0}>
          <SkipPrevious />
        </Fab>
      </Tooltip>
      <Tooltip title={t('replay.step_forward')}>
        <Fab size="small" onClick={handleStepForward} disabled={maxTick === undefined || currentTick >= maxTick}>
          <SkipNext />
        </Fab>
      </Tooltip>
      <Tooltip title={t('replay.jump_to_end')}>
        <Fab size="small" onClick={handleJumpToEnd}>
          <LastPage />
        </Fab>
      </Tooltip>
    </Box>
  );
};
