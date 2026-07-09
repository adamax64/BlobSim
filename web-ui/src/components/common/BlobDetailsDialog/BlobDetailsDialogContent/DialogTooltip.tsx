import DynamicTooltip from '../../DynamicTooltip';

interface DialogTooltipProps {
  icon: React.ReactElement;
  title: React.ReactNode;
}

const DialogTooltip = ({ icon, title }: DialogTooltipProps) => {
  return <DynamicTooltip title={title}>{icon}</DynamicTooltip>;
};

export default DialogTooltip;
