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

## 2026-08-16 13:19 UTC addendum

During the later heartbeat, the latest submissions and leaderboard were
rechecked again:

```text
latest_competition_submissions_unchanged=True
B012_submission=55495429 COMPLETE Public Score 88.665 Private Score blank
B005R_submission=55461853 COMPLETE Public Score 86.945 Private Score blank
B011_submission=55433780 COMPLETE Public Score 72.680 Private Score blank
B008R_submission=55393959 COMPLETE Public Score 88.760 Private Score blank
B008_submission=55266445 ERROR Public Score 92.165 Private Score blank
current_leaderboard_effective_public_score=88.760
team_rank=342
score_at_50=98.415
score_at_100=92.880
score_at_200=90.270
rank_if_88_665=360
rank_if_88_760=342
rank_if_92_165=111
rank_if_100_000=39
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-16_1319_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-16T13:20:16.csv
```

The public kernels list showed a newly rerun `evgendvorkin/ai-agent` artifact
after the previous screen:

```text
evgendvorkin/ai-agent
  title=AI Agent
  last_run=2026-08-16 11:41:04.377 UTC
  total_votes=256
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_1319/evgendvorkin_ai-agent_latest
  notebook_sha256=b88657e612ea653fae88206de4d5a38d7e6ba888ea0d669cf3260ca94f085ff0
  code_source_len=7911
  attack_code_len=7298
  attack_code_sha256=9a9e9d1b86edca0c892457035e3f5925917ddf41c18ecabf858fa93e36d5c79a
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=False
  EXFILTRATION=False
  CONFUSED_DEPUTY=False
  .invalid=False
  .co=True
  BEST_HARMONY=True
  analysis=True
  commentary=False
  SPLIT_CLASSIFY_N=8
  REPLAY_SAFE_FRAC=0.999
  SLOW_MULTIPOST_N=1
  SPLIT_THRESHOLD_S=12.0
  PROBE_HOPS=0
```

Relative to the previously screened `2026-08-15 11:16 UTC` snapshot, the attack
code is not byte-identical. The substantive code change is that `TEMPLATE` was
changed from the verbose single `http.post` instruction to the same
`BEST_HARMONY` analysis-token injection string that was previously only a
fallback. The other core route variables remain `.co` targets,
`SPLIT_CLASSIFY_N=8`, `REPLAY_SAFE_FRAC=0.999`, `SLOW_MULTIPOST_N=1`, and
`PROBE_HOPS=0`.

This is not selected as a formal B013 candidate because the new change is
explicitly in the excluded prompt-token / analysis-channel direction and remains
coupled to public `.co` URL policy plus rollback of B008R's classify5 and
slow-row four-endpoint lineage. No B013 preregistration, Notebook, or competition
submission is created from this addendum.

## 2026-08-16 09:18 UTC addendum

During the later heartbeat, the latest submissions and leaderboard were
rechecked again:

```text
latest_competition_submissions_unchanged=True
B012_submission=55495429 COMPLETE Public Score 88.665 Private Score blank
B005R_submission=55461853 COMPLETE Public Score 86.945 Private Score blank
B011_submission=55433780 COMPLETE Public Score 72.680 Private Score blank
B008R_submission=55393959 COMPLETE Public Score 88.760 Private Score blank
B008_submission=55266445 ERROR Public Score 92.165 Private Score blank
current_leaderboard_effective_public_score=88.760
team_rank=340
score_at_50=98.415
score_at_100=92.925
score_at_200=90.270
rank_if_88_665=359
rank_if_88_760=340
rank_if_92_165=112
rank_if_100_000=39
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-16_0918_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-16T09:20:35.csv
```

The current public kernels listing did not show a newly rerun candidate beyond
the already screened Verity and Dimong snapshots. This pass therefore filled in
remaining older public artifacts from the visible listing that had not been
individually recorded in the B013 evidence:

```text
paul720810/hermes-attack-v71-n1000-20260721-102018
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0918/paul_hermes_v71
  script_sha256=00758654fb6ef095cd4b6ef129dd235e41d821627a973cbde30c5e2ce698610c
  decoded_attack_sha256=a8c3947f7552ea5146935460cd63fc3c00e802b4ee9d68f1922ad01289859526
  decoded_len=2554
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  .invalid=False
  .co=False
  .x=True

paul720810/hermes-attack-v70-n900-20260721-101920
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0918/paul_hermes_v70
  script_sha256=354492cb1d2b197ab34d23f885d80be803d9ada84f13cc526bb11a420cf61993
  decoded_attack_sha256=dcae430fac2addb8b566e517b8681e9c17efa7bfbfca50ac312953282d1e8f2f
  decoded_len=2553
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  .invalid=False
  .co=False
  .x=True

paul720810/hermes-attack-v69-proven-code-20260721-052046
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0918/paul_hermes_v69
  script_sha256=b6b58501a74b405a8bef492c4346a7afc1e7da56d9179f0b0d1479bfd3ee9585
  decoded_attack_sha256=7bd7edf13f13a923ccdeef1e282f1e515806c98b6a15dc15bd330ff4008392a6
  decoded_len=2553
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  .invalid=False
  .co=False
  .x=True

paul720810/hermes-attack-v68-tight-20260721-003427
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0918/paul_hermes_v68
  script_sha256=96c58e8d8daf076bebca237be091e0ecfe932c2c16cd618e106ff6a6c6677bde
  decoded_attack_sha256=9e2112305b4ed426a87e27d603b72f950d70ee3a801560eeaff093dd46caeee2
  decoded_len=1801
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  .invalid=False
  .co=False
  .x=True

ojanapalash/notebook6d94950baf
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0918/ojana_notebook6d94950baf
  script_sha256=6a8a00583f856844b085451f1a8b5cb46ce2ba19f51a2038a140a8466b3e4e1c
  AttackAlgorithm=False
  AttackCandidate=False
  http.post=False

foysalemonshanto/ai-agent-security-v12
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0918/foysal_v12
  notebook_sha256=6a26b45402e8acc5b35f7a559c85aedbd70783b62a4ae6edfc1bd765a790ee9b
  extracted_attack_sha256=6c01abb24a729f9a2aef0c5f6a5dccb5f8940dadd431e34618402b57f8d49eb5
  extracted_len=27279
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  EXFILTRATION=True
  CONFUSED_DEPUTY=True
  .invalid=False
  .co=True
  SPLIT_CLASSIFY_N=8
  REPLAY_SAFE_FRAC=0.97
  SLOW_MULTIPOST_N=1
```

None of these artifacts is selected as a formal B013 candidate:

- Paul's older Hermes v68-v71 snapshots are the same route family as the already
  rejected v72 line: compact base64-wrapped single-post generators using `.x`
  URL policy and tuned target-count variants, without evidence that rolling
  back B008R's classify5 / slow-row four-endpoint lineage would improve the
  current `88.760` effective score.
- `ojanapalash/notebook6d94950baf` does not expose a usable SDK
  `AttackAlgorithm`/`AttackCandidate` attack implementation in the pulled
  snapshot.
- `foysalemonshanto/ai-agent-security-v12` is an older broad exfil/deputy route
  using public `.co` targets, `SPLIT_CLASSIFY_N=8`, `REPLAY_SAFE_FRAC=0.97`,
  `SLOW_MULTIPOST_N=1`, and analysis-token shaping. This repeats or rolls back
  excluded/rejected variables rather than isolating a new low-correlated
  mechanism.

No B013 preregistration, Notebook, or competition submission is created from
this addendum.

## 2026-08-16 07:17 UTC addendum

During the next heartbeat, submissions and leaderboard were rechecked again:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_public_score=88.760
team_rank=337
score_at_50=98.415
score_at_100=92.925
score_at_200=90.250
rank_if_88_665=356
rank_if_88_760=337
rank_if_92_165=112
rank_if_100_000=39
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-16_0717_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-16T07:18:23.csv
```

The competition submission list is unchanged: B012 `55495429` remains
`COMPLETE` with Public Score `88.665`, B008R `55393959` remains the current
leaderboard-effective `COMPLETE` submission with Public Score `88.760`, and
historical B008 `55266445` remains score-bearing `ERROR` with Public Score
`92.165`.

The current public kernels list showed no newly rerun artifact beyond already
screened Verity and Dimong snapshots. This pass pulled three older unrecorded or
partially recorded public artifacts for static screening:

```text
tiktoktrendz/jed-submission
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0717/tiktoktrendz_jed_submission
  notebook_sha256=9dca9ce109b03bcfa618f456a92a23e1e36d0aa8ed7bcfe7e0f087429a365cfe
  extracted_attack_sha256=9ce724435f180a81412d128bb1e0da35301ee7da19448888fd228ff25bb03857
  extracted_len=68104
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  EXFILTRATION=True
  CONFUSED_DEPUTY=True
  eval_predicates=True
  fs.delete=True

