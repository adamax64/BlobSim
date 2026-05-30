import { Box, IconButton, Tooltip } from '@mui/material';
import InfoOutlined from '@mui/icons-material/InfoOutlined';
import { useTranslation } from 'react-i18next';
import { ProgressButton } from './ProgressButton';
import { useAuth } from '../../../context/AuthContext';
import { Dispatch, SetStateAction, useEffect } from 'react';
import { StepBackButton, StepForwardButton } from '../../common/ReplayStepButtons';
import { useIsMobile } from '../../../hooks/useIsMobile';

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
  const isMobile = useIsMobile();

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

  const shortcutTooltip = t('event_controls.shortcuts');

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
        case 'ArrowLeft':
          handlePreviousTick();
          event.preventDefault();
          break;
        case 'ArrowRight':
          handleNextTick();
          event.preventDefault();
          break;
        default:
          return;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleNextTick, handlePreviousTick]);

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
      <StepBackButton onClick={handlePreviousTick} disabled={replayTick <= 0} />
      <StepForwardButton onClick={handleNextTick} disabled={replayTick >= tick} />
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
      {!isMobile && (
        <Tooltip
          title={
            <Box component="span" sx={{ whiteSpace: 'pre-line', fontSize: '0.85rem', lineHeight: 1.4 }}>
              {shortcutTooltip}
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
