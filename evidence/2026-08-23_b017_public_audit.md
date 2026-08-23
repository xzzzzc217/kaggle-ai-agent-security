# B017 public-route audit and candidate screen

This is a read-only B017 scouting record plus the local mechanism screen
that selected `SLOW_MULTIPOST_N: 4 -> 6`. It does **not** authorize a
Kaggle Notebook push or competition submission. B016-destructive
`55708612` is still `PENDING`; B017 stays pre-staged until that
submission is terminal.

## Current Kaggle state (2026-08-23 08:35 UTC)

```text
leaderboard_rows=3922
heralces_rank=541
heralces_score=88.760
heralces_last_submission_date=2026-08-22 16:33:52
heralces_submission_count=10
score_at_1=138.250
score_at_10=116.620
score_at_50=101.500
score_at_100=95.805
score_at_200=91.710
score_at_300=90.495
approx_bronze_10pct_rank=392
approx_bronze_10pct_score=89.625
gap_to_bronze=0.865
rank_if_92.165=181
rank_if_100.000=62
current_effective_baseline=B008R
current_effective_submission_ref=55393959
current_effective_public_score=88.760
historical_high_baseline=B008
historical_high_submission_ref=55266445
historical_high_public_score_original=92.165
historical_high_public_score_now_cli=88.070
```

Public leaderboard still shows B008R `88.760` even though later
submissions scored lower. Latest B015-C-modified `55695369` is
`COMPLETE` at `58.610`. B016-destructive `55708612` is `PENDING` with
blank score.

## Why the second-predicate piggybacks are rejected as the next axis

| experiment | shape | public |
|---|---|---|
| B008R | 1 user message, EXFIL only | 88.760 |
| B011 | 1 user message, inline email | 72.680 |
| B013 | 4 user messages, chain4 | 61.930 |
| B014 | 4 user messages + warmkeep + tail | 45.790 |
| B015-C-modified | 2 user messages, email follow-up | 58.610 |
| B016-destructive | 2 user messages, delete follow-up | PENDING |

B015-C-modified is the cleanest negative: it restored the B008R envelope
and added only a second user message. Public score fell from 88.760 to
58.610, about a one-third loss of EXFIL cells. B016 is the same 2-message
shape on a different tool, so it is **not** the planned B017 parent.

Inlining a second predicate (B011) also lost cells. Extra user messages
and extra instructions on the same candidate both tax replay more than
they add severity.

## Public artifacts pulled (2026-08-23 16:36 local)

Pulled into `artifacts/kaggle/public_audit/2026-08-23_1636/`:

```text
lopure/jed-multi-step-attack-relay-push100
  decoded_attack_sha256=ee75e4cca064d865bc50dfd191cb6d1baa4353330e2c3110f64f970a587985f2
  URL_TLD=.co  (not adaptable under the reserved-domain policy)
  techniques=harmony inj_close, per-model fire-rate selector, replay-safe 0.99
  overlap=B008R already uses analysis-channel close on the slow row
  claimed_aim~100; public ancestor v24 claimed 87.9, v26 replay-safe 67

mccocoful/local-cpu-submission-for-hengck23
  30 blind COT-hijack candidates to http://{id}.co/cc
  no live validate-fill; not a throughput competitor for 88.760

antoniorotundo2/a-throughput-floor-plus-a-genuine-multi-step-searc
  notebook has no code cells in the pulled snapshot; no AttackAlgorithm

verityix/ai-agent-security-attack-algorithm-hitherto
  4 styles x 10 real-TLD URL patterns; not reserved-domain safe

evgendvorkin/ai-agent
  local GGUF private-eval notes; candidate sketches for deputy / dest /
  untrusted-to-action are separate single-message probes, not a fill
  algorithm. Useful as wording evidence, not as a drop-in attack.py.

georgymamarin/red-team-starter-what-fires-and-what-it-s-worth
  educational one-finding demo; not a competitor
```

No public snapshot is a clean single-variable child of B008R that both
(1) stays on `*.invalid` and (2) has a larger expected lift than
widening the already-validated slow-row frame.

## Local mechanism screen

Rejected for B017:

- **Another 2-message follow-up** (email, delete, or both): B015-C already
  falsified the shape.
- **Inline second-predicate template** (B011 family): already falsified
  at 72.680.
- **Independent second-family candidates paid for by cutting EXFIL
  budget**: replacing an EXFIL finding (weight 16 + 2) with CONFUSED_DEPUTY
  (weight 4 + 2) or DESTRUCTIVE_WRITE (weight 8 + 2) is a net raw-score
  loss unless the extra family is free leftover budget, which the 0.99
  replay cap does not leave.
- **Real TLD / `.co` URL policy**: forbidden by `docs/safety.md`.
- **Template bank / per-model fire-rate selector**: multi-variable rewrite
  of the B008R split; overlaps B001/B010/lopure.
- **PROBE_HOPS 8 -> 4**: already B009, terminal `ERROR`, no retry.
- **REPLAY_SAFE_FRAC 0.99 -> 0.995**: previously predicted as
  `+0.05-0.10` public points, not enough for a 0.865 bronze gap, and
  B014 already mixed this axis into a collapse.

Selected:

- **B017 `SLOW_MULTIPOST_N: 4 -> 6`**, still one user message.
  B004's `1 -> 4` inside one message is the only unused widening of a
  *winning* axis. Evaluator hops remain 8, so six sequential posts still
  fit. Fast-row shape is unchanged. Predicted effect: each slow-row
  finding that completes the extra posts adds two more severity-5
  EXFILTRATION events (weight 16 each) without adding user messages.

## Decision

B017 is selected as a formal single-variable candidate and pre-staged
only. No Kaggle write in this cycle.

Submission remains gated on B016-destructive `55708612` reaching
COMPLETE / ERROR / FAILED, plus the post-B016 decision tree in
`evidence/2026-08-23_b017_slowmultipost6_preflight.md`.
