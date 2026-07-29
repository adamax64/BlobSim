import Close from '@mui/icons-material/Close';
import { DialogTitle, IconButton } from '@mui/material';
import { Box } from '@mui/system';

type DialogTitleWithCloseButtonProps = {
  title: string;
  elementIcon?: React.ReactNode;
  onClose: () => void;
};

const DialogTitleWithCloseButton = ({ title, elementIcon, onClose }: DialogTitleWithCloseButtonProps) => {
  return (
    <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <Box gap={1} display="flex" alignItems="center">
        {elementIcon}
        {title}
      </Box>
      <IconButton onClick={onClose} size="small">
        <Close />
      </IconButton>
    </DialogTitle>
  );
};

export default DialogTitleWithCloseButton;
