import {
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  useTheme,
  useMediaQuery,
  Tooltip,
} from '@mui/material';
import { GrandmasterStandingsDTO } from '../../../generated';
import { BlobState, getClassNameForBlobState } from '../../utils/BlobStateUtils';
import { IconName } from '../common/IconName';
import { useTranslation } from 'react-i18next';
import { EmojiEvents, WorkspacePremium } from '@mui/icons-material';

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
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { t } = useTranslation();

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
        <p>{t('grandmaster_standings_table.no_data', { eon })}</p>
      </Paper>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ margin: 2, width: 'auto' }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>#</TableCell>
            <TableCell>{t('grandmaster_standings_table.name')}</TableCell>
            <TableCell align="center">
              {isMobile ? (
                <Tooltip title={t('grandmaster_standings_table.championships')}>
                  <EmojiEvents />
                </Tooltip>
              ) : (
                t('grandmaster_standings_table.championships')
              )}
            </TableCell>
            <TableCell align="center">
              {isMobile ? (
                <Tooltip title={t('grandmaster_standings_table.gold')}>
                  <WorkspacePremium />
                </Tooltip>
              ) : (
                t('grandmaster_standings_table.gold')
              )}
            </TableCell>
            {!isMobile && <TableCell align="center">{t('grandmaster_standings_table.silver')}</TableCell>}
            {!isMobile && <TableCell align="center">{t('grandmaster_standings_table.bronze')}</TableCell>}
            {!isMobile && <TableCell align="center">{t('grandmaster_standings_table.points')}</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {standings.map((standing, index) => (
            <TableRow key={index} className={getRowClass(hasEonEnded, index + 1)}>
              <TableCell>{index + 1}</TableCell>
              <TableCell>
                <IconName name={standing.name} color={standing.color} renderFullName={!isMobile} />
              </TableCell>
              <TableCell align="center">{standing.championships}</TableCell>
              <TableCell align="center">{standing.gold}</TableCell>
              {!isMobile && <TableCell align="center">{standing.silver}</TableCell>}
              {!isMobile && <TableCell align="center">{standing.bronze}</TableCell>}
              {!isMobile && <TableCell align="center">{standing.points}</TableCell>}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
