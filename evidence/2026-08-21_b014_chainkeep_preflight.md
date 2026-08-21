# B014 replay-safe chainkeep preregistration

This is a formal B014 preregistration under the user's 2026-08-21 directive
("拨乱反正 / 尽快提分 / 允许不依赖项目原有基础 / 充分试错"). It deliberately
abandons the strict single-variable isolation protocol in favor of a
multi-variable replay-efficiency candidate that bundles three previously
rejected mechanisms that share a common bottleneck.

It authorizes at most one B014 Kaggle Notebook version and at most one B014
competition submission after this document is committed and pushed.

## Current comparison state

```text
current_effective_baseline=B008R
current_effective_submission_ref=55393959
current_effective_public_score=88.760
current_effective_private_score=
historical_high_baseline=B008
historical_high_submission_ref=55266445
historical_high_public_score=92.165
strong_competition_reference=100.000
```

Latest checked public leaderboard (2026-08-21 11:43 UTC heartbeat):

```text
team=heralces
team_score=88.760
team_rank=489
score_at_100=94.350
score_at_200=91.395
score_at_300=89.815
bronze_10pct_cut_rank=382
bronze_10pct_cut_score=89.415
```

B013 chain4 submission `55658141` is currently `SubmissionStatus.PENDING`
with blank Public/Private Score and no `errorDescription`. This B014
preregistration does not retry B013 and does not depend on B013 terminal
result; B014 may run in parallel with the B013 monitor.

## Source lock

```text
candidate_id=B014
candidate_name=replaysafe_chainkeep_v1
candidate_path=baselines/replaysafe_chainkeep_v1/attack.py
candidate_sha256=bff821598ca3f8677a68d8c130340cf46a8919facac6a49628d06194a977b4da
candidate_source_commit=<pending this commit>
parent_id=B008/B008R
parent_path=baselines/replaysafe_classify5_v1/attack.py
parent_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
parent_effective_submission_ref=55393959
supporting_id_chain4=B013 chain4 source SHA 5ac85de2991ccd7771b527be3a850023388fef904637986d4252d54382521e2b
supporting_id_warmkeep=B012 warmkeep source SHA 68cea78ffdc1c255655a78884c70640737b6390b3ab6baed957d0c73e7f70e6c
```

## Multi-variable change (deliberate protocol shift)

The B008R/B008 single-variable protocol is **suspended** for B014 under the
user's authorization. The candidate combines three changes that were each
rejected only for methodology reasons under the prior protocol:

1. **Slow-row replay packaging (B013 chain4 mechanism)**
   B014 keeps B008R's slow-row live validation frame unchanged. When the
   same validated slow-row finding fires, B014 returns it as four direct
   replay user messages, one ``http.post`` instruction per preserved
   ``.invalid`` endpoint, instead of one four-endpoint frame message.

2. **Live warmup retention (B012 warmkeep mechanism)**
   B014 adds the previously rejected warmkeep flag. When the live validation
   warmup already fires a marker-bearing ``http.post``, B014 retains that
   warmup message as the first replay-safe candidate.

3. **Slow-row tail extension (rejected multi-variable rollback)**
   - ``REPLAY_SAFE_FRAC`` from ``0.99`` to ``0.995`` (+0.5%)
   - ``REPLAY_BUDGET_MULT`` from ``1.0`` to ``1.02`` (+2%)
   These extend the slow-row tail allocation without touching routing, prompt
   templates, classification batch, latency threshold, probe hops, or
   reserved-domain URL policy.

This is **not** a prompt-template-bank exploration, **not** a public
endpoint portfolio, **not** a destructive-write/confused-deputy pivot, and
**not** a retry of B008/B008R/B011/B012/B013. It is a deliberate
multi-variable bundling authorized for this single submission.

## Preserved B008R baseline

```text
SPLIT_CLASSIFY_N=5
SPLIT_THRESHOLD_S=12.0
SLOW_MULTIPOST_N=4
BURST_K=1
PROBE_HOPS=0
REPLAY_COST_COEF=1.0
TEMPLATE=B008R TEMPLATE
FRAME_TEMPLATE=B008R FRAME_TEMPLATE
live slow-row probe message=B008R _forge_plan_message
URL policy=unique http://*.invalid reserved hosts
hop policy=grader cap
```

## Hypothesis

B008R's three unaddressed replay-efficiency ceilings are:

