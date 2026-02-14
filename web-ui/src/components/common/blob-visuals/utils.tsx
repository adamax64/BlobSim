import { JSX } from 'react';
import { ActivityTypeDbo } from '../../../../generated';
import { Dumbbells } from './blob-parts/tools/Dumbbells';
import { DoubleDumbbells } from './blob-parts/tools/DoubleDumbbells';
import { Hammer } from './blob-parts/tools/Hammer';
import { Pickaxe } from './blob-parts/tools/Pickaxe';
import { Wrench } from './blob-parts/tools/Wrench';
import { Scroll } from './blob-parts/tools/Scroll';

export const mapActivityToTool = (activity?: ActivityTypeDbo | null): JSX.Element | undefined => {
  switch (activity) {
    case ActivityTypeDbo.Practice:
      return <Dumbbells />;
    case ActivityTypeDbo.IntenseTraining:
      return <DoubleDumbbells />;
    case ActivityTypeDbo.Labour:
      return <Hammer />;
    case ActivityTypeDbo.Mining:
      return <Pickaxe />;
    case ActivityTypeDbo.Maintenance:
      return <Wrench />;
    case ActivityTypeDbo.Administration:
      return <Scroll />;
    case ActivityTypeDbo.IntensePractice:
      return <DoubleDumbbells />;
    default:
      return undefined;
  }
};
