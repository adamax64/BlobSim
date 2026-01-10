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
import { useTranslation } from 'react-i18next';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';
import { GrandmasterDto } from '../../../../generated';

interface GrandmasterChronologyTableProps {
  grandmasters: GrandmasterDto[];
}

export const GrandmasterChronologyTable = ({ grandmasters }: GrandmasterChronologyTableProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  return (
    <TableContainer component={Paper} sx={{ padding: 2, width: isMobile ? 'auto' : '100%' }}>
      {!isMobile && (
        <Typography variant="h6">{t('hall-of-fame.chronology-tab.table.grandmaster_table_title')}</Typography>
      )}
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>{t('hall-of-fame.chronology-tab.table.eon')}</TableCell>
            <TableCell>{t('hall-of-fame.chronology-tab.table.grandmaster')}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {grandmasters?.map((grandmaster) => (
            <TableRow key={grandmaster.eon}>
              <TableCell>{grandmaster.eon}</TableCell>
              <TableCell>
                <IconNameWithDetailsModal
                  blob={grandmaster.blob}
                  color={grandmaster.blob.color}
                  name={grandmaster.blob.name}
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
