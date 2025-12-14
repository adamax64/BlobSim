import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { BlobStatsDto } from '../../../generated';
import { IconNameWithDetailsModal } from '../common/IconNameWithDetailsModal';
import { BlobState, getClassNameForBlobState } from '../../utils/blob-state-utils';

function getRowClass(position: number): string | undefined {
  let state: BlobState | undefined;
  switch (position) {
    case 1:
      state = BlobState.FIRST;
      break;
    case 2:
      state = BlobState.SECOND;
      break;
    case 3:
      state = BlobState.THIRD;
      break;
  }

  return state ? getClassNameForBlobState(state) : undefined;
}

type ResultDto = {
  blob: BlobStatsDto;
  position: number;
  points: number;
};

type ResultsTableProps = {
  results: ResultDto[];
};

export const ResultsTable = ({ results }: ResultsTableProps) => {
  return (
    <TableContainer component={Paper}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>#</TableCell>
            <TableCell>Blob</TableCell>
            <TableCell align="right">Points</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {results.map((r, idx) => (
            <TableRow key={idx} className={getRowClass(r.position)}>
              <TableCell>{r.position}</TableCell>
              <TableCell>
                <IconNameWithDetailsModal blob={r.blob} color={r.blob.color} name={r.blob.name} />
              </TableCell>
              <TableCell align="right">{r.points}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ResultsTable;
