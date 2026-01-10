import { useTranslation } from 'react-i18next';
import { TitleCountDto } from '../../../../generated';
import {
  Paper,
  Skeleton,
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
import { JSX } from 'react';
import { NarrowCell } from '../../common/StyledComponents';

interface TitleCountTableProps {
  title?: string | JSX.Element;
  data?: TitleCountDto[];
}

export const TitleCountTable = ({ title, data }: TitleCountTableProps) => {
  const { t } = useTranslation();

  const theme = useTheme();
  const isMobile = useMediaQuery(`${theme.breakpoints.down('sm')} or (max-height:600px)`);

  return (
    <TableContainer component={Paper} sx={{ padding: 1, width: isMobile ? 'auto' : '100%' }}>
      {title && (
        <Typography variant="h6" padding={1}>
          {title}
        </Typography>
      )}
      <Table size="small">
        <TableHead>
          <TableRow>
            <NarrowCell>#</NarrowCell>
            <NarrowCell>{t('hall-of-fame.titles-tab.table.name')}</NarrowCell>
            <NarrowCell>{t('hall-of-fame.titles-tab.table.count')}</NarrowCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data === undefined
            ? Array.from({ length: 5 }).map((_, index) => (
                <TableRow key={`skeleton-${index}`}>
                  <NarrowCell>
                    <Skeleton variant="text" width="20px" />
                  </NarrowCell>
                  <NarrowCell>
                    <Skeleton variant="text" />
                  </NarrowCell>
                  <NarrowCell>
                    <Skeleton variant="text" width="30px" />
                  </NarrowCell>
                </TableRow>
              ))
            : data.map((item, index) => (
                <TableRow key={index}>
                  <NarrowCell>{index + 1}</NarrowCell>
                  <NarrowCell>
                    <IconNameWithDetailsModal
                      blob={item.blob}
                      color={item.blob.color}
                      name={item.blob.name}
                      renderFullName={!isMobile}
                    />
                  </NarrowCell>
                  <NarrowCell>{item.count}</NarrowCell>
                </TableRow>
              ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
