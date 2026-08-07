# B010 replay-safe slow-commentary

Single-variable child of B008 `baselines/replaysafe_classify5_v1/attack.py`.

The only intended behavior change is the slow-row frame-plan channel:

- B008 slow frame: `<|channel|>analysis<|message|>`
- B010 slow frame: `<|channel|>commentary<|message|>`

B008 constants and routing are otherwise unchanged: `SPLIT_CLASSIFY_N=5`,
`SPLIT_THRESHOLD_S=12.0`, `REPLAY_SAFE_FRAC=0.99`, `SLOW_MULTIPOST_N=4`,
`BURST_K=1`, `PROBE_HOPS=0`, replay-cost coefficient, and `*.invalid`
reserved URLs.
