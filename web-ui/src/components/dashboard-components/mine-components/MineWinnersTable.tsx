import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  useTheme,
} from '@mui/material';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTranslation } from 'react-i18next';
import { MineWinnerDto } from '../../../../generated';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';
import { formatToShort } from '../../../utils/sim-time-utils';
import { NarrowCell } from '../../common/StyledComponents';

type MineWinnersTableProps = {
  winners: MineWinnerDto[];
};

const MineWinnersTable = ({ winners }: MineWinnersTableProps) => {
  const { t } = useTranslation();
  const theme = useTheme();
  // Shorten the blob name when the viewport is between 1080px and 900px, or under 450px.
  const inMidRange = useMediaQuery(`(min-width: ${theme.breakpoints.values.md}px) and (max-width: 1080px)`);
  const isVerySmall = useMediaQuery('(max-width:450px)');
  const renderFullName = !inMidRange && !isVerySmall;

  return (
    <TableContainer component={Paper}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>{t('mine.winners.date')}</TableCell>
            <TableCell>{t('mine.winners.blob')}</TableCell>
            <NarrowCell align="center">{t('mine.winners.amount')}</NarrowCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {winners.map((winner) => (
            <TableRow
              key={`${winner.blob.id}-${winner.date.eon}-${winner.date.season}-${winner.date.epoch}-${winner.date.cycle}`}
            >
              <TableCell>
                <Typography variant="body2" component="span">
                  {formatToShort(winner.date)}
                </Typography>
              </TableCell>
              <TableCell>
                <IconNameWithDetailsModal
                  blob={winner.blob}
                  name={winner.blob.name}
                  color={winner.blob.color}
                  renderFullName={renderFullName}
                />
              </TableCell>
              <NarrowCell align="center">{winner.amount}</NarrowCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default MineWinnersTable;
