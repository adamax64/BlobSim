import {
  Paper,
  Skeleton,
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { RecordDto } from '../../../../generated';
import { useTranslation } from 'react-i18next';
import { NarrowCell } from '../../common/StyledComponents';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';
import { roundToThreeDecimals } from '../../event-components/event-utils';

interface RecordsByEventTableProps {
  data?: RecordDto[];
}

export const RecordsByLeagueTable = ({ data }: RecordsByEventTableProps) => {
  const { t } = useTranslation();

  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  const isLoading = !data;
  const skeletonRows = 5;

  return (
    <TableContainer component={Paper} sx={{ padding: 1, width: isMobile ? 'auto' : '100%' }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <NarrowCell>{t('hall-of-fame.events-tab.table.event_type')}</NarrowCell>
            <NarrowCell>{t('hall-of-fame.events-tab.table.record_holder')}</NarrowCell>
            <NarrowCell>{t('hall-of-fame.events-tab.table.score')}</NarrowCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {isLoading
            ? Array.from({ length: skeletonRows }).map((_, index) => (
                <TableRow key={`skeleton-${index}`}>
                  <NarrowCell>
                    <Skeleton variant="text" width="80%" />
                  </NarrowCell>
                  <NarrowCell>
                    <Skeleton variant="text" width="70%" />
                  </NarrowCell>
                  <NarrowCell>
                    <Skeleton variant="text" width="40%" />
                  </NarrowCell>
                </TableRow>
              ))
            : data?.map((record) => (
                <TableRow key={record.eventType}>
                  <NarrowCell>{t(`enums.event_types.${record.eventType}`)}</NarrowCell>
                  <NarrowCell>
                    <IconNameWithDetailsModal
                      blob={record.blob}
                      color={record.blob.color}
                      name={record.blob.name}
                      renderFullName={!isMobile}
                    />
                  </NarrowCell>
                  <NarrowCell>{roundToThreeDecimals(record.score)}</NarrowCell>
                </TableRow>
              ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
