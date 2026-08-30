# B023 allforge preregistration

User authorized a **new route** after envelope knobs, host-suffix, and
wording families were exhausted.

## Route

B008R spends five live slots on plain single-post classification, then
four-endpoint forge only on the slow row. B023 sets `ALWAYS_FORGE=True`:
every live-validated and returned candidate is the reserved-domain
four-endpoint analysis-channel forge. No fast-row 1-post path.

```text
candidate_id=B023-allforge
candidate_path=baselines/replaysafe_allforge_v1/attack.py
candidate_sha256=1d2b15548795417ca9cb05235781513e8e6369eba2506b274055c44a23bb4755
candidate_size_bytes=11174
parent_id=B008R
parent_public_score=88.760
single_variable=ALWAYS_FORGE
old_value=implicit False (classify then maybe forge)
new_value=True (every candidate is forge4)
hosts=http://{label}.invalid
```

Not a wording, Notify, UTA carve, tail, width, or `.example.com` change.
gpt-oss Q4 probe already showed forge4 4/4 full-fire. Gemma is untested;
that is the main risk.

## Local gates

```text
ruff check/format: PASS
pytest tests/test_replaysafe_allforge.py: 5 passed
pytest full: 209 passed in 92.54s
preflight: PASS sha256=1d2b15548795417ca9cb05235781513e8e6369eba2506b274055c44a23bb4755 size=11174
SDK validate redteam: PASS
```

## Acceptance gates

| B023 terminal | Decision |
|---|---|
| COMPLETE and `>88.760` | New floor; keep |
| COMPLETE and `>=90.585` | Bronze-cut chase on the 2026-08-30 snapshot |
| COMPLETE and `<=88.760` | Reject; keep B008R |
| ERROR / blank / unsafe | Reject |

Do not retry B023. Private pair stays B008R `55393959` + B012
`55495429` unless public score is `>88.760`.
