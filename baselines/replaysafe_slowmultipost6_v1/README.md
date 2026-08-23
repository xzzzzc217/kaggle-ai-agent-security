# replaysafe_slowmultipost6_v1

Single-variable B008R child that widens the slow-row frame from four
endpoints to six. Each slow-row candidate remains **one user message**.

## Single-variable change versus B008R

- ``SLOW_MULTIPOST_N = 6`` (B008R was ``4``).
- ``REPLAY_SAFE_FRAC = 0.99`` (unchanged).
- ``REPLAY_BUDGET_MULT = 1.0`` (unchanged).
- ``SPLIT_CLASSIFY_N = 5`` (unchanged).
- ``KEEP_WARMUP_FIRED`` is not introduced.
- No extra user-message follow-up (B015-C / B016 axes are not inherited).
- Reserved ``*.invalid`` URL policy is preserved.

B004 already showed that widening the slow-row frame *inside one message*
raises score. B013/B014/B015-C showed that splitting the same work across
extra user messages collapses replay. B017 therefore stays on the B004 axis.
