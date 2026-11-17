import { useEffect, useRef, useState } from "react";
import { browserTiming, createReactionTrial } from "./reactionTimer";
import { computeReactionStats, type ReactionTrial } from "./stats";

const VALID_TRIALS_REQUIRED = 5;

type Phase = "ready" | "waiting" | "stimulus" | "tooEarly" | "result" | "complete";

type TrialRunner = ReturnType<typeof createReactionTrial>;

export default function ReactionTimeTest() {
  const [phase, setPhase] = useState<Phase>("ready");
  const [trials, setTrials] = useState<ReactionTrial[]>([]);
  const trialRef = useRef<TrialRunner | null>(null);

  // If the user leaves the page mid-trial, stop the pending timeout.
  useEffect(() => {
    return () => trialRef.current?.cancel();
  }, []);

  const validTrials = trials.filter((trial) => !trial.isPremature);
  const lastTrial = trials[trials.length - 1];

  function startNextTrial() {
    const trial = createReactionTrial(trials.length, browserTiming, () => setPhase("stimulus"));
    trialRef.current = trial;
    trial.start();
    setPhase("waiting");
  }

  function recordResponse() {
    const result = trialRef.current?.respond();
    if (!result) return;

    setTrials([...trials, result]);

    if (result.isPremature) {
      setPhase("tooEarly");
    } else if (validTrials.length + 1 >= VALID_TRIALS_REQUIRED) {
      setPhase("complete");
    } else {
      setPhase("result");
    }
  }

  function handlePointerDown() {
    if (phase === "waiting" || phase === "stimulus") {
      recordResponse();
    } else if (phase !== "complete") {
      startNextTrial();
    }
  }

  function restart() {
    setTrials([]);
    setPhase("ready");
  }

  if (phase === "complete") {
    const stats = computeReactionStats(trials);

    return (
      <div className="reaction-results">
        <h3>Results</h3>
        {stats && (
          <>
            <dl>
              <dt>Mean</dt>
              <dd>{Math.round(stats.meanMs)} ms</dd>
              <dt>Median</dt>
              <dd>{Math.round(stats.medianMs)} ms</dd>
              <dt>Fastest</dt>
              <dd>{stats.fastestMs} ms</dd>
              <dt>Slowest</dt>
              <dd>{stats.slowestMs} ms</dd>
              <dt>Variability (SD)</dt>
              <dd>
                {stats.standardDeviationMs === null
                  ? "n/a"
                  : `${Math.round(stats.standardDeviationMs)} ms`}
              </dd>
            </dl>
            <p className="reaction-note">
              Based on {stats.validTrialCount} valid trials ({stats.prematureCount} premature
              excluded). This measures reaction speed only.
            </p>
          </>
        )}
        <button type="button" onClick={restart}>
          Run again
        </button>
      </div>
    );
  }

  const messages: Record<Phase, string> = {
    ready: `Trial ${validTrials.length + 1} of ${VALID_TRIALS_REQUIRED}: click to start`,
    waiting: "Wait for green...",
    stimulus: "Click!",
    tooEarly: "Too early. Click to retry this trial.",
    result: `${lastTrial?.reactionTimeMs} ms. Click for the next trial.`,
    complete: "",
  };

  return (
    <button type="button" className={`reaction-box ${phase}`} onPointerDown={handlePointerDown}>
      {messages[phase]}
    </button>
  );
}