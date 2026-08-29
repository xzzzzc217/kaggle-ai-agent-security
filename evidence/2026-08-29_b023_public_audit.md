# B023 public-route audit (read-only)

After B022 `55832399` COMPLETE public `86.925` (reject vs B008R
`88.760`), this pass listed 120 public kernels by `dateRun` and pulled
18 current heads. It does **not** authorize a Kaggle Notebook or
competition submission.

Live board at B022 terminal (2026-08-29 00:36 UTC): 4164 teams,
heralces rank 694 / 88.760, bronze cut 90.410, nctuan 91.710.

## Pulled artifacts

Local copies live under
`artifacts/kaggle/public_audit/2026-08-29_b023_screen/`.

| ref | AttackAlgorithm | reserved host | overlap / decision |
|---|---|---|---|
| nctuan/jed-v25 | yes | `.co` | classify8, frac 0.97, n=1; parent of B003; forbidden TLD |
| nctuan/jed-slow-multipost | yes | `.co` | still `.co`; n=1/3 knobs already tested as B004/B017 |
| kaiwalyaatulraut/...solution | yes | `.co` | byte-same SHA as nctuan v25 |
| evgendvorkin/ai-agent | yes | `.co` | PHOENIX V84: classify5 (ours), n=8 (beyond rejected n=6), frac 0.99999 (beyond rejected 0.995), replay-safe sizing off |
| dimong4/ai-agent-security | yes | `.co` | classify5 + destructive + analysis frame; B007/B011/B016 family |
| coolin666/jed-attack-v12 | yes | `.co` | classify8, frac 0.90, n=2; rollback + forbidden TLD |
| verityix/...hitherto | yes | real TLDs | v298 `.ai/.pro/.xyz/.cloud/.app/.dev/.io/.org/.com/.net` |
| gouthamkonduru/twoforfamily | yes | `.co` + example.com | 8 multi-turn scenarios; `.co` collect; not a B008R child |
| koushikkumardinda/...exfil | yes | example.com | mutation searcher, no live EXFIL factory; not 88-class |
| ducnamphan/jed-v19-pure-exfil | yes | `.invalid` | static N=225 spray, self-est ~20 public; DWX/CDX mix |
| ducnamphan/jed-v21-best-combo | yes | `.invalid` | same static factory, 85/10/5 EXFIL/DWX/CDX |
| ducnamphan/jed-v18-cd-exfil | yes | `.invalid` | UTA probe + static fill; their v19 notes say UTA cut EXFIL |
| ducnamphan/jed-v17-precision-uta | yes | `.invalid` | two-turn UTA vs web_corpus; OptimalGuardrail denies |
| yuriymikityuk/taint-window-trap | no | n/a | SDK demo: plain post ALLOW, web→post DENY, secret delete DENY |
| antoniorotundo2/...searc | no | n/a | no AttackAlgorithm in pulled snapshot |
| lopure/relay-push100 | no | n/a | no top-level AttackAlgorithm in extracted cells |
| qyq1693/multiturn-v14 | yes | `.co` | multi-turn replacement |
| commencethescourge/baseline | yes | none | 222-byte stub |

## What the high-score public code actually does

- nctuan's **public** notebooks are still `http://{label}.co` with
  classify8 / tail 0.97 / single slow post. Their leaderboard 91.710
  is not explained by the public v25 snapshot (46 private submits).
- evgendvorkin is the closest JED-envelope cousin, but every aggressive
  knob is one we already lost: n=8 vs B017 n=6 (88.505), tail 0.99999
  vs B019 0.995 (87.470), and `.co`.
- The only reserved-domain (`.invalid`) executable family is
  ducnamphan: 20 natural-language templates, **https**, static 225
  candidates, optional delete/notify piggybacks. Their own comment
  estimates `N * 0.09 ≈ 20` public. That cannot replace B008R 88.760.
  Delete+post and notify+post are B016 / B021.

## Unused leftover on B008R

Scheme `http://` → `https://` on the existing `{label}.invalid` hosts.
ducnamphan uses https. B022 already showed that changing URL appearance
(`invalid` → `example.com`) cost 1.835 public points. Scheme-only is
the same family of host/URL surface changes, not a new mechanism.

No other leftover is a reserved-domain single-variable B008R child
outside rejected families (wording, extra messages, UTA carve, tail,
width, classify N, hops, channel, host suffix).

## Decision

- Do not preregister B023.
- Do not push a Notebook or create a competition submission.
- Keep B008R `88.760`. Private pair stays B008R + B012.
