# B008 score-bearing ERROR status audit

## 1. Why this audit exists

The user-provided Kaggle submissions screenshot shows B008 with a warning/error
icon while still displaying Public Score `92.165`. This audit checks that state
against Kaggle CLI/API and the Kaggle Notebook worker status.

No submission, retry, selection, or Notebook rerun was performed.

## 2. Current API/CLI observations

```text
audit_observed_utc=2026-08-10 01:31
competition=ai-agent-security-multi-step-tool-attacks
submission_ref=55266445
experiment_id=B008
description=B008 classify5 | attack 4d433a77 | prereg 34aaa89 | SDK 3.1.2
submission_date_utc=2026-08-05 09:59:15.037000
competition_submission_status=SubmissionStatus.ERROR
public_score=92.165
private_score=
error_description=
notebook_slug=heralces/ai-agent-security-b008-classify5
notebook_status=KernelWorkerStatus.COMPLETE
```

For comparison, the latest low-scoring B010 row is currently the only recent
score-bearing submission with `SubmissionStatus.COMPLETE`:

```text
submission_ref=55327331
experiment_id=B010
competition_submission_status=SubmissionStatus.COMPLETE
public_score=52.330
private_score=
error_description=
notebook_slug=heralces/ai-agent-security-b010-slow-commentary
notebook_status=KernelWorkerStatus.COMPLETE
```

The latest downloaded public leaderboard still uses B010, not B008:

```text
leaderboard_observed_utc=2026-08-10 01:31
team_name=heralces
leaderboard_rank=711
leaderboard_score=52.330
leaderboard_last_submission_date=2026-08-07 14:48:07
rank_if_b008_92_165_were_used=70
score_at_50=94.160
score_at_100=90.540
score_at_200=88.560
```

## 3. Interpretation

- B008's Notebook execution is not the failing component: the Kaggle Notebook
  worker status is still `COMPLETE`.
- The competition submission object for B008 is currently inconsistent but
  unfavorable: it keeps `_public_score='92.165'` while exposing
  `SubmissionStatus.ERROR` and no `error_description`.
- The public leaderboard currently follows the B010 `52.330` row rather than the
  B008 `92.165` score-bearing row. This means B008 should no longer be treated
  as a currently selectable or leaderboard-effective submission unless Kaggle UI
  or Kaggle support restores/selects it.
- The previous wording that the user should manually select B008 "if available"
  was too optimistic. The current evidence says the immediate blocker is that
  B008 itself is in an ERROR/Warning state despite having a visible score.

## 4. Decision impact

Until this status issue is resolved:

1. Do not create a new formal competition submission.
2. Do not claim current rank from B008 `92.165`; current visible leaderboard rank
   is tied to B010 `52.330`.
3. Do not resubmit B008 without explicit user authorization, because that would
   be an exception to the no-retry/no-duplicate discipline.
4. The practical paths are Kaggle support/status restoration, a user-authorized
   narrow B008 restoration rerun, or accepting the current low leaderboard row
   while continuing only local research.
