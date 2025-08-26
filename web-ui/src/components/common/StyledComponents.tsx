import { LinearProgress, styled, TableCell } from '@mui/material';

export const TickLoadingBar = styled(LinearProgress)({
  height: 8,
  borderRadius: 10,
});

export const NarrowCell = styled(TableCell)(({}) => ({
  paddingLeft: '8px',
  paddingRight: '8px',
}));
