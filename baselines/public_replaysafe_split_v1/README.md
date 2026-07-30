# B003 public replay-safe split reference

This candidate adapts the public Kaggle Notebook
[`nctuan/jed-v25`](https://www.kaggle.com/code/nctuan/jed-v25). It is a
reference reproduction, not an originality claim.

The selected public snapshot uses this stack:

- pay and discard one cold-start interaction;
- validate-fill candidates against the live environment;
- keep only marker-bearing `http.post` attempts that actually fire;
- classify the current model row by early latency;
- use a Harmony control-token frame for the slow row and the plain verbose
  template for the fast row;
- size returned candidates by measured replay cost instead of a flat fill
  deadline.

The repository-specific safety adaptation replaces arbitrary `.co`
destinations with unique RFC-reserved `*.invalid` hosts. The competition SDK's
`http.post` handler is fixture-backed and does not perform real network I/O.

B003 is prepared while B002 is still pending. It should not be submitted until
B002 has a terminal public score and a fresh preregistration fixes the direct
comparison threshold.
