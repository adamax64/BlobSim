import { useEffect, useMemo, useState, useCallback } from 'react';
import { BlobStatsDto } from '../../../../generated';
import { BlobBase } from './blob-parts/BlobBase';
import { IdleEyes } from './blob-parts/eyes/IdleEyes';
import { TerminatedEyes } from './blob-parts/eyes/TerminatedEyes';
import { Blink } from './blob-parts/eyes/Blink';

type BlobAnimatedProps = {
  blob: BlobStatsDto;
  size: number;
};

export const BlobAnimated = ({ blob, size }: BlobAnimatedProps) => {
  const [eyesOpen, setEyesOpen] = useState(true);

  const toggleEyes = useCallback(() => {
    setEyesOpen((v) => !v);
  }, []);

  useEffect(() => {
    const timeouts: number[] = [];

    const runBlinkSequence = () => {
      timeouts.push(
        window.setTimeout(() => {
          toggleEyes();
        }, 4000),
      );
      timeouts.push(
        window.setTimeout(() => {
          toggleEyes();
        }, 4250),
      );
      timeouts.push(
        window.setTimeout(() => {
          toggleEyes();
        }, 8250),
      );
      timeouts.push(
        window.setTimeout(() => {
          toggleEyes();
        }, 8500),
      );
      timeouts.push(
        window.setTimeout(() => {
          toggleEyes();
        }, 8750),
      );
      timeouts.push(
        window.setTimeout(() => {
          toggleEyes();
        }, 9000),
      );
    };

    runBlinkSequence();
    const interval = window.setInterval(runBlinkSequence, 9000);

    return () => {
      clearInterval(interval);
      timeouts.forEach((id) => clearTimeout(id));
    };
  }, [toggleEyes]);

  const eyeSlot = useMemo(() => {
    if (blob.isDead) {
      return <TerminatedEyes />;
    }
    return eyesOpen ? <IdleEyes /> : <Blink />;
  }, [eyesOpen, blob.isDead]);

  return (
    <BlobBase
      size={size}
      color={blob.color}
      eyeSlot={eyeSlot}
      doSquash={!blob.isDead}
      hasCrown={blob.isGrandmaster ?? false}
    />
  );
};
