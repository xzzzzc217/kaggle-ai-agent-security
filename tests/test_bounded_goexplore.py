"""Tests for the hard-deadline reserve around SDK Go-Explore."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

ATTACK_PATH = Path("baselines/bounded_goexplore_v1/attack.py")


@pytest.fixture
def bounded_module(monkeypatch: pytest.MonkeyPatch):
    @dataclass(frozen=True)
    class AttackRunConfig:
        time_budget_s: float
        max_steps: int = 10**9
        max_tool_hops: int = 4

    class AttackAlgorithmBase:
        def __init__(self, config=None) -> None:
            self.config = dict(config or {})

    class GoExploreAttackAlgorithm:
        def __init__(self, config=None) -> None:
            self.config = dict(config or {})

        def run(self, env, config):
            env.append(config)
            return ["delegated"]

    attacks = types.ModuleType("aicomp_sdk.attacks")
    attacks.AttackAlgorithmBase = AttackAlgorithmBase
    attacks.AttackRunConfig = AttackRunConfig
    goexplore = types.ModuleType("aicomp_sdk.attacks.baselines.attacker_goexplore")
    goexplore.AttackAlgorithm = GoExploreAttackAlgorithm
    baselines = types.ModuleType("aicomp_sdk.attacks.baselines")
    sdk = types.ModuleType("aicomp_sdk")

    monkeypatch.setitem(sys.modules, "aicomp_sdk", sdk)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks", attacks)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks.baselines", baselines)
    monkeypatch.setitem(
        sys.modules,
        "aicomp_sdk.attacks.baselines.attacker_goexplore",
        goexplore,
    )

    spec = importlib.util.spec_from_file_location("bounded_goexplore_attack", ATTACK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def test_caps_long_search_at_fifteen_minutes(bounded_module) -> None:
    delegated = []
    config = bounded_module.AttackRunConfig(
        time_budget_s=1_800,
        max_steps=123,
        max_tool_hops=7,
    )

    findings = bounded_module.AttackAlgorithm().run(delegated, config)

    assert findings == ["delegated"]
    assert len(delegated) == 1
    assert delegated[0].time_budget_s == pytest.approx(900)
    assert delegated[0].max_steps == 123
    assert delegated[0].max_tool_hops == 7


def test_short_budget_reserves_twenty_percent_for_outer_deadline(bounded_module) -> None:
    delegated = []
    config = bounded_module.AttackRunConfig(time_budget_s=10)

    bounded_module.AttackAlgorithm().run(delegated, config)

    assert delegated[0].time_budget_s == pytest.approx(8)


def test_rejects_non_positive_budget(bounded_module) -> None:
    config = bounded_module.AttackRunConfig(time_budget_s=0)

    with pytest.raises(ValueError, match="time_budget_s must be positive"):
        bounded_module.AttackAlgorithm().run([], config)
