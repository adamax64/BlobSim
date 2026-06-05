import Battery20 from '@mui/icons-material/Battery20';
import { StateDto, StateType } from '../../../../../generated';
import HeartBroken from '@mui/icons-material/HeartBroken';
import MoodBad from '@mui/icons-material/MoodBad';
import OfflineBolt from '@mui/icons-material/OfflineBolt';
import { Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import React from 'react';
import DialogTooltip from './DialogTooltip';

interface StateIconProps {
  state: StateDto;
}

const StateIcon = ({ state }: StateIconProps) => {
  const { t } = useTranslation();

  let stateIcon;
  switch (state.type) {
    case StateType.Tired:
      stateIcon = <Battery20 fontSize="small" />;
      break;
    case StateType.Injured:
      stateIcon = <HeartBroken fontSize="small" />;
      break;
    case StateType.Gloomy:
      stateIcon = <MoodBad fontSize="small" />;
      break;
    case StateType.Focused:
      stateIcon = <OfflineBolt fontSize="small" />;
      break;
    default:
      stateIcon = <></>;
      break;
  }

  return (
    <DialogTooltip
      icon={stateIcon}
      title={
        <React.Fragment>
          <Typography sx={{ fontWeight: 700 }}>{t(`enums.states.${state.type}`)}</Typography>
          <Typography variant="body2">{t(`state_descriptions.${state.type}`)}</Typography>
        </React.Fragment>
      }
    />
  );
};

export default StateIcon;
