import { Box, Fab, Tooltip } from '@mui/material';
import SkipNext from '@mui/icons-material/SkipNext';
import SkipPrevious from '@mui/icons-material/SkipPrevious';
import { useTranslation } from 'react-i18next';
import { ProgressButton } from './ProgressButton';
import { useAuth } from '../../../context/AuthContext';
import { Dispatch, SetStateAction } from 'react';

interface EventControlsProps {
  // Replay navigation
  tick: number;
  replayTick: number;
  setReplayTick: Dispatch<SetStateAction<number>>;

  // Progress button
  isStart: boolean;
  isEnd: boolean;
  isEventFinished: boolean;
  progressButtonDisabled: boolean;
  onClickStart: () => void;
  onClickNext: () => void;
  onClickEnd: () => void;
}

export const EventControls: React.FC<EventControlsProps> = ({
  tick,
  replayTick,
  setReplayTick,
  isStart,
  isEnd,
  isEventFinished,
  progressButtonDisabled: disabled,
  onClickStart,
  onClickNext,
  onClickEnd,
}) => {
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();

  const handlePreviousTick = () => {
    if (replayTick > 0) {
      setReplayTick((prev) => prev - 1);
    }
  };

  const handleNextTick = () => {
    if (replayTick < tick) {
      setReplayTick((prev) => prev + 1);
    }
  };

  return (
    <Box
      sx={{
        position: 'fixed',
        bottom: 16,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        zIndex: 1000,
      }}
    >
      <Tooltip title={t('replay.step_back')}>
        <Fab size="small" onClick={handlePreviousTick} disabled={replayTick <= 0}>
          <SkipPrevious />
        </Fab>
      </Tooltip>
      <Tooltip title={t('replay.step_forward')}>
        <Fab size="small" onClick={handleNextTick} disabled={replayTick >= tick}>
          <SkipNext />
        </Fab>
      </Tooltip>
      {isAuthenticated && (
        <ProgressButton
          isStart={isStart}
          isEnd={isEnd}
          isEventFinished={isEventFinished}
          disabled={disabled}
          onClickStart={onClickStart}
          onClickNext={onClickNext}
          onClickEnd={onClickEnd}
        />
      )}
    </Box>
  );
};
