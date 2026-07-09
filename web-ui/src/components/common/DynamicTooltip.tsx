import { Tooltip } from '@mui/material';
import { useIsMobile } from '../../hooks/useIsMobile';

type DynamicTooltipProps = {
  children: React.ReactElement;
  title: string | React.ReactNode;
  placement?: 'top' | 'bottom' | 'left' | 'right';
};

const DynamicTooltip = ({ children, title, placement }: DynamicTooltipProps) => {
  const isMobile = useIsMobile();

  return isMobile ? (
    <Tooltip title={title} placement={placement} enterTouchDelay={0} disableHoverListener>
      {children}
    </Tooltip>
  ) : (
    <Tooltip title={title} placement={placement}>
      {children}
    </Tooltip>
  );
};

export default DynamicTooltip;
