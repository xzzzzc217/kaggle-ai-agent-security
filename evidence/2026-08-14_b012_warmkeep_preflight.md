# B012 replay-safe warmkeep preregistration

This is a formal B012 preregistration. It authorizes at most one B012 Kaggle
Notebook version and at most one B012 competition submission after this document
is committed and pushed.

## Current comparison state

```text
current_effective_baseline=B008R
current_effective_submission_ref=55393959
current_effective_public_score=88.760
current_effective_private_score=
historical_high_baseline=B008
historical_high_submission_ref=55266445
historical_high_public_score=92.165
historical_high_current_status=score-bearing SubmissionStatus.ERROR
strong_competition_reference=100.000
```

Latest checked public leaderboard:

```text
leaderboard_checked_utc=2026-08-14 01:47
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-14_0145_b012_resume_v3/ai-agent-security-multi-step-tool-attacks.zip
team=heralces
team_score=88.760
team_rank=277
score_at_200=89.550
rank_if_92_165=97
```

## Source lock

```text
candidate_id=B012
candidate_name=replaysafe_warmkeep_v1
candidate_path=baselines/replaysafe_warmkeep_v1/attack.py
candidate_sha256=68cea78ffdc1c255655a78884c70640737b6390b3ab6baed957d0c73e7f70e6c
candidate_source_commit=f84bbfd3fc8fff0d68daa1b6c093a7a1eb938fcd

parent_id=B008/B008R
parent_path=baselines/replaysafe_classify5_v1/attack.py
parent_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
```

## Single behavior variable

B012 keeps B008R's prompt templates, latency routing, classification batch,
replay-safe sizing, slow-row four-endpoint frame plan, hop policy, replay-cost
coefficients, and reserved `.invalid` URL policy.

The only behavior change is:

```text
B008R behavior: live warmup is used only for timing/model stabilization and is never returned.
B012 behavior: if the live warmup already fires a marker-bearing http.post, return that exact warmup message as the first replay-safe candidate.
```

This is not a prompt-token/template-bank route and does not modify:

```text
SPLIT_CLASSIFY_N=5
SPLIT_THRESHOLD_S=12.0
REPLAY_SAFE_FRAC=0.99
SLOW_MULTIPOST_N=4
BURST_K=1
PROBE_HOPS=0
REPLAY_COST_COEF=1.0
REPLAY_BUDGET_MULT=1.0
TEMPLATE=B008R TEMPLATE
FRAME_TEMPLATE=B008R FRAME_TEMPLATE
```

Replay accounting note: B008R already subtracts warmup elapsed time from the
fresh replay cap. B012 does not add warmup elapsed again to `replay_cost`; this
keeps returned warmup plus subsequent candidates inside the same replay cap
instead of double-charging the warmup.

## Hypothesis

If the warmup trace fires in hidden rerun, B012 recovers one already-validated
marker-bearing `http.post` candidate per model without spending another live
interaction or changing later fill behavior. The expected effect is small but
mechanistically clean and low-correlated with the rejected B006/B007/B009/B010/
B011 routes.

This candidate is only worth one formal submission because current public
leaderboard auto-selection has preserved B008R `88.760` despite lower later
submissions, and because no stronger B012 candidate emerged from the 2026-08-12
or 2026-08-14 public audits.

## Local dynamic contract

Deterministic fake-env samples compare B008R and B012 under identical latency,
budget, hop, and always-firing traces:

```text
latency=5s  B008_returned=92 B012_returned=93 delta=1 warmup_kept=1 forge4=0  urls=93  hops=[8]
latency=9s  B008_returned=51 B012_returned=52 delta=1 warmup_kept=1 forge4=0  urls=52  hops=[8]
latency=13s B008_returned=35 B012_returned=36 delta=1 warmup_kept=1 forge4=30 urls=126 hops=[8]
latency=20s B008_returned=23 B012_returned=24 delta=1 warmup_kept=1 forge4=18 urls=78  hops=[8]
```

The samples show:

- B012 returns exactly one additional candidate when warmup fires;
- `.invalid` URLs are preserved;
- hop cap remains `[8]`;
- fast rows remain plain single-post after classification;
- slow rows keep B008R's four-endpoint frame plan.

## Validation already completed before preregistration

```text
preflight_submission.py PASS
SDK validate redteam PASS
pytest tests/test_replaysafe_warmkeep.py -q: 3 passed
pytest -q: 111 passed
ruff check: PASS
ruff format --check: PASS
git diff --check: PASS
candidate-file credential-shape scan: 0 matches
```

SDK validate required `PYTHONPATH=data/competition/extracted` in the local
Windows shell because `aicomp_sdk` is stored under the extracted competition
data directory.

## Acceptance gates

| B012 terminal result | Decision |
|---|---|
| `COMPLETE` and Public Score `>92.165` | New historical high; keep B012 as strongest observed candidate |
| `COMPLETE` and `88.760 < Public Score <= 92.165` | Improves current leaderboard-effective score, but does not refresh historical high |
| `COMPLETE` and Public Score `>=100.000` | Strong competition reproduction marker; also satisfies the two improvement gates |
| `COMPLETE` and Public Score `<=88.760` | Reject B012 |
| `ERROR`, failure, blank score, timeout, duplicate route, or unsafe artifact | Reject B012 |

Do not retry B012, do not repush the same Notebook, and do not create B013 while
the B012 competition submission is unknown.

## Planned Kaggle artifact

```text
kernel_id=heralces/ai-agent-security-b012-warmkeep
title=AI Agent Security B012 Warmkeep
experiment_id=B012
submission_dir=submissions/B012
submission_message_template=B012 warmkeep | attack 68cea78f | prereg {short_prereg_commit} | SDK 3.1.2
```

Before any Kaggle write operation after this preregistration, recheck:

1. git status is clean except the intended committed preregistration state;
2. no previous B012 submission or attack hash prefix exists in Kaggle submissions;
3. `submission-manifest.json` binds the preregistration commit;
4. generated Notebook uses only safe `.invalid` URLs and no credentials;
5. cloud output `attack.py` SHA matches
   `68cea78ffdc1c255655a78884c70640737b6390b3ab6baed957d0c73e7f70e6c`;
6. Notebook logs have zero operational errors except known benign warnings;
7. cloud artifacts have zero credential-shape matches.
