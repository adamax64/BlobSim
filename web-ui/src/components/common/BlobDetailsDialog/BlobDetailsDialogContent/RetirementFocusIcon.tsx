import EmojiEvents from '@mui/icons-material/EmojiEvents';
import AddAlarmIcon from '@mui/icons-material/AddAlarm';
import { useTranslation } from 'react-i18next';
import { RetirementFocusTypeDto } from '../../../../../generated';
import DialogTooltip from './DialogTooltip';

interface RetirementFocusIconProps {
  retirementFocus: RetirementFocusTypeDto;
}

const RetirementFocusIcon = ({ retirementFocus }: RetirementFocusIconProps) => {
  const { t } = useTranslation();

  let focusIcon;
  switch (retirementFocus) {
    case RetirementFocusTypeDto.Legacy:
      focusIcon = <EmojiEvents />;
      break;
    case RetirementFocusTypeDto.ProlongedLife:
      focusIcon = <AddAlarmIcon />;
      break;
  }

  return <DialogTooltip icon={focusIcon} title={t(`enums.retirement_focus.${retirementFocus}`)} />;
};

export default RetirementFocusIcon;
