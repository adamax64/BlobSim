import {
  Paper,
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  useMediaQuery,
  useTheme,
  Skeleton,
  Typography,
} from '@mui/material';
import { WinsByEventDto } from '../../../../generated';
import { useTranslation } from 'react-i18next';
import { NarrowCell } from '../../common/StyledComponents';
import { IconNameWithDetailsModal } from '../../common/IconNameWithDetailsModal';

interface WinsByEventTypeTableProps {
  title?: string;
  data?: WinsByEventDto[];
}

export const WinsByEventTypeTable = ({ data, title }: WinsByEventTypeTableProps) => {
  const { t } = useTranslation();

  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  const isLoading = !data;
  const skeletonRows = 5;

  return (
    <TableContainer component={Paper} sx={{ padding: 1, width: isMobile ? 'auto' : '100%' }}>
      {title && <Typography variant="h6">{title}</Typography>}
      <Table size="small">
        <TableHead>
          <TableRow>
            <NarrowCell>{t('hall-of-fame.events-tab.table.event_type')}</NarrowCell>
            <NarrowCell>{t('hall-of-fame.events-tab.table.record_holder')}</NarrowCell>
            <NarrowCell>{t('hall-of-fame.events-tab.table.wins')}</NarrowCell>
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
            : data.map((record) => (
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
                  <NarrowCell>{record.winCount}</NarrowCell>
                </TableRow>
              ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
