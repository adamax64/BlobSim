import AddCircle from '@mui/icons-material/AddCircle';
import Close from '@mui/icons-material/Close';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormGroup,
  IconButton,
  TextField,
  Typography,
} from '@mui/material';
import { useState, useEffect } from 'react';
import { BlobsApi, FactoryApi, ResponseError } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { closeSnackbar, useSnackbar } from 'notistack';
import { useTranslation } from 'react-i18next';

interface BlobNamingDialogProps {
  open: boolean;
  prefilledLastName?: string;
  nameId?: number;
  parentId?: number;
  onClose: (update?: boolean) => void;
  mode: 'create' | 'add';
}

export function BlobNamingDialog({ open, onClose, mode, prefilledLastName, nameId, parentId }: BlobNamingDialogProps) {
  const [firstName, setFirstName] = useState<string>('');
  const [lastName, setLastName] = useState<string>(prefilledLastName ?? '');
  const [validationError, setValidationError] = useState<string>();
  const { t } = useTranslation();

  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    setLastName(prefilledLastName ?? '');
  }, [prefilledLastName]);

  const factoryApi = new FactoryApi(defaultConfig);
  const blobsApi = new BlobsApi(defaultConfig);

  const { mutate: saveNameSuggestion } = useMutation<void, ResponseError>({
    mutationFn: () => factoryApi.saveNameSuggestionFactorySaveNameSuggestionPost({ firstName, lastName }),
  });

  const { mutate: createBlob } = useMutation<void, ResponseError>({
    mutationFn: () => blobsApi.createBlobBlobsCreatePost({ firstName, lastName, parentId }),
  });

  const { mutate: updateNameSuggestion } = useMutation<void, ResponseError>({
    mutationFn: () => factoryApi.updateNameSuggestionFactoryUpdateNameSuggestionPost({ id: nameId!, firstName }),
  });

  const responseHandler = {
    onSuccess: () => {
      setFirstName('');
      setLastName('');
      onClose(true);
    },
    onError: (error: ResponseError) => {
      error.response.json().then((errorBody) => {
        if (errorBody.detail === 'NAME_ALREADY_OCCUPIED') {
          enqueueSnackbar(t('blob_naming.name_exists_error'), {
            key: errorBody.detail,
            variant: 'error',
            autoHideDuration: 6000,
            anchorOrigin: { horizontal: 'right', vertical: 'bottom' },
            action: (key) => (
              <IconButton onClick={() => closeSnackbar(key)} color="inherit">
                <Close />
              </IconButton>
            ),
          });
        }
      });
    },
  };

  const handleCreate = () => {
    createBlob(undefined, responseHandler);
  };

  const handleAdd = () => {
    saveNameSuggestion(undefined, responseHandler);
  };

  const handleUpdate = () => {
    updateNameSuggestion(undefined, responseHandler);
  };

  const setAndValidateName = (value: string, isFirstName: boolean) => {
    if (isFirstName) {
      setFirstName(value);
    } else {
      setLastName(value);
    }

    if (!value.match(/[A-Z]/)) {
      setValidationError(t('blob_naming.validation_error'));
    } else {
      setValidationError(undefined);
    }
  };

  return (
    <Dialog open={open} onClose={() => onClose()}>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', padding: '1.2rem', paddingBottom: 0 }}>
        {mode == 'create' ? t('blob_naming.create_title') : t('blob_naming.add_title')}
        <IconButton aria-label="close" onClick={() => onClose()}>
          <Close />
        </IconButton>
      </DialogTitle>
      <DialogContent sx={{ display: 'flex', flexDirection: 'column', padding: '1.2rem 1.2rem 0 1.2rem  !important' }}>
        <FormGroup sx={{ flexWrap: 'nowrap', flexDirection: 'row', gap: '1rem' }}>
          <TextField
            autoFocus
            id="first-name"
            label={t('blob_naming.first_name')}
            type="text"
            fullWidth
            value={firstName}
            error={!!validationError}
            onChange={(event) => setAndValidateName(event.target.value, true)}
          />
          <TextField
            id="last-name"
            label={t('blob_naming.last_name')}
            type="text"
            fullWidth
            value={lastName}
            error={!!validationError}
            disabled={!!prefilledLastName}
            onChange={(event) => setAndValidateName(event.target.value, false)}
          />
        </FormGroup>
        {!!validationError && (
          <Typography variant="caption" marginTop={1} color="error">
            {validationError}
          </Typography>
        )}
      </DialogContent>
      <DialogActions>
        <Button
          variant="contained"
          color="primary"
          endIcon={<AddCircle />}
          onClick={mode == 'create' ? handleCreate : nameId ? handleUpdate : handleAdd}
          sx={{ margin: '0.5rem' }}
          disabled={!firstName || !!validationError}
        >
          {mode == 'create' ? t('blob_naming.create_button') : t('blob_naming.add_button')}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
