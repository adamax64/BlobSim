import {
  Box,
  Button,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@mui/material';
import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useMutation } from '@tanstack/react-query';
import { useSnackbar } from 'notistack';
import { AdminApi, LeagueDto, LeagueNameUpdateDto, LeaguesApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { getLocalizedText } from '../../utils/translation-utils';

type LeagueNameDraft = {
  id: number;
  level: number;
  nameEn: string;
  nameHu: string;
};

const toDraft = (league: LeagueDto): LeagueNameDraft => ({
  id: league.id,
  level: league.level,
  nameEn: getLocalizedText(league.name, 'en'),
  nameHu: getLocalizedText(league.name, 'hu'),
});

const toUpdateDto = (draft: LeagueNameDraft): LeagueNameUpdateDto => ({
  id: draft.id,
  name: [
    { language: 'en', text: draft.nameEn },
    { language: 'hu', text: draft.nameHu },
  ],
});

type LeaguesAdminCardProps = {
  isAuthenticated: boolean;
};

export function LeaguesAdminCard({ isAuthenticated }: LeaguesAdminCardProps) {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const [drafts, setDrafts] = useState<LeagueNameDraft[]>([]);
  const [savedDrafts, setSavedDrafts] = useState<LeagueNameDraft[]>([]);

  const leaguesApi = new LeaguesApi(defaultConfig);
  const adminApi = new AdminApi(defaultConfig);

  const {
    data: leagues,
    isPending: leaguesLoading,
    mutate: loadLeagues,
  } = useMutation({
    mutationFn: () => leaguesApi.getLeaguesWithQueueLeaguesAllWithQueueGet(),
    onError: (error) => {
      console.error('Failed to fetch leagues:', error);
      enqueueSnackbar(t('admin.leagues_fetch_failed'), { variant: 'error' });
    },
  });

  const { isPending: saving, mutate: saveLeagueNames } = useMutation({
    mutationFn: (updates: LeagueNameUpdateDto[]) =>
      adminApi.updateAdminLeagueNamesAdminLeaguesNamesPost({ leagueNameUpdateDto: updates }),
    onSuccess: (updatedLeagues) => {
      const nextDrafts = updatedLeagues.map(toDraft);
      setDrafts((prev) => prev.map((draft) => nextDrafts.find((nd) => nd.id === draft.id) ?? draft));
      setSavedDrafts(nextDrafts);
      enqueueSnackbar(t('admin.leagues_save_success'), { variant: 'success' });
    },
    onError: (error) => {
      console.error('Failed to update league names:', error);
      enqueueSnackbar(t('admin.leagues_save_failed'), { variant: 'error' });
    },
  });

  useEffect(() => {
    loadLeagues();
  }, [loadLeagues]);

  useEffect(() => {
    if (leagues) {
      const nextDrafts = leagues.map(toDraft);
      setDrafts(nextDrafts);
      setSavedDrafts(nextDrafts);
    }
  }, [leagues]);

  const hasChanges = useMemo(() => JSON.stringify(drafts) !== JSON.stringify(savedDrafts), [drafts, savedDrafts]);

  const hasInvalidName = drafts.some((draft) => !draft.nameEn.trim() || !draft.nameHu.trim());

  const handleNameChange = (id: number, field: 'nameEn' | 'nameHu', value: string) => {
    setDrafts((current) => current.map((draft) => (draft.id === id ? { ...draft, [field]: value } : draft)));
  };

  const handleSave = () => {
    const updates = drafts.filter((draft) => {
      const saved = savedDrafts.find((item) => item.id === draft.id);
      return JSON.stringify(draft) !== JSON.stringify(saved);
    });
    saveLeagueNames(updates.map(toUpdateDto));
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {t('admin.leagues_management')}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {t('admin.leagues_description')}
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>{t('admin.leagues_id')}</TableCell>
                <TableCell>{t('admin.leagues_level')}</TableCell>
                <TableCell>{t('admin.leagues_name_en')}</TableCell>
                <TableCell>{t('admin.leagues_name_hu')}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {leaguesLoading && drafts.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4}>{t('admin.loading')}</TableCell>
                </TableRow>
              ) : (
                drafts.map((draft) => (
                  <TableRow key={draft.id}>
                    <TableCell>{draft.id}</TableCell>
                    <TableCell>{draft.level}</TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        fullWidth
                        value={draft.nameEn}
                        onChange={(event) => handleNameChange(draft.id, 'nameEn', event.target.value)}
                        disabled={!isAuthenticated || saving}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        fullWidth
                        value={draft.nameHu}
                        onChange={(event) => handleNameChange(draft.id, 'nameHu', event.target.value)}
                        disabled={!isAuthenticated || saving}
                      />
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <Box mt={2}>
          <Button
            variant="contained"
            onClick={handleSave}
            disabled={!isAuthenticated || !hasChanges || hasInvalidName || saving}
          >
            {t('admin.leagues_save')}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}
