import { Box } from '@mui/material';
import { DataGrid, GridRenderCellParams, GridRowClassNameParams } from '@mui/x-data-grid';
import { BlobStatsDto } from '../../../generated';
import { BlobState } from '../../utils/BlobStateUtils';
import { IconName } from '../common/IconName';

const desktopColumns = [
  {
    field: 'name',
    headerName: 'Name',
    flex: 1,
    resizable: false,
    renderCell: (params: GridRenderCellParams<BlobStatsDto>) => (
      <Box padding={2} sx={{ cursor: 'pointer' }}>
        <IconName name={params.row.name} color={params.row.color} />
      </Box>
    ),
  },
  { field: 'born', headerName: 'Born', resizable: false },
  { field: 'debut', headerName: 'Debut', resizable: false },
  { field: 'contract', headerName: 'Contract', resizable: false },
  { field: 'podiums', headerName: 'Podiums', resizable: false },
  { field: 'wins', headerName: 'Wins', resizable: false },
  { field: 'championships', headerName: 'Championships', resizable: false },
  { field: 'grandmasters', headerName: 'Grandmasters', resizable: false },
  { field: 'leagueName', headerName: 'League', flex: 1, resizable: false },
];

function getRowClass(params: GridRowClassNameParams<BlobStatsDto>) {
  if (params.row.atRisk) {
    return BlobState.AT_RISK;
  }
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
  return (
    <Box display="flex" justifyContent="center">
      <Box
        width="98%"
        margin={2}
        alignContent="center"
        pb="1vw"
        sx={{
          '& .MuiDataGrid-root': {
            width: '100%',
            overflowX: 'hidden',
          },
        }}
      >
        <DataGrid
          columns={desktopColumns}
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
        />
      </Box>
    </Box>
  );
}
