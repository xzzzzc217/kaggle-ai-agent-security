# B008R authorized best-score restoration exception

## 1. Scope and authorization

This record preregisters a narrow restoration exception for the current Kaggle
leaderboard risk.

The user explicitly authorized recovery operations on 2026-08-10 with:
`恢复最佳分数，授权所有操作`.

This is not a new algorithm candidate and not a new single-variable experiment.
The goal is to restore a currently leaderboard-effective score using the same
source as the historical best B008 result, because the original B008 competition
submission is now score-bearing but marked `SubmissionStatus.ERROR`.

## 2. Current state before restoration

The latest checks before this preregistration show:

```text
observed_utc=2026-08-10 01:42
competition=ai-agent-security-multi-step-tool-attacks
historical_best_submission_ref=55266445
historical_best_experiment=B008
historical_best_public_score=92.165
historical_best_private_score=
historical_best_current_status=SubmissionStatus.ERROR
historical_best_error_description=None
historical_best_notebook=heralces/ai-agent-security-b008-classify5
historical_best_notebook_version=1
historical_best_notebook_status=KernelWorkerStatus.COMPLETE
current_leaderboard_submission_ref=55327331
current_leaderboard_experiment=B010
current_leaderboard_public_score=52.330
current_leaderboard_status=SubmissionStatus.COMPLETE
```

The public leaderboard snapshot downloaded at 2026-08-10 01:42 UTC shows:

```text
leaderboard_rows=911
team_name=heralces
current_leaderboard_rank=712
current_leaderboard_score=52.330
current_leaderboard_last_submission_date=2026-08-07 14:48:07
rank_if_92_165_were_leaderboard_effective=71
score_at_50=94.160
score_at_100=90.585
score_at_200=88.560
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-10_b008_restore/ai-agent-security-multi-step-tool-attacks.zip
```

The downloaded leaderboard artifact is under `artifacts/` and remains ignored by
Git.

## 3. Restoration source identity

The restoration will use the original B008 attack source byte-for-byte:

```text
restore_id=B008R
source_attack_file=baselines/replaysafe_classify5_v1/attack.py
source_experiment=B008
source_attack_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
source_size_bytes=10799
source_commit=4b1ce2b
original_prereg_commit=34aaa89
original_submission_ref=55266445
original_notebook=heralces/ai-agent-security-b008-classify5
original_notebook_script_version_id=340336068
```

No behavior variable is changed. The duplicate-source submission is allowed only
because the user authorized a best-score restoration exception after the
leaderboard-effective row fell back to B010.

## 4. Pre-submission checks

The source was rechecked before this restoration preregistration:

```text
preflight=PASS
preflight_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
pytest=101 passed
ruff_check=passed
ruff_format_check=passed
git_diff_check=passed
sdk_validate=passed
credential_value_secret_scan=0
```

SDK validate required setting:

```text
PYTHONPATH=D:\kaggle\ai-agent-security\data\competition\extracted
PYTHONIOENCODING=utf-8
PYTHONUTF8=1
```

## 5. Restoration decision rule

This restoration is judged separately from normal B011 candidate selection:

| Real result | Fixed decision |
|---|---|
| `COMPLETE` and Public Score `>=92.165` | Historical best is restored as a current score-bearing result |
| `COMPLETE` and `52.330 < Public Score < 92.165` | Leaderboard is partially restored, but historical best is not restored |
| `COMPLETE` and Public Score `<=52.330` | Restoration failed |
| `ERROR`, `FAILED`, blank score, or timeout | Restoration failed |

If the restoration fails, do not repeat the same restoration Notebook without a
new explicit user authorization. If it succeeds, resume B011 only after the
leaderboard row is rechecked.

## 6. Planned Kaggle objects

After this preregistration document is committed and pushed, the planned private
Notebook is:

```text
kernel=heralces/ai-agent-security-b008r-restore-classify5
title=AI Agent Security B008R Restore Classify5
experiment_id=B008R
kernel_version=1
submission_file=submission.csv
submission_message=B008R restore classify5 | attack 4d433a77 | authorized restore | SDK 3.1.2
```

Before formal competition submission, the cloud artifact hash must match the
local B008 source hash, notebook logs must not show actionable execution errors,
and artifact credential-value scan must be clean.

## 7. Actual restore creation record

The preregistration above was committed and pushed before any Kaggle write:

```text
restore_prereg_commit=2e45dd7
restore_prereg_full_commit=2e45dd7945aa46d5cbfb7b9663bf514307a28eb5
```

The private restoration Notebook was then built and pushed:

```text
kernel=heralces/ai-agent-security-b008r-restore-classify5
kernel_version=1
kernel_status=KernelWorkerStatus.COMPLETE
cloud_artifact_dir=artifacts/kaggle/B008R_v1
cloud_attack_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
cloud_hash_matches_local=true
submission_csv_bytes=88
log_actionable_error_scan=0
artifact_credential_value_scan=0
```

The only B008R competition submission created under this restoration exception
is:

```text
restore_submission_ref=55393959
restore_submission_created_utc=2026-08-10 01:53:43.003
restore_submission_initial_status=SubmissionStatus.PENDING
restore_submission_initial_public_score=
restore_submission_initial_private_score=
restore_submission_message=B008R restore classify5 | attack 4d433a77 | authorized restore | SDK 3.1.2
```

Until `55393959` reaches a terminal state, do not create B011 or any other new
formal competition submission.
