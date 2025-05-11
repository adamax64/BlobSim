import { PlayArrowRounded, SkipNextRounded } from '@mui/icons-material';
import { Button } from '@mui/material';

interface ProgressButtonProps {
  isStart: boolean;
  isEnd: boolean;
  onClickStart: () => void;
  onClickEnd: () => void;
  onClickNext: () => void;
}

export const ProgressButton = ({ isStart, isEnd, onClickStart, onClickNext, onClickEnd }: ProgressButtonProps) => {
  return (
    <>
      {isStart && (
        <Button variant="contained" color="primary" onClick={onClickStart} startIcon={<PlayArrowRounded />}>
          Start Competition
        </Button>
      )}
      {!isStart && !isEnd && (
        <Button variant="contained" color="primary" onClick={onClickNext} startIcon={<PlayArrowRounded />}>
          Next
        </Button>
      )}
      {isEnd && (
        <Button variant="contained" color="primary" onClick={onClickEnd} startIcon={<SkipNextRounded />}>
          Conclude Event
        </Button>
      )}
    </>
  );
};
