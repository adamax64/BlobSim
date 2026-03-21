import { AccordionSummary, LinearProgress, styled, TableCell } from '@mui/material';
import { width } from '@mui/system';

export const TickLoadingBar = styled(LinearProgress)({
  height: 8,
  borderRadius: 10,
});

export const NarrowCell = styled(TableCell)(({}) => ({
  paddingLeft: '8px',
  paddingRight: '8px',
}));

export const DistanceProgress = styled(LinearProgress)({
  '&.MuiLinearProgress-root': {
    width: '100%',
  },
  height: 24,
  borderRadius: 2,
});

export const SmallAccordionTitle = styled(AccordionSummary)(({ theme }) => ({
  '& .MuiAccordionSummary-content, & .MuiAccordionSummary-content.Mui-expanded': {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
  '&, &.Mui-expanded': {
    minHeight: '40px',
  },
}));
