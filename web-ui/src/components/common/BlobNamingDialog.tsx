import { AddCircle, Close } from '@mui/icons-material';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, IconButton, TextField } from '@mui/material';
import { useState } from 'react';

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
  onClose: () => void;
  mode: 'create' | 'add';
}

export function BlobNamingDialog({ open, onClose, mode }: BlobNamingDialogProps) {
  const [name, setName] = useState<string>();
  const [validationError, setValidationError] = useState<NameValidationError | undefined>();

  function handleCreate() {
    console.log('Create');
    onClose();
  }

  function handleAdd() {
    console.log('Add');
    onClose();
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
    <Dialog open={open} onClose={onClose}>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', padding: '1.2rem', paddingBottom: 0 }}>
        {mode == 'create' ? 'Create new blob' : 'Add name suggestion'}{' '}
        <IconButton aria-label="close" onClick={onClose}>
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
