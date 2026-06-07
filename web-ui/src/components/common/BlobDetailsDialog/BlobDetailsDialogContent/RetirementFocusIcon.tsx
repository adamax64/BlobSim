import EmojiEvents from '@mui/icons-material/EmojiEvents';
import AddAlarmIcon from '@mui/icons-material/AddAlarm';
import { useTranslation } from 'react-i18next';
import { RetirementFocusType } from '../../../../../generated';
import DialogTooltip from './DialogTooltip';

interface RetirementFocusIconProps {
  retirementFocus: RetirementFocusType;
}

const RetirementFocusIcon = ({ retirementFocus }: RetirementFocusIconProps) => {
  const { t } = useTranslation();

  let focusIcon;
  switch (retirementFocus) {
    case RetirementFocusType.Legacy:
      focusIcon = <EmojiEvents />;
      break;
    case RetirementFocusType.ProlongedLife:
      focusIcon = <AddAlarmIcon />;
      break;
  }

  return <DialogTooltip icon={focusIcon} title={t(`enums.retirement_focus.${retirementFocus}`)} />;
};

export default RetirementFocusIcon;
