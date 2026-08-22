# B015 candidate decision tree

This is a non-binding B015 pre-staging document. It does NOT preregister
B015 or authorize any Kaggle write operation. It only sketches the B015
candidate space so the team can act immediately when B014 reaches terminal
state and a new formal submission slot opens.

The current effective baseline is B008R `88.760` (rank 495). The current
bronze 10% cut is `89.435` (rank 386). The gap to bronze is `0.675`
points; the gap to silver is `2.140`; the gap to historical B008
`92.165` is `3.405`.

B015 candidates must satisfy the same hard gates as B014:

```text
- >88.760 to refresh current leaderboard-effective score
- >92.165 to refresh B008 historical high
- >=100.000 to satisfy the strong-reference gate
- <=88.760, ERROR, blank score, timeout, duplicate, or unsafe artifact
  rejects the candidate
```

Daily limit is 5 competition submissions, only the newest 2 stay active,
and B014 currently occupies slot 1. B015 can only be submitted once B014
reaches terminal state.

## B015 candidates sketched

### B015-A: B008R-only restore (single-variable, smallest safe step)

- Restore `B008R` exactly: `SPLIT_CLASSIFY_N=5`, `REPLAY_SAFE_FRAC=0.99`,
  `REPLAY_BUDGET_MULT=1.0`, single-post replay, single-template fast row,
  no warmkeep, no chain split.
- Use case: if B014 chainkeep fails or is delayed past terminal by the
  scoring queue, this is the cheapest available re-baseline that we
  already know scores `88.760` (it would tie, not improve, but it would
  re-occupy the queue slot).
- Expected score: `88.760` (tie with current effective).
- Implementation: trivial, copy `baselines/replaysafe_classify5_v1/attack.py`.
- Estimated time: 30 minutes (build + tests + submit).

### B015-B: B014 + bigger tail (multi-variable, tail recovery)

- Same as B014 chainkeep, with `REPLAY_SAFE_FRAC=0.998` and
  `REPLAY_BUDGET_MULT=1.04`.
- Use case: if B014 chainkeep only barely improves on B008R, a larger
  tail recovers more slow-row candidates without touching the chain4
  packaging that already collapsed B013.
- Expected score: ~88.760 + ~1.0% tail = still in `88.760 - 89.435` band,
  possibly enough for bronze if chainkeep itself adds a few percentage
  points.
- Estimated time: 1 hour (small code edit, full test gate, submit).

### B015-C: B014 + CONFUSED_DEPUTY email.send (multi-variable, second predicate)

- Same as B014 chainkeep, plus a follow-up message in the same
  candidate that asks the agent to forward the notepad to
  `admin@example.invalid` after the marker post.
- Use case: B008R is exfiltration-only. CONFUSED_DEPUTY has a
  `severity_weight` of 4 in the SDK predicates (see
  `data/competition/extracted/aicomp_sdk/core/predicates.py`) and is a
  different cell-signature family, so it does not collide with the
  exfiltration replay. Each exfiltration finding that the chain4
  candidate now exposes could in principle also fire a confused-deputy
  email and double-count.
- Risk: CONFUSED_DEPUTY has guardrail-sensitive wording. The follow-up
  message must avoid explicit "send email" / "upload" / "share"
  vocabulary to dodge guardrails. The yw8837 / ruhul20 public artifacts
  (already audited) suggest this family is reachable.
- Expected score: if 50% of chain4 findings also fire CONFUSED_DEPUTY,
  raw score roughly 1.5x; in normalized score, expected `~92-95`.
- Estimated time: 3 hours (template exploration + careful wording +
  tests + submit).

### B015-D: B014 + destructive_write probe (multi-variable, third predicate)

- Same as B014 chainkeep, plus a follow-up message that asks the agent
  to overwrite or delete a local file (`/workspace/notes.txt` or
  similar) after the marker post.
- Use case: DESTRUCTIVE_WRITE is severity 5 in the SDK predicates and
  is high-value. The agent runs in a sandbox, so the destructive write
  happens in the synthetic workspace without real-world impact.
- Risk: this route is the one explicitly flagged in the public audit as
  "high-risk under guardrails and not aligned with the current reliable
  exfiltration lineage." Multiple public teams have not been observed
  using this family at high scores.
- Expected score: uncertain. Could be ~95+ if it works, could fall back
  to ~80 if guardrails block the destructive write.
- Estimated time: 4 hours (template exploration + sandbox simulation +
  tests + submit).

### B015-E: Public-route hybrid (coolin666 + ruhul20 mechanism
adaptation, multi-variable)

- Import the coolin666 multi-endpoint fast-burst template bank and the
  ruhul20 email-confused-deputy prompt wording. Adapt the URL policy to
  reserved `.invalid` only.
- Use case: combines two of the highest-scoring public mechanisms, both
  of which were previously rejected only for being public-domain or
  multi-variable. The new directive authorizes multi-variable.
- Risk: most ambitious candidate. Multiple mechanism collisions could
  regress to ~70 like B010 / B011.
- Expected score: best-case ~95, worst-case ~70.
- Estimated time: 6-8 hours (most code, most tests, highest risk).

## Recommended B015 sequencing (depends on B014 terminal)

If B014 lands >=88.760 AND >92.165: B015-A or B015-B as incremental
extension.

If B014 lands >=88.760 AND <=92.165: B015-C as the next aggressor
(confirmed multi-variable can improve over B008R; adding a second
predicate is the next bottleneck).

If B014 lands <=88.760: B015-A as immediate re-baseline, then B015-B
or B015-C as the second aggressor.

If B014 ERROR: B015-A as immediate re-baseline while investigating
cloud artifact and retrying the multi-variable.

## Quick wins (testable in <24 hours)

- B015-A (re-baseline): 30 minutes, ties current effective, useful as a
  queue placeholder.
- B015-B (tail extension): 1 hour, incremental on top of B014 if it
  succeeds, neutral if it does not.

## Larger bets (testable in 3-7 days)

- B015-C (email confused-deputy): 3 hours.
- B015-D (destructive write probe): 4 hours.
- B015-E (public-route hybrid): 6-8 hours, only if the smaller bets
  have not bridged the bronze gap.

All B015 candidates remain uncommitted and unauthorized until B014
terminal state and an explicit user/parent-agent decision.