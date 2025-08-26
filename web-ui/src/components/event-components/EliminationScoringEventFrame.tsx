import { useTranslation } from 'react-i18next';
import {
  ActionDto,
  ActionsApi,
  BlobCompetitorDto,
  CompetitionApi,
  EventDto,
  EventRecordsApi,
} from '../../../generated';
import { useAuth } from '../../context/AuthContext';
import { useCallback, useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Paper,
  Snackbar,
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
import { ProgressButton } from './ProgressButton';
import { EliminationEventRecordDto as EventRecordDto } from '../../../generated/models/EliminationEventRecordDto';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { TickLoadingBar } from '../common/StyledComponents';
import { IconName } from '../common/IconName';
import { roundToThreeDecimals } from './EventUtils';
import { BarChart } from '@mui/x-charts/BarChart';
import { ChartsTooltipContainer, useAxesTooltip } from '@mui/x-charts/ChartsTooltip';

type SnackbarState = {
  message: string | null;
  severity: 'error' | 'success' | 'info' | 'warning';
  anchorOrigin: { vertical: 'top' | 'bottom'; horizontal: 'left' | 'center' | 'right' };
};

interface EliminationScoringEventFrameProps {
  event: EventDto;
}

export const EliminationScoringEventFrame = ({ event }: EliminationScoringEventFrameProps) => {
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarState, setSnackbarState] = useState<SnackbarState>({
    message: null,
    severity: 'error',
    anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
  });

  const [tick, setTick] = useState(Math.max(...event.actions.map((action: ActionDto) => action.scores.length), 0));
  const [isEventFinished, setIsEventFinished] = useState(false);
  const [loadingNextTick, setLoadingNextTick] = useState(false);
  const [eventRecordsCache, setEventRecordsCache] = useState<EventRecordDto[]>([]);

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const actionApi = new ActionsApi(defaultConfig);
  const eventRecordsApi = new EventRecordsApi(defaultConfig);
  const competitionApi = new CompetitionApi(defaultConfig);

  const { data: eventRecords, mutate: getEventRecords } = useMutation<EventRecordDto[], Error, number>({
    mutationFn: (eventId: number) => eventRecordsApi.getEliminationEventRecordsEliminationGet({ eventId }),
    onSuccess: (data) => {
      setLoadingNextTick(false);
      setEventRecordsCache(data);
      return data;
    },
    onError: (error) => {
      setLoadingNextTick(false);
      setSnackbarState({
        message: error.message || t('error.generic'),
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  const { mutate: createAction } = useMutation<
    { name: string; score: number } | undefined,
    Error,
    { contenders: BlobCompetitorDto[] }
  >({
    mutationFn: ({ contenders }) =>
      actionApi.eliminationActionsCreateEliminationPost({ eventId: event.id, blobCompetitorDto: contenders }),
    onSuccess: (data) => {
      if (data) {
        setSnackbarState({
          message: t('elimination_event.new_record', { name: data.name, score: data.score }),
          severity: 'success',
          anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
        });
        setSnackbarOpen(true);
      }
      setTick((prev) => prev + 1);
      setLoadingNextTick(false);
      getEventRecords(event.id);
    },
    onError: (error) => {
      setLoadingNextTick(false);
      setSnackbarState({
        message: error.message || t('error.generic'),
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  const { mutate: finishEvent } = useMutation<void, Error>({
    mutationFn: () =>
      competitionApi.saveEliminationCompetitionEliminationEventResultsPost({
        bodySaveEliminationCompetitionEliminationEventResultsPost: { event, eventRecords: eventRecords ?? [] },
      }),
    onSuccess: () => {
      setIsEventFinished(true);
    },
    onError: (error) => {
      setSnackbarState({
        message: error.message || t('error.generic'),
        severity: 'error',
        anchorOrigin: { vertical: 'bottom', horizontal: 'center' },
      });
      setSnackbarOpen(true);
    },
  });

  useEffect(() => {
    getEventRecords(event.id);
  }, [event.id]);

  const progressEvent = useCallback(() => {
    if (eventRecords && !isEventFinished) {
      setLoadingNextTick(true);
      setTimeout(() => {
        createAction({ contenders: eventRecords.filter((record) => !record.eliminated).map((record) => record.blob) });
      }, 1000);
    }
  }, [eventRecords, isEventFinished, createAction]);

  const getRowClass = useCallback(
    (index: number, isEliminated: boolean) => {
      if (isEventFinished) {
        switch (index) {
          case 0:
            return 'row-gold';
          case 1:
            return 'row-silver';
          case 2:
            return 'row-bronze';
        }
      } else {
        if (isEliminated) {
          return 'row-inactive';
        }
      }
      return '';
    },
    [isEventFinished],
  );

  return (
    <Card>
      <CardHeader title={t(`event_types.${event.type}`)} />
      <Divider />
      <CardContent>
        {isAuthenticated && (
          <ProgressButton
            isStart={tick === 0}
            isEnd={tick >= event.actions.length - 1}
            isEventFinished={isEventFinished}
            disabled={loadingNextTick}
            onClickStart={progressEvent}
            onClickNext={progressEvent}
            onClickEnd={finishEvent}
          />
        )}
        <Typography fontSize={18} fontWeight={600} paddingBottom={1}>
          {t('elimination_event.tick')}: {tick}
        </Typography>
        <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginBottom={2}>
          <TickLoadingBar />
        </Box>
        <Box display="flex" flexDirection="row">
          <Box>
            <TableContainer component={Paper}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell width={30}>#</TableCell>
                    <TableCell>{t('elimination_event.name')}</TableCell>
                    <TableCell>{t('elimination_event.score')}</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {(eventRecords ?? eventRecordsCache).map((record, index) => (
                    <TableRow key={index} className={getRowClass(index, record.eliminated ?? false)}>
                      <TableCell width={30}>{index + 1}</TableCell>
                      <TableCell>
                        <IconName name={record.blob.name} color={record.blob.color} renderFullName={!isMobile} />
                      </TableCell>
                      <TableCell>
                        {record.eliminated
                          ? t('elimination_event.eliminated')
                          : (roundToThreeDecimals(record.lastScore) ?? '-')}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
          <Box flexGrow={1}>
            <BarChart
              height={33 * (eventRecords?.length ?? 0) + 35}
              series={[
                {
                  data: (eventRecords ?? eventRecordsCache).map((record) =>
                    record.eliminated ? 0 : (record.lastScore ?? 0),
                  ),
                },
              ]}
              yAxis={[
                {
                  data: (eventRecords ?? eventRecordsCache).map((record) => record.blob.name),
                  tickLabelStyle: { display: 'none' },
                  colorMap: {
                    colors: (eventRecords ?? eventRecordsCache).map((record) => record.blob.color),
                    type: 'ordinal',
                  },
                },
              ]}
              layout="horizontal"
              margin={{ top: 12, right: 16, bottom: 0, left: 0 }}
              xAxis={[{ position: 'top' }]}
              slots={{ tooltip: CustomTooltip }}
            />
          </Box>
        </Box>
        <Box visibility={loadingNextTick ? 'visible' : 'hidden'} marginTop={2}>
          <TickLoadingBar />
        </Box>
        <Snackbar
          open={snackbarOpen}
          autoHideDuration={6000}
          onClose={() => setSnackbarOpen(false)}
          anchorOrigin={snackbarState.anchorOrigin}
        >
          <Alert onClose={() => setSnackbarOpen(false)} severity={snackbarState.severity} variant="filled">
            {snackbarState.message}
          </Alert>
        </Snackbar>
      </CardContent>
    </Card>
  );
};

const CustomTooltip = () => {
  const axisTooltip = useAxesTooltip();

  const name = axisTooltip?.[0].axisFormattedValue ?? '';
  const color = axisTooltip?.[0].seriesItems[0].color ?? '';
  const value = Number.parseFloat(axisTooltip?.[0].seriesItems[0].formattedValue ?? '');

  return (
    <ChartsTooltipContainer>
      <Card>
        <Box padding={1} display="flex" justifyContent="space-between" width={210}>
          <IconName name={name} color={color} />
          <Typography variant="body2" align="right">
            {value > 0 ? value : '-'}
          </Typography>
        </Box>
      </Card>
    </ChartsTooltipContainer>
  );
};
