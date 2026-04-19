import { useState, useEffect } from 'react';

const STORAGE_KEY = 'replay_ticks';
const MAX_ENTRIES = 16;

interface ReplayTickEntry {
  eventId: number;
  tick: number;
}

export function useReplayState(eventId: number, initialTick: number = 0) {
  const [replayTick, setReplayTick] = useState<number>(initialTick);

  // Load stored replay tick from localStorage on mount
  useEffect(() => {
    const storedData = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    const eventEntry = storedData.find((entry: ReplayTickEntry) => entry.eventId === eventId);
    if (eventEntry) {
      setReplayTick(eventEntry.tick);
    }
  }, [eventId]);

  // Save replay tick to localStorage when it changes
  useEffect(() => {
    let storedData = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');

    // Remove existing entry for this eventId if it exists
    storedData = storedData.filter((entry: ReplayTickEntry) => entry.eventId !== eventId);

    // Add new entry at the end
    storedData.push({ eventId, tick: replayTick });

    // Keep only the last MAX_ENTRIES entries
    if (storedData.length > MAX_ENTRIES) {
      storedData = storedData.slice(-MAX_ENTRIES);
    }

    localStorage.setItem(STORAGE_KEY, JSON.stringify(storedData));
  }, [eventId, replayTick]);

  return { replayTick, setReplayTick };
}
