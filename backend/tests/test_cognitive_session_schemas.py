"""Unit tests for the reaction-time request schema (no HTTP, no database)."""

from datetime import timedelta

import pytest
from pydantic import ValidationError

from app.schemas.cognitive_sessions import ReactionSessionCreate


def trial(index, time_ms, premature=False):
    """One trial, shaped exactly like the JSON the frontend sends."""
    return {"trialIndex": index, "reactionTimeMs": time_ms, "isPremature": premature}


def valid_payload(trials=None):
    """A correct request body. Tests change one thing to make it invalid."""
    return {
        "startedAt": "2026-11-17T21:00:00Z",
        "completedAt": "2026-11-17T21:01:30Z",
        "trials": trials
        if trials is not None
        else [trial(0, 280), trial(1, None, premature=True), trial(2, 310)],
    }


# --- Accepted -----------------------------------------------------------------


def test_valid_payload_is_accepted():
    session = ReactionSessionCreate.model_validate(valid_payload())

    assert len(session.trials) == 3
    assert session.trials[1].is_premature is True
    assert session.trials[1].reaction_time_ms is None


def test_timestamps_are_converted_to_utc():
    payload = valid_payload()
    payload["startedAt"] = "2026-11-17T14:00:00-07:00"  # Calgary time
    payload["completedAt"] = "2026-11-17T14:01:30-07:00"

    session = ReactionSessionCreate.model_validate(payload)

    assert session.started_at.utcoffset() == timedelta(0)
    assert session.started_at.hour == 21


@pytest.mark.parametrize("time_ms", [100, 5000])
def test_boundary_reaction_times_are_accepted(time_ms):
    session = ReactionSessionCreate.model_validate(valid_payload([trial(0, time_ms)]))

    assert session.trials[0].reaction_time_ms == time_ms


# --- Rejected: a single bad trial ----------------------------------------------


@pytest.mark.parametrize(
    "bad_trial",
    [
        pytest.param(trial(0, 250, premature=True), id="premature trial with a time"),
        pytest.param(trial(0, None), id="valid trial without a time"),
        pytest.param({"trialIndex": 0, "isPremature": False}, id="reactionTimeMs missing"),
        pytest.param(trial(0, 99), id="faster than 100 ms"),
        pytest.param(trial(0, 5001), id="slower than 5000 ms"),
        pytest.param(trial(0, 280.5), id="decimal reaction time"),
        pytest.param(trial(0, "280"), id="reaction time as a string"),
        pytest.param(trial(0, 280, premature="false"), id="isPremature as a string"),
    ],
)
def test_invalid_trial_is_rejected(bad_trial):
    with pytest.raises(ValidationError):
        ReactionSessionCreate.model_validate(valid_payload([bad_trial]))


# --- Rejected: the session as a whole ------------------------------------------


@pytest.mark.parametrize(
    "trials",
    [
        pytest.param([], id="no trials"),
        pytest.param([trial(0, 280), trial(2, 300)], id="gap in trialIndex"),
        pytest.param([trial(0, 280), trial(0, 300)], id="repeated trialIndex"),
        pytest.param([trial(1, 280), trial(0, 300)], id="trialIndex out of order"),
        pytest.param([trial(0, None, premature=True)], id="every trial premature"),
        pytest.param([trial(i, 300) for i in range(51)], id="more than 50 trials"),
    ],
)
def test_invalid_trial_list_is_rejected(trials):
    with pytest.raises(ValidationError):
        ReactionSessionCreate.model_validate(valid_payload(trials))


def test_timestamp_without_timezone_is_rejected():
    payload = valid_payload()
    payload["startedAt"] = "2026-11-17T21:00:00"  # no Z, no offset

    with pytest.raises(ValidationError):
        ReactionSessionCreate.model_validate(payload)


def test_completed_before_started_is_rejected():
    payload = valid_payload()
    payload["completedAt"] = "2026-11-17T20:59:00Z"

    with pytest.raises(ValidationError, match="completedAt cannot be before startedAt"):
        ReactionSessionCreate.model_validate(payload)


def test_client_cannot_choose_the_user():
    payload = valid_payload()
    payload["userId"] = 2

    with pytest.raises(ValidationError, match="userId"):
        ReactionSessionCreate.model_validate(payload)