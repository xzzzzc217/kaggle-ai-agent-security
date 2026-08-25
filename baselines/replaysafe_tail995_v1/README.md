# replaysafe_tail995_v1

Single-variable B008R child. Extends the replay-safe returned-candidate
tail from 0.99 to 0.995.

## Single-variable change versus B008R

- ``REPLAY_SAFE_FRAC = 0.995`` (B008R was ``0.99``).
- ``SLOW_MULTIPOST_N = 4`` (unchanged; B017's 6 is rejected).
- ``FAST_USE_FRAME`` is not introduced (B018 is rejected).
- Classification still uses plain ``TEMPLATE``.
- Slow-row still uses the four-endpoint forge plan.
- One user message per candidate. No second-predicate follow-up.
