import { Box } from '@mui/material';
import { DataGrid, GridColDef, GridRenderCellParams, GridRowClassNameParams } from '@mui/x-data-grid';
import { BlobStatsDto } from '../../../generated';
import { BlobState } from '../../utils/BlobStateUtils';
import { IconName } from '../common/IconName';
import { useTranslation } from 'react-i18next';

const desktopColumns = (t: (key: string) => string): GridColDef[] => [
  {
    field: 'name',
    headerName: t('blobs_grid.name'),
    resizable: false,
    renderCell: (params: GridRenderCellParams<BlobStatsDto>) => {
      return (
        <Box padding={2} sx={{ cursor: 'pointer' }}>
          <IconName
            name={params.row.name}
            color={params.row.color}
            atRisk={params.row.atRisk}
            isRookie={params.row.isRookie}
          />
        </Box>
      );
    },
    flex: 1.5,
  },
  { field: 'born', headerName: t('blobs_grid.born'), resizable: false, flex: 1 },
  { field: 'debut', headerName: t('blobs_grid.debut'), resizable: false, flex: 0.8 },
  { field: 'contract', headerName: t('blobs_grid.contract'), resizable: false, flex: 0.8 },
  { field: 'podiums', headerName: t('blobs_grid.podiums'), resizable: false, flex: 0.8 },
  { field: 'wins', headerName: t('blobs_grid.wins'), resizable: false, flex: 0.8 },
  { field: 'championships', headerName: t('blobs_grid.championships'), resizable: false, flex: 0.8 },
  { field: 'grandmasters', headerName: t('blobs_grid.grandmasters'), resizable: false, flex: 0.8 },
  { field: 'leagueName', headerName: t('blobs_grid.league'), resizable: false, flex: 1.5 },
];

function getRowClass(params: GridRowClassNameParams<BlobStatsDto>) {
  if (params.row.isDead) {
    return BlobState.DEAD;
  }
  if (params.row.isRetired) {
    return BlobState.RETIRED;
  }
  return '';
}

interface BlobsDesktopGridProps {
  blobs: BlobStatsDto[] | undefined;
  isPending: boolean;
  onBlobSelect: (blob: BlobStatsDto) => void;
}

export function BlobsDesktopGrid({ blobs, isPending, onBlobSelect }: BlobsDesktopGridProps) {
  const { t } = useTranslation();

  return (
    <Box margin={2} pb="1vw">
      <Box display="grid" width="100%">
        <DataGrid
          columns={desktopColumns(t)}
          rows={blobs ?? []}
          getRowId={(blob: BlobStatsDto) => blob.name}
          loading={isPending}
          disableColumnResize
          disableColumnMenu
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: {
              paginationModel: {
                pageSize: 25,
              },
            },
          }}
          rowSelection={false}
          getRowClassName={getRowClass}
          onRowClick={(params) => onBlobSelect(params.row)}
          autosizeOnMount
        />
      </Box>
    </Box>
  );
}
