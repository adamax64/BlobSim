import { Box, Fab } from '@mui/material';
import ArrowBackIosNewRoundedIcon from '@mui/icons-material/ArrowBackIosNewRounded';
import PlayArrowRounded from '@mui/icons-material/PlayArrowRounded';
import SkipNextRounded from '@mui/icons-material/SkipNextRounded';

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
  return (
    <Box position="fixed" right={0} bottom={0} padding={2}>
      {isStart && (
        <Fab variant="extended" color="primary" onClick={onClickStart}>
          <PlayArrowRounded />
          Start Competition
        </Fab>
      )}
      {!isStart && !isEnd && (
        <Fab variant="extended" color="primary" onClick={onClickNext}>
          <PlayArrowRounded />
          Next
        </Fab>
      )}
      {isEnd && !isEventFinished && (
        <Fab variant="extended" color="primary" onClick={onClickEnd}>
          <SkipNextRounded />
          Conclude Event
        </Fab>
      )}
      {isEventFinished && (
        <Fab variant="extended" color="primary" onClick={() => (window.location.href = '/')}>
          <ArrowBackIosNewRoundedIcon />
          Back to Dashboard
        </Fab>
      )}
    </Box>
  );
};
