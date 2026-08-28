# B022 example.com host-suffix preregistration

## B021 terminal (gate)

```text
formal_submission_ref=55808416
status=SubmissionStatus.COMPLETE
public_score=73.700
parent_gate=B008R 88.760
decision=REJECT; do not retry
```

User authorized the reserved-domain host-suffix swap as the next submit.
This is not another fast-row wording change.

## Source lock

```text
candidate_id=B022-examplecom
candidate_path=baselines/replaysafe_examplecom_v1/attack.py
candidate_sha256=9472a06d2d77141359af0dff30d63b9b035b96d36a643325f74c758dd74ac4f7
candidate_size_bytes=11032
parent_id=B008R
parent_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
parent_public_score=88.760
single_variable=URL_HOST_SUFFIX
old_value=invalid
new_value=example.com
```

Single-variable change: generated destinations become
`http://{label}.example.com` instead of `http://{label}.invalid`.
Prompt templates, classify5, replay-safe 0.99, slow-row four-endpoint
forge, hops, and one-message candidates stay unchanged.

This is not B011/B018/B021 wording, not a B020 budget carve, not a tail
or width knob, and not a public `.co` copy. Hosts remain RFC-reserved
(`example.com`).

## Local gates

```text
ruff check/format: PASS
pytest tests/test_replaysafe_examplecom.py: 5 passed
pytest full: 202 passed in 90.65s
preflight: PASS sha256=9472a06d2d77141359af0dff30d63b9b035b96d36a643325f74c758dd74ac4f7 size=11032
SDK validate redteam: PASS
```

Fake-env slow-row (13s / 9000s) returns the same candidate count as
B008R; only the host suffix differs.

## Leaderboard snapshot (2026-08-28 02:27 UTC)

```text
rows=4148
heralces_rank=658
heralces_score=88.760
bronze_10pct_rank=414
bronze_10pct_score=90.270
gap_to_bronze=1.510
nctuan_rank=375
nctuan_score=90.630
```

## Acceptance gates

| B022 terminal | Decision |
|---|---|
| COMPLETE and `>=100.000` | Strong reproduction |
| COMPLETE and `>92.165` | New historical high |
| COMPLETE and `>88.760` | New leaderboard-effective floor |
| COMPLETE and `>=90.270` | Bronze-cut chase on the 2026-08-28 snapshot |
| COMPLETE and `<=88.760` | Reject B022; keep B008R |
| ERROR / blank / unsafe | Reject B022 |

Do not retry B022. Keep the already-selected private pair B008R
`55393959` + B012 `55495429` unless B022 public score is `>88.760`.
