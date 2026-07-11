import Close from '@mui/icons-material/Close';
import { DialogTitle, IconButton } from '@mui/material';

type DialogTitleWithCloseButtonProps = {
  title: string;
  onClose: () => void;
};

const DialogTitleWithCloseButton = ({ title, onClose }: DialogTitleWithCloseButtonProps) => {
  return (
    <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      {title}
      <IconButton onClick={onClose} size="small">
        <Close />
      </IconButton>
    </DialogTitle>
  );
};

export default DialogTitleWithCloseButton;
