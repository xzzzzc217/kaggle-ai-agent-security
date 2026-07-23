# Adaptive budget v1

This variant changes one mechanism from the official starter: fixed time margins are
replaced by a conservative adaptive budget controller.

The controller observes completed interaction latency, estimates the cost of the next
candidate, and preserves a hard reserve before starting more work. Candidate prompts
and sandbox-only destinations remain the same as the starter so that the first
comparison isolates scheduling.

Status: locally unit-tested and validated against competition SDK 3.1.2. The
deterministic smoke result is mechanism evidence only and is not comparable to the
Kaggle leaderboard. This variant has not been submitted for a competition rerun.
