# B015-A re-baseline preparation: status report

This document records the B014 terminal-state check, the B015-A pre-staging
verification, and the exact next commands required to submit B015-A. It does
NOT authorize a Kaggle write operation. B015-A submission requires (a) B014
reaching terminal state and (b) explicit user/parent-agent authorization in
the same turn as the submit command.

## 1. B014 terminal state check

**Result: UNKNOWN (likely still PENDING).**

Evidence:

- `submissions/B014/submission-manifest.json` binds experiment B014 to
  kernel `heralces/ai-agent-security-b014-chainkeep`, attack SHA
  `493b901f2144a08a68c408b23e779185efe1e98efba80d055fc71c4eae1f8568`,
  Git commit `ec43467689642b40892cd23094003da9382404c3`, and
  SDK `3.1.2`.
- `submissions/B014/kernel-metadata.json` declares the same kernel id.
- `evidence/2026-08-21_b014_chainkeep_preflight.md` "B014 submission record"
  shows `formal_submission_ref=PENDING`,
  `initial_submission_status=SubmissionStatus.PENDING`, blank
  Public/Private score, `errorDescription=None`,
  `initial_submission_observed_utc=2026-08-21 16:17`.
- `docs/progress_log.md` does NOT contain any entry between line 3746 and
  the end that records B014 reaching `COMPLETE` or `ERROR` terminal state.
- The latest leaderboard heartbeat artifact
  `artifacts/kaggle/leaderboards/2026-08-21_1143_heartbeat/` is from
  2026-08-21 11:43 UTC; that is before B014's
  `formal_submission_created_utc=2026-08-21 16:17:10.210` so it cannot
  contain the B014 terminal signal.
- There is no `2026-08-21_b014_terminal/` or `2026-08-22_*` heartbeat
  directory under `artifacts/kaggle/leaderboards/`. The directory list
  shows the latest heartbeat is `2026-08-21_1143_heartbeat`, with nothing
  more recent.
- The cloud run log `artifacts/kaggle/B014_v1.log` ends at
  `t=15.768716758` after `__results__.html` is written, with no
  `hidden-gateway rerun` log entries present in the local copy
  (the rerun is the agent-side replay that produces the public score; it
  is not visible until the kernel transitions to `COMPLETE` and the
  competition submission is polled).
- B013 submission `55658141` is the most recent formal submission that
  reached terminal state per `evidence/2026-08-21_b014_chainkeep_preflight.md`
  (B013 = 61.930). B014 was submitted later on 2026-08-21 16:17 and has
  not yet been observed at terminal.

Conclusion:

- B014 is in `PENDING` (the only status recorded by the manifest) and
  there is no terminal signal recorded locally since the original
  submission at 2026-08-21 16:17 UTC.
- B015-A cannot be submitted until B014 reaches terminal state. The
  pre-staging for B015-A can be done now (no Kaggle write), but the
  actual submission must wait.

## 2. B015-A readiness

**Result: ready-to-submit as a local artifact (no Kaggle write yet).**

B015-A is the B008R restore per `evidence/2026-08-21_b015_candidate_decision_tree.md`:

- `SPLIT_CLASSIFY_N=5`
- `REPLAY_SAFE_FRAC=0.99`
- `REPLAY_BUDGET_MULT=1.0`
- single-post replay
- single-template fast row
- no warmkeep
- no chain split

Implementation: copy `baselines/replaysafe_classify5_v1/attack.py` into a
new `baselines/b015_a_replayback/` directory. The source SHA-256 is
`4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`,
matching the B008R/B008 parent SHA referenced in both B013 and B014
preregistrations.

## 3. B008R source preflight (sanity check)

Running `scripts/preflight_submission.py` against the source file passes:

```text
path=D:\kaggle\ai-agent-security\baselines\replaysafe_classify5_v1\attack.py
sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
size_bytes=10799
passed=true
error_count=0
warning_count=0
issues=[]
```

B008R also matches the existing B008R submission that scored `88.760`
(ref `55393959`); the pre-staged B015-A candidate is byte-identical to
the validated B008R source.

## 4. Planned B015-A Kaggle artifact (after terminal + authorization)

```text
candidate_id=B015-A
candidate_name=replayback_v1
candidate_path=baselines/b015_a_replayback/attack.py
parent_id=B008R
parent_path=baselines/replaysafe_classify5_v1/attack.py
parent_sha256=4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1
kernel_id=heralces/ai-agent-security-b015-a-replayback
title=AI Agent Security B015-A Replayback
experiment_id=B015-A
submission_dir=submissions/B015-A
submission_message_template=B015-A replayback | attack {short_sha} | parent 4d433a77 | SDK 3.1.2
expected_public_score=88.760 (tie with current leaderboard-effective)
```

