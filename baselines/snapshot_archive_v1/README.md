# Snapshot archive v1

This variant builds on the adaptive-budget and novelty-scheduling experiments.
Its single additional mechanism is a trace-validated snapshot archive:

1. a prefix is archived only when its trace contains a successful source tool call;
2. the same archive state/mechanism branch is expanded at most once;
3. snapshot execution is discovery-only;
4. every retained candidate is rerun from a fresh reset using its complete message
   sequence, and only that fresh replay trace is used for retention.

This directly targets a code-competition failure mode: a path may work after restoring
an in-memory snapshot but fail when the evaluator replays only `user_messages`.

Status: fixture-level source validation, archive deduplication, and full-replay gating
are unit-tested; the submission shape validates against competition SDK 3.1.2. The
deterministic smoke result is not comparable to the Kaggle leaderboard. This variant
has not been submitted for a competition rerun.