sravanikamjula/ai-agent-security-multi-step-tool-attack-baseline
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0717/sravani_baseline
  notebook_sha256=972716325417baa8be8a422b66d8ff4bb212f48c4ebe8a013abeca24c59b7227
  extracted_attack_sha256=2e49f2cb59256b36c4ff33e3395b4da653564e8e04b5b9fbe095ae389696cf02
  extracted_len=4073
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=False
  eval_predicates=True

anvithpothula/aisec-sevstack
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0717/anvith_sevstack
  notebook_sha256=6313b4f9ca32cb360c80115f7d522c99f0280e52570e405f686b22944c8ddf3e
  extracted_attack_sha256=86047663cbfdf44e060b9afee0f4a8913422f42e2780e060fb1ab2d9d2ba9322
  extracted_len=62219
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  eval_predicates=True
  SEARCH_PROFILE=single_900
```

None of these artifacts is selected as a formal B013 candidate:

- `tiktoktrendz/jed-submission` is a broad multi-family severity stack with
  single/dual exfiltration templates, confused-deputy/deputy-style families,
  destructive-write logic, predicate validation, randomization, and multi-route
  prioritization. It is not a B008R-derived single behavior variable.
- `sravanikamjula/...baseline` is a starter-style baseline with SDK predicate
  scaffolding but no `http.post` exfiltration route in the extracted attack
  implementation.
- `anvithpothula/aisec-sevstack` is the same extracted attack SHA as the
  previously screened multi-endpoint severity stacker route. It remains a broad
  route replacement rather than a single-variable improvement over B008R.

No B013 preregistration, Notebook, or competition submission is created from
this addendum.

## 2026-08-16 05:16 UTC addendum

During the next heartbeat, submissions and leaderboard were rechecked again:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_public_score=88.760
team_rank=334
score_at_50=98.415
score_at_100=92.925
score_at_200=90.225
rank_if_88_665=352
rank_if_88_760=334
rank_if_92_165=112
rank_if_100_000=39
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-16_0516_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-16T05:16:56.csv
```

The competition submission list is unchanged: B012 `55495429` remains
`COMPLETE` with Public Score `88.665`, B008R `55393959` remains the current
leaderboard-effective `COMPLETE` submission with Public Score `88.760`, and
historical B008 `55266445` remains score-bearing `ERROR` with Public Score
`92.165`.

The current public kernels list showed no newly rerun artifact beyond already
screened Verity and Dimong snapshots. This pass therefore pulled two
unrecorded exfiltration-labeled public artifacts for static screening:

```text
koushikkumardinda/ai-agent-security-replay-safe-exfiltration
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0516/koushik_replay_safe_exfiltration
  notebook_sha256=026a797a255953c281b87f4662411c62e9ac82a96a7b924f7897bfe4c28d842a
  extracted_code_sha256=794560130e0221aff5cc1ba8b4b152a45eb787f3528e403b83a5e0cbaca3f0d3
  code_len=7764
  AttackAlgorithm=False
  AttackCandidate=False
  http.post=False
  env.interact=False

pilkwang/ai-agent-v3-1-2-single-post-exfiltration
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0516/pilkwang_single_post_exfiltration
  notebook_sha256=447f892022f420d0ff9e8482fd30087d87a579943a148d282afc274717af3043
  extracted_code_sha256=a636588b2155b991829b63abff222722b1f700f9d30c78543deffb2d5cf37d69
  code_len=26370
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  EXFILTRATION=True
  CONFUSED_DEPUTY=True
  SPLIT_CLASSIFY_N=8
  REPLAY_SAFE_FRAC=0.97
  SLOW_MULTIPOST_N=1
```

