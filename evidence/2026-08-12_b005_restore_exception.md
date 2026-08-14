# B005R authorized score restoration exception

## 1. Scope and authorization

This record preregisters a narrow leaderboard-effective score restoration
exception. It is not a B012 algorithm candidate and not a new single-variable
experiment.

The user explicitly authorized recovery operations on 2026-08-10 with
`恢复最佳分数，授权所有操作`. B008R partially restored the leaderboard-effective
score from B010 `52.330` to `88.760`, but it did not restore the historical high
B008 score `92.165` or the prior B005 score `91.930`. Because no strong B012
single-variable mechanism is currently selected, a byte-identical B005 restore is
tested as a separate restoration exception.

## 2. Current state before restoration

Latest checks before this preregistration:

```text
observed_utc=2026-08-12 15:12
competition=ai-agent-security-multi-step-tool-attacks
current_leaderboard_effective_submission_ref=55393959
current_leaderboard_effective_experiment=B008R
current_leaderboard_effective_status=SubmissionStatus.COMPLETE
current_leaderboard_effective_public_score=88.760
current_leaderboard_effective_private_score=
latest_rejected_submission_ref=55433780
latest_rejected_experiment=B011
latest_rejected_public_score=72.680
historical_high_submission_ref=55266445
historical_high_experiment=B008
historical_high_public_score=92.165
historical_high_current_status=SubmissionStatus.ERROR
historical_b005_submission_ref=55185029
historical_b005_public_score=91.930
historical_b005_current_status=SubmissionStatus.ERROR
```

The public leaderboard snapshot downloaded at 2026-08-12 15:15 UTC shows:

```text
leaderboard_rows=1266
team_name=heralces
current_leaderboard_rank=250
current_leaderboard_score=88.760
current_leaderboard_last_submission_date=2026-08-11 13:22:50
current_leaderboard_submission_count=3
score_at_50=96.435
score_at_100=91.935
score_at_200=89.325
rank_if_88_760=249
rank_if_91_930=101
rank_if_92_165=95
rank_if_72_680=879
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-12_1512_b005r_consider/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=artifacts/kaggle/leaderboards/2026-08-12_1512_b005r_consider/extracted_py2/ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-12T15_15_29.csv
```

The downloaded leaderboard artifact is under `artifacts/` and remains ignored by
Git.

## 3. Restoration source identity

The restoration will use the original B005 attack source byte-for-byte:

```text
restore_id=B005R
source_attack_file=baselines/replaysafe_tail99_v1/attack.py
source_experiment=B005
source_attack_sha256=9d86d633b50a72f7499f7ad6c4f81c03fb61887e12351da977f7cb64e413c67f
source_size_bytes=10764
source_commit=a4a70ac
original_prereg_commit=3e5f741
original_submission_ref=55185029
original_notebook=heralces/ai-agent-security-b005-tail99
```

No behavior variable is changed. This duplicate-source submission is allowed only
as a restoration exception and must not be counted as B012.

## 4. Pre-submission checks

The source was rechecked before this restoration preregistration:

