# Novelty scheduler v1

This variant builds on `adaptive_budget_v1` and changes one additional mechanism:
candidate execution is scheduled in rounds by expected tool-call signature.

The first round covers each distinct source/transformation/sink mechanism once before
spending budget on paraphrases of a mechanism already tried. Successful traces are
normalized by tool name and argument *shape*, not literal values, and retained with a
small per-signature cap.

Why this should matter: the official metric explicitly rewards diversity through
`unique_cell_count`, while the private guardrail makes repeated variants of one public
mechanism a fragile strategy.

Status: locally unit-tested against representative trace shapes; SDK replay and Kaggle
score remain pending competition access.
