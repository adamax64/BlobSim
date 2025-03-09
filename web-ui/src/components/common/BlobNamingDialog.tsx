import { AddCircle, Close } from '@mui/icons-material';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Snackbar,
  TextField,
} from '@mui/material';
import { useEffect, useState } from 'react';
import { BlobsApi, FactoryApi, ResponseError } from '../../../generated';
import defaultConfig from '../../default-config';
import { useMutation } from '@tanstack/react-query';
import { closeSnackbar, useSnackbar } from 'notistack';

enum NameValidationError {
  NotConsistsOfTwoNames = 'NotConsistsOfTwoNames',
  FirstLetterIsNotCapital = 'FirstLetterIsNotCapital',
}

function getValidationErrorMessage(validationError: NameValidationError | undefined) {
  switch (validationError) {
    case NameValidationError.NotConsistsOfTwoNames:
      return 'Name must consist of two words';
    case NameValidationError.FirstLetterIsNotCapital:
      return 'Each word must start with a capital letter';
    default:
      return undefined;
  }
}

interface BlobNamingDialogProps {
  open: boolean;
  onClose: (update?: boolean) => void;
  mode: 'create' | 'add';
}

export function BlobNamingDialog({ open, onClose, mode }: BlobNamingDialogProps) {
  const [name, setName] = useState<string>();
  const [validationError, setValidationError] = useState<NameValidationError | undefined>();

  const { enqueueSnackbar } = useSnackbar();

  const factoryApi = new FactoryApi(defaultConfig);
  const blobsApi = new BlobsApi(defaultConfig);

  const { mutate: saveNameSuggestion } = useMutation<void, ResponseError>({
    mutationFn: () => factoryApi.saveNameSuggestionFactorySaveNameSuggestionPost({ name: name! }),
  });

  const { mutate: createBlob } = useMutation<void, ResponseError>({
    mutationFn: () => blobsApi.createBlobBlobsCreatePost({ name: name! }),
  });

  const responseHandler = {
    onSuccess: () => {
      setName(undefined);
      onClose(true);
    },
    onError: (error: ResponseError) => {
      error.response.json().then((errorBody) => {
        if (errorBody.detail === 'NAME_ALREADY_OCCUPIED') {
          enqueueSnackbar('Name already exists in suggestions list', {
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

  function handleCreate() {
    createBlob(undefined, responseHandler);
  }

  function handleAdd() {
    saveNameSuggestion(undefined, responseHandler);
  }

  function setAndValidateName(value: string) {
    setName(value);

    const words = value.trim().split(' ');

    if (words.length !== 2) {
      setValidationError(NameValidationError.NotConsistsOfTwoNames);
    } else if (words.some((word) => !word[0].match(/[A-Z]/))) {
      setValidationError(NameValidationError.FirstLetterIsNotCapital);
    } else {
      setValidationError(undefined);
    }
  }

  return (
    <Dialog open={open} onClose={() => onClose()}>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', padding: '1.2rem', paddingBottom: 0 }}>
        {mode == 'create' ? 'Create new blob' : 'Add name suggestion'}{' '}
        <IconButton aria-label="close" onClick={() => onClose()}>
          <Close />
        </IconButton>
      </DialogTitle>
      <DialogContent sx={{ display: 'flex', padding: '1.2rem 1.2rem 0 1.2rem  !important' }}>
        <TextField
          autoFocus
          id="name"
          label="Name"
          type="text"
          fullWidth
          value={name}
          error={!!validationError}
          helperText={getValidationErrorMessage(validationError)}
          onChange={(event) => setAndValidateName(event.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button
          variant="contained"
          color="primary"
          endIcon={<AddCircle />}
          onClick={mode == 'create' ? handleCreate : handleAdd}
          sx={{ margin: '0.5rem' }}
          disabled={!name || !!validationError}
        >
          {mode == 'create' ? 'Create' : 'Add'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
