import { useMutation } from '@tanstack/react-query';
import { FactoryApi, FactoryProgressDto, NameSuggestionDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { PageFrame } from '../common/PageFrame';
import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  CardContent,
  CircularProgress,
  LinearProgress,
  List,
  ListItem,
  Paper,
  styled,
  Typography,
} from '@mui/material';
import AddCircle from '@mui/icons-material/AddCircle';
import { BlobNamingDialog } from '../common/BlobNamingDialog';
import { EfficiencyMeter } from '../common/EfficiencyMeter';
import { useAuth } from '../../context/AuthContext';
import { useTranslation } from 'react-i18next';

const FactoryProgressBar = styled(LinearProgress)({
  height: 16,
  borderRadius: 10,
});

export function FactoryPage() {
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();

  const [open, setOpen] = useState(false);
  const [selectedNameId, setSelectedNameId] = useState<number>();
  const [selectedLastName, setSelectedLastName] = useState<string>();

  const factoryApi = new FactoryApi(defaultConfig);

  const {
    data: factoryProgress,
    isPending: isFactoryProgressLoading,
    mutate: fetchFactoryprogress,
  } = useMutation<FactoryProgressDto, Error>({
    mutationFn: () => factoryApi.getFactoryProgressFactoryProgressGet(),
  });
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

  const handleDialogClose = (update?: boolean) => {
    setOpen(false);
    setSelectedNameId(undefined);
    setSelectedLastName(undefined);
    if (update) {
      fetchNameSuggestions();
    }
  };

  const handleAddFirstName = (nameId: number, lastName: string) => {
    setSelectedNameId(nameId);
    setSelectedLastName(lastName);
    setOpen(true);
  };

  const progress = factoryProgress?.progress ?? 0;
  const progressValue = progress * 100 > 100 ? 100 : progress * 100;

  return (
    <PageFrame showLoading={isFactoryProgressLoading || isLoadingNames} pageName="factory">
      <Paper>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">{t('factory.factory_progress')}</Typography>
            <FactoryProgressBar
              color={progress > 1 ? 'success' : 'primary'}
              variant={isFactoryProgressLoading ? 'query' : 'determinate'}
              value={progressValue}
            />
          </Box>
          <Box display="flex" flexWrap="wrap" justifyContent="space-around" gap={1} mt={2}>
            <EfficiencyMeter label={t('factory.solar_efficiency')} value={factoryProgress?.solarEfficiency ?? 0} />
            <EfficiencyMeter label={t('factory.wind_efficiency')} value={factoryProgress?.windEfficiency ?? 0} />
            <EfficiencyMeter label={t('factory.hydro_efficiency')} value={factoryProgress?.hydroEfficiency ?? 0} />
          </Box>
        </CardContent>
      </Paper>
      <Paper>
        <CardContent>
          <Box display="flex" alignItems="flex-start" flexDirection="column" gap={1}>
            <Typography variant="h6">{t('factory.name_suggestions')}</Typography>
            {isAuthenticated && (
              <Button variant="contained" onClick={() => setOpen(true)} endIcon={<AddCircle />}>
                {t('factory.add_name_suggestion')}
              </Button>
            )}
            {isLoadingNames ? (
              <Box display="flex" justifyContent="center" p={1}>
                <CircularProgress />
              </Box>
            ) : (
              <List dense>
                {nameSuggestions?.map((name, i) => (
                  <ListItem key={i} sx={{ display: 'flex', gap: 1 }}>
                    {name.firstName} {name.lastName}{' '}
                    {!name.firstName && isAuthenticated && (
                      <Button
                        variant="outlined"
                        size="small"
                        onClick={() => handleAddFirstName(name.id, name.lastName)}
                      >
                        {t('factory.add_first_name')}
                      </Button>
                    )}
                  </ListItem>
                ))}
              </List>
            )}
          </Box>
        </CardContent>
        <BlobNamingDialog
          open={open}
          onClose={handleDialogClose}
          mode="add"
          prefilledLastName={selectedLastName}
          nameId={selectedNameId}
        />
      </Paper>
    </PageFrame>
  );
}
