# replaysafe_fastharmony_v1

Single-variable B008R child. After latency classification, fast-row
single-post candidates use the analysis-channel `FRAME_TEMPLATE` instead
of plain `TEMPLATE`.

## Single-variable change versus B008R

- ``FAST_USE_FRAME = True`` (new).
- ``SLOW_MULTIPOST_N = 4`` (unchanged; B017's 6 is rejected).
- Classification still uses plain ``TEMPLATE``.
- Slow-row still uses the four-endpoint forge plan.
- ``REPLAY_SAFE_FRAC = 0.99`` (unchanged).
- One user message per candidate. No second-predicate follow-up.