Neither artifact is selected as a formal B013 candidate:

- `koushikkumardinda/...replay-safe-exfiltration` is not an SDK
  `AttackAlgorithm`/`AttackCandidate` implementation in the pulled snapshot; it
  appears to be a notebook-side exploratory scaffold rather than a valid Code
  Competition attack file.
- `pilkwang/...single-post-exfiltration` is a legacy live-fill single-post
  exfiltration route. It combines public `.co` URL policy, classify8, a lower
  replay-safe fraction, `SLOW_MULTIPOST_N=1`, and older live-fill behavior. It
  therefore rolls back several proven B008R/B004/B005 variables at once instead
  of offering a B008R-derived single behavior variable.

No B013 preregistration, Notebook, or competition submission is created from
this addendum.

## 2026-08-16 01:15 UTC addendum

During the next heartbeat, the latest submissions and leaderboard were
rechecked again:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_public_score=88.760
team_rank=327
score_at_50=98.100
score_at_100=92.700
score_at_200=90.180
rank_if_88_665=345
rank_if_88_760=327
rank_if_92_165=110
rank_if_100_000=39
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-16_0115_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-16T01:16:08.csv
```

The competition submission list is unchanged: B012 `55495429` remains
`COMPLETE` with Public Score `88.665`, B008R `55393959` remains the current
leaderboard-effective `COMPLETE` submission with Public Score `88.760`, and
historical B008 `55266445` remains score-bearing `ERROR` with Public Score
`92.165`.

The current public kernels list showed two updated artifacts after the previous
audit window: `verityix/ai-agent-security-attack-algorithm-hitherto` last run
`2026-08-15 23:47:54.347 UTC` and `dimong4/ai-agent-security` last run
`2026-08-15 20:16:19.357 UTC`. This pass pulled those updated snapshots plus
older relevant-looking artifacts that had not been separately recorded:

```text
verityix/ai-agent-security-attack-algorithm-hitherto
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0115/verityix_hitherto_latest
  notebook_sha256=05424ef59655aef819f3e3ba35e3fcef3324cd593f6b8c2781062da9ea8717b9
  extracted_code_sha256=800194653191d3fe45e3ee5b16fb6a44034ea2d71759c108f1a391ca480bf900
  code_len=2898
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  eval_predicates=True

dimong4/ai-agent-security
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0115/dimong_latest
  notebook_sha256=de31e1f5811afb55d56b4cc2336c2d7a3cf50eed02b4344d83273e0a51941e7f
  extracted_code_sha256=50cb69ec3a448054af2f20e95b76b2441a2c1461679152b32a1eb4e90a06d112
  code_len=8800
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  SPLIT_CLASSIFY_N=5
  REPLAY_SAFE_FRAC=0.975

cleanorlabs/single-post-live-fill-reference-baseline
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0115/cleanorlabs_single_post_live_fill
  notebook_sha256=246ef113e197b57f20bcfc3f7656ac3f06e6ff208af8ed209196521286cb0db0
  extracted_attack_sha256=0315e823036de2f182a6e343cffe87d31a61d9054c96a09b833e1da13ec3a9f3
  extracted_len=6751
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  env.interact=True

shreyascppsc/jed-payload-blind-egress-working-note
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0115/shreyas_blind_egress
  notebook_sha256=d72310a6e5f86e7be1a04e6c0b8b4904620dd3c99ead26204529afc97d23a472
  code_len=0
  AttackAlgorithm=True (markdown mention only)
  AttackCandidate=False

ferencjuhsz/ghostpost-verify-and-keep-agent-red-team
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-16_0115/ferenc_ghostpost
  notebook_sha256=55b1884e42b8a5a00dfd13edfb5ce98b1e06160bac08aab6d2cac1c1f548ca8f
  extracted_attack_sha256=81b3c29995372c1f48810266df9cf11402cef9a5af73653d8fa2a237458377ac
  extracted_len=10480
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=True
  EXFILTRATION=True
  CONFUSED_DEPUTY=True
```

None of these artifacts is selected as a formal B013 candidate:

- The updated `verityix` artifact is a live-validated prompt/style and public
  URL grid. It changes template family, URL policy, and validation/selection
  behavior together, and does not preserve the B008R replay-safe split lineage.
- The updated `dimong4` artifact now combines a public `.co` URL policy,
  destructive `fs.delete` follow-up, prompt-token frame injection, a changed
  replay-safe fraction, and fill-budget behavior. This is not a safe
  single-variable change against B008R.
- `cleanorlabs/...single-post-live-fill` is a compact live-fill baseline, but it
  uses public `.co` hosts, classify6, `REPLAY_SAFE=0.97`, and prompt-token
  switching. It largely rolls back or weakens the B008R/B005 evidence stack.
- `shreyascppsc/...working-note` is markdown/background material rather than a
  usable attack implementation.
- `ferencjuhsz/...ghostpost` provides useful background evidence for
  verify-and-keep exfiltration plus confused-deputy/email families, but it is a
  broad multi-family route with calibration, exfil variants, deputy variants,
  search budget allocation, and live keep-selection all changing together.

No B013 preregistration, Notebook, or competition submission is created from
this addendum.

## 2026-08-15 13:22 UTC addendum

During the later heartbeat, the latest submissions and leaderboard were
rechecked again:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_public_score=88.760
team_rank=308
score_at_50=97.965
score_at_100=92.340
score_at_200=89.905
rank_if_88_665=327
rank_if_88_760=308
rank_if_92_165=105
rank_if_100_000=37
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-15_1322_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-15T13:23:06.csv
```

The public kernels listing did not show a newer candidate than the already
screened `evgendvorkin/ai-agent`. This pass therefore screened older unreviewed
or lightly reviewed public artifacts whose titles suggested possible throughput
or attack-route mechanisms:

```text
aratisantoshshinde/ai-agent-security-adaptive-tool-call-throughput-se
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1322/arati_adaptive_tool_call
  notebook_sha256=5bdf337036027c3688c3c167ac8ea269bf98e0b2e40aa73b97425f1f36bd0551
  decoded_attack_sha256=91d5cf0edb92b364197ce41b836d797dfc8a693c5ac5347a06ba8df25a858e97
  decoded_len=20560
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=False
  EXFILTRATION=True
  CONFUSED_DEPUTY=False
  .invalid=False
  .co=True

paul720810/hermes-attack-v72-m112-20260721-151926
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1322/paul_hermes_v72
  script_sha256=eb54da7f4a63fe45ec568053c63936b0609f9c0caefc1588e28b46eee227af06
  decoded_attack_sha256=3fda6ca441ec0e718e5ccca66f2bed19fc5805ad6187b2466ee32ab8ce120890
  decoded_len=2452
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=False
  EXFILTRATION=False
  CONFUSED_DEPUTY=False
  .invalid=False
  .co=False
  .x=True

prvsiyan/ai-agent-security-defense-in-depth-audit
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1322/prvsiyan_defense_audit
  notebook_sha256=75cd92c11c17d0dec9db92099d5735cb2ba6262e178bd87d230b40e14776aa9e
  source_len=22800
  AttackAlgorithm=True
  AttackCandidate=False
  http.post=True
  email.send=True
  return_empty_candidates=True
```

None of these artifacts is selected as a B013 candidate:

- `aratisantoshshinde/...throughput-se` is a broad live arm-selection system. It
  changes template families, single-vs-dual post density, exact predicate
  validation, rolling probation/rollback, replay-budget accounting, dynamic
  reserve sizing, and `.co` URL policy together. It also includes injected
  analysis/commentary prompt-token variants. This is useful background evidence
  about throughput search, but not a B008R-derived single variable.
- `paul720810/hermes-attack-v72...` is a compact single-post generator with
  micro-tuned target count and margin multiplier. It uses `.x` targets and is a
  simple single-post rollback rather than a route expected to beat B008R's
  classify5/four-endpoint lineage.
- `prvsiyan/...defense-in-depth-audit` is explicitly defensive/inert: its
  compatibility `AttackAlgorithm` returns no candidates. It is not an attack
  candidate.

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

## 2026-08-15 15:23 UTC addendum

During the later heartbeat, the latest submissions and leaderboard were
rechecked again:

