import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';
import { useTranslation } from 'react-i18next';
import { LeagueChampionsDto } from '../../../../generated';

interface ChampionsChronologyTableProps {
  leagueChampions: LeagueChampionsDto | null;
}

export const ChampionsChronologyTable = ({ leagueChampions }: ChampionsChronologyTableProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  return (
    <TableContainer component={Paper} sx={{ padding: 2, width: isMobile ? 'auto' : '100%' }}>
      {!isMobile && <Typography variant="h6">{leagueChampions?.league.name}</Typography>}
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>{t('hall-of-fame.chronology-tab.table.season')}</TableCell>
            <TableCell>{t('hall-of-fame.chronology-tab.table.champion')}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {leagueChampions?.champions.map((champion) => (
            <TableRow key={champion.season}>
              <TableCell>{champion.season}</TableCell>
              <TableCell>
                <IconNameWithDetailsModal
                  blob={champion.blob}
                  color={champion.blob.color}
                  name={champion.blob.name}
                  renderFullName={!isMobile}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
