# B012 public-route audit and candidate screen

This is a read-only B012 scouting record. It does not preregister a formal
B012 candidate and does not authorize a Kaggle Notebook or competition
submission.

## Current leaderboard and submission state

```text
audit_time_utc=2026-08-12 13:11
competition=ai-agent-security-multi-step-tool-attacks
current_leaderboard_effective_submission=B008R 55393959
current_leaderboard_effective_public_score=88.760
historical_high_submission=B008 55266445
historical_high_public_score=92.165
latest_rejected_submission=B011 55433780
latest_rejected_public_score=72.680
latest_submission_cli_status=SubmissionStatus.COMPLETE
```

The latest Kaggle CLI submission list still shows B011 `55433780` as
`SubmissionStatus.COMPLETE` with Public Score `72.680`; B008R `55393959`
remains the strongest current score-bearing `COMPLETE` submission with Public
Score `88.760`. B008 `55266445` still carries raw Public Score `92.165` but is
currently `SubmissionStatus.ERROR`, so it is retained only as the historical
high and not as the leaderboard-effective score.

The public leaderboard snapshot downloaded during this audit contains `1258`
rows. The team row is:

```text
team=heralces
public_score=88.760
rank=250
last_submission_date=2026-08-11 13:22:50
submission_count=3
score_at_50=96.435
score_at_100=91.935
score_at_200=89.325
rank_if_88_760=249
rank_if_92_165=95
rank_if_72_680=875
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-12_1311_b012_resume/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=artifacts/kaggle/leaderboards/2026-08-12_1311_b012_resume/extracted_py/ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-12T13_12_23.csv
```

## Public notebooks pulled for this pass

The current public kernel listing was queried with score-descending ordering.
This pass pulled the newest or highest-signal notebooks not already covered by
B011's formal preflight, plus two already-known high-signal notebooks to verify
whether their current snapshots changed.

```text
adhirajjagtap/probe-and-flood-strategy
  notebook_sha256=27a6243457e2d0f14e0d8d1a9b996773d7f80c4683557d52096b62973029b6d1
  extracted_attack_sha256=ea319468f0115d2970dc4eb7e9a6d4ff7a745d6aa87c16c450fc8e9480c69620
  extracted_path=artifacts/kaggle/public_audit/2026-08-12/extracted_attack_py/adhirajjagtap_probe-and-flood-strategy.py

anasriaz/ai-agent-security
  notebook_sha256=9da7e7483e6591c53b3b0479b2ecfb4f2a9a543a6509eb122f5093ea9a87c650
  extracted_attack_sha256=bd99b0b0d0d5a600ce31d1070c7feadf575193d269ec72dae4fba21a736377a4
  extracted_path=artifacts/kaggle/public_audit/2026-08-12/extracted_attack_py/anasriaz_ai-agent-security.py

foysalemonshanto/ai-agent-security-v15
  notebook_sha256=f7f57088cff63d1d095a0f48e3499dfc0be18d09f45820b4163c2b39236e29f0
  extracted_attack_sha256=bd99b0b0d0d5a600ce31d1070c7feadf575193d269ec72dae4fba21a736377a4
  extracted_path=artifacts/kaggle/public_audit/2026-08-12/extracted_attack_py/foysalemonshanto_ai-agent-security-v15.py

nikitagajbhiye30/ai-security-0011
  notebook_sha256=1894c209de08791d36d68a2d0faca77c35d86c5d23e9e61f17bef3932998ccf7
  extracted_attack_sha256=bd99b0b0d0d5a600ce31d1070c7feadf575193d269ec72dae4fba21a736377a4
  extracted_path=artifacts/kaggle/public_audit/2026-08-12/extracted_attack_py/nikitagajbhiye30_ai-security-0011.py
```

## Mechanism screen

### Foysal / Anas / Nikita V15-family code

`anasriaz/ai-agent-security`, `foysalemonshanto/ai-agent-security-v15`, and
`nikitagajbhiye30/ai-security-0011` currently extract to the same attack source
hash `bd99b0b0d0d5a600ce31d1070c7feadf575193d269ec72dae4fba21a736377a4`.

The code is a replay-safe live-fill family with the same broad shape as the
B003→B008 lineage. It sets:

- `SPLIT_THRESHOLD_S=12.0`;
- `SPLIT_CLASSIFY_N=8` before later local B008's `5`;
- `REPLAY_SAFE_FRAC=0.97` with a final notebook-level override to `0.98`;
- `SLOW_MULTIPOST_N=1`;
- `PROBE_HOPS=0`;
- a notebook-level `FRAME_TEMPLATE` override to the same plain-plus-analysis
  frame shape already used in B008/B008R.

This does not produce a clean B012 move. B008/B008R already incorporated the
same family and then improved it with `SPLIT_CLASSIFY_N=5`,
`REPLAY_SAFE_FRAC=0.99`, and `SLOW_MULTIPOST_N=4`. Reverting any one of those
variables would be a blind parameter rollback against prior evidence:

- B005 showed `REPLAY_SAFE_FRAC=0.99` was better than `0.98` in this account;
- B004 showed slow-row multi-post was better than single-post;
- B008 showed classify5 was better than classify8 at least once, even though the
  current B008 submission later became score-bearing `ERROR`.

Therefore this public family is retained as background evidence, not a B012
candidate.

### Adhiraj probe-and-flood route

`adhirajjagtap/probe-and-flood-strategy` is structurally different from B008R:
it probes four prompt templates with `max_tool_hops=1`, chooses the highest
local raw-points-per-second template, then emits `MAX_CANDIDATES=2000` flood
candidates from that one template.

It is not suitable as a formal B012 candidate in its current form:

- the public source uses `.co` targets, which violates this repository's
  reserved-domain safety boundary;
- it does not keep only replay-safe fired candidates and intentionally returns a
  full flood set;
- a safe adaptation would need to change at least domain policy, validation
  policy, hop cap, and fill/replay sizing together;
- using only the template-probe idea on top of B008/B008R would continue the
  already weak prompt-template direction rather than a clearly stronger
  mechanism-low-correlated variable.

The route is worth retaining as an audit artifact because it is current and
mechanistically different, but it does not yet define a single-variable B012
that is strong enough to spend a formal submission.

### Restoration-exception route

The current practical leaderboard gap is not only algorithmic. B005's historical
score `91.930` and B008's historical score `92.165` are both better than the
current leaderboard-effective `88.760`, but the corresponding old submissions
are currently score-bearing `ERROR`. A byte-identical B005 restore could be
investigated as a separate restoration exception, but it would be a repeat of a
previous candidate rather than a mechanism-low-correlated B012 algorithm. It is
therefore not selected in this B012 audit.

## Decision

No B012 formal candidate is selected in this pass. No B012 preregistration,
Notebook, or competition submission is created.

The next B012 pass should continue looking for a single-variable mechanism that:

1. changes tool coverage or replay reliability rather than only budget margin;
2. keeps B008R `88.760` as the current effective comparison;
3. keeps B008 `92.165` as the historical-high threshold;
4. has fixed acceptance gates of `>88.760`, `>92.165`, and `>=100.000`;
5. rejects `<=88.760`, blank score, `ERROR`, failure, timeout, or duplicate
   route;
6. avoids repeats of B006/B007/B008/B009/B010/B008R/B011 and the weak
   prompt/channel/template routes already rejected.
