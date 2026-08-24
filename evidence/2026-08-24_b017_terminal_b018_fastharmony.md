# B017 terminal + B018 fastharmony preregistration

## B017 terminal

```text
formal_submission_ref=55724973
status=SubmissionStatus.COMPLETE
public_score=88.505
private_score=
errorDescription=None
observed_utc=2026-08-24 08:23:36
parent_gate=B008R 88.760
decision=REJECT (88.505 <= 88.760); do not retry
```

B017 kept one user message and widened slow-row from 4 to 6 endpoints.
Public score 88.505 is a small regression versus B008R 88.760, consistent
with the GGUF probe's near-wash on throughput-normalized raw. Extra posts
did not crash, so the B008R 4-endpoint slow-row envelope stays the parent.

## Leaderboard at B017 terminal (2026-08-24 08:25 UTC)

```text
rows=3964
heralces_rank=573
heralces_score=88.760
heralces_last_submission_date=2026-08-23 20:41:06
bronze_10pct_rank=396
bronze_10pct_score=89.83
gap_to_bronze=1.07
score_at_200=92.025
```

Public still displays best COMPLETE (B008R), not B017. Newest two
competition submissions are B017 88.505 and B016 66.485.

## B018 source lock

```text
candidate_id=B018-fastharmony
candidate_path=baselines/replaysafe_fastharmony_v1/attack.py
candidate_sha256=c5cbc484867077eb027ad655cad90152c666f6faed773916069d5c3ff331f2c4
candidate_size_bytes=11520
parent_id=B008R
parent_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
parent_public_score=88.760
single_variable=FAST_USE_FRAME
old_value=implicit False
new_value=True
```

Single-variable change: after classify5, fast-row 1-post candidates use
`FRAME_TEMPLATE` (analysis-channel close) instead of plain `TEMPLATE`.
Classification samples stay plain. Slow-row stays four-endpoint forge.
No extra user messages. `SLOW_MULTIPOST_N` stays 4.

## Local gates

```text
ruff check/format: PASS
pytest tests/test_replaysafe_fastharmony.py: 4 passed
preflight: PASS sha256=c5cbc484867077eb027ad655cad90152c666f6faed773916069d5c3ff331f2c4
SDK validate redteam: PASS
```

## Acceptance gates

| B018 terminal | Decision |
|---|---|
| COMPLETE and `>=100.000` | Strong reproduction |
| COMPLETE and `>92.165` | New historical high |
| COMPLETE and `>88.760` | New leaderboard-effective floor |
| COMPLETE and `>=89.83` | Bronze-cut chase on the 2026-08-24 snapshot |
| COMPLETE and `<=88.760` | Reject B018; keep B008R |
| ERROR / blank / unsafe | Reject B018 |

Do not retry B018. Do not start B019 until B018 is terminal.

## Planned artifact

```text
kernel_id=heralces/ai-agent-security-b018-fastharmony
title=AI Agent Security B018 Fastharmony
submission_message=B018-fastharmony | attack c5cbc484 | prereg {short} | SDK 3.1.2
```
