"""Unit tests for the adaptive scheduler without the competition-only SDK."""

import importlib.util
import sys
import types
from pathlib import Path

import pytest

ATTACK_PATH = Path("baselines/adaptive_budget_v1/attack.py")


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture
def attack_module(monkeypatch: pytest.MonkeyPatch):
    attacks = types.ModuleType("aicomp_sdk.attacks")
    attacks.AttackAlgorithmBase = type("AttackAlgorithmBase", (), {})
    attacks.AttackCandidate = type("AttackCandidate", (), {})
    attacks.AttackRunConfig = type("AttackRunConfig", (), {})

    predicates = types.ModuleType("aicomp_sdk.core.predicates")
    predicates.eval_predicates = lambda trace: []
    core = types.ModuleType("aicomp_sdk.core")
    sdk = types.ModuleType("aicomp_sdk")

    monkeypatch.setitem(sys.modules, "aicomp_sdk", sdk)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks", attacks)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core", core)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core.predicates", predicates)

    spec = importlib.util.spec_from_file_location("adaptive_budget_attack", ATTACK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fast_observations_reduce_the_conservative_default(attack_module) -> None:
    clock = FakeClock()
    controller = attack_module.BudgetController(300, clock=clock, default_step_s=60)

    started_at = clock()
    clock.advance(10)
    controller.record_attempt(started_at, 1)

    assert controller.estimated_step_s() == pytest.approx(13.5)
    assert controller.can_start(2)


def test_slow_observation_prevents_an_unsafe_next_attempt(attack_module) -> None:
    clock = FakeClock()
    controller = attack_module.BudgetController(300, clock=clock, default_step_s=60)

    started_at = clock()
    clock.advance(120)
    controller.record_attempt(started_at, 1)

    assert controller.estimated_step_s() == pytest.approx(162)
    assert not controller.can_start(1)


def test_adaptive_policy_uses_more_budget_than_fixed_starter_margin(attack_module) -> None:
    clock = FakeClock()
    controller = attack_module.BudgetController(220, clock=clock, default_step_s=60)
    adaptive_attempts = 0

    while controller.can_start(1):
        started_at = clock()
        clock.advance(10)
        controller.record_attempt(started_at, 1)
        adaptive_attempts += 1

    fixed_margin_attempts = 0
    fixed_time_left = 220
    while fixed_time_left >= 180:
        fixed_time_left -= 10
        fixed_margin_attempts += 1

    assert adaptive_attempts > fixed_margin_attempts
    assert controller.time_left_s() >= controller.reserve_s


@pytest.mark.parametrize("interaction_count", [0, -1])
def test_invalid_interaction_counts_are_rejected(attack_module, interaction_count: int) -> None:
    controller = attack_module.BudgetController(300, clock=FakeClock())

    with pytest.raises(ValueError):
        controller.estimated_attempt_s(interaction_count)
