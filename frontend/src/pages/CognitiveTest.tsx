import ReactionTimeTest from "../features/reactionTime/ReactionTimeTest";

export default function CognitiveTest() {
  return (
    <section>
      <h2>Simple Reaction Time</h2>
      <p>
        When the box turns green, click as fast as you can. Clicking before green counts as
        premature and the trial is repeated.
      </p>
      <ReactionTimeTest />
    </section>
  );
}