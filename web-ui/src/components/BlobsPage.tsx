import { Box, CircularProgress, FormControl, FormControlLabel, IconButton, InputAdornment, InputLabel, OutlinedInput, Paper, Switch, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { DataGrid, GridRowClassNameParams } from '@mui/x-data-grid';
import { PageFrame } from "./PageFrame";
import { PageTitleCard } from "./PageTitleCard";
import { Search } from "@mui/icons-material";
import { useEffect, useState } from "react";
import { BlobsApi, BlobStatsDto } from "../../generated";
import defaultConfig from "../default-config";
import { useMutation } from "@tanstack/react-query";

const columns = [
  { field: 'name', headerName: 'Name', flex: 1, resizable: false },
  { field: 'born', headerName: 'Born', flex: 1, resizable: false },
  { field: 'debut', headerName: 'Debut', flex: 1, resizable: false },
  { field: 'contract', headerName: 'Contract', flex: 1, resizable: false },
  { field: 'podiums', headerName: 'Podiums', flex: 1, resizable: false },
  { field: 'wins', headerName: 'Wins', flex: 1, resizable: false },
  { field: 'championships', headerName: 'Championships', flex: 1, resizable: false },
  { field: 'grandmasters', headerName: 'Grandmasters', flex: 1, resizable: false },
  { field: 'leagueName', headerName: 'League', flex: 1, resizable: false },
]

function getRowClass(params: GridRowClassNameParams<BlobStatsDto>) {
  if (params.row.atRisk) {
    return 'row-at-risk'
  }
  if (params.row.isDead) {
    return 'row-dead'
  }
  if (params.row.isRetired) {
    return 'row-retired'
  }
  return ''
}

export function BlobsPage() {
  const [nameSearch, setNameSearch] = useState<string | undefined>()
  const [showDead, setShowDead] = useState<boolean>(false)

  const blobsApi = new BlobsApi(defaultConfig)

  const { data: blobs, isPending, mutate: getAllBlobs } = useMutation<BlobStatsDto[], Error>({ mutationFn: () => blobsApi.getAllBlobsAllGet({ nameSearch, showDead }) })

  useEffect(() => {
    getAllBlobs()
  }, [showDead])

  return (
    <PageFrame>
      <PageTitleCard title="Blobs" center />
      <Paper>
        <Box display="flex" gap={3} p={2}>
          <FormControl variant="outlined">
            <InputLabel htmlFor="search-by-name">Search by name</InputLabel>
            <OutlinedInput id="search-by-name" type="text" endAdornment={
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
          <FormControlLabel control={<Switch value={showDead} onChange={e => setShowDead(e.target.checked)} />} label="Show dead" />
        </Box>
        <Box display="flex" justifyContent="center">
          <Box width="98%" alignContent="center" pb="1vw">
            <DataGrid
              columns={columns}
              rows={blobs ?? []}
              getRowId={(blob) => blob.name}
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
  )
}