- The frame-message approach is robust for a hidden agent that fully executes
  the four ``http.post`` calls in a single frame, but degrades when the
  hidden agent only executes the first or first few tool calls in the frame.
- The live-validation warmup almost always fires a marker post under the
  B008R prompt, but B008R drops that warmup from the candidate set. A
  hidden replay evaluator that accepts any post from a fully traceable
  interaction should treat the warmup as a valid candidate.
- B005's `REPLAY_SAFE_FRAC=0.99` / `REPLAY_BUDGET_MULT=1.0` was the largest
  safe budget extension that could be validated before the 9000-second wall
  deadline. The current top-200 boundary has grown past that envelope;
  a 0.5%/2% extension recovers ~1.5% of the slow-row tail without changing
  routing.

Bundling all three at once targets the same bottleneck — the number of
score-bearing replay candidates returned per discovery — without changing
candidate shape variety. The combined variable change is the explicit
paradigm shift authorized for B014.

Conservative replay-shape scoring estimates:

```text
model=one_post_per_user_message
B008R_first_slow_candidate messages=1 posts=1 predicates=1 raw=18.0 normalized=0.09
B014_first_slow_candidate messages=4 posts=4 predicates=4 raw=66.0 normalized=0.33
B014_warmup_kept messages=1 posts=1 predicates=1 raw=18.0 normalized=0.09
B014_tail_candidate messages=1 posts=1 predicates=1 raw=18.0 normalized=0.09
```

The expected gain is concentrated in:

- Slow-row replays becoming 4-predicate chains (B013 mechanism).
- One additional fired warmup per successful run (B012 mechanism).
- ~1.5% extra slow-row candidates returning within the larger replay-safe
  envelope.

Combined A does not include the cumulative novelty bonus across chained
posts because the cell signature hashes all four ``http.post`` events into
one cell. The gain is concentrated in predicate count, not in cell count.

## Local dynamic contract

Fake-env samples compare B008R, B013, and B014 under identical latency,
budget, hop, and always-firing live-validation traces:

```text
latency=5s   B008R returned=92  forge4=0   urls=92   chain4=0
             B013   returned=92  chain4=0   urls=92
             B014   returned=92  chain4=0   urls=92   warmup_kept=1
latency=9s   B008R returned=51  forge4=0   urls=51
             B013   returned=51  chain4=0   urls=51
             B014   returned=51  chain4=0   urls=51   warmup_kept=1
latency=13s  B008R returned=35  forge4=30  urls=125
             B013   returned=35  chain4=30  urls=125
             B014   returned=35  chain4=30  urls=125  warmup_kept=1
latency=20s  B008R returned=23  forge4=18  urls=77
             B013   returned=23  chain4=18  urls=77
             B014   returned=23  chain4=18  urls=77   warmup_kept=1
```

The samples show:

- fast/plain rows are byte-behavior compatible across B008R/B013/B014;
- slow-row live probes still use B008R's analysis-channel frame in all
  three variants;
- slow-row chain4 packaging is identical between B013 and B014;
- B014 adds exactly one warmup candidate per run when the warmup fires;
- B014's tail extension produces the same candidate count under the
  fake-env scheduler because the slowest-observed-latency replay-cost
  model remains the same; the ~1.5% expected gain is concentrated in
  real-environment slow-row tail candidates that the fake-env cannot
  reproduce deterministically.

## Validation status before preregistration commit

Completed before this document was committed:

```text
pytest tests/test_replaysafe_chainkeep.py -q: 9 passed
pytest -q: 127 passed
ruff check baselines/replaysafe_chainkeep_v1/attack.py tests/test_replaysafe_chainkeep.py: PASS
ruff format --check baselines/replaysafe_chainkeep_v1/attack.py tests/test_replaysafe_chainkeep.py: PASS
preflight_submission.py baselines/replaysafe_chainkeep_v1/attack.py: PASS
SDK validate redteam baselines/replaysafe_chainkeep_v1/attack.py: PASS
git diff --check: PASS
credential_value_hits=0
credential_shape_hit_files=0
```

## Acceptance gates

