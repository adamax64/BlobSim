import {
  Box,
  Card,
  CardContent,
  CardHeader,
  LinearProgress,
  Paper,
  styled,
  Table,
  TableCell,
  TableContainer,
  TableHead,
  Typography,
} from '@mui/material';
import { EventDto } from '../../../generated';
import { translateEventType } from '../../utils/EnumTranslationUtils';
import { ProgressButton } from './ProgressButton';
import { useState } from 'react';

const TickLoadingBar = styled(LinearProgress)({
  marginTop: 12,
  height: 8,
  borderRadius: 10,
});

interface EnduranceRaceEventFrameProps {
  event: EventDto;
}

export const EnduranceRaceEventFrame = ({ event }: EnduranceRaceEventFrameProps) => {
  const [tick, setTick] = useState(0);
  const [isEventFinished, setIsEventFinished] = useState(false);
  const [loadingNextTick, setLoadingNextTick] = useState(false);

  return (
    <Card>
      <CardHeader title={translateEventType(event.type)} />
      <CardContent>
        <ProgressButton
          isStart={tick === 0}
          isEnd={false}
          isEventFinished={isEventFinished}
          onClickStart={() => {}}
          onClickNext={() => {}}
          onClickEnd={() => {}}
        />
        <Typography fontSize={18} fontWeight={600} paddingBottom={2}>
          Tick: {tick}
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableCell>#</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Distance</TableCell>
              <TableCell>Delta leader</TableCell>
              <TableCell>Delta interval</TableCell>
            </TableHead>
          </Table>
        </TableContainer>
        {loadingNextTick && <TickLoadingBar />}
      </CardContent>
    </Card>
  );
};
