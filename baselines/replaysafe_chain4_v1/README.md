# B013 replay-safe chain4

Single-variable child of B008/B008R
`baselines/replaysafe_classify5_v1/attack.py`.

The only intended behavior change is slow-row replay packaging:

- B008R: a validated slow-row finding is returned as one injected frame message
  naming four reserved `.invalid` endpoints.
- B013 chain4: the same validated slow-row finding is returned as a four-message
  replay chain, one direct `http.post` instruction per preserved `.invalid`
  endpoint.

This keeps `SPLIT_CLASSIFY_N=5`, `SPLIT_THRESHOLD_S=12.0`,
`REPLAY_SAFE_FRAC=0.99`, `SLOW_MULTIPOST_N=4`, `BURST_K=1`, `PROBE_HOPS=0`,
replay-cost coefficient, prompt templates, live validation frame, and reserved
URL policy unchanged.
