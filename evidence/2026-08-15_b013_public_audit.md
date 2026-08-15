# B013 public-route audit and candidate screen

This is a read-only B013 scouting record. It does not preregister a formal B013
candidate and does not authorize a Kaggle Notebook or competition submission.

## Current Kaggle state

Checked during the `2026-08-15 01:37-01:42 UTC` monitor/research pass.

Current effective and historical references:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_label=B008R restore classify5
current_leaderboard_effective_public_score=88.760
historical_high_submission=55266445
historical_high_label=B008 classify5
historical_high_public_score=92.165
historical_high_current_status=score-bearing ERROR, not leaderboard-effective
direct_current_gate=>88.760
historical_high_gate=>92.165
strong_reference_gate=>=100.000
```

Latest submission state:

```text
B012 55495429 COMPLETE public=88.665 private=blank api_errorDescription=None
B005R 55461853 COMPLETE public=86.945 private=blank api_errorDescription=None
B011 55433780 COMPLETE public=72.680 private=blank api_errorDescription=None
B008R 55393959 COMPLETE public=88.760 private=blank api_errorDescription=None
B010 55327331 COMPLETE public=52.330 private=blank
```

Public leaderboard snapshot:

```text
artifact_zip=artifacts/kaggle/leaderboards/2026-08-15_0915_b013_research/ai-agent-security-multi-step-tool-attacks.zip
extracted_csv=artifacts/kaggle/leaderboards/2026-08-15_0915_b013_research/extracted_py/ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-15T01_42_00.csv
rows=1444
team=heralces
team_rank=298
team_score=88.760
team_last_submission_date=2026-08-14 02:01:38
team_submission_count=5
score_at_50=97.640
score_at_100=92.250
score_at_200=89.865
rank_if_88_665=311
rank_if_88_760=298
rank_if_92_165=103
rank_if_100_000=36
```

The current top-200 gap is about `1.105` points over B008R `88.760`. A B013
candidate should therefore be expected to beat `89.865`, not merely improve by a
few hundredths, unless it has unusually strong evidence toward the historical
`92.165` range.

## Public artifacts pulled

Pulled current public snapshots into
`artifacts/kaggle/public_audit/2026-08-15/`. Those artifacts are local audit
inputs and are not committed to git.

```text
coolin666/jed-attack-v12
  notebook_sha256=15d93f4720325d95cebd3f901b39cf513859006cc4a7ae0f8be6dd35e05c286c
  extracted_attack_sha256=cdc7486b2a653cf0e1b2d0fec6a782559e24c74834300c75e586869591037c20
  extracted_path=artifacts/kaggle/public_audit/2026-08-15/extracted_attack_py_literals/coolin666_jed-attack-v12.py

dimong4/ai-agent-security
  notebook_sha256=a2c8bf54783c444ef8f68b9eed570cf7b2538ebd0de8a496b1b0cd646fea47c2
  extracted_attack_sha256=38ecb61818e4767cb8a4b46bea95aa75d258f90bd3aa5e00cd65c19ade5aca9c
  extracted_path=artifacts/kaggle/public_audit/2026-08-15/extracted_attack_py_literals/dimong4_ai-agent-security.py

jvn3jean/rq2-newww
  notebook_sha256=c44ea84434021d140686b6fca53bfeb89fb8f906627b84f6753865ab88cf2516
  extracted_attack_sha256=7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6
  extracted_status=no AttackAlgorithm source extracted

saitejabandaruin/ai-agent-security-red-teaming-toolkit
  notebook_sha256=a6c550072ec38ee8eb56066a863ef024ec9b3f4a47da69bc3f8c1fb76bb2607e
  extracted_attack_sha256=7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6
  extracted_status=no AttackAlgorithm source extracted

verityix/ai-agent-security-attack-algorithm-hitherto
  notebook_sha256=5f4dd9e2ebccbdea045536ddb67bcc07817bc8af7c2db2c3e44cc8dc922fdd0e
  extracted_attack_sha256=c5195012e1bbb4f6763b5b7a41c94bcd49330e3fb3906a7579112a6954012038
  extracted_path=artifacts/kaggle/public_audit/2026-08-15/extracted_attack_py_literals/verityix_ai-agent-security-attack-algorithm-hitherto.py

yw8837/88-875-lb-open-source-jed-attack-full-code
  notebook_sha256=a458fc3da6d4ec3c482ea0652c1487db715e08b2b8b28a23485e83fe55818f96
  extracted_attack_sha256=b563633370cc010c49ddd4d4f98559653e26fec3d9fc239cdd519436b7797a3e
  extracted_path=artifacts/kaggle/public_audit/2026-08-15/extracted_attack_py_literals/yw8837_88-875-lb-open-source-jed-attack-full-code.py
