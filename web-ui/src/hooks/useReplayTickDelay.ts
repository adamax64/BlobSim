import { useEffect, useRef } from 'react';

/**
 * Custom hook that applies a delay when replayTick increases (forward scrub)
 * but not when it decreases (backward scrub).
 * @param replayTick - The current replay tick value
 * @param callback - Function to call after the delay (if increasing) or immediately (if decreasing)
 * @param onLoadingChange - Optional callback to set loading state
 */
export const useReplayTickDelay = (
  replayTick: number,
  callback: () => void,
  onLoadingChange?: (loading: boolean) => void,
) => {
  const previousReplayTickRef = useRef(replayTick);
  const callbackRef = useRef(callback);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    onLoadingChange?.(true);
    const isIncreasing = replayTick > previousReplayTickRef.current;
    previousReplayTickRef.current = replayTick;
    const delay = isIncreasing ? 500 : 0;

    const timer = setTimeout(() => {
      callbackRef.current();
    }, delay);

    return () => clearTimeout(timer);
  }, [replayTick, onLoadingChange]);
};
