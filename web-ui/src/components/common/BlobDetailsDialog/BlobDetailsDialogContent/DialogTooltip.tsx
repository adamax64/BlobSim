import { Tooltip } from '@mui/material';

interface DialogTooltipProps {
  icon: React.ReactElement;
  title: React.ReactNode;
}

const DialogTooltip = ({ icon, title }: DialogTooltipProps) => {
  return <Tooltip title={title}>{icon}</Tooltip>;
};

export default DialogTooltip;