```

## Local scoring and contract anchors

Read-only SDK inspection during this pass:

- `data/competition/extracted/aicomp_sdk/attacks/contracts.py` shows
  `AttackCandidate` accepts only `user_messages`. Public routes that rely on
  extra candidate metadata are not SDK-valid without adaptation.
- `data/competition/extracted/aicomp_sdk/core/cells.py` includes tool sequence,
  side effects, sources, outcomes, `secret_read`, `egress_count`, normalized
  tool args such as `http.post` domain, output samples, and user message hashes
  in cell signatures. This explains why domain policy and user-message template
  changes are material behavioral variables, not harmless presentation details.
- `data/competition/extracted/aicomp_sdk/scoring.py` normalizes raw score by
  `raw / 200000 * 1000`; current 88-point scores imply roughly one thousand
  useful exfiltration findings/cells, so tiny one-candidate deltas are unlikely
  to cross a live top-200 boundary by themselves.
- `data/competition/extracted/aicomp_sdk/core/predicates.py` exposes possible
  extra predicate families such as confused-deputy email and destructive
  writes, but those routes have materially higher guardrail and replay risk than
  the already validated exfiltration-only lineage.

## Mechanism screen

### `yw8837/88-875-lb-open-source-jed-attack-full-code`

The title claims an `88.875` leaderboard route, which is slightly above B008R
`88.760` but still below the current top-200 boundary `89.865` and far below
historical B008 `92.165`.

Mechanism summary:

- probes a prompt/template bank and selects by observed fire rate;
- uses a `.co` target policy in the public artifact;
- includes multiple prompt forms rather than a single B008R-compatible behavior
  variable;
- returns blind projected candidates after probe selection.

This route is not selected for B013 because a repository-safe adaptation would
simultaneously change domain policy, template bank, probe/selection policy, and
fill behavior. It also falls into the prompt/template-bank direction that the
current candidate gate explicitly excludes. The claimed score is not large
enough to justify spending a formal submission on a multi-variable rewrite.

### `coolin666/jed-attack-v12`

The artifact is mostly a code string extraction. Its mechanism overlaps known
rejected or excluded variables: fast burst size, probe/hop saturation,
`SPLIT_CLASSIFY_N=8`, `REPLAY_SAFE_FRAC=0.90`, reduced slow multipost, and `.co`
targets.

This is not selected because it repeats B007/B009-style mechanisms and rolls
back B005/B008 evidence. A safe adaptation would be multi-variable.

### `dimong4/ai-agent-security`

The current snapshot differs from earlier Dimong hashes but remains a known
public family. It uses `SPLIT_CLASSIFY_N=8`, lower replay-safe fraction than
B008R, reduced slow multipost in some variants, and public-domain targets.

Relative to B008R, this mostly points backward on variables already tested or
explicitly excluded. It is retained as background evidence, not a B013
candidate.

### `verityix/ai-agent-security-attack-algorithm-hitherto`

This is a broad multi-template grid. It also constructs candidates with
metadata-like fields, while the local SDK contract only accepts `user_messages`.

It is not SDK-valid in current form. Making it safe and valid would require
simultaneous changes to candidate construction, template set, URL policy, and
selection/fill behavior, so it is not a clean single-variable candidate.

### `jvn3jean/rq2-newww` and `saitejabandaruin/...toolkit`

No usable `AttackAlgorithm` source was extracted from these public snapshots.
They do not provide enough mechanism evidence for a formal candidate.

## Local mechanism screen

The following local ideas were considered but not selected:

- **Trace-derived exact replay**: returning actual fired warmup/probe user
  messages could improve replay reliability, but B012's smaller warmkeep version
  already failed at `88.665`, and a broader trace replay would risk reducing
  multi-endpoint coverage.
- **Another warmup/extra-candidate variant**: too close to B012 and unlikely to
  bridge the live top-200 gap.
- **Email/confused-deputy addition**: mechanistically different, but it adds a
  new predicate family, new tool channel, and likely guardrail exposure; no
  local hidden-score evidence supports spending a formal slot.
- **Destructive write/delete routes**: potentially score-bearing in SDK, but
  high-risk under guardrails and not aligned with the current reliable
  exfiltration lineage.

## Decision

No B013 formal candidate is selected in this pass. No B013 preregistration,
Notebook, or competition submission is created.

Current standing state after this audit:

- current leaderboard-effective score remains B008R `88.760`;
- historical observed high remains B008 `92.165`, but it is not
  leaderboard-effective;
- B012 is terminal and rejected at `88.665`;
- current public rank is `298`, top-200 boundary is `89.865`;
- a future B013 candidate must be a stronger, mechanism-low-correlated,
  falsifiable single-variable change with gates `>88.760`, `>92.165`, and
  `>=100.000`; `<=88.760`, blank score, `ERROR`, failure, timeout, duplicate,
  or unsafe artifact rejects without retry.

## 2026-08-15 09:22 UTC addendum

During the later heartbeat, the latest submissions and leaderboard were
rechecked:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_public_score=88.760
team_rank=302
score_at_200=89.865
rank_if_88_665=317
rank_if_88_760=302
rank_if_92_165=103
```

