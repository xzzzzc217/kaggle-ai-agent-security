# B008 replay-safe classify5

Single-variable child of `baselines/replaysafe_tail99_v1/attack.py`.

The only intended behavioral change is `SPLIT_CLASSIFY_N: 8 -> 5`. B005's
latency threshold, replay-safe tail, slow-row `SLOW_MULTIPOST_N=4` frame plan,
probe hops, replay-cost coefficient, prompt templates, and reserved `.invalid`
destinations stay unchanged.

This tests whether reducing the plain latency-classification overhead can shift
three additional slow-row candidates into the already validated four-endpoint
frame plan without repeating the failed B006 threshold change or B007 direct
burst change.
