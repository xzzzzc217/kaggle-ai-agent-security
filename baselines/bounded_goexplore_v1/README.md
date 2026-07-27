# Bounded Go-Explore v1

This candidate delegates search to the Go-Explore attacker shipped in competition
SDK 3.1.2 while limiting delegated search to 80% of the scorer-provided wall-clock
budget and at most 900 seconds.

The reserve addresses a reproduced failure: the unwrapped SDK attacker uses its
entire `time_budget_s`, so the evaluator can raise `attack generation exceeded its
time budget` before the findings list is returned. A 5% reserve was also reproduced
as insufficient because one 12-branch batch can cross the outer deadline. The
15-minute cap additionally bounds the SDK archive's documented long-run memory
growth. The wrapper preserves
`max_steps`, `max_tool_hops`, the SDK prompt bank, archive policy, scoring hints and
replayable `AttackCandidate` contract.

This is a competition-fixture-only candidate. It does not add internet access,
credentials or non-fixture targets.

Status: implementation candidate for formal experiment E005. A public Kaggle score
must not be inferred from deterministic local-agent results.
