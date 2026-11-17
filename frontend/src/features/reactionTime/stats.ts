// Summary statistics for one Simple Reaction Time session.
// Pure functions only: no React, no timers, no network.

export interface ReactionTrial {
  trialIndex: number;
  reactionTimeMs: number | null; // null when the click was premature
  isPremature: boolean;
}

export interface ReactionStats {
  validTrialCount: number;
  prematureCount: number;
  meanMs: number;
  medianMs: number;
  fastestMs: number;
  slowestMs: number;
  standardDeviationMs: number | null; // null when fewer than 2 valid trials
}

export function computeReactionStats(trials: ReactionTrial[]): ReactionStats | null {
  const times: number[] = [];
  let prematureCount = 0;

  for (const trial of trials) {
    if (trial.isPremature) {
      prematureCount += 1;
    } else if (trial.reactionTimeMs !== null) {
      times.push(trial.reactionTimeMs);
    }
  }

  if (times.length === 0) {
    return null;
  }

  const sorted = times.sort((a, b) => a - b);
  const n = sorted.length;

  const sum = sorted.reduce((total, time) => total + time, 0);
  const mean = sum / n;

  const middle = Math.floor(n / 2);
  const median = n % 2 === 0 ? (sorted[middle - 1] + sorted[middle]) / 2 : sorted[middle];

  let standardDeviation: number | null = null;
  if (n >= 2) {
    const squaredDiffs = sorted.reduce((total, time) => total + (time - mean) ** 2, 0);
    standardDeviation = Math.sqrt(squaredDiffs / (n - 1));
  }

  return {
    validTrialCount: n,
    prematureCount,
    meanMs: mean,
    medianMs: median,
    fastestMs: sorted[0],
    slowestMs: sorted[n - 1],
    standardDeviationMs: standardDeviation,
  };
}