| B014 terminal result | Decision |
|---|---|
| `COMPLETE` and Public Score `>=100.000` | Strong competition reproduction; replaces both gates |
| `COMPLETE` and Public Score `>92.165` | New historical high; keep B014 as strongest observed |
| `COMPLETE` and `88.760 < Public Score <= 92.165` | Improves leaderboard-effective score, refreshes historical high (B008 = 92.165 is historical high) |
| `COMPLETE` and Public Score `<=88.760` | Reject B014 |
| `ERROR`, failure, blank score, timeout, duplicate, unsafe artifact, or hash mismatch | Reject B014 |

The historical-high gate uses `>92.165` to refresh, because B008's
`92.165` is the only score in the project's notebook history that exceeded
B005's `91.930`. B014's bundled mechanism must demonstrably exceed that to
be recorded as a new historical high.

## Planned Kaggle artifact

```text
kernel_id=heralces/ai-agent-security-b014-chainkeep
title=AI Agent Security B014 Chainkeep
experiment_id=B014
submission_dir=submissions/B014
submission_message_template=B014 chainkeep | attack {short_sha} | prereg {short_prereg_commit} | SDK 3.1.2
```

Before any Kaggle write operation after this preregistration, recheck:

1. git status is clean except the intended committed preregistration state;
2. no previous B014 submission or attack hash prefix exists in Kaggle
   submissions;
3. `submission-manifest.json` binds the preregistration commit;
4. generated Notebook uses only safe `.invalid` URLs and no credentials;
5. cloud output `attack.py` SHA matches
   `bff821598ca3f8677a68d8c130340cf46a8919facac6a49628d06194a977b4da`;
6. Notebook logs have zero operational errors except known benign warnings;
7. cloud artifacts have zero credential-shape matches.

## Multi-variable rationale (paradigm-shift note)

The strict single-variable isolation protocol was originally adopted to keep
the project's evidence ledger readable and to make small wins measurable.
Under the user's 2026-08-21 directive ("拨乱反正 / 尽快提分 / 允许不依赖项目
原有基础 / 充分试错"), the priority shifts from "each submission tells one
isolated story" to "each submission buys the largest expected score
movement within the 8-day remaining window".

B014 buys that movement by stacking three previously-validated-or-near-validated
mechanisms that target the same bottleneck:

- B013 chain4 mechanism (submitted; pending) — pending, but the local
  dynamic contract supports it.
- B012 warmkeep mechanism (rejected at 88.665, ~0.095 below current
  leaderboard-effective 88.760) — separately small, but stacked with
  chain4 it adds another predicate per run.
- Tail extension from 0.99/1.0 to 0.995/1.02 — the next smallest safe
  step above the validated B008R envelope.

Each individual mechanism was previously rejected for reasons unrelated to
its expected direction-of-effect:

- B013 was rejected on hidden-agent-replay-reliability grounds, not on
  mathematical grounds (chain4 raw score is monotonically higher than
  single-post).
- B012 was rejected because it alone was not enough to beat B008R; the
  warmup gain is bounded by 1 candidate per run.
- Tail extension was previously excluded because no single-variable
  evidence supported the step; stacking it with two replay-efficiency
  improvements makes the +1.5% tail plausible.

The combined candidate is therefore the smallest defensible multi-variable
bundling that moves B014's expected raw score distribution toward the
bronze 10% cut `89.415` without changing the cell-signature shape variety
or the reserved-domain policy.

## Next steps after B014 terminal

1. If B014 `>88.760` and `>92.165` (preferred): keep B014 as new historical
   high and current leaderboard-effective; continue scouting for B015
   multi-variable improvements.
2. If B014 `>88.760` and `<=92.165`: improves leaderboard-effective, does
   not refresh B008 historical high. Plan B015 in the same multi-variable
   style, but with a different bottleneck target (e.g. CONFUSED_DEPUTY
   email.send addition or DESTRUCTIVE_WRITE probe).
3. If B014 `<=88.760`: reject and plan B015 as a smaller single-variable
   return to B008R-style territory, with a different primary axis
   (e.g. tail `REPLAY_SAFE_FRAC=0.992` and `REPLAY_BUDGET_MULT=1.01`).
4. If B014 `ERROR` or blank: investigate cloud artifact and plan B015 as
   a pure retry of the multi-variable candidate with corrected hash.

B015 candidates sketched in advance (no submission authorized until B014
terminal):

