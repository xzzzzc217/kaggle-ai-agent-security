# B004 slow-row multi-post variant

B004 is a single-variable child of B003. It keeps the public replay-safe split
stack from [`nctuan/jed-v25`](https://www.kaggle.com/code/nctuan/jed-v25) and the
project's `*.invalid` safety adaptation, but changes the default slow-row
multi-post count from `1` to `4`.

The parent B003 stack remains:

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

The B004 behavioral delta is limited to the slow branch after latency
classification. When the row is classified as slow, B004 emits one candidate that
asks for four ordered `http.post` calls to four unique `*.invalid` hosts instead
of one single-post frame candidate.

Direct comparison is B003 submission `55123773`, Public Score `81.585`. B004
must be preregistered, tested, SDK-validated, hash-pinned, and checked for
historical duplication before any Kaggle Notebook or competition submission.