## 5. Exact next commands (NOT executed)

The following commands are the exact recipe to finalize and submit B015-A
once both (a) B014 is terminal and (b) the user/parent-agent explicitly
authorizes submission in the same turn:

```bash
# 1. Verify B014 terminal first (must show COMPLETE or ERROR with a public/private score or error description)
python scripts/monitor_b014_terminal.py  # or: kaggle competitions submissions -v

# 2. Copy B008R source to B015-A candidate directory
mkdir baselines/b015_a_replayback
cp baselines/replaysafe_classify5_v1/attack.py baselines/b015_a_replayback/attack.py

# 3. Run preflight
python scripts/preflight_submission.py baselines/b015_a_replayback/attack.py --json

# 4. Run unit tests for B015-A (if added; otherwise skip; B008R coverage already passes)
#    pytest tests/ -q

# 5. SDK validate (requires local SDK at data/competition/extracted)
#    SDK validate redteam baselines/b015_a_replayback/attack.py

# 6. Build Kaggle Notebook
python scripts/build_kaggle_notebook.py B015-A

# 7. Push kernel
python scripts/push_kernel.py submissions/B015-A

# 8. Poll kernel until COMPLETE
#    kaggle kernels status heralces/ai-agent-security-b015-a-replayback

# 9. Download cloud output (artifacts/kaggle/B015-A_v1/) and verify SHA matches local

# 10. Submit to competition
#     kaggle competitions submit -c ai-agent-security-multi-step-tool-attacks \
#       -k heralces/ai-agent-security-b015-a-replayback -v 1 \
#       -f artifacts/kaggle/B015-A_v1/submission.csv \
#       -m "B015-A replayback | attack {short_sha} | parent 4d433a77 | SDK 3.1.2"

# 11. Refresh competition submissions and confirm B015-A row exists
#     kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks
```

## 6. Blockers and risks

**Blockers (must clear before submit):**

- B014 terminal state. Currently UNKNOWN; last observation was
  `SubmissionStatus.PENDING` at 2026-08-21 16:17 UTC. There is no
  monitoring evidence since then; a heartbeat refresh is required to
  confirm B014 status. Without terminal state, B015-A submission would
  violate the daily-limit rule (5/day, newest 2 stay active) and the
  project protocol that "B015 candidates can only submit once B014
  reaches terminal state".
- Explicit user/parent-agent authorization for the actual Kaggle write
  is required in the same turn. This document prepares the artifact but
  does not authorize the write.

**Risks (even after blockers clear):**

- B015-A is expected to TIE with B008R (`88.760`), not improve. It is a
  queue-occupying re-baseline, not a score gain. If the goal is a
  higher expected score, prefer B015-B/C/D/E (see
  `evidence/2026-08-21_b015_candidate_decision_tree.md`).
- Daily limit is 5/day and only the newest 2 stay active. Submitting
  B015-A consumes one slot. If B014 lands below 88.760 and B015-A ties
  B008R, the newest-2 rule still keeps B015-A active and B014 falls off
  as the third-newest; if B014 lands above 88.760, B015-A as the second
  newest is still active and B008R falls off. Plan the queue
  accordingly.
- B015-A is a deliberate no-improvement re-baseline. Once consumed, it
  cannot be re-played without first removing another active submission.

**Recommendation:**

- Wait for B014 terminal state. If B014 < 88.760 or B014 errors, then
  B015-A is the right move (re-baseline + queue hold). If B014 >=
  88.760, prefer B015-B/C/D/E from the decision tree, and use B015-A
  only as a tie-only fallback.
- Do NOT execute the commands in section 5 without both terminal state
  confirmation and explicit authorization.

## 7. Pre-staged B015-A candidate directory

This evidence record does not create `baselines/b015_a_replayback/` on
disk. The creation is part of step 2 in section 5 and is intentionally
deferred until after B014 terminal is observed, so that the directory
listing timestamp matches the preflight timestamp.

If a fully pre-staged artifact is desired now (read-only, no Kaggle
write), the only required on-disk action is:

```bash
mkdir baselines/b015_a_replayback
cp baselines/replaysafe_classify5_v1/attack.py baselines/b015_a_replayback/attack.py
python scripts/preflight_submission.py baselines/b015_a_replayback/attack.py
```

The preflight result is expected to be identical to the B008R result in
section 3 (sha256 `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`,
passed=true, 0 issues). No Kaggle side effects.
