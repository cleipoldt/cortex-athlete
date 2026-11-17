import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  createReactionTrial,
  randomDelayMs,
  MIN_DELAY_MS,
  MAX_DELAY_MS,
  type TimingSource,
} from './reactionTimer';

// random() = 0.5 makes every delay exactly 3000 ms.
// Date.now() is controlled by Vitest's fake timers.
const fakeTiming: TimingSource = {
  now: () => Date.now(),
  random: () => 0.5,
};

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

describe('randomDelayMs', () => {
  it('stays within the configured range', () => {
    expect(randomDelayMs(() => 0)).toBe(MIN_DELAY_MS);
    expect(randomDelayMs(() => 0.5)).toBe(3000);
    expect(randomDelayMs(() => 0.999)).toBeLessThan(MAX_DELAY_MS);
  });
});

describe('createReactionTrial', () => {
  it('shows the stimulus only after the delay', () => {
    const onStimulus = vi.fn();
    const trial = createReactionTrial(0, fakeTiming, onStimulus);

    trial.start();
    vi.advanceTimersByTime(2999);
    expect(onStimulus).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1);
    expect(onStimulus).toHaveBeenCalledTimes(1);
  });

  it('measures time from stimulus to response', () => {
    const trial = createReactionTrial(0, fakeTiming, () => {});

    trial.start();
    vi.advanceTimersByTime(3000 + 250);

    expect(trial.respond()).toEqual({ trialIndex: 0, reactionTimeMs: 250, isPremature: false });
  });

  it('marks a click during the wait as premature and cancels the stimulus', () => {
    const onStimulus = vi.fn();
    const trial = createReactionTrial(1, fakeTiming, onStimulus);

    trial.start();
    vi.advanceTimersByTime(2000);
    expect(trial.respond()).toEqual({ trialIndex: 1, reactionTimeMs: null, isPremature: true });

    vi.advanceTimersByTime(5000);
    expect(onStimulus).not.toHaveBeenCalled();
  });

  it('marks a response faster than the anticipation threshold as premature', () => {
    const trial = createReactionTrial(2, fakeTiming, () => {});

    trial.start();
    vi.advanceTimersByTime(3000 + 60);

    expect(trial.respond()).toEqual({ trialIndex: 2, reactionTimeMs: null, isPremature: true });
  });

  it('ignores a second click on the same trial', () => {
    const trial = createReactionTrial(0, fakeTiming, () => {});

    trial.start();
    vi.advanceTimersByTime(3250);
    trial.respond();

    expect(trial.respond()).toBeNull();
  });

  it('ignores a click before the trial starts', () => {
    const trial = createReactionTrial(0, fakeTiming, () => {});

    expect(trial.respond()).toBeNull();
  });

  it('never shows the stimulus after cancel', () => {
    const onStimulus = vi.fn();
    const trial = createReactionTrial(0, fakeTiming, onStimulus);

    trial.start();
    trial.cancel();
    vi.advanceTimersByTime(10000);

    expect(onStimulus).not.toHaveBeenCalled();
  });
});