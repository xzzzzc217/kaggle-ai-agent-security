# multistep_tool_chain_v1

Portfolio / B021-staged candidate. Not a Kaggle submit while B020
`55784609` is pending.

B008R is a one-message exfil factory. This baseline adds the competition's
actual threat model as a first-class search family:

```text
untrusted source (web.search / web.open / email.list / email.read)
    -> tool chain
    -> SHARE / WRITE sink
```

## What is new versus B008R and B020

- **Two-turn UTA**: discover (open page / inbox item), then a second user
  message that only says to continue the checklist. The last message has no
  `send` / `email` / `upload` / `save` / `write`, so CONFUSED_DEPUTY and
  UNTRUSTED_TO_ACTION SHARE gates can still fire.
- **Snapshot branching**: one discover prefix, several follow-ups via
  `env.snapshot` / `env.restore`. Official starter used this; the JED
  envelope never did.
- **One-shot chains**: a larger web/inbox query bank than B020's 5% leftover.
- **EXFIL floor**: remaining replay-safe budget still runs the unchanged
  B008R classify5 / four-endpoint forge. Multi-step candidates are disjoint
  messages, not piggybacks on EXFIL.

## Budget

- ``REPLAY_SAFE_FRAC = 0.99`` (same envelope cap)
- ``MULTISTEP_REPLAY_FRAC = 0.20`` reserved for the tool-chain family
- EXFIL fill uses the remaining ``0.79``

Do not competition-submit until B020 is terminal and a fresh preregistration
fixes the acceptance gates.
