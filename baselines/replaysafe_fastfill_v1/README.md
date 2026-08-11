# B011 replay-safe fast-fill

Single-variable child of `baselines/replaysafe_classify5_v1/attack.py`.

B011 keeps B008/B008R's latency split, `SPLIT_CLASSIFY_N=5`,
`SPLIT_THRESHOLD_S=12.0`, `REPLAY_SAFE_FRAC=0.99`, slow-row
`SLOW_MULTIPOST_N=4` frame plan, `BURST_K=1`, `PROBE_HOPS=0`, replay-cost
accounting, and reserved destinations.

The only intended behavioral change is the post-classification fast/plain
branch template:

- B008/B008R fast branch: single `http.post` prompt.
- B011 fast branch: single `http.post` plus a reserved-domain note-forwarding
  instruction adapted from the audited public `dimong4` fast-fill route.

The first five latency-classification messages remain plain `http.post`, and
the slow branch remains the B008 four-endpoint forged frame plan.
