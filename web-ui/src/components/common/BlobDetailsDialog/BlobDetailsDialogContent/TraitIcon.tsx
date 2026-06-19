import { useTranslation } from 'react-i18next';
import { TraitType } from '../../../../../generated';
import Engineering from '@mui/icons-material/Engineering';
import AutoGraph from '@mui/icons-material/AutoGraph';
import BeachAccessIcon from '@mui/icons-material/BeachAccess';
import Explore from '@mui/icons-material/Explore';
import { Typography } from '@mui/material';
import React from 'react';
import DialogTooltip from './DialogTooltip';

interface TraitIconProps {
  trait: TraitType;
}

const TraitIcon = ({ trait }: TraitIconProps) => {
  const { t } = useTranslation();

  let traitIcon;
  switch (trait) {
    case TraitType.HardWorking:
      traitIcon = <Engineering />;
      break;
    case TraitType.Determined:
      traitIcon = <AutoGraph />;
      break;
    case TraitType.Lazy:
      traitIcon = <BeachAccessIcon />;
      break;
    case TraitType.Adventurous:
      traitIcon = <Explore />;
  }

  return (
    <DialogTooltip
      icon={traitIcon}
      title={
        <React.Fragment>
          <Typography sx={{ fontWeight: 700 }}>{t(`enums.traits.${trait}`)}</Typography>
          <Typography variant="body2">{t(`trait_descriptions.${trait}`)}</Typography>
        </React.Fragment>
      }
    />
  );
};

export default TraitIcon;
