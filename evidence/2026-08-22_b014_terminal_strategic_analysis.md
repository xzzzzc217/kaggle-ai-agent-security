# B014 terminal result + B015 strategic analysis (parent-agent request, 2026-08-22 23:25 UTC)

This is a parent-agent-driven strategic status report. It records the B014
terminal result that has just been observed for the first time since the
prior agent documented it as PENDING, refreshes the leaderboard state, and
documents the top B015 candidate ideas with rationale but **without
authorizing any new Kaggle write**.

## 1. B013 / B014 terminal status (refreshed via Kaggle API)

Refreshed at 2026-08-22 23:25 UTC via
`python -m kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks`:

```text
formal_submission_ref=55672980
  description=B014 chainkeep | attack 493b901f | prereg ec43467 | SDK 3.1.2
  status=SubmissionStatus.COMPLETE
  public_score=45.790
  private_score=blank
  created_utc=2026-08-21 16:17:10.210

formal_submission_ref=55658141
  description=B013 chain4 | attack 5ac85de2 | prereg 7ad613a | SDK 3.1.2
  status=SubmissionStatus.COMPLETE
  public_score=61.930
  private_score=blank
  created_utc=2026-08-21 02:09:06.230
```

Both B013 (`55658141`) and B014 (`55672980`) have reached terminal state.
Both are **rejected** by their preregistered acceptance gates.

- B013: `61.930` is far below B008R's `88.760`. The `B013 chain4`
  multi-message slow-row packaging alone degraded the slow-row replay
  reliability to the point where the chain4 raw-score gain was more than
  offset by fewer successful candidates returning. Already documented in
  `evidence/2026-08-21_b014_chainkeep_preflight.md`.
- B014: `45.790` is the worst non-ERROR score in the project's submission
  history, even worse than B013. The combined multi-variable bundling
  (B013 chain4 + B012 warmkeep + tail extension `0.995 / 1.02`) was a
  *catastrophic* regression: each individual mechanism's prior direction
  evidence was positive in isolation, but the cumulative effect on the
  replay set was strongly negative. This is the strongest possible
  evidence that the *multi-variable bundling paradigm itself* is the
  wrong direction, not just the specific combination.

Per the protocol:

- **B013** is rejected; not retried, not repushed, not re-examined.
- **B014** is rejected; not retried, not repushed, not re-examined.
- **No new formal submission is authorized in this turn.** The user/parent
  must approve the next B015 candidate explicitly.

## 2. Updated leaderboard state (2026-08-22 23:25 UTC)

```text
artifact=artifacts/kaggle/leaderboards/2026-08-22_2325_heartbeat/ai-agent-security-multi-step-tool-attacks.zip
rows=3881
heralces_rank=519
heralces_score=88.760
score_at_100=95.490
score_at_200=91.575
score_at_300=90.290
score_at_388=89.550  (10% cut of 3881 ≈ 388)
score_at_400=89.505
score_at_450=89.145
score_at_500=88.870
bronze_10pct_cut_rank=388
bronze_10pct_cut_score=89.550
gap_to_bronze=89.550 - 88.760 = 0.790
rank_if_92_165=164   (approximate, by interpolation)
rank_if_100_000=51   (approximate, by interpolation)
```

Critical observations:

