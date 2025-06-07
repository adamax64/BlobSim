import {
  Box,
  FormControl,
  FormControlLabel,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  Paper,
  Switch,
  TableCell,
} from '@mui/material';
import { DataGrid, GridRenderCellParams, GridRowClassNameParams } from '@mui/x-data-grid';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { Search } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { BlobsApi, BlobStatsDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { BlobState } from '../../utils/BlobStateUtils';
import { IconName } from '../common/IconName';

const columns = [
  {
    field: 'name',
    headerName: 'Name',
    flex: 1,
    resizable: false,
    renderCell: (params: GridRenderCellParams<BlobStatsDto>) => <Box padding={2}><IconName name={params.row.name} color={params.row.color} /></Box>,
  },
  { field: 'born', headerName: 'Born', flex: 1, resizable: false },
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

export function BlobsPage() {
  const [nameSearch, setNameSearch] = useState<string | undefined>();
  const [showDead, setShowDead] = useState<boolean>(false);

  const blobsApi = new BlobsApi(defaultConfig);

  const {
    data: blobs,
    isPending,
    mutate: getAllBlobs,
  } = useMutation<BlobStatsDto[], Error>({ mutationFn: () => blobsApi.getAllBlobsAllGet({ nameSearch, showDead }) });

  useEffect(() => {
    getAllBlobs();
  }, [showDead]);

  return (
    <PageFrame>
      <PageTitleCard title="Blobs" center />
      <Paper>
        <Box display="flex" gap={3} p={2}>
          <FormControl variant="outlined">
            <InputLabel htmlFor="search-by-name">Search by name</InputLabel>
            <OutlinedInput
              id="search-by-name"
              type="text"
              endAdornment={
                <InputAdornment position="end">
                  <IconButton onClick={() => getAllBlobs()}>
                    <Search />
                  </IconButton>
                </InputAdornment>
              }
              value={nameSearch}
              onChange={(e) => setNameSearch(e.target.value.length > 0 ? e.target.value : undefined)}
              onKeyDown={(e) => e.key === 'Enter' && getAllBlobs()}
              label="Search by name"
            />
          </FormControl>
          <FormControlLabel
            control={<Switch value={showDead} onChange={(e) => setShowDead(e.target.checked)} />}
            label="Show dead"
          />
        </Box>
        <Box display="flex" justifyContent="center">
          <Box width="98%" alignContent="center" pb="1vw">
            <DataGrid
              columns={columns}
              rows={blobs ?? []}
              getRowId={(blob: BlobStatsDto) => blob.name}
              loading={isPending}
              disableColumnResize
              disableColumnMenu
              pageSizeOptions={[10, 25, 50]}
              rowSelection={false}
              getRowClassName={getRowClass}
            />
          </Box>
        </Box>
      </Paper>
    </PageFrame>
  );
}
