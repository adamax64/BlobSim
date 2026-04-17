import { Button } from '@mui/material';
import { FactoryApi, NameSuggestionDto, NewsDto, NewsType } from '../../../generated';
import Stadium from '@mui/icons-material/Stadium';
import { useNavigate } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import AddCircle from '@mui/icons-material/AddCircle';
import { useEffect, useState } from 'react';
import { BlobNamingDialog } from '../common/BlobNamingDialog';
import { useMutation } from '@tanstack/react-query';
import defaultConfig from '../../default-config';

type NewsActionButtonProps = {
  newsItem: NewsDto;
  fetchNews: () => void;
};

export const NewsActionButton = ({ newsItem, fetchNews }: NewsActionButtonProps) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [open, setOpen] = useState(false);
  const [prefilledSuggestion, setPrefilledSuggestion] = useState<NameSuggestionDto>();

  const factoryApi = new FactoryApi(defaultConfig);

  const { mutate: getNameSuggestions } = useMutation({
    mutationFn: () => factoryApi.getNameSuggestionsFactoryNameSuggestionsGet(),
    onSuccess: (data) => {
      const suggestionWithParent = data
        .filter((suggestion) => suggestion.parentId)
        .sort((a, b) => a.created.getTime() - b.created.getTime())[0];
      setPrefilledSuggestion(suggestionWithParent);
    },
  });

  useEffect(() => {
    if (newsItem.type === NewsType.BlobInCreation) {
      getNameSuggestions();
    }
  }, [newsItem.type]);

  const handleDialogClose = (update?: boolean) => {
    setOpen(false);
    if (update) {
      fetchNews();
    }
  };

  switch (newsItem.type) {
    case NewsType.EventStarted:
    case NewsType.OngoingEvent:
      return (
        <Button
          variant="contained"
          color="success"
          size="small"
          endIcon={<Stadium />}
          onClick={() => navigate({ to: '/event' })}
          sx={{ marginTop: 1 }}
        >
          {t('dashboard.proceed_to_event')}
        </Button>
      );
    case NewsType.BlobInCreation:
      return (
        <>
          {isAuthenticated && (
            <Button
              variant="contained"
              color="primary"
              size="small"
              endIcon={<AddCircle />}
              onClick={() => setOpen(true)}
              sx={{ marginTop: 1 }}
            >
              {t('dashboard.create_new_blob')}
            </Button>
          )}
          <BlobNamingDialog
            open={open}
            onClose={handleDialogClose}
            prefilledLastName={prefilledSuggestion?.lastName}
            nameId={prefilledSuggestion?.id}
            parentId={prefilledSuggestion?.parentId ?? undefined}
            mode="create"
          />
        </>
      );
    default:
      return null;
  }
};