```text
current_leaderboard_effective_submission=55393959
current_leaderboard_effective_public_score=88.760
team_rank=313
score_at_50=97.965
score_at_100=92.385
score_at_200=89.910
rank_if_88_665=331
rank_if_88_760=313
rank_if_92_165=106
rank_if_100_000=37
leaderboard_artifact=artifacts/kaggle/leaderboards/2026-08-15_1523_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
leaderboard_csv=ai-agent-security-multi-step-tool-attacks-publicleaderboard-2026-08-15T15:25:33.csv
```

The public kernels list still showed no newer candidate than the already
screened `evgendvorkin/ai-agent`. This pass therefore pulled older high-vote or
mechanism-titled artifacts that had not been individually recorded in the B013
evidence:

```text
uradkr/ai-security-urad-code
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1523/urad_code
  notebook_sha256=2b2045f1922c8bcd2482b03f8c03a5df9fd437591ccab44f65d6637d573a63bc
  extracted_attack_sha256=d3894b2bb2038814d469ea0c83dc637957c2ed421ec667389015a99453aba325
  extracted_len=3141
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  live_env_interact=False

karnakbaevarthur/multi-endpoint-severity-stacker
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1523/karnak_multi_endpoint
  notebook_sha256=ff5b2f52d3f477ca0cd811db178bc73ddd6b671a47daf068ec9ade734529b0d6
  extracted_attack_sha256=86047663cbfdf44e060b9afee0f4a8913422f42e2780e060fb1ab2d9d2ba9322
  extracted_len=62219
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=False
  EXFILTRATION=True
  CONFUSED_DEPUTY=False

yaroslavkholmirzayev/replay-dense-boundary-exact-aggressive
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1523/yaroslav_replay_dense_boundary
  notebook_sha256=b9a5ba88bf7587b3405e2bb337c1b6344c6393648bfea6169102308407f3b96c
  extracted_attack_sha256=db6d15fabea97779b1563c685b5c20e26442d07ad793e9e52a956ff8e0882afc
  extracted_len=2585
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  live_env_interact=False

lopure/jed-multi-step-attack-relay-push100
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1523/lopure_relay_push100
  notebook_sha256=b6e05b39959f4b044f9c4235440a42cfa11045985a51c27c2eef2c85490e7bec
  AttackAlgorithm=False
  AttackCandidate=False
  http.post=False

arizalfirdaus123/multi-turn-exfiltration-with-adaptive-burst
  local_pull_dir=artifacts/kaggle/public_audit/2026-08-15_1523/arizal_adaptive_burst
  notebook_sha256=3bb3c9d5f4bc5e556572fed350a90ed03d22500ffabe29205fb753eebcb6cd85
  extracted_class_cell_sha256=1004bb6a42febbc26461eb751baef546ff46d079fc573685846d49d707f42a18
  extracted_len=10772
  AttackAlgorithm=True
  AttackCandidate=True
  http.post=True
  email.send=False
  EXFILTRATION=True
  CONFUSED_DEPUTY=True
```

None of these artifacts is selected as a formal B013 candidate:

- `uradkr/ai-security-urad-code` and
  `yaroslavkholmirzayev/replay-dense-boundary-exact-aggressive` are simple
  fixed single-post portfolios. They do not use live validation, do not preserve
  B008R's classify5 / slow-row four-endpoint split, and would require a
  broad rollback plus URL-policy adaptation rather than a mechanism expected to
  beat B008R.
- `karnakbaevarthur/multi-endpoint-severity-stacker` is a broad route
  replacement: it changes payload families, endpoint host generation,
  live predicate verification, candidate priority, replay-hop budgeting,
  mutation/mass-fallback behavior, and search profile settings together.
- `arizalfirdaus123/multi-turn-exfiltration-with-adaptive-burst` combines
  many exfil prompt families, multi-turn deputy wording, burst probing, stable
  hit counting, budget-adaptive fill, and URL policy in one route.
- `lopure/jed-multi-step-attack-relay-push100` did not expose a usable
  `AttackAlgorithm`/`AttackCandidate` implementation in the pulled snapshot.

No B013 preregistration, Notebook, or competition submission is created from
this addendum.