```text
preflight=PASS
preflight_sha256=9d86d633b50a72f7499f7ad6c4f81c03fb61887e12351da977f7cb64e413c67f
target_pytest=9 passed
pytest=106 passed
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

This restoration is judged separately from normal B012 candidate selection:

| Real result | Fixed decision |
|---|---|
| `COMPLETE` and Public Score `>=91.930` | B005 historical score is restored as a current score-bearing result |
| `COMPLETE` and `88.760 < Public Score < 91.930` | Leaderboard-effective score improves, but B005 historical score is not restored |
| `COMPLETE` and Public Score `>92.165` | Also record a new historical high |
| `COMPLETE` and Public Score `>=100.000` | Also mark strong competition reproduction |
| `COMPLETE` and Public Score `<=88.760` | Restoration failed |
| `ERROR`, `FAILED`, blank score, or timeout | Restoration failed |

Do not repeat B005R or repush the same Notebook. While B005R is unknown, do not
create B012 or any other new formal competition submission.

## 6. Planned Kaggle objects

After this preregistration document is committed and pushed, the planned private
Notebook is:

```text
kernel=heralces/ai-agent-security-b005r-restore-tail99
title=AI Agent Security B005R Restore Tail99
experiment_id=B005R
kernel_version=1
submission_file=submission.csv
submission_message=B005R restore tail99 | attack 9d86d633 | authorized restore | SDK 3.1.2
```

Before formal competition submission, the cloud artifact hash must match the
local B005 source hash, notebook logs must not show actionable execution errors,
artifact credential-value scan must be clean, and the submission list must
confirm that no previous B005R restoration submission exists.

## 7. Actual restore creation record

This restore was created only after the preregistration document was committed
and pushed.

```text
restore_prereg_commit=9a4b96a
restore_prereg_full_commit=9a4b96a4f87fab3ddbff635a8080ab938fdf0b95
kernel=heralces/ai-agent-security-b005r-restore-tail99
title=AI Agent Security B005R Restore Tail99
experiment_id=B005R
kernel_version=1
kernel_status=KernelWorkerStatus.COMPLETE
manifest_git_commit=9a4b96a4f87fab3ddbff635a8080ab938fdf0b95
cloud_artifact_dir=artifacts/kaggle/B005R_v1
local_attack_sha256=9d86d633b50a72f7499f7ad6c4f81c03fb61887e12351da977f7cb64e413c67f
cloud_attack_sha256=9d86d633b50a72f7499f7ad6c4f81c03fb61887e12351da977f7cb64e413c67f
cloud_hash_matches_local=true
submission_csv_bytes=88
log_actionable_error_scan=0
artifact_credential_value_scan=0
```

Immediately before formal submission, the Kaggle submissions list contained no
B005R entry and no submission with the restoration message. The correct Code
Competition submission used Kaggle kernel output binding:

```text
kernel=heralces/ai-agent-security-b005r-restore-tail99
kernel_version=1
submission_file=submission.csv
submission_message=B005R restore tail99 | attack 9d86d633 | authorized restore | SDK 3.1.2
```

The only B005R competition submission created under this restoration exception
is:

```text
restore_submission_ref=55461853
restore_submission_created_utc=2026-08-12 15:22:19.533
restore_submission_initial_observed_utc=2026-08-12 15:22
restore_submission_initial_status=SubmissionStatus.PENDING
restore_submission_initial_public_score=
restore_submission_initial_private_score=
restore_submission_error_description=None
```

Until `55461853` reaches a terminal state, do not create B012 or any other new
formal competition submission. Do not repeat B005R or repush the same Notebook.

## 8. Actual terminal result

The only B005R competition submission reached a terminal state during the
`2026-08-13 23:53 UTC` monitor heartbeat:

```text
restore_submission_ref=55461853
restore_submission_created_utc=2026-08-12 15:22:19.533
restore_submission_first_terminal_observed_utc=2026-08-13 23:53
restore_submission_terminal_status=SubmissionStatus.COMPLETE
restore_submission_public_score=86.945
restore_submission_private_score=
restore_submission_error_description=None
```

The fresh leaderboard snapshot downloaded for terminal verification shows:

```text
leaderboard_rows=1348
current_leaderboard_effective_submission=B008R 55393959
current_leaderboard_effective_score=88.760
team_rank=277
team_last_submission_date=2026-08-12 15:22:19
team_submission_count=4
score_at_50=97.110
score_at_100=92.025
score_at_200=89.550
rank_if_86_945=565
rank_if_88_760=276
rank_if_91_930=104
rank_if_92_165=97
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-13_2353_b005r_terminal/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=artifacts/kaggle/leaderboards/2026-08-13_2353_b005r_terminal/extracted_py/ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-14T01_39_51.csv
```

Fixed decision:

- `86.945 <= 88.760`, so B005R is a failed restoration under the preregistered
  rule.
- B005R did not improve the current leaderboard-effective score, did not restore
  B005 historical `91.930`, did not refresh B008 historical `92.165`, and did not
  reach the strong-competition reference `100.000`.
- Do not retry B005R and do not repush the same Notebook.
- B012 scouting may resume only after this terminal record is committed and
  pushed; no B012 or later formal competition submission is authorized without a
  new preregistration.
