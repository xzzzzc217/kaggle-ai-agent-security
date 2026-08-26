# B020 disjoint-uta preregistration

## B019 terminal (gate)

```text
formal_submission_ref=55772221
status=SubmissionStatus.COMPLETE
public_score=87.470
parent_gate=B008R 88.760
decision=REJECT; do not retry
```

User confirmed private-selection of B008R `55393959` and B012 `55495429`,
then authorized the disjoint untrusted-source family as the next submit.

## Source lock

```text
candidate_id=B020-disjoint-uta
candidate_path=baselines/replaysafe_disjoint_uta_v1/attack.py
candidate_sha256=6d8b4be018caf33cfb8a56d7ade89681aa5ea08c744c4ee7c480ede113a03512
candidate_size_bytes=16716
parent_id=B008R
parent_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
parent_public_score=88.760
single_variable=DISJOINT_FAMILY
old_value=implicit False
new_value=True (DISJOINT_REPLAY_FRAC=0.05)
```

Single-variable change: after the unchanged B008R EXFIL live-validate
fill, spend a reserved 0.05 slice of the existing 0.99 replay-safe cap
on one-message candidates that open untrusted web/inbox fixture content.
EXFIL `user_messages` stay the B008R plain template / four-endpoint
forge. Disjoint messages do not mention `http.post`, do not contain
`send` / `email` / `upload` / `save` / `write`, and are not follow-ups
on EXFIL candidates.

This is not B015-C/B016 piggyback and not a tail/width/prompt-shape
knob. Reserved destinations stay `*.invalid`.

## Local gates

```text
ruff check/format: PASS
pytest tests/test_replaysafe_disjoint_uta.py: 7 passed
pytest full: 181 passed in 88.86s
preflight: PASS sha256=6d8b4be018caf33cfb8a56d7ade89681aa5ea08c744c4ee7c480ede113a03512 size=16716
SDK validate redteam: PASS
9000s fake 13s slow-row: B008R returned=682; B020 EXFIL returned=648 disjoint_kept=0
```

The fake FiringEnv has no web/email tools, so the disjoint loop keeps
nothing and only the 0.05 carve is visible. DualEnv tests keep disjoint
candidates when untrusted tools then a marker post fire.

## Acceptance gates

| B020 terminal | Decision |
|---|---|
| COMPLETE and `>=100.000` | Strong reproduction |
| COMPLETE and `>92.165` | New historical high |
| COMPLETE and `>88.760` | New leaderboard-effective floor |
| COMPLETE and `>=89.910` | Bronze-cut chase on the 2026-08-26 snapshot |
| COMPLETE and `<=88.760` | Reject B020; keep B008R |
| ERROR / blank / unsafe | Reject B020 |

Do not retry B020. Do not start B021 until B020 is terminal.
Keep the already-selected private pair B008R + B012 unless B020 public
score is `>88.760`.

## Formal submission record

Submitted once after B019 `55772221` COMPLETE publicScore 87.470.
Cloud `attack.py` hash matched local. Competition submit used kernel
output basename `submission.csv`. Do not submit B020 again.

```text
formal_submission_ref=55784609
formal_submission_created_utc=2026-08-26 03:36:58.993
initial_submission_status=SubmissionStatus.PENDING
initial_public_score=
initial_error_description=None
kernel_id=heralces/ai-agent-security-b020-disjoint-uta
kernel_version=1
kernelId=132018645
kernel_status=KernelWorkerStatus.COMPLETE
local_attack_sha256=6d8b4be018caf33cfb8a56d7ade89681aa5ea08c744c4ee7c480ede113a03512
cloud_artifact_dir=artifacts/kaggle/B020_v1
cloud_attack_sha256=6d8b4be018caf33cfb8a56d7ade89681aa5ea08c744c4ee7c480ede113a03512
cloud_hash_matches_local=true
submission_csv_bytes=88
submission_file=submission.csv
submission_message=B020-disjoint-uta | attack 6d8b4be0 | prereg f00c45d | SDK 3.1.2
git_commit=f00c45dd038c3df4f2b958108658f0875aa119a4
```

Do not start B021 until `55784609` is terminal.
