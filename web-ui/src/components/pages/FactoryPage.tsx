import { useMutation } from '@tanstack/react-query';
import { FactoryApi, NameSuggestionDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  LinearProgress,
  List,
  ListItem,
  styled,
  Typography,
} from '@mui/material';
import { AddCircle } from '@mui/icons-material';
import { BlobNamingDialog } from '../common/BlobNamingDialog';

const FactoryProgressBar = styled(LinearProgress)({
  height: 16,
  borderRadius: 10,
});

export function FactoryPage() {
  const [open, setOpen] = useState(false);

  const factoryApi = new FactoryApi(defaultConfig);

  const {
    data: factoryProgress,
    isPending: isFactoryProgressLoading,
    mutate: fetchFactoryprogress,
  } = useMutation<number, Error>({ mutationFn: () => factoryApi.getFactoryProgressFactoryProgressGet() });
  const {
    data: nameSuggestions,
    isPending: isLoadingNames,
    mutate: fetchNameSuggestions,
  } = useMutation<NameSuggestionDto[], Error>({
    mutationFn: () => factoryApi.getNameSuggestionsFactoryNameSuggestionsGet(),
  });

  useEffect(() => {
    fetchFactoryprogress();
    fetchNameSuggestions();
  }, []);

  const progressValue = (factoryProgress ?? 0) * 100 > 100 ? 100 : (factoryProgress ?? 0) * 100;

  return (
    <PageFrame>
      <PageTitleCard title="Blob Factory" center />
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">Factory Progress</Typography>
            <FactoryProgressBar
              color={(factoryProgress ?? 0 > 1) ? 'success' : 'primary'}
              variant={isFactoryProgressLoading ? 'query' : 'determinate'}
              value={progressValue}
            />
          </Box>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <Box display="flex" alignItems="flex-start" flexDirection="column" gap={1}>
            <Typography variant="h6">Blob name suggestions</Typography>
            <Button variant="contained" onClick={() => setOpen(true)} endIcon={<AddCircle />}>
              Add name suggestion
            </Button>
            {isLoadingNames ? (
              <Box display="flex" justifyContent="center" p={1}>
                <CircularProgress />
              </Box>
            ) : (
              <List dense>{nameSuggestions?.map((name, i) => <ListItem key={i}>{name.name}</ListItem>)}</List>
            )}
          </Box>
        </CardContent>
        <BlobNamingDialog open={open} onClose={() => setOpen(false)} mode="add" />
      </Card>
    </PageFrame>
  );
}
