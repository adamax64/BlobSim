import { StateType } from '../../../../../../generated';
import { GloomyEyebrows } from './GloomyEyebrows';
import { IdleEyes } from './IdleEyes';
import { EyeCircles } from './EyeCircles';
import { EyeStars } from './EyeStars';

type OpenedEyesProps = {
  blobStates: StateType[];
  eyeColor?: string;
};

export const OpenedEyes = ({ blobStates, eyeColor }: OpenedEyesProps) => {
  return (
    <>
      {blobStates.find((state) => state === StateType.Gloomy) !== undefined && <GloomyEyebrows />}
      <IdleEyes color={eyeColor} />
      {blobStates.find((state) => state === StateType.Tired) !== undefined && <EyeCircles />}
      {blobStates.find((state) => state === StateType.Focused) !== undefined && <EyeStars />}
    </>
  );
};
