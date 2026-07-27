"""Time-bounded wrapper around the competition SDK's Go-Explore attacker.

The wrapped search operates only through the competition-provided offline
environment. This module does not add network access or external destinations.
"""

import glob
import sys
from pathlib import Path

# The competition dataset contains kaggle_evaluation/ and aicomp_sdk/ at its root.
for candidate in glob.glob("/kaggle/input/**/kaggle_evaluation", recursive=True):
    dataset_root = str(Path(candidate).parent)
    if dataset_root not in sys.path:
        sys.path.insert(0, dataset_root)
    break

from aicomp_sdk.attacks import AttackAlgorithmBase, AttackRunConfig  # noqa: E402
from aicomp_sdk.attacks.baselines.attacker_goexplore import (  # noqa: E402
    AttackAlgorithm as GoExploreAttackAlgorithm,
)


class AttackAlgorithm(AttackAlgorithmBase):
    """Run the SDK Go-Explore search with a hard-deadline safety reserve."""

    maximum_search_s = 900.0
    search_fraction = 0.80

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.search = GoExploreAttackAlgorithm(config)

    def run(self, env, config: AttackRunConfig):
        total_budget_s = float(config.time_budget_s)
        if total_budget_s <= 0:
            raise ValueError("time_budget_s must be positive")

        delegated_budget_s = max(
            1.0,
            min(self.maximum_search_s, total_budget_s * self.search_fraction),
        )

        delegated_config = AttackRunConfig(
            time_budget_s=delegated_budget_s,
            max_steps=config.max_steps,
            max_tool_hops=config.max_tool_hops,
        )
        return self.search.run(env, delegated_config)
