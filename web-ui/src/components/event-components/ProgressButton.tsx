import { Box, Fab } from '@mui/material';
import ArrowBackIosNewRoundedIcon from '@mui/icons-material/ArrowBackIosNewRounded';
import PlayArrowRounded from '@mui/icons-material/PlayArrowRounded';
import SkipNextRounded from '@mui/icons-material/SkipNextRounded';
import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';
import { useNavigate } from '@tanstack/react-router';

interface ProgressButtonProps {
  isStart: boolean;
  isEnd: boolean;
  isEventFinished: boolean;
  disabled?: boolean;
  onClickStart: () => void;
  onClickEnd: () => void;
  onClickNext: () => void;
}

export const ProgressButton: React.FC<ProgressButtonProps> = ({
  isStart,
  isEnd,
  isEventFinished,
  disabled,
  onClickStart,
  onClickNext,
  onClickEnd,
}: ProgressButtonProps) => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  // Add key listener for spacebar to trigger progressEvent
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' || e.key === ' ') {
        e.preventDefault();
        if (isStart) {
          onClickStart();
        } else if (!isStart && !isEnd) {
          onClickNext();
        } else if (isEnd && !isEventFinished) {
          onClickEnd();
        } else if (isEventFinished) {
          navigate({ to: '/' });
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isStart, isEnd, isEventFinished, onClickStart, onClickNext, onClickEnd]);

  return (
    <Box position="fixed" right={0} bottom={0} padding={2} zIndex={1000}>
      {isStart && (
        <Fab variant="extended" color="primary" onClick={onClickStart} disabled={disabled}>
          <PlayArrowRounded />
          {t('progress_button.start_competition')}
        </Fab>
      )}
      {!isStart && !isEnd && (
        <Fab variant="extended" color="primary" onClick={onClickNext} disabled={disabled}>
          <PlayArrowRounded />
          {t('progress_button.next')}
        </Fab>
      )}
      {isEnd && !isEventFinished && (
        <Fab variant="extended" color="primary" onClick={onClickEnd} disabled={disabled}>
          <SkipNextRounded />
          {t('progress_button.conclude_event')}
        </Fab>
      )}
      {isEventFinished && (
        <Fab variant="extended" color="primary" onClick={() => navigate({ to: '/' })} disabled={disabled}>
          <ArrowBackIosNewRoundedIcon />
          {t('progress_button.back_to_dashboard')}
        </Fab>
      )}
    </Box>
  );
};
