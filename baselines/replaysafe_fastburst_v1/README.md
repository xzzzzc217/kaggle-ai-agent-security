# B007 replay-safe fast-burst

Single-variable child of `baselines/replaysafe_tail99_v1/attack.py`.

The only intended behavioral change is `FAST_BURST_K: 1 -> 2` for the
post-classification fast/plain branch. B005's latency threshold, replay-safe
tail, slow-row `SLOW_MULTIPOST_N=4` frame plan, probe hops, replay-cost
accounting, and `*.invalid` reserved destinations stay fixed.

This candidate tests whether the fast/plain row can profit from two direct
`http.post` calls per validated candidate without sacrificing the slow-row
mechanism that survived through B005.
