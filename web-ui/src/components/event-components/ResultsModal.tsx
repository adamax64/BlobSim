import { Dialog, DialogTitle, DialogContent, CircularProgress, Box, Typography, IconButton } from '@mui/material';
import { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import defaultConfig from '../../default-config';
import ResultsTable from './ResultsTable';
import { CompetitionApi, ResultDto } from '../../../generated';
import Close from '@mui/icons-material/Close';

type ResultsModalProps = {
  eventId: number | null;
  open: boolean;
  onClose: () => void;
};

export const ResultsModal = ({ eventId, open, onClose }: ResultsModalProps) => {
  const [results, setResults] = useState<ResultDto[]>([]);

  const competitionApi = new CompetitionApi(defaultConfig);

  const {
    mutate: fetchResults,
    isPending,
    isError,
    error,
    reset,
  } = useMutation<ResultDto[], Error, number>({
    mutationFn: async (id: number) =>
      competitionApi.getResultsForEventRouteCompetitionResultsEventEventIdGet({ eventId: id }),
    onSuccess: (data) => setResults(data),
  });

  useEffect(() => {
    if (open && eventId) {
      fetchResults(eventId);
    }
    if (!open) {
      // reset state when modal closes
      reset();
    }
  }, [open, eventId]);

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        Event Results
        <IconButton onClick={onClose} size="small">
          <Close />
        </IconButton>
      </DialogTitle>
      <DialogContent>
        {isPending ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={140}>
            <CircularProgress />
          </Box>
        ) : isError ? (
          <Typography color="error">{(error as Error)?.message ?? 'Unknown error'}</Typography>
        ) : results.length === 0 ? (
          <Typography>No results available.</Typography>
        ) : (
          <ResultsTable results={results} />
        )}
      </DialogContent>
    </Dialog>
  );
};

export default ResultsModal;
