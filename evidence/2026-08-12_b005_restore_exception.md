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
