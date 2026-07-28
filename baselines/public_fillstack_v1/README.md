# B002 public fill-stack reference

This candidate adapts the public Kaggle Notebook
[`pilkwang/ai-agent-v3-1-2-single-post-exfiltration`](https://www.kaggle.com/code/pilkwang/ai-agent-v3-1-2-single-post-exfiltration).
It is a reference reproduction, not an originality claim.

The selected public snapshot described the following throughput stack:

- pay and discard one cold-start interaction;
- probe eight single-post wordings five times at one tool hop;
- retain only attempts that actually produced a marker-bearing `http.post`;
- choose the wording with the highest measured raw score per second;
- estimate forced full-hop replay cost with a published `1.43` multiplier;
- return only the selected wording and stop at `99.5%` of the replay budget.

The repository-specific safety adaptation replaces arbitrary `.co` destinations
with unique RFC-reserved `*.invalid` hosts. The competition SDK's `http.post`
handler is fixture-backed and does not perform real network I/O.

The upstream author's leaderboard score is provenance only. B002 must be judged
from this account's own competition rerun relative to B001 (`65.340`).
