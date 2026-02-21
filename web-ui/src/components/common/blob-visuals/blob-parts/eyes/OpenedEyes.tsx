import { StateType } from '../../../../../../generated';
import { GloomyEyebrows } from './GloomyEyebrows';
import { IdleEyes } from './IdleEyes';

type OpenedEyesProps = {
  blobStates: StateType[];
};

export const OpenedEyes = ({ blobStates }: OpenedEyesProps) => {
  return (
    <>
      {blobStates.find((state) => state === StateType.Gloomy) !== undefined && <GloomyEyebrows />}
      <IdleEyes />
    </>
  );
};
