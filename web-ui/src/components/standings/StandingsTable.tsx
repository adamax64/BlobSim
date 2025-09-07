import {
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { StandingsDTO } from '../../../generated';
import { BlobState, getClassNameForBlobState } from '../../utils/BlobStateUtils';
import { useCallback } from 'react';
import { useSimTime } from '../../context/SimTimeContext';
import { useTranslation } from 'react-i18next';
import { IconNameWithDetailsModal } from '../common/IconNameWithDetailsModal';

function getRowClass(position: number, hasSeasonEnded: boolean): string | undefined {
  let state: BlobState | undefined;
  if (hasSeasonEnded) {
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
  }

  return state ? getClassNameForBlobState(state) : undefined;
}

interface StandingsTableProps {
  standings: StandingsDTO[];
  loading: boolean;
  leagueName?: string;
  season?: number;
  hasSeasonEnded: boolean;
}

export const StandingsTable = ({ loading, standings, leagueName, season, hasSeasonEnded }: StandingsTableProps) => {
  const { simTime } = useSimTime();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { t } = useTranslation();

  const getThresholdClassName = useCallback(
    (position: number) => {
      return Math.ceil(standings.length / 2) === position && simTime?.season === season ? 'row-middle' : '';
    },
    [standings.length],
  );

  const getPositionClassName = (position: number): string => {
    if (position === 1) return ' text-gold';
    if (position === 2) return ' text-silver';
    if (position === 3) return ' text-bronze';
    return '';
  };

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
        <p>{t('standings_table.no_data', { leagueName, season })}</p>
      </Paper>
    );
  }

  return (
    <TableContainer
      component={Paper}
      sx={{
        margin: 2,
        width: 'auto',
      }}
    >
      <Table>
        <TableHead>
          <TableRow>
            <TableCell width={25}>#</TableCell>
            <TableCell>{t('standings_table.name')}</TableCell>
            {!isMobile &&
              standings[0]?.results.map((_, index) => (
                <TableCell key={index}>{t('standings_table.round', { round: index + 1 })}</TableCell>
              ))}
            {!isMobile &&
              Array.from(
                { length: standings[0]?.numOfRounds - standings[0]?.results.length },
                (_, index) => index + 1,
              ).map((index) => (
                <TableCell key={index}>
                  {t('standings_table.round', { round: standings[0].results.length + index })}
                </TableCell>
              ))}
            <TableCell>{t('standings_table.sum')}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {standings.map((standing, index) => (
            <TableRow key={index} className={getRowClass(index + 1, hasSeasonEnded)}>
              <TableCell className={getThresholdClassName(index + 1)}>{index + 1}</TableCell>
              <TableCell className={getThresholdClassName(index + 1)}>
                <IconNameWithDetailsModal
                  blobId={standing.blobId}
                  name={standing.name}
                  color={standing.color}
                  renderFullName={!isMobile}
                  atRisk={standing.isContractEnding}
                  isRookie={standing.isRookie}
                />
              </TableCell>
              {!isMobile &&
                standing.results.map((result, resultIndex) => (
                  <TableCell
                    key={resultIndex}
                    className={getThresholdClassName(index + 1) + getPositionClassName(result.position)}
                  >
                    {result.points}
                  </TableCell>
                ))}
              {!isMobile &&
                Array.from({ length: standing.numOfRounds - standing.results.length }, (_, index) => index + 1).map(
                  (roundIndex) => <TableCell key={roundIndex} className={getThresholdClassName(index + 1)} />,
                )}
              <TableCell className={getThresholdClassName(index + 1)}>{standing.totalPoints}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
