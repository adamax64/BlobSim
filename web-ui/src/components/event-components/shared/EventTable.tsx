import { Box, Paper, Table, TableContainer } from '@mui/material';

type EventTableProps = {
  children: React.ReactNode;
};

export const EventTable = ({ children }: EventTableProps) => {
  return (
    <Box>
      <TableContainer
        component={Paper}
        sx={{
          width: '100%',
          height: '100%',
        }}
      >
        <Table size="small" stickyHeader>
          {children}
        </Table>
      </TableContainer>
    </Box>
  );
};
