import { useTranslation } from 'react-i18next';
import { TraitType } from '../../../../generated';
import Engineering from '@mui/icons-material/Engineering';
import AutoGraph from '@mui/icons-material/AutoGraph';
import Hotel from '@mui/icons-material/Hotel';
import { Tooltip, Typography } from '@mui/material';
import React from 'react';

interface TraitIconProps {
  trait: TraitType;
}

export const TraitIcon = ({ trait }: TraitIconProps) => {
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
      traitIcon = <Hotel />;
      break;
  }

  return (
    <Tooltip
      title={
        <React.Fragment>
          <Typography sx={{ fontWeight: 700 }}>{t(`enums.traits.${trait}`)}</Typography>
          <Typography variant="body2">{t(`trait_descriptions.${trait}`)}</Typography>
        </React.Fragment>
      }
    >
      {traitIcon}
    </Tooltip>
  );
};
