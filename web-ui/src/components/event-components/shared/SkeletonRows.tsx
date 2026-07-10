import { Skeleton, TableCell, TableRow } from '@mui/material';

type SkeletonRowsProps = {
  columnCount: number;
};

const SkeletonRows = ({ columnCount }: SkeletonRowsProps) => {
  return Array.from({ length: 5 }, (_, index) => (
    <TableRow key={index}>
      {Array.from({ length: columnCount }, (_, i) => (
        <TableCell key={i}>
          <Skeleton variant="text" />
        </TableCell>
      ))}
    </TableRow>
  ));
};

export default SkeletonRows;
