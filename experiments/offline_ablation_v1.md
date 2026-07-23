# Offline ablation v1

This report compares the four committed `attack.py` variants in one deterministic,
SDK-free fixture harness. It is mechanism evidence, **not a Kaggle score**.

The harness advances a fake clock by 10 seconds for every `env.interact`, evaluates the
same fixture-backed tool traces, and independently cold-replays every returned
`AttackCandidate.user_messages`.

## Tight budget: all candidates replay

Budget: 220 seconds.

| Variant | Interactions | Findings | Unique tool mechanisms | Remaining seconds |
|---|---:|---:|---:|---:|
| Official starter | 4 | 4 | 2 | 180 |
| Adaptive budget (E001) | 12 | 9 | 4 | 100 |
| Novelty scheduler (E002) | 12 | 8 | 4 | 100 |
| Snapshot replay gate (E003) | 15 | 8 | 4 | 70 |

Observed mechanism claim: replacing fixed 180/360-second margins allowed three times as
many interactions while retaining a positive reserve. Novelty scheduling traded one
duplicate finding for the same four-mechanism coverage.

## Snapshot discovery succeeds but cold replay fails

Budget: 900 seconds.

| Variant | Returned findings | Unreplayable findings | Unique tool mechanisms |
|---|---:|---:|---:|
| Official starter | 9 | 3 | 4 |
| Adaptive budget (E001) | 9 | 3 | 4 |
| Novelty scheduler (E002) | 8 | 2 | 4 |
| Snapshot replay gate (E003) | 6 | 0 | 4 |

Observed replay claim: E003 rejected all snapshot-only successes while preserving the
four replayable mechanisms. The lower raw finding count is intentional; the evaluator
cannot score candidates that fail fresh replay.

## Reproduction

```powershell
.\.venv\Scripts\python.exe .\scripts\offline_ablation.py `
  --output .\experiments\offline_ablation_v1.json
```

Machine-readable evidence is stored in
[`offline_ablation_v1.json`](offline_ablation_v1.json). Each row binds results to the
SHA-256 digest of the evaluated `attack.py`.

## Limits

- The fake traces cover only the tool shapes already present in the starter candidates.
- Model behavior, guardrails, hidden fixtures, and competition runner overhead are not
  simulated.
- These results justify which mechanisms deserve SDK evaluation; they cannot establish
  leaderboard improvement.
