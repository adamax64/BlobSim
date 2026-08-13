import { useEffect, useMemo, useState, useCallback } from 'react';
import { BlobStatsDto, StateType, ActivityTypeDbo, Element } from '../../../../generated';
import { BlobBase } from './blob-parts/BlobBase';
import { TerminatedEyes } from './blob-parts/eyes/TerminatedEyes';
import { Blink } from './blob-parts/eyes/Blink';
import { mapActivityToTool } from './utils';
import { OpenedEyes } from './blob-parts/eyes/OpenedEyes';
import { Bruises } from './blob-parts/Bruises';
import { ClosedEyes } from './blob-parts/eyes/ClosedEyes';

type BlobAnimatedProps = {
  blob: BlobStatsDto;
  size: number;
};

const ELEMENT_EYE_COLORS: Partial<Record<Element, string>> = {
  [Element.Fire]: '#ffb366',
  [Element.Wind]: '#99f6ff',
  [Element.Water]: '#6394da',
  [Element.Ice]: '#aee9ff',
  [Element.Beast]: '#c9a27a',
};

export const BlobAnimated = ({ blob, size }: BlobAnimatedProps) => {
  const [eyesOpen, setEyesOpen] = useState(true);

  const toggleEyes = useCallback(() => {
    setEyesOpen((v) => !v);
  }, []);

  useEffect(() => {
    const timeouts: number[] = [];
    let cancelled = false;

    const rand = (min: number, max: number) => min + Math.random() * (max - min);

    const scheduleNextBlink = () => {
      if (cancelled) return;
      const gap = rand(2500, 5500);
      const id = window.setTimeout(() => {
        blinkOnce();
      }, gap);
      timeouts.push(id);
    };

    const blinkOnce = (followUpsLeft = Math.random() < 0.3 ? 1 : 0) => {
      if (cancelled) return;
      const blinkDuration = rand(90, 180);
      const closeId = window.setTimeout(() => {
        toggleEyes();
        const openId = window.setTimeout(() => {
          toggleEyes();
          if (followUpsLeft > 0) {
            blinkOnce(followUpsLeft - 1);
          } else {
            scheduleNextBlink();
          }
        }, blinkDuration);
        timeouts.push(openId);
      }, 0);
      timeouts.push(closeId);
    };

    scheduleNextBlink();

    return () => {
      cancelled = true;
      timeouts.forEach((id) => clearTimeout(id));
    };
  }, [toggleEyes]);

  const eyeColor = blob.element ? ELEMENT_EYE_COLORS[blob.element] : undefined;

  const eyeSlot = useMemo(() => {
    if (blob.isDead) {
      return <TerminatedEyes />;
    }
    if (blob.currentActivity === ActivityTypeDbo.Idle) {
      return <ClosedEyes />;
    }
    return eyesOpen ? (
      <OpenedEyes blobStates={blob.states.map((s) => s.type)} eyeColor={eyeColor} />
    ) : (
      <Blink />
    );
  }, [eyesOpen, blob.isDead, blob.currentActivity, blob.states, eyeColor]);

  return (
    <BlobBase
      size={size}
      color={blob.color}
      eyeSlot={eyeSlot}
      doSquash={!blob.isDead}
      hasCrown={blob.isGrandmaster ?? false}
      hasCatEars={blob.element === Element.Beast}
      toolSlot={mapActivityToTool(blob.currentActivity)}
      bruiseSlot={blob.states.find((s) => s.type === StateType.Injured) !== undefined ? <Bruises /> : undefined}
    />
  );
};