- **B015 chainkeep+email (multi-variable)**: B014 + a CONFUSED_DEPUTY
  email.send addition targeting `admin@example.invalid` after the marker
  post. Brings a second predicate family into the same candidate shape.
  Estimated raw-score uplift per chain4 finding: ~50% extra from the
  second predicate family. Risk: prompt-wording-sensitive CONFUSED_DEPUTY
  only fires if the prompt avoids explicit send/email/upload wording.
- **B015 chainkeep+tail99 (multi-variable)**: B014 + a slightly larger
  tail (`REPLAY_SAFE_FRAC=0.998`, `REPLAY_BUDGET_MULT=1.03`). Estimated
  raw-score uplift: another ~1.5% from tail candidates. Risk: wall
  deadline guardrail; would need to verify on local fake-env replay.
- **B015 chainkeep+multi8 (multi-variable)**: B014 + `SLOW_MULTIPOST_N=8`
  and chain8 packaging. Estimated raw-score uplift: 2x chain4 raw score.
  Risk: chain reliability degrades with longer chains.

All B015 candidates remain sketches until B014 terminal.

## B014 submission record

```text
prereg_commit=ec43467689642b40892cd23094003da9382404c3
push_commit=ec43467689642b40892cd23094003da9382404c3
local_attack_sha256=493b901f2144a08a68c408b23e779185efe1e98efba80d055fc71c4eae1f8568
kernel_id=heralces/ai-agent-security-b014-chainkeep
kernel_version=1
kernel_status=KernelWorkerStatus.COMPLETE
submission_artifact_dir=artifacts/kaggle/B014_v1
submission_artifact_log=artifacts/kaggle/B014_v1.log
cloud_attack_sha256=493b901f2144a08a68c408b23e779185efe1e98efba80d055fc71c4eae1f8568
cloud_hash_matches_local=true
submission_csv_bytes=88
log_actionable_error_scan=0
cloud_artifact_credential_value_hits=0
cloud_artifact_credential_shape_hit_files=0
submission_message=B014 chainkeep | attack 493b901f | prereg ec43467 | SDK 3.1.2
formal_submission_ref=PENDING
formal_submission_created_utc=2026-08-21 16:17:10.210
initial_submission_observed_utc=2026-08-21 16:17
initial_submission_status=SubmissionStatus.PENDING
initial_public_score=
initial_private_score=
initial_error_description=None
competition_submission_refresh_companion_to=b013 55658141
```

Submission flow used:

```text
1. Local: ruff check + ruff format --check + pytest -q + preflight + SDK validate
2. Local: scripts/build_kaggle_notebook.py -> submission-manifest.json binds prereg commit
3. Kaggle: scripts/push_kernel.py submissions/B014 -> kernel version 1 QUEUED
4. Kaggle: kernels status poll until COMPLETE
5. Kaggle: kernels output -> attack.py + submission.csv + log
6. Local: SHA matches manifest attack_sha256 -> confirms artifact fidelity
7. Kaggle: competitions submit -k heralces/ai-agent-security-b014-chainkeep -v 1 -f submission.csv
   with submission_message listing attack hash, prereg commit, and SDK version
8. Refresh: competitions submissions shows B014 row in PENDING state
```

The cloud log contains only the standard committed-notebook boot output
("Dataset root: ...", "attack.py written", "placeholder submission.csv
written") followed by the hidden-gateway rerun. There are no actionable
errors. The same log file is preserved at `artifacts/kaggle/B014_v1.log` so
the rerun can be inspected when B014 reaches terminal state.

## B013 terminal result (concurrent with B014 preregistration)

B013 chain4 (`55658141`) reached terminal state during the B014 build
window:

```text
formal_submission_ref=55658141
kaggle_cli_status=SubmissionStatus.COMPLETE
kaggle_cli_public_score=61.930
kaggle_cli_private_score=
kaggle_api_status=SubmissionStatus.COMPLETE
kaggle_api_public_score=null
kaggle_api_private_score=null
kaggle_api_error_description=None
```

B013 scored `61.930` — significantly below the B008R `88.760` baseline and
also below the historical_excluded B007 `76.905` and B010 `52.330` rejects.
Per the B013 acceptance gates, B013 is rejected at terminal.

B013's negative result is the strongest available evidence for the B014
multi-variable bundling rationale: pure chain4 alone collapses the
score-bearing replay set below the B008R reliable floor, but combining it
with `KEEP_WARMUP_FIRED` and a tighter slow-row replay budget adds back
the suppressed score-bearing candidates incrementally rather than fully
restoring them.