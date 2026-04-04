import { Box, Fab, TextField, Tooltip } from '@mui/material';
import SkipPrevious from '@mui/icons-material/SkipPrevious';
import SkipNext from '@mui/icons-material/SkipNext';
import FirstPage from '@mui/icons-material/FirstPage';
import LastPage from '@mui/icons-material/LastPage';
import ArrowBack from '@mui/icons-material/ArrowBack';
import { useTranslation } from 'react-i18next';
import { useCallback, useEffect, useState } from 'react';

interface ReplayControlsProps {
  currentTick: number;
  maxTick: number | undefined;
  setCurrentTick: (tick: number | ((prev: number) => number)) => void;
  onGoBack: () => void;
}

const TickInput: React.FC<{
  maxTick: number | undefined;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur: () => void;
}> = ({ maxTick, ...props }) => (
  <TextField
    size="small"
    type="number"
    slotProps={{ input: { inputProps: { min: 0, max: maxTick } } }}
    sx={{
      width: 45,
      '& .MuiInputBase-input': {
        padding: '8px',
        textAlign: 'center',
      },
      '& input[type=number]': {
        '-moz-appearance': 'textfield',
      },
      '& input[type=number]::-webkit-outer-spin-button, & input[type=number]::-webkit-inner-spin-button': {
        '-webkit-appearance': 'none',
        margin: 0,
      },
    }}
    {...props}
  />
);

export const ReplayControls: React.FC<ReplayControlsProps> = ({ currentTick, maxTick, setCurrentTick, onGoBack }) => {
  const { t } = useTranslation();
  const [inputValue, setInputValue] = useState(currentTick.toString());

  useEffect(() => {
    setInputValue(currentTick.toString());
  }, [currentTick]);

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

  const handleBlur = useCallback(() => {
    const num = parseInt(inputValue, 10);

    if (!isNaN(num) && num >= 0) {
      const validNum = maxTick !== undefined ? Math.min(num, maxTick) : num;
      setCurrentTick(validNum);
      setInputValue(validNum.toString());
    } else {
      setInputValue(currentTick.toString());
    }
  }, [inputValue, maxTick, setCurrentTick, currentTick]);

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
      <Tooltip title={t('replay.set_tick')}>
        <TickInput
          maxTick={maxTick}
          value={inputValue}
          onChange={(e) => {
            const value = e.target.value;
            if (value.length <= 3) {
              setInputValue(value);
            }
          }}
          onBlur={handleBlur}
        />
      </Tooltip>
      <Tooltip title={t('replay.step_forward')}>
        <Fab size="small" onClick={handleStepForward} disabled={maxTick === undefined || currentTick >= maxTick}>
          <SkipNext />
        </Fab>
      </Tooltip>
      <Tooltip title={t('replay.jump_to_end')}>
        <Fab size="small" onClick={handleJumpToEnd} disabled={maxTick === undefined || currentTick >= maxTick}>
          <LastPage />
        </Fab>
      </Tooltip>
    </Box>
  );
};
