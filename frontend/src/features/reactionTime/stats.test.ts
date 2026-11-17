import { describe, it, expect } from 'vitest';
import { computeReactionStats, type ReactionTrial } from './stats';

function validTrial(trialIndex: number, reactionTimeMs: number): ReactionTrial {
  return { trialIndex, reactionTimeMs, isPremature: false };
}

function prematureTrial(trialIndex: number): ReactionTrial {
  return { trialIndex, reactionTimeMs: null, isPremature: true };
}

describe('computeReactionStats', () => {
  it('returns null when there are no trials', () => {
    expect(computeReactionStats([])).toBeNull();
  });

  it('returns null when every trial was premature', () => {
    const trials = [prematureTrial(0), prematureTrial(1)];
    expect(computeReactionStats(trials)).toBeNull();
  });

  it('excludes premature trials from the stats but counts them', () => {
    const trials = [validTrial(0, 300), validTrial(1, 200), prematureTrial(2), validTrial(3, 1000)];

    expect(computeReactionStats(trials)).toMatchObject({
      validTrialCount: 3,
      prematureCount: 1,
      meanMs: 500,
      medianMs: 300,
      fastestMs: 200,
      slowestMs: 1000,
    });
  });

  it('averages the two middle values for an even number of trials', () => {
    const trials = [validTrial(0, 400), validTrial(1, 100), validTrial(2, 300), validTrial(3, 200)];

    expect(computeReactionStats(trials)?.medianMs).toBe(250);
  });

  it('sorts numerically, not alphabetically', () => {
    const trials = [validTrial(0, 900), validTrial(1, 1000), validTrial(2, 250)];

    expect(computeReactionStats(trials)).toMatchObject({
      fastestMs: 250,
      slowestMs: 1000,
      medianMs: 900,
    });
  });

  it('returns null standard deviation for a single valid trial', () => {
    const trials = [validTrial(0, 250)];

    expect(computeReactionStats(trials)).toMatchObject({
      validTrialCount: 1,
      meanMs: 250,
      medianMs: 250,
      standardDeviationMs: null,
    });
  });

  it('computes sample standard deviation', () => {
    // mean = 250, squared diffs = 2500 + 2500, divided by (n - 1) = 1, sqrt(5000) ≈ 70.71
    const trials = [validTrial(0, 200), validTrial(1, 300)];

    expect(computeReactionStats(trials)?.standardDeviationMs).toBeCloseTo(70.71, 2);
  });
});