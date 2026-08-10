# Current public leaderboard audit

## 1. Query identity

This is a read-only leaderboard/ranking audit. It does not create, retry, select,
or resubmit any Kaggle competition submission.

```text
audit_observed_utc=2026-08-09 14:25
competition=ai-agent-security-multi-step-tool-attacks
command=kaggle competitions leaderboard ai-agent-security-multi-step-tool-attacks --download
leaderboard_rows=816
current_best_recorded_experiment=B008
current_best_recorded_submission_ref=55266445
current_best_recorded_public_score=92.165
latest_submission_experiment=B010
latest_submission_ref=55327331
latest_submission_public_score=52.330
```

## 2. Observed team row

The downloaded leaderboard row for the account/team currently shows the latest
B010 score rather than the previously recorded B008 best score.

```text
team_name=heralces
rank=637
score=52.330
last_submission_date=2026-08-07 14:48:07
submission_count=1
```

The same audit computed where the recorded B008 score would rank if the public
leaderboard row used `92.165`:

```text
rank_if_score_92_165=59
ties_at_92_165=0
score_at_50=92.655
score_at_100=90.055
score_at_200=88.065
```

## 3. Interpretation

- The project evidence still records B008 submission `55266445` with Public Score
  `92.165` as the highest true rerun result observed for this account.
- The current public leaderboard download, however, ranks the team at B010's
  `52.330`, not at B008's `92.165`.
- This creates a ranking/selection risk: continuing to submit exploratory
  candidates without restoring or selecting the best scored submission can leave
  the visible public leaderboard position far below the best recorded score.
- No automatic corrective action was taken in this audit because resubmitting
  B008 would violate the preregistered no-retry rule, and the current Kaggle CLI
  exposes listing/submission commands but no clear prior-submission selection
  command.

## 4. Required decision

Before creating another formal Kaggle competition submission, the project should
resolve whether the user wants to:

1. manually select B008 submission `55266445` in the Kaggle UI if selection is
   available,
2. authorize a narrow exception to the no-retry rule to restore B008's public
   leaderboard score if manual selection is unavailable, or
3. continue submitting new candidates while accepting that the visible public
   leaderboard row may remain at the latest scored submission.

## 5. Follow-up snapshot

The next heartbeat repeated the read-only submissions and leaderboard checks.
The selection risk remained unresolved and the visible rank worsened as the
leaderboard grew.

```text
audit_observed_utc=2026-08-10 01:31
leaderboard_rows=910
team_name=heralces
rank=711
score=52.330
last_submission_date=2026-08-07 14:48:07
rank_if_score_92_165=70
score_at_50=94.160
score_at_100=90.540
score_at_200=88.560
latest_submission_ref=55327331
latest_submission_score=52.330
best_recorded_submission_ref=55266445
best_recorded_public_score=92.165
```

No new submission, selection, or retry was performed.
