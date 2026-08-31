# B024 probe1 preregistration

Public screen 2026-08-31 12:53 UTC: evgendvorkin PHOENIX V93 live-fills
with `PROBE_HOPS=1` while replay stays at the grader cap. B009 tested
hops=4 and returned Kaggle system ERROR; hops=1 was never scored.

## Source lock

```text
candidate_id=B024-probe1
candidate_path=baselines/replaysafe_probe1_v1/attack.py
candidate_sha256=1ff5343a3c900cd5869ea28262b8d227054457aa5eb48ae2baa6865b1bc7a846
candidate_size_bytes=10785
parent_id=B008R
parent_public_score=88.760
single_variable=PROBE_HOPS
old_value=0 (configured hops, 8)
new_value=1
```

Messages, classify5, forge4, tail 0.99, and `http://{label}.invalid`
unchanged. Not a `.co` copy, not N=8, not all-forge.

## Local gates

```text
ruff check/format: PASS
pytest tests/test_replaysafe_probe1.py: 4 passed
pytest full: 215 passed in 97.74s
preflight: PASS sha256=1ff5343a3c900cd5869ea28262b8d227054457aa5eb48ae2baa6865b1bc7a846 size=10785
SDK validate redteam: PASS
```

## Acceptance gates

| B024 terminal | Decision |
|---|---|
| COMPLETE and `>88.760` | New floor |
| COMPLETE and `>=90.855` | Bronze-cut chase on the 2026-08-31 12:53 snapshot |
| COMPLETE and `<=88.760` | Reject; keep B008R |
| ERROR / blank / unsafe | Reject (B009-style ERROR is reject, no retry) |

Do not retry B024. Private pair stays B008R + B012 unless public `>88.760`.

## Formal submission record

```text
formal_submission_ref=55916092
formal_submission_created_utc=2026-08-31 13:07:21.883
status=SubmissionStatus.PENDING
kernel_id=heralces/ai-agent-security-b024-probe1
kernel_version=1
kernelId=132669683
cloud_attack_sha256=1ff5343a3c900cd5869ea28262b8d227054457aa5eb48ae2baa6865b1bc7a846
cloud_hash_matches_local=true
submission_message=B024-probe1 | attack 1ff5343a | prereg 3dbefb3 | SDK 3.1.2
git_commit=3dbefb342f51888a0d73fdc08046ea93a23837a3
scriptVersionId=346284281
```
