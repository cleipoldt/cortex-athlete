// Timing logic for a single Simple Reaction Time trial.
// No React here. Time and randomness are injected so tests can control them.

import type { ReactionTrial } from './stats';

export const MIN_DELAY_MS = 1500;
export const MAX_DELAY_MS = 4500;
// A response faster than this is a guess, not a reaction.
export const ANTICIPATION_THRESHOLD_MS = 100;

export interface TimingSource {
  now: () => number;
  random: () => number;
}

export const browserTiming: TimingSource = {
  now: () => performance.now(),
  random: () => Math.random(),
};

export function randomDelayMs(random: () => number): number {
  return MIN_DELAY_MS + random() * (MAX_DELAY_MS - MIN_DELAY_MS);
}

type TrialState = 'idle' | 'waiting' | 'stimulus' | 'finished';

export function createReactionTrial(
  trialIndex: number,
  timing: TimingSource,
  onStimulus: () => void,
) {
  let state: TrialState = 'idle';
  let timeoutId: ReturnType<typeof setTimeout> | undefined;
  let stimulusShownAt = 0;

  function start(): void {
    if (state !== 'idle') return;

    state = 'waiting';
    timeoutId = setTimeout(() => {
      state = 'stimulus';
      stimulusShownAt = timing.now();
      onStimulus();
    }, randomDelayMs(timing.random));
  }

  function respond(): ReactionTrial | null {
    if (state === 'waiting') {
      clearTimeout(timeoutId);
      state = 'finished';
      return { trialIndex, reactionTimeMs: null, isPremature: true };
    }

    if (state === 'stimulus') {
      state = 'finished';
      const elapsed = Math.round(timing.now() - stimulusShownAt);
      if (elapsed < ANTICIPATION_THRESHOLD_MS) {
        return { trialIndex, reactionTimeMs: null, isPremature: true };
      }
      return { trialIndex, reactionTimeMs: elapsed, isPremature: false };
    }

    return null;
  }

  function cancel(): void {
    clearTimeout(timeoutId);
    state = 'finished';
  }

  return { start, respond, cancel };
}