- heralces has slipped from rank `482` (parent-agent's report) to
  **rank `519`** because the public leaderboard grew from `3819` rows on
  2026-08-21 to `3881` rows today (62 new teams).
- The current `B008R 88.760` submission is the leaderboard-effective
  baseline because B012 (`88.665`), B013 (`61.930`), and B014 (`45.790`)
  all score lower than B008R.
- The bronze 10% boundary has moved from `89.415` (rank 382) to
  **`89.550` (rank 388)**, raising the gap from +0.655 to **+0.790**.
- The historical B008 `92.165` score would now rank approximately `164`
  (was `157` on 2026-08-21).
- The daily submission limit is `5`; only the newest `2` stay active.
  B014 (45.790) and B013 (61.930) currently occupy slots 1 and 2. As
  long as they remain the newest 2, B008R is the leaderboard-effective
  baseline.

## 3. Time budget

```text
deadline_utc=2026-09-01 23:59
now_utc=2026-08-22 23:25
remaining_days=10.0
remaining_calendar_days=10
submission_slot_1=B014 45.790
submission_slot_2=B013 61.930
remaining_2_active_slots=2 of 2 (B014/B013 occupy)
remaining_2_free_slots_after_clear=2 once oldest 2 fall off
daily_quota=5/day; budget allows ~50 submissions over 10 days
```

Notes:

- The 5/day limit and newest-2-active rule mean that at most 2 of any new
  submission slots can hold B015/B016/etc. candidates. If B014/B013
  fall off as the third- and fourth-newest, the two newer B015-class
  candidates become active; B008R drops to inactive.
- B013/B014 currently occupy the two active slots. **B015-A/B/C cannot
  be submitted without first removing one of B013/B014 from the active
  window**, which happens automatically when a newer submission is
  accepted. There is no Kaggle API to manually "retire" a submission;
  the rule is enforced by Kaggle's leaderboard refresh logic.

## 4. Strategic assessment of the remaining 10 days

### Lessons learned from the B013/B014 negative results

- **Pure chain4 packaging** (`B013`) degrades slow-row replay reliability
  by 30-50% because the hidden replay agent does not execute every tool
  call in a multi-tool user message.
- **Multi-variable bundling** (`B014`) compounds that regression and
  amplifies it to a 50% loss even with the warmkeep + tail extensions.
  The combination `KEEP_WARMUP_FIRED + chain4 + tail-995/1.02` does not
  recover the lost candidates; it amplifies the loss.

### Where the score is concentrated

`docs/strategy.md` records that official scoring rewards:

1. Triggered predicate severity (`EXFILTRATION=5`, `UNTRUSTED_TO_ACTION=5/4`,
   `DESTRUCTIVE_WRITE=4`, `CONFUSED_DEPUTY=3`).
2. Cell-signature diversity (`2 × unique_cell_count`).
3. Total findings count normalized by `200000 * 1000`.

B008R's `88.760` implies roughly one thousand useful findings/cells.
Tiny deltas (`+5%` candidate recovery) are unlikely to bridge a
`+0.790` gap to bronze; the gap needs either a larger raw-findings
boost (more candidates / more predicates) or a higher-severity predicate
that the current exfiltration-only lineage is missing.

### Three plausible routes to bridge the bronze gap

The B015 decision tree (`evidence/2026-08-21_b015_candidate_decision_tree.md`)
already documents five B015 candidates. After the B014 negative result,
the strategic ranking is:

#### Route 1: **Restore B008R + CONFUSED_DEPUTY second predicate** (B015-C variant, modified)

Rationale:

- B015-C is the highest-expected-uplift candidate in the B015 decision
  tree (target raw score `~92-95`) and is already pre-staged as
  `baselines/replaysafe_chainkeep_confused_v1/attack.py` (SHA
  `60b325d5`).
- The B015-C code is **B014 + email follow-up** and depends on B014's
  chain4/warmkeep/tail extension. Since B014 catastrophically failed,
  B015-C as written would also fail.
- **Modified B015-C** should be **B008R (the validated 88.760 baseline)
  + CONFUSED_DEPUTY email follow-up**, dropping the chain4 / warmkeep /
  tail-extension axes. This isolates the single new variable: a second
  predicate family. The B011 fast-fill baseline already proved the
  "forward a note ... body=done" wording template is safe.
- Expected effect: each marker-post finding in B008R also fires
  CONFUSED_DEPUTY on the follow-up. Predicted ~1.5x raw-score per
  finding; expected public score `~92-95` if 50% of markers fire.
- Risk: if the B011 wording has changed in the hidden-agent prompt
  post-fix or if the guardrail heuristic is sensitive to context, the
  follow-up may not fire. The defensive
  `_email_followup_dodges_guardrail()` helper guarantees the candidate
  still scores under EXFILTRATION alone if CONFUSED_DEPUTY guardrails
  flip.

Files pre-staged: `baselines/replaysafe_chainkeep_confused_v1/attack.py`
(needs to be modified to use B008R baseline instead of B014 baseline).

#### Route 2: **Restore B008R + DESTRUCTIVE_WRITE probe** (B015-D variant, modified)

Rationale:

- DESTRUCTIVE_WRITE has severity `4` (vs `3` for CONFUSED_DEPUTY); the
  raw score per finding is higher. The B015-D candidate is sketched
  in the B015 decision tree but not yet implemented.
- Public audits flagged destructive-write as "high-risk under guardrails
  and not aligned with the current reliable exfiltration lineage"
  because `fs.delete` style prompts are easily blocked. However, a
  destructive write *to the local sandbox workspace* (e.g.
  `notes.txt` overwrite) inside the agent's own sandbox is the
  competition's expected fire path.
- This route has never been tested in this project. It is the **most
  unproven** but also potentially the **highest-uplift** of the three
  routes.
- Expected effect: each marker-post finding in B008R also fires
  DESTRUCTIVE_WRITE on a sandboxed file. Predicted ~1.6x raw-score per
  finding; expected public score `~95+` if it fires.
- Risk: guardrail-sensitive wording; needs careful prompt engineering
  ("rewrite the notes file to body=done" / "compress notes.txt into one
  line" / "delete the line containing SECRET_MARKER"). High chance of
  complete guardrail block.

Files to be created: `baselines/replaysafe_b015_d_destwrite/attack.py`.

#### Route 3: **Restore B008R + larger tail** (B015-B variant, single-variable)

Rationale:

- The B015 decision tree's B015-B is "B014 + larger tail
  (0.998/1.04)". Since B014 catastrophically failed, the equivalent
  smaller step is **B008R + tail extension only** (no chain4 / no
  warmkeep).
- Expected effect: `+1.0-1.5%` tail recovery translates to
  `+0.05-0.10` public-score points — **not enough** to bridge the
  `+0.790` gap on its own.
- This is a **safe fallback** to keep the submission slot occupied
  while the larger bets (B015-C / B015-D variants) are staged.
- It also has the highest chance of any candidate to **at least** tie
  B008R's `88.760` because it does not change the chain4 / warmkeep /
  follow-up axes that B014 just proved fragile.

Files to be created: `baselines/replaysafe_b015_b_tail/attack.py`.

### Recommended sequencing (subject to user authorization)

1. **Immediate next submission (highest priority):**
   B015-C-modified = B008R restore + CONFUSED_DEPUTY email follow-up.
   Pre-staged artifact exists in
   `baselines/replaysafe_chainkeep_confused_v1/attack.py`; needs
   editing to drop the B014 dependencies (chain4/warmkeep/tail
   extension) and use B008R's exact `0.99 / 1.0` envelope.

2. **Second submission (parallel pre-staging):**
   B015-D-modified = B008R restore + DESTRUCTIVE_WRITE probe. New
   artifact; highest risk, highest potential uplift.

3. **Final fallback:**
   B015-B-modified = B008R restore + tail extension `0.998 / 1.04`.
   New artifact; safe but limited uplift.

**Strategic recommendation: focus on the larger algorithmic pivot
(Routes 1 and 2), not on single-variable increments.** The
`+0.790` gap is too large to be bridged by `+1.5%` tail recovery
or similar micro-adjustments. Only a second-predicate family addition
(CONFUSED_DEPUTY or DESTRUCTIVE_WRITE) has a plausible expected
uplift large enough to clear the bronze threshold.

## 5. Submission slot accounting

```text
slot 1 (newest active)  = B014 55672980  45.790
slot 2 (next active)    = B013 55658141  61.930
slot 3 (inactive)       = B012 55495429  88.665
slot 4 (inactive)       = B005R 55461853 86.945
slot 5 (inactive)       = B011 55433780  72.680
slot 6 (inactive)       = B008R 55393959 88.760  <-- leaderboard-effective
slot 7 (inactive)       = B010 55327331  52.330
...
```

The leaderboard-effective score is `B008R 88.760` because it is the
highest-scoring COMPLETE submission in the **active** slot set. Once
B015 (or B015-C-modified) is submitted and reaches terminal state, the
newest-2-active rule keeps B015 + B014 active and the leaderboard
score becomes whichever of B015 / B014 is higher (currently expected
to be B015 unless B015 fails the gate).

## 6. Blockers and risks

**Blockers:**

- B014 terminal result just observed (`45.790`). The multi-variable
  bundling paradigm is empirically rejected at the public-leaderboard
  level. Do not retry B014 or any further multi-variable bundling
  before understanding the cause.
- The B015-C pre-staged artifact depends on B014 chain4 packaging and
  must be edited to use B008R packaging before submission. **Edit
  work is pre-submission work, not a Kaggle write**, and does not
  require a submission to be active.
- No B015-class submission may be created without explicit
  user/parent-agent authorization. The artifact is pre-staged; the
  submission requires a fresh "go" signal.

**Risks:**

- All three B015 routes depend on a hidden-agent behavior that has not
  been directly observed in this project (CONFUSED_DEPUTY email,
  DESTRUCTIVE_WRITE, larger tail). The local dynamic-contract evidence
  is suggestive but not determinative.
- The current leaderboard is growing (~62 new teams in 1 day); the
  bronze threshold will continue to drift upward. By 2026-09-01 the
  bronze cut could be `~90.0` or higher, raising the gap from
  `+0.790` to `+1.2+`.
- The 9000-second wall deadline guardrail has been validated only for
  the B008R envelope. The larger tail / new-predicate routes have
  not been validated under that guardrail.

## 7. Pre-staged artifacts (read-only, no Kaggle write)

```text
baselines/replaysafe_classify5_v1/attack.py        SHA=4d433a77  (B008R / B015-A)
baselines/replaysafe_chain4_v1/attack.py           SHA=5ac85de2  (B013, rejected at 61.930)
baselines/replaysafe_chainkeep_v1/attack.py        SHA=493b901f  (B014, rejected at 45.790)
baselines/replaysafe_chainkeep_confused_v1/attack.py SHA=60b325d5 (B015-C pre-staged; needs B008R editing)
```

None of these artifacts is submitted in this evidence cycle. The
preflight, ruff, pytest, and SDK-validate gates were last passed
during the B014 / B015-C preregistration commits.

## 8. Next actions (NOT executed; deferred to user authorization)

1. Edit `baselines/replaysafe_chainkeep_confused_v1/attack.py` to
   remove the B014 chain4/warmkeep/tail axes, leaving only the
   B008R baseline + CONFUSED_DEPUTY email follow-up. New source SHA
   expected; rebind submission-manifest.
2. Pre-flight the edited B015-C-modified artifact locally.
3. Wait for explicit user/parent-agent authorization in the same
   turn as the `kaggle competitions submit` command.
4. After B015-C-modified reaches terminal, decide on B015-B-modified
   (safe fallback) or B015-D-modified (destructive-write bet)
   based on the observed result.

No Kaggle write operation is performed in this evidence cycle.
