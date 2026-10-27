# Database Schema — v1

## Tables

```
users
  id                    PK
  email                 unique, required
  display_name
  created_at

cognitive_sessions      one row per test sitting
  id                    PK
  user_id               FK -> users.id
  test_type             'simple_reaction' (more later)
  started_at
  completed_at          null if abandoned
  sport_session_id      FK -> sport_sessions.id, nullable

cognitive_trials        one row per trial
  id                    PK
  cognitive_session_id  FK -> cognitive_sessions.id
  trial_index
  reaction_time_ms      null if premature
  is_premature

sport_sessions          fields shared by every sport
  id                    PK
  user_id               FK -> users.id
  sport                 'golf' | 'volleyball'
  played_at
  focus_rating          1-10
  fatigue_rating        1-10
  notes                 optional
  created_at

golf_performance        one-to-one with sport_sessions
  sport_session_id      PK + FK -> sport_sessions.id
  holes_played          9 or 18
  total_strokes
  course_par
  fairways_hit
  fairways_attempted
  greens_in_regulation
  total_putts

volleyball_performance  one-to-one with sport_sessions
  sport_session_id      PK + FK -> sport_sessions.id
  sets_played
  serves_attempted
  service_errors
  aces
  attack_attempts
  kills
  attack_errors
  digs
```

## Design decisions

- **One table per sport.** Typed columns the database can validate. A new sport is a new table; a new metric is a new column. Existing tables never get restructured. Rejected: key/value metrics table and JSON columns (no validation, painful queries).
- **Derived values are never stored.** Score to par, serves in, and reaction-time mean/median are computed from the raw columns, so there is one source of truth.
- **Exposure is recorded.** `holes_played`, `sets_played`, and `attack_attempts` exist so performance can be normalized. Raw counts across different-length sessions would confound every correlation.
- **Cognitive sessions point to sport sessions.** Several tests can precede one game, so the foreign key lives on the "many" side. Nullable because the test is taken before the game is logged.
- **Every athlete-data table is scoped to a user.** Hardcoded `user_id = 1` until authentication (Phase 13).
- **Not yet included:** password hash (added in Phase 13 via migration) and columns for choice reaction / go-no-go (added when those tests are built).