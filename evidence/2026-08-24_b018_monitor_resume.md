# B018 monitor resume + read-only screen

Resumed after the previous poller stopped at `2026-08-24 11:40:14 UTC`.
This record is observational. It does **not** authorize a Kaggle write,
a B018 retry, or a B019 kernel/submission.

## B018 status (2026-08-24 13:09 UTC)

```text
formal_submission_ref=55737814
status=SubmissionStatus.PENDING
public_score=blank
errorDescription=blank
created_utc=2026-08-24 08:39:02.783
age_at_resume=~4.5h
kernel=heralces/ai-agent-security-b018-fastharmony v1
kernelId=131791935
attack_sha256=c5cbc484867077eb027ad655cad90152c666f6faed773916069d5c3ff331f2c4
parent=B008R 88.760
```

Sibling terminals still rejected: B017 `55724973` `88.505`, B016
`55708612` `66.485`, B015-C-modified `55695369` `58.610`.

Prior B017/B016 COMPLETE times were ~12-13.5h after create, so B018 is
still in the expected scoring queue.

## Monitor

Previous 20-minute poller died after check 10/48 (connection resets, then
session end). Restarted `scripts/monitor_b018.py` at 13:09:33 UTC with a
fresh 16h window (`interval=1200s`, `max=48`). First restarted check:

```text
[2026-08-24 13:09:37 UTC] check 1/48 status=SubmissionStatus.PENDING public='' err=''
```

Log: `evidence/b018_monitor.log`. Do not resubmit B018. Do not start
B019 until `55737814` is COMPLETE / ERROR / FAILED.

Preregistered gates remain:

| B018 terminal | Decision |
|---|---|
| COMPLETE and `>=100.000` | Strong reproduction |
| COMPLETE and `>92.165` | New historical high |
| COMPLETE and `>88.760` | New leaderboard-effective floor |
| COMPLETE and `>=89.83` (snapshot 08:25) / `>=89.85` (this snapshot) | Bronze-cut chase |
| COMPLETE and `<=88.760` | Reject B018; keep B008R |
| ERROR / blank / unsafe | Reject B018 |

## Leaderboard (2026-08-24 13:10:35 UTC)

Artifact: `artifacts/kaggle/leaderboards/2026-08-24_b018_resume/`

```text
rows=3960
heralces_rank=575
heralces_score=88.760
heralces_last_submission_date=2026-08-23 20:41:06
heralces_submission_count=12
bronze_10pct_rank=396
bronze_10pct_score=89.850
gap_to_bronze=1.090
score_at_1=138.250
score_at_100=97.055
score_at_200=92.085
score_at_300=90.765
rank_if_92.165=~195
rank_if_100.000=~74
```

Public board still displays B008R, not B017. B018 PENDING does not yet
change rank.

Team-merger deadline is `2026-08-25 23:59 UTC`. Combined-team submission
count must stay at or under the competition cap. This resume does not
merge or invite anyone.

## Public kernel screen (read-only)

`kernels_list` by `dateRun`, 40 rows:
`artifacts/kaggle/public_audit/2026-08-24_1310/kernels_list.csv`

New or previously unpulled refs versus the 2026-08-23 B017 screen:

```text
llkh0a/aas-local-validation
  last_run=2026-08-24 01:51:34 UTC
  votes=426
  kind=GGUF local validator (gpt-oss + Gemma T4)
  copies attack_pilkwang.py; no new AttackAlgorithm
  overlap=already used as the B017 n4n6 probe model source
  decision=not a B008R child; no B019

addonyas/adiya
  last_run=2026-08-21 18:36:53 UTC
  votes=3
  extracted_attack_sha256=3c2eebbdbe0291fee69e535898fb94547a0e2049d53e220018c0cdb64a499019
  techniques=snapshot/restore search, base64 encoding, mixed
    http.post / email.send / fs.delete
  URLs include https://attacker.com/collect (real TLD) plus example.com
  decision=rejected by docs/safety.md reserved-domain policy; also a
    multi-family route replacement, not a single-variable B008R child
```

Already-screened dateRun heads (verityix, mccocoful, lopure,
adhirajjagtap, antoniorotundo2, evgendvorkin, georgymamarin, dimong4)
were not re-pulled.

No public snapshot is a reserved-domain single-variable child of B008R
stronger than the in-flight FAST_USE_FRAME test.

## Decision

- Keep monitoring `55737814` only.
- Do not retry B018.
- Do not preregister, push, or submit B019 until B018 is terminal.
- Parent stays B008R unless B018 public score is `>88.760`.