Additional public snapshots were pulled into
`artifacts/kaggle/public_audit/2026-08-15_0922/`:

```text
ruhul20/red-team-ai-agent-security
  notebook_sha256=9f4353543c9441fd9b8f73e71119797e67c337f3f054c2d1e3c3b9a80dd2a320
  candidate_text_sha256=6219c842aec74cdac91c2ebabe14958a071583ad935f1a6007e9b18556ade002
  source_len=28370
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=True
  CONFUSED_DEPUTY=True
  EXFILTRATION=True

georgymamarin/red-team-starter-what-fires-and-what-it-s-worth
  notebook_sha256=9cc9825b189333b272182b7d8087f835e689e807ba0003e9ec8af082e0cd62a4
  candidate_text_sha256=b1df6b25154928186506b8e45f601c0cc22d8c43bfca712ed6d1649f3f410213
  source_len=157816
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=True
  CONFUSED_DEPUTY=True
  EXFILTRATION=True
```

`ruhul20/red-team-ai-agent-security` is the only newly checked artifact that
contains a compact SDK-valid `AttackAlgorithm`. It is useful as public evidence
that `email.send` confused-deputy scoring is considered reachable by another
participant, but it is not selected as B013 in its current form:

- it is a full route replacement, not a single variable against B008R;
- it combines exfiltration, confused-deputy email, multi-endpoint prompts,
  live replay verification, family efficiency scheduling, replay-cost sorting,
  and fallback generation;
- using it safely would require deciding whether to keep or remove the email
  family, combo family, public-domain URL pool, discovery count, replay safety
  fraction, mutation policy, and fallback policy together;
- it therefore does not satisfy the current B013 single-variable gate.

`georgymamarin/red-team-starter-what-fires-and-what-it-s-worth` is retained as
background SDK/reachability evidence, not a formal candidate. It is a starter
analysis notebook rather than a directly preregisterable B008R-derived
single-variable attack.

No B013 preregistration, Notebook, or competition submission is created from
this addendum.

## 2026-08-15 11:22 UTC addendum

During the later heartbeat, the latest submissions and leaderboard were
rechecked again:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_public_score=88.760
team_rank=305
score_at_50=97.640
score_at_100=92.250
score_at_200=89.880
rank_if_88_665=321
rank_if_88_760=305
rank_if_92_165=103
rank_if_100_000=37
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-15_1122_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-15T11:25:33.csv
```

The public kernels listing showed a recent high-vote artifact that had not been
screened in earlier B013 passes:

```text
evgendvorkin/ai-agent
  title=AI Agent
  last_run=2026-08-15 11:16:02.717 UTC
  total_votes=255
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1122/evgendvorkin_ai-agent
  notebook_sha256=2a553049aa12ee00c93a1db31c92229719edf5d17ebf6dfd1d27ae461ac67c7d
  source_len=8787
  attack_code_len=7294
  attack_code_sha256=e528a47f72dcd456d9427ea68d5298400c3ab6fcbe521a24f815ac811d053729
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=True (markdown mention only)
  EXFILTRATION=False
  CONFUSED_DEPUTY=False
  .invalid=False
  .co=True
```

The extracted attack code is an SDK-valid `AttackAlgorithm`, but it is not a
clean B013 candidate against B008R:

- it uses public `.co` domains rather than the repository's retained
  reserved-domain URL policy;
- it rolls `SPLIT_CLASSIFY_N` back to `8`, reversing B008's successful
  classify5 change;
- it sets `REPLAY_SAFE_FRAC=0.999`, a pure replay-tail/budget variable that is
  already excluded from the current search space;
- it reduces `SLOW_MULTIPOST_N` to `1`, reversing the B004/B005/B008 slow-row
  four-endpoint mechanism;
- it introduces a raw `BEST_HARMONY` assistant/analysis-token prompt fallback,
  which falls under the excluded prompt-token/template direction;
- the notebook comment describes it as an `80+` fallback route, not as evidence
  for bridging the current top-200 gap or refreshing the historical `92.165`
  high.

No B013 preregistration, Notebook, or competition submission is created from
this addendum.
