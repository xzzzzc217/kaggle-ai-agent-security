# B001 public two-probe reference baseline

This candidate reproduces the public replay-dense single-post approach published in
[`tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery`](https://www.kaggle.com/code/tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery).
The source was downloaded on 2026-07-27 and is retained locally under the ignored
`data/public_notebooks/` research cache.

The upstream Notebook describes earlier Hosted scores of `88.515` and `89.055`. These
numbers are third-party provenance only. They are not this repository's Kaggle score and
must not be entered in the experiment ledger as a reproduced result.

Our adaptation makes one safety-focused change: candidate destinations are unique
subdomains of the RFC-reserved `example.com`, not arbitrary `.co` hosts. The evaluator's
`http.post` tool is fixture-backed and offline.

Mechanism:

- probe five wordings twice at the evaluator's full hop limit;
- retain only attempts whose trace contains a scored predicate or successful marker post;
- choose the lowest observed latency per successful attempt;
- fill unique reserved destinations while tracking a separate replay-cost ledger;
- cap the returned portfolio at 2,000 candidates and 99% of the 9,000-second replay budget.

This is a public reference baseline, not an originality claim. Any later project-specific
improvement must be registered as a separate experiment relative to its reproduced score.
