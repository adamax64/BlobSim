import { Box, IconButton, TextField, Tooltip } from '@mui/material';
import InfoOutlined from '@mui/icons-material/InfoOutlined';
import { useTranslation } from 'react-i18next';
import { useCallback, useEffect, useState } from 'react';
import {
  GoBackButton,
  JumpToEndButton,
  JumpToStartButton,
  StepBackButton,
  StepForwardButton,
} from '../common/ReplayStepButtons';
import { useIsMobile } from '../../hooks/useIsMobile';

interface ReplayControlsProps {
  currentTick: number;
  maxTick: number | undefined;
  setCurrentTick: (tick: number | ((prev: number) => number)) => void;
  onGoBack: () => void;

  // Stage navigation: lets the step buttons also walk between the introduction, standings and
  // results stages once the tick range within the competition stage is exhausted.
  isCompetitionStage: boolean;
  canStepStageBack: boolean;
  canStepStageForward: boolean;
  onStepStageBack: () => void;
  onStepStageForward: () => void;
}

const TickInput: React.FC<{
  maxTick: number | undefined;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur: () => void;
  enabled: boolean;
}> = ({ maxTick, enabled, ...props }) => (
  <TextField
    size="small"
    type="number"
    slotProps={{ input: { inputProps: { min: 0, max: maxTick } } }}
    disabled={!enabled}
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

export const ReplayControls: React.FC<ReplayControlsProps> = ({
  currentTick,
  maxTick,
  setCurrentTick,
  onGoBack,
  isCompetitionStage,
  canStepStageBack,
  canStepStageForward,
  onStepStageBack,
  onStepStageForward,
}) => {
  const { t } = useTranslation();
  const isMobile = useIsMobile();
  const [inputValue, setInputValue] = useState(currentTick.toString());

  useEffect(() => {
    setInputValue(currentTick.toString());
  }, [currentTick]);

  const canGoBack = (isCompetitionStage && currentTick > 0) || canStepStageBack;
  const canGoForward = (isCompetitionStage && maxTick !== undefined && currentTick < maxTick) || canStepStageForward;

  const handleStepBack = useCallback(() => {
    if (isCompetitionStage && currentTick > 0) {
      setCurrentTick((prev) => Math.max(0, prev - 1));
    } else if (canStepStageBack) {
      onStepStageBack();
    }
  }, [isCompetitionStage, currentTick, canStepStageBack, onStepStageBack, setCurrentTick]);

  const handleStepForward = useCallback(() => {
    if (isCompetitionStage && maxTick !== undefined && currentTick < maxTick) {
      setCurrentTick((prev) => (maxTick !== undefined ? Math.min(maxTick, prev + 1) : prev));
    } else if (canStepStageForward) {
      onStepStageForward();
    }
  }, [isCompetitionStage, currentTick, maxTick, canStepStageForward, onStepStageForward, setCurrentTick]);

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

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.repeat) {
        return;
      }

      const activeElement = document.activeElement;
      if (
        activeElement instanceof HTMLInputElement ||
        activeElement instanceof HTMLTextAreaElement ||
        (activeElement instanceof HTMLElement && activeElement.isContentEditable)
      ) {
        return;
      }

      switch (event.key) {
        case 'Backspace':
          onGoBack();
          event.preventDefault();
          break;
        case 'Home':
          handleJumpToStart();
          event.preventDefault();
          break;
        case 'ArrowLeft':
          handleStepBack();
          event.preventDefault();
          break;
        case 'ArrowRight':
          handleStepForward();
          event.preventDefault();
          break;
        case 'End':
          handleJumpToEnd();
          event.preventDefault();
          break;
        default:
          return;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onGoBack, handleJumpToStart, handleStepBack, handleStepForward, handleJumpToEnd]);

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
      <GoBackButton onClick={onGoBack} />
      <JumpToStartButton onClick={handleJumpToStart} disabled={!isCompetitionStage || currentTick <= 0} />
      <StepBackButton onClick={handleStepBack} disabled={!canGoBack} />
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
          enabled={isCompetitionStage}
        />
      </Tooltip>
      <StepForwardButton onClick={handleStepForward} disabled={!canGoForward} />
      <JumpToEndButton onClick={handleJumpToEnd} disabled={!isCompetitionStage || maxTick === undefined || currentTick >= maxTick} />
      {!isMobile && (
        <Tooltip
          title={
            <Box component="span" sx={{ whiteSpace: 'pre-line', fontSize: '0.85rem', lineHeight: 1.4 }}>
              {t('replay.shortcuts')}
            </Box>
          }
        >
          <IconButton size="small" sx={{ color: 'text.secondary' }}>
            <InfoOutlined fontSize="small" />
          </IconButton>
        </Tooltip>
      )}
    </Box>
  );
};
