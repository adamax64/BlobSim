import { Box, Fab } from '@mui/material';
import ArrowBackIosNewRoundedIcon from '@mui/icons-material/ArrowBackIosNewRounded';
import PlayArrowRounded from '@mui/icons-material/PlayArrowRounded';
import SkipNextRounded from '@mui/icons-material/SkipNextRounded';
import { useTranslation } from 'react-i18next';

interface ProgressButtonProps {
  isStart: boolean;
  isEnd: boolean;
  isEventFinished: boolean;
  onClickStart: () => void;
  onClickEnd: () => void;
  onClickNext: () => void;
}

export const ProgressButton = ({
  isStart,
  isEnd,
  isEventFinished,
  onClickStart,
  onClickNext,
  onClickEnd,
}: ProgressButtonProps) => {
  const { t } = useTranslation();

  return (
    <Box position="fixed" right={0} bottom={0} padding={2}>
      {isStart && (
        <Fab variant="extended" color="primary" onClick={onClickStart}>
          <PlayArrowRounded />
          {t('progress_button.start_competition')}
        </Fab>
      )}
      {!isStart && !isEnd && (
        <Fab variant="extended" color="primary" onClick={onClickNext}>
          <PlayArrowRounded />
          {t('progress_button.next')}
        </Fab>
      )}
      {isEnd && !isEventFinished && (
        <Fab variant="extended" color="primary" onClick={onClickEnd}>
          <SkipNextRounded />
          {t('progress_button.conclude_event')}
        </Fab>
      )}
      {isEventFinished && (
        <Fab variant="extended" color="primary" onClick={() => (window.location.href = '/')}>
          <ArrowBackIosNewRoundedIcon />
          {t('progress_button.back_to_dashboard')}
        </Fab>
      )}
    </Box>
  );
};
