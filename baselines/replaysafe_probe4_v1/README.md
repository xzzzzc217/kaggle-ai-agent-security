# B009 replay-safe probe4

Single-variable child of `baselines/replaysafe_classify5_v1/attack.py`.

The only intended behavioral change is `PROBE_HOPS: 0 -> 4`, where `0` means
probing at the grader-provided hop cap. B008's `SPLIT_CLASSIFY_N=5`, latency
threshold, replay-safe tail, slow-row `SLOW_MULTIPOST_N=4` frame plan,
replay-cost coefficient, prompt templates, and reserved `.invalid` destinations
stay unchanged.

This tests whether validating the already proven four-endpoint slow-row frame
plan with exactly four tool hops can skip scoring-irrelevant wrap-up work while
still exercising every intended `http.post` endpoint during the live fill. It
does not repeat the failed B006 threshold change, B007 direct burst, or B008
classification-batch change.
