import {
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import { GrandmasterStandingsDTO } from '../../../generated';
import { BlobState, getClassNameForBlobState } from '../../utils/BlobStateUtils';
import { IconName } from '../common/IconName';

function getRowClass(hasEonEnded: boolean, position: number): string {
  return hasEonEnded ? (position === 1 ? getClassNameForBlobState(BlobState.FIRST) : '') : '';
}

interface GrandmasterStandingsTableProps {
  standings: GrandmasterStandingsDTO[];
  loading: boolean;
  eon?: number;
  hasEonEnded: boolean;
}

export function GrandmasterStandingsTable({ loading, standings, eon, hasEonEnded }: GrandmasterStandingsTableProps) {
  if (loading) {
    return (
      <Paper sx={{ margin: 2, padding: 2, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Paper>
    );
  }

  if (!standings || standings.length === 0) {
    return (
      <Paper sx={{ margin: 2, padding: 2, display: 'flex', justifyContent: 'center' }}>
        <p>No data found for eon {eon}</p>
      </Paper>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ margin: 2, width: '97%' }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>#</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Championships</TableCell>
            <TableCell>Gold</TableCell>
            <TableCell>Silver</TableCell>
            <TableCell>Bronze</TableCell>
            <TableCell>Points</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {standings.map((standing, index) => (
            <TableRow key={index} className={getRowClass(hasEonEnded, index + 1)}>
              <TableCell>{index + 1}</TableCell>
              <TableCell>
                <IconName name={standing.name} color={standing.color} />
              </TableCell>
              <TableCell>{standing.championships}</TableCell>
              <TableCell>{standing.gold}</TableCell>
              <TableCell>{standing.silver}</TableCell>
              <TableCell>{standing.bronze}</TableCell>
              <TableCell>{standing.points}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
