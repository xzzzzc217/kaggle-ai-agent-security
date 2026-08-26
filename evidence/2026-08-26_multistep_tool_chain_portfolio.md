# Multi-step tool-chain portfolio baseline (B021-staged)

This is **not** a competition submission. B020 `55784609` is still
pending. The file exists so the repository can show the competition's
actual threat model instead of only the B008R one-message exfil factory.

## Why this exists

B008R is the leaderboard-effective floor (`88.760`) and is easy to
explain, but it is a single user message that asks for `http.post`.
The competition is named Multi-Step Tool Attacks. Scoring also rewards
`unique_cell_count` over tool sequences and untrusted sources
(`web` / `email`), which B008R never touches.

B013–B016 already showed that gluing extra user messages onto EXFIL
candidates destroys replay. B020 only spends a 5% leftover on one-shot
web/inbox prompts. This baseline is the first JED-envelope child that
makes the tool chain first-class.

## New mechanisms (previously unimplemented on the JED stack)

1. **One-shot untrusted chain**: one user message asks the agent to
   search/open fixture web or inbox content and follow that content.
   Live keep requires untrusted tools then a SHARE/WRITE sink.
2. **Two-turn UTA**: discover, then a last user message with no
   `send` / `email` / `upload` / `save` / `write`, so
   `UNTRUSTED_TO_ACTION` and `CONFUSED_DEPUTY` can still fire.
3. **Snapshot branching**: `env.snapshot` after discover, several
   follow-ups via `restore`. Official starter used this; B008R never did.
4. **EXFIL floor**: remaining replay-safe budget still runs unchanged
   B008R classify5 / four-endpoint forge. Multi-step messages are
   disjoint, not piggybacks.

## Identity

```text
path=baselines/multistep_tool_chain_v1/attack.py
sha256=d7cdfeb3a1b450bd3717438522a77add2f6eb72eb546595960dc90d75407a022
size=21106
parent=B008R
MULTISTEP_REPLAY_FRAC=0.20
REPLAY_SAFE_FRAC=0.99
SLOW_MULTIPOST_N=4
SPLIT_CLASSIFY_N=5
```

## Local gates

```text
ruff check/format: PASS
pytest tests/test_multistep_tool_chain.py: 6 passed
pytest full: 189 passed in 90.12s
preflight: PASS sha256=d7cdfeb3a1b450bd3717438522a77add2f6eb72eb546595960dc90d75407a022
SDK validate redteam: PASS
```

## Decision

- Keep in the repository as the multi-step portfolio algorithm.
- Do not push a Notebook or create a competition submission until B020
  `55784609` is terminal and a B021 preregistration is written.
- Parent for any later submit remains B008R unless B020 public score is
  `>88.760`.
