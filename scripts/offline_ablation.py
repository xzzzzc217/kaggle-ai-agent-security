"""Deterministic SDK-free ablation across all attack variants.

This harness is not a substitute for Kaggle evaluation. It isolates three engineering
claims before SDK access: budget utilization, mechanism diversity, and cold-replay
validity of snapshot-discovered candidates.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VARIANT_PATHS = {
    "official_starter_v17": Path("baselines/official_starter_v17/attack.py"),
    "adaptive_budget_v1": Path("baselines/adaptive_budget_v1/attack.py"),
    "novelty_scheduler_v1": Path("baselines/novelty_scheduler_v1/attack.py"),
    "snapshot_archive_v1": Path("baselines/snapshot_archive_v1/attack.py"),
}


class StubAttackAlgorithmBase:
    """Minimal SDK base for importing competition submissions."""


@dataclass(frozen=True)
class StubAttackCandidate:
    user_messages: tuple[str, ...]


@dataclass(frozen=True)
class Scenario:
    name: str
    budget_s: float
    step_s: float
    snapshot_cold_replay_succeeds: bool


SCENARIOS = (
    Scenario(
        name="tight_budget_all_replayable",
        budget_s=220.0,
        step_s=10.0,
        snapshot_cold_replay_succeeds=True,
    ),
    Scenario(
        name="snapshot_discovery_not_replayable",
        budget_s=900.0,
        step_s=10.0,
        snapshot_cold_replay_succeeds=False,
    ),
)


@dataclass
class FakeClock:
    now_s: float = 0.0

    def __call__(self) -> float:
        return self.now_s

    def advance(self, seconds: float) -> None:
        self.now_s += seconds


class FakeEnvironment:
    """Fixture-backed trace model with controllable snapshot replay behavior."""

    def __init__(self, clock: FakeClock, scenario: Scenario) -> None:
        self.clock = clock
        self.scenario = scenario
        self.messages: list[str] = []
        self.restored = False
        self.interaction_count = 0
        self.reset_count = 0
        self.snapshot_count = 0
        self.restore_count = 0

    def reset(self) -> None:
        self.messages = []
        self.restored = False
        self.reset_count += 1

    def interact(self, message: str) -> None:
        self.messages.append(message)
        self.interaction_count += 1
        self.clock.advance(self.scenario.step_s)

    def snapshot(self) -> tuple[str, ...]:
        self.snapshot_count += 1
        return tuple(self.messages)

    def restore(self, snapshot: tuple[str, ...]) -> None:
        self.messages = list(snapshot)
        self.restored = True
        self.restore_count += 1

    @staticmethod
    def _events(messages: tuple[str, ...] | list[str]) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for message in messages:
            lowered = message.lower()
            if "read " in lowered:
                events.append(
                    {
                        "tool_name": "fs.read",
                        "arguments": {"path": "fixture.txt"},
                        "status": "success",
                    }
                )
            if "post " in lowered:
                events.append(
                    {
                        "tool_name": "http.post",
                        "arguments": {
                            "url": "http://fixture.example.com",
                            "data": "fixture",
                        },
                        "status": "success",
                    }
                )
            if any(token in lowered for token in ("email ", "forward ", "notify ", "inform ")):
                events.append(
                    {
                        "tool_name": "email.send",
                        "arguments": {
                            "to": "fixture@company.invalid",
                            "body": "fixture",
                        },
                        "status": "success",
                    }
                )
        return events

    def export_trace_dict(self) -> dict[str, Any]:
        events = self._events(self.messages)
        has_sink = any(event["tool_name"] in {"email.send", "http.post"} for event in events)
        is_snapshot_path = bool(self.messages) and "config.json" in self.messages[0]
        replay_allowed = (
            not is_snapshot_path or self.restored or self.scenario.snapshot_cold_replay_succeeds
        )
        return {
            "events": events,
            "predicate": has_sink and replay_allowed,
            "restored": self.restored,
        }


def _eval_predicates(trace: dict[str, Any]) -> list[dict[str, str]]:
    return [{"predicate": "fixture"}] if trace.get("predicate") else []


def _install_sdk_stubs() -> None:
    attacks = types.ModuleType("aicomp_sdk.attacks")
    attacks.AttackAlgorithmBase = StubAttackAlgorithmBase
    attacks.AttackCandidate = StubAttackCandidate
    attacks.AttackRunConfig = type("AttackRunConfig", (), {})

    predicates = types.ModuleType("aicomp_sdk.core.predicates")
    predicates.eval_predicates = _eval_predicates
    core = types.ModuleType("aicomp_sdk.core")
    sdk = types.ModuleType("aicomp_sdk")

    sys.modules["aicomp_sdk"] = sdk
    sys.modules["aicomp_sdk.attacks"] = attacks
    sys.modules["aicomp_sdk.core"] = core
    sys.modules["aicomp_sdk.core.predicates"] = predicates


def _load_variant(name: str, path: Path, clock: FakeClock) -> types.ModuleType:
    module_name = f"_offline_ablation_{name}_{id(clock)}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    if hasattr(module, "BudgetController"):
        original_controller = module.BudgetController

        def controller_factory(total_budget_s: float):
            return original_controller(total_budget_s, clock=clock)

        module.BudgetController = controller_factory
    else:
        module.time = types.SimpleNamespace(time=clock)
    return module


def _mechanism(messages: tuple[str, ...]) -> tuple[str, ...]:
    events = FakeEnvironment._events(messages)
    return tuple(event["tool_name"] for event in events)


def _cold_replay_succeeds(messages: tuple[str, ...], scenario: Scenario) -> bool:
    clock = FakeClock()
    environment = FakeEnvironment(clock, scenario)
    environment.reset()
    for message in messages:
        environment.interact(message)
    return bool(_eval_predicates(environment.export_trace_dict()))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_variant(name: str, path: Path, scenario: Scenario) -> dict[str, Any]:
    clock = FakeClock()
    _install_sdk_stubs()
    module = _load_variant(name, path, clock)
    environment = FakeEnvironment(clock, scenario)
    config = types.SimpleNamespace(time_budget_s=scenario.budget_s)

    findings = module.AttackAlgorithm().run(environment, config)
    messages = [tuple(finding.user_messages) for finding in findings]
    mechanisms = {_mechanism(candidate) for candidate in messages}
    unreplayable = sum(not _cold_replay_succeeds(candidate, scenario) for candidate in messages)

    return {
        "scenario": scenario.name,
        "variant": name,
        "attack_sha256": _sha256(path),
        "budget_s": scenario.budget_s,
        "elapsed_s": clock.now_s,
        "remaining_s": scenario.budget_s - clock.now_s,
        "interactions": environment.interaction_count,
        "findings": len(findings),
        "unique_mechanisms": len(mechanisms),
        "unreplayable_findings": unreplayable,
        "snapshots": environment.snapshot_count,
        "restores": environment.restore_count,
    }


def run_matrix() -> dict[str, Any]:
    rows = [
        run_variant(name, path, scenario)
        for scenario in SCENARIOS
        for name, path in VARIANT_PATHS.items()
    ]
    return {
        "schema_version": 1,
        "scope": "deterministic fixture simulation; not a Kaggle score",
        "claims_tested": [
            "adaptive scheduling uses more of a tight interaction budget",
            "novelty scheduling limits redundant returned mechanisms",
            "snapshot findings are retained only after cold replay",
        ],
        "rows": rows,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = run_matrix()
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
