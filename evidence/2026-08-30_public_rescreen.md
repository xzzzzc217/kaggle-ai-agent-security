# 2026-08-30 public rescreen (no B023)

```text
now_utc=2026-08-30 01:26
rows=4183
heralces_rank=723
heralces_score=88.760
bronze_10pct_rank=418
bronze_10pct_score=90.585
gap=1.825
nctuan=91.710 rank 312
```

Newest dateRun heads vs 2026-08-29:

| ref | sha256[:16] | flags | decision |
|---|---|---|---|
| anasriaz/ai-agent-security | 4eda5d4836d59386 | `.co` classify8 frac 0.9999 n=6 deputy/DW | forbidden TLD + rejected knobs |
| ruhul20/red-team-... | 384f89efbb0cb85f | mixed `.co` / example.com / `.invalid`, multi-family | not a B008R child |
| evgendvorkin/ai-agent | ea9298feb69cc617 | `.co` classify8 n=10 frac 0.9999 | wider than rejected B017 n=6 |
| verityix/...hitherto | f417a405242a97d1 | public TLDs | unsafe |
| nctuan/jed-v25 | 614176a339e71b80 | unchanged `.co` classify8 n=1 | already parent of B003 |

Papers rechecked the same day (Framing Gap, Silent Egress sharding,
STAC, SoK agentic surface) still map onto refused families: wording,
web-then-sink UTA, extra messages, or real destinations.

ABC probe from 2026-08-29 already showed https is a wash and framing
is worse. No new reserved-domain single-variable B008R child.

Decision: do not submit. Freeze B008R. Advance Working Note and
private-pair confirmation.
