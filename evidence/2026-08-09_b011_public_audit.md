# B011 public-route and local mechanism audit

## 1. Current baseline

This audit is a read-only B011 scouting record. It does not preregister a formal
B011 candidate and does not authorize a Kaggle Notebook or competition
submission.

```text
audit_observed_utc=2026-08-09 07:38
current_real_best_experiment=B008
current_real_best_submission_ref=55266445
current_real_best_public_score=92.165
current_real_best_private_score=
current_real_best_terminal_record_commit=57911f9
latest_rejected_experiment=B010
latest_rejected_submission_ref=55327331
latest_rejected_public_score=52.330
latest_rejected_terminal_record_commit=c2401fb
```

The latest Kaggle submissions query during this audit still showed B010 as the
most recent formal competition submission and B008 as the highest visible
Public Score. No B011 competition submission exists.

## 2. Public route audit

The audit pulled current public Kaggle notebooks for read-only inspection. The
hashes below pin the inspected notebook/code snapshots and prevent accidental
unattributed drift into a future candidate.

```text
foysalemonshanto/ai-agent-security-v15
notebook_sha256=f7f57088cff63d1d095a0f48e3499dfc0be18d09f45820b4163c2b39236e29f0
code_sha256=99906a1e61373d2bbcdae60b6fad1c59bef106c7d524e29c1565e242b70d002d
observed_cues=public replay-safe family; notebook-level FRAME_TEMPLATE override; REPLAY_SAFE_FRAC override to 0.98; unsafe .co URL in public source

anvithpothula/aisec-pilk
notebook_sha256=c183d58f9f24efa6f62818d34ca65f394f26d8631d9d641cffd6a543f44db82b
code_sha256=97a9934e00c8abfa95e5c40068937900f6c6191e604bbab0d58efe87cfecf4d4
observed_cues=adaptive eight-template bank; PROBE_REPS=5; MIN_FIRE_RATE=0.2; REPLAY_SAFE=0.99; unsafe .co URL in public source

tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery
notebook_sha256=54b7d943dc717ea9c357d954dd3ac3f1f4d6bf3eae9d43b65092f25913666bb1
code_sha256=bd975b811b0cc959d342451977b1566ae5976369745c810d9e6ec53bdaa2a630
observed_cues=adaptive five-template route; PROBE_REPS=2; MIN_FIRE_RATE=0.2; REPLAY_SAFE=0.99; unsafe .co URL in public source

canqiang/aiagsec-ea-b-0721
notebook_sha256=6a6ad5bcbb3a959ef7dac04aed7e26d180fb71a50849bfb585185d686429f33d
code_sha256=fdf86c15c1b4a04115b576b921e3f7e56605415a16639ec20d6a7db7916e041c
observed_cues=public replay-safe split family; SPLIT_CLASSIFY_N=8; REPLAY_SAFE_FRAC=0.97; SLOW_MULTIPOST_N=1; PROBE_HOPS=0; unsafe .co URL in public source

nikitagajbhiye30/ai-security-0011
notebook_sha256=1894c209de08791d36d68a2d0faca77c35d86c5d23e9e61f17bef3932998ccf7
code_sha256=1fb9f5fcd3132212453abc9443e94a66c9851aea95b9bafab3d3a5cd32a746e3
observed_cues=public replay-safe split family; SPLIT_CLASSIFY_N=8; REPLAY_SAFE_FRAC=0.97; SLOW_MULTIPOST_N=1; unsafe .co URL in public source

pengwang91/jed-fill-v26-replaysafe
notebook_sha256=f2f33fff9cac6c5dedde73557f1c546405a19c727763c390fa0bf9b02d2de42e
code_sha256=c459b1eddc2d75064df051f1f0ceeb67205bf412c052ba56c800a311e3feac41
observed_cues=sparse parsed attack body; no clean higher-confidence single-variable cue over B008
```

## 3. Rejected audit ideas

The audit did not select a formal B011 candidate.

- The Foysal/Nikita/Canqiang route is already the same public replay-safe family
  that B003 through B008 have materially adapted and improved. It does not offer
  a clean mechanism-low-correlated B011 move by itself.
- The Anvith and tetsutani adaptive template-bank routes are structurally
  different, but adopting them on top of B008 would replace the prompt-selection
  mechanism rather than change one isolated behavior variable. They also use
  unsafe `.co` endpoints in public form and would need a separate safe-domain
  adaptation and local contract proof.
- The Foysal `FRAME_TEMPLATE` override is a prompt-shape/channel-adjacent cue.
  After B010's large regression from changing the slow-frame channel token, this
  is not strong enough to justify another formal channel/prompt-token submission
  without better evidence.
- Increasing `REPLAY_BUDGET_MULT` above `1.0` had no candidate-count effect in
  sampled constant-latency fake-clock rows because the wall-clock deadline, not
  the replay cap, was binding.
- Tightening `SLOWEST_MULT` from `1.35` to `1.15`/`1.05` produced only about one
  extra candidate in most sampled constant-latency rows. This is a real
  single-variable budget-cushion idea, but the expected score upside is too small
  for a formal Kaggle submission at the current B008 `92.165` baseline.

## 4. Decision and next gate

No B011 preregistration, Notebook build, or competition submission is created in
this audit cycle.

The next B011 attempt should remain anchored to B008 `92.165`, avoid B006/B007/
B008/B009/B010 mechanisms, and only proceed to preregistration after identifying
a stronger single-variable candidate with:

1. fixed source/parent hash,
2. candidate source SHA-256,
3. a single falsifiable hypothesis,
4. a direct acceptance threshold of `>92.165`,
5. `>=100.000` as the strong-competition marker, and
6. rejection for `<=92.165`, blank score, failure, timeout, or duplicate route.
