"""Tests for source validation, archive deduplication, and cold replay gating."""

import importlib.util
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest

ATTACK_PATH = Path("baselines/snapshot_archive_v1/attack.py")


@pytest.fixture
def snapshot_module(monkeypatch: pytest.MonkeyPatch):
    class AttackCandidate:
        def __init__(self, *, user_messages: tuple[str, ...]) -> None:
            self.user_messages = user_messages

    attacks = types.ModuleType("aicomp_sdk.attacks")
    attacks.AttackAlgorithmBase = type("AttackAlgorithmBase", (), {})
    attacks.AttackCandidate = AttackCandidate
    attacks.AttackRunConfig = type("AttackRunConfig", (), {})

    predicates = types.ModuleType("aicomp_sdk.core.predicates")
    predicates.eval_predicates = lambda trace: bool(trace.get("predicate"))
    core = types.ModuleType("aicomp_sdk.core")
    sdk = types.ModuleType("aicomp_sdk")

    monkeypatch.setitem(sys.modules, "aicomp_sdk", sdk)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks", attacks)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core", core)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core.predicates", predicates)

    spec = importlib.util.spec_from_file_location("snapshot_archive_attack", ATTACK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def source_trace(*, success: bool) -> dict[str, object]:
    return {
        "events": [
            {
                "tool_name": "fs.read",
                "arguments": {"path": "config.json"},
                "success": success,
            }
        ]
    }


def test_archive_requires_a_successful_source_tool(snapshot_module) -> None:
    archive = snapshot_module.SnapshotArchive()

    rejected = archive.add(
        prefix_label="config",
        prefix_messages=("read config",),
        snapshot="state",
        trace=source_trace(success=False),
    )
    accepted = archive.add(
        prefix_label="config",
        prefix_messages=("read config",),
        snapshot="state",
        trace=source_trace(success=True),
    )

    assert rejected is None
    assert accepted is not None
    assert accepted.source_signatures[0].startswith("fs.read:")


def test_archive_deduplicates_states_and_branch_mechanisms(snapshot_module) -> None:
    archive = snapshot_module.SnapshotArchive()
    first = archive.add(
        prefix_label="config",
        prefix_messages=("read config",),
        snapshot="state-a",
        trace=source_trace(success=True),
    )
    duplicate = archive.add(
        prefix_label="config",
        prefix_messages=("read config again",),
        snapshot="state-b",
        trace=source_trace(success=True),
    )

    assert first is not None
    assert duplicate is None
    assert archive.claim_branch(first, ("fs.read", "http.post"))
    assert not archive.claim_branch(first, ("fs.read", "http.post"))
    assert archive.claim_branch(first, ("fs.read", "email.send"))


class FakeSnapshotEnv:
    def __init__(self, *, source_success: bool, replay_success: bool) -> None:
        self.source_success = source_success
        self.replay_success = replay_success
        self.messages: list[str] = []
        self.restored = False
        self.snapshot_calls = 0

    def reset(self) -> None:
        self.messages = []
        self.restored = False

    def interact(self, message: str) -> None:
        self.messages.append(message)

    def snapshot(self) -> tuple[str, ...]:
        self.snapshot_calls += 1
        return tuple(self.messages)

    def restore(self, snapshot: tuple[str, ...]) -> None:
        self.messages = list(snapshot)
        self.restored = True

    def export_trace_dict(self) -> dict[str, object]:
        is_config_path = bool(self.messages) and "config.json" in self.messages[0]
        events: list[dict[str, object]] = []
        if is_config_path:
            events.append(
                {
                    "tool_name": "fs.read",
                    "arguments": {"path": "config.json"},
                    "success": self.source_success,
                }
            )
        if len(self.messages) > 1:
            sink = "http.post" if "Post" in self.messages[-1] else "email.send"
            events.append(
                {
                    "tool_name": sink,
                    "arguments": {"destination": "reserved-fixture"},
                    "success": True,
                }
            )
        predicate = (
            is_config_path and len(self.messages) > 1 and (self.restored or self.replay_success)
        )
        return {"events": events, "predicate": predicate}


def test_failed_source_never_creates_a_snapshot(snapshot_module) -> None:
    environment = FakeSnapshotEnv(source_success=False, replay_success=True)

    findings = snapshot_module.AttackAlgorithm().run(
        environment, SimpleNamespace(time_budget_s=10_000)
    )

    assert environment.snapshot_calls == 0
    assert findings == []


def test_snapshot_discovery_is_rejected_when_cold_replay_fails(snapshot_module) -> None:
    environment = FakeSnapshotEnv(source_success=True, replay_success=False)

    findings = snapshot_module.AttackAlgorithm().run(
        environment, SimpleNamespace(time_budget_s=10_000)
    )

    assert environment.snapshot_calls == 1
    assert findings == []


def test_snapshot_candidate_is_retained_after_cold_replay(snapshot_module) -> None:
    environment = FakeSnapshotEnv(source_success=True, replay_success=True)

    findings = snapshot_module.AttackAlgorithm().run(
        environment, SimpleNamespace(time_budget_s=10_000)
    )

    assert environment.snapshot_calls == 1
    assert findings
    assert all(len(finding.user_messages) == 2 for finding in findings)
