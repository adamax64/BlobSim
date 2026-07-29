import LocalFireDepartment from '@mui/icons-material/LocalFireDepartment';
import Air from '@mui/icons-material/Air';
import WaterDrop from '@mui/icons-material/WaterDrop';
import AcUnit from '@mui/icons-material/AcUnit';
import Pets from '@mui/icons-material/Pets';
import { useTranslation } from 'react-i18next';
import { Element } from '../../../../../generated';
import DialogTooltip from './DialogTooltip';

interface ElementIconProps {
  element: Element;
}

const ElementIcon = ({ element }: ElementIconProps) => {
  const { t } = useTranslation();

  let elementIcon;
  switch (element) {
    case Element.Fire:
      elementIcon = <LocalFireDepartment fontSize="small" />;
      break;
    case Element.Wind:
      elementIcon = <Air fontSize="small" />;
      break;
    case Element.Water:
      elementIcon = <WaterDrop fontSize="small" />;
      break;
    case Element.Ice:
      elementIcon = <AcUnit fontSize="small" />;
      break;
    case Element.Beast:
      elementIcon = <Pets fontSize="small" />;
      break;
    default:
      return null;
  }

  return <DialogTooltip icon={elementIcon} title={t(`enums.elements.${element}`)} />;
};

export default ElementIcon;
