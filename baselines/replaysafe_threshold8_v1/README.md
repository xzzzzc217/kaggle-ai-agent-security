# B006 replay-safe threshold8 candidate

B006 is a single-variable child of B005. It keeps B005's replay-safe tail
(`REPLAY_SAFE_FRAC=0.99`), slow-row four-endpoint forge plan
(`SLOW_MULTIPOST_N=4`), probe hops, replay-cost coefficient, prompt templates,
and unique `*.invalid` reserved hosts unchanged.

The only intended behavioral change is lowering the latency split threshold:

```text
SPLIT_THRESHOLD_S: 12.0 -> 8.0
```

This tests whether rows with medium observed latency should be routed into the
frame / slow-row multi-post branch instead of remaining on the plain single-post
template. It is a routing-boundary hypothesis, not a prompt or replay-tail
tuning change.
