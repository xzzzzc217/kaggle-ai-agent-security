"""Tests for signature normalization and diversity-first scheduling."""

import importlib.util
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest

ATTACK_PATH = Path("baselines/novelty_scheduler_v1/attack.py")


@pytest.fixture
def novelty_module(monkeypatch: pytest.MonkeyPatch):
    class AttackCandidate:
        def __init__(self, *, user_messages: tuple[str, ...]) -> None:
            self.user_messages = user_messages

    attacks = types.ModuleType("aicomp_sdk.attacks")
    attacks.AttackAlgorithmBase = type("AttackAlgorithmBase", (), {})
    attacks.AttackCandidate = AttackCandidate
    attacks.AttackRunConfig = type("AttackRunConfig", (), {})

    predicates = types.ModuleType("aicomp_sdk.core.predicates")
    predicates.eval_predicates = lambda trace: []
    core = types.ModuleType("aicomp_sdk.core")
    sdk = types.ModuleType("aicomp_sdk")

    monkeypatch.setitem(sys.modules, "aicomp_sdk", sdk)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.attacks", attacks)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core", core)
    monkeypatch.setitem(sys.modules, "aicomp_sdk.core.predicates", predicates)

    spec = importlib.util.spec_from_file_location("novelty_scheduler_attack", ATTACK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def test_literal_values_share_one_tool_shape(novelty_module) -> None:
    first = {
        "type": "tool_call",
        "name": "http.post",
        "arguments": {"url": "http://one.example.com", "data": "TOKEN=one"},
        "success": True,
    }
    second = {
        "type": "tool_call",
        "name": "http.post",
        "arguments": {"url": "http://two.example.com", "data": "TOKEN=two"},
        "success": True,
    }

    assert novelty_module.extract_tool_signatures(first) == (
        'http.post:{"data":"string","url":"string"}',
    )
    assert novelty_module.extract_tool_signatures(first) == (
        novelty_module.extract_tool_signatures(second)
    )


def test_argument_structure_changes_the_signature(novelty_module) -> None:
    flat = {
        "tool_name": "email.send",
        "args": {"to": "admin@company.invalid", "body": "ready"},
    }
    with_attachment = {
        "tool_name": "email.send",
        "args": {
            "to": "admin@company.invalid",
            "body": "ready",
            "attachment": {"name": "report.txt", "content": "fixture"},
        },
    }

    assert novelty_module.extract_tool_signatures(flat) != (
        novelty_module.extract_tool_signatures(with_attachment)
    )


def test_failed_calls_do_not_count_as_signatures(novelty_module) -> None:
    trace = {
        "events": [
            {
                "tool_name": "fs.read",
                "arguments": {"path": "fixture.txt"},
                "status": "success",
            },
            {
                "tool_name": "http.post",
                "arguments": {"url": "http://audit.example.com"},
                "status": "failed",
            },
        ]
    }

    signatures = novelty_module.extract_tool_signatures(trace)

    assert len(signatures) == 1
    assert signatures[0].startswith("fs.read:")


def test_scheduler_covers_each_signature_before_repeating(novelty_module) -> None:
    candidate = novelty_module.CandidateSpec
    candidates = [
        candidate("http-a", ("a",), ("http.post",), 5),
        candidate("http-b", ("b",), ("http.post",), 5),
        candidate("mail", ("c",), ("email.send",), 3),
        candidate("file-http", ("d", "e"), ("fs.read", "http.post"), 5),
    ]

    ordered = novelty_module.NoveltyScheduler.order(candidates)
    first_round = ordered[:3]

    assert len({item.expected_signature for item in first_round}) == 3
    assert ordered[-1].label == "http-b"


def test_scheduler_is_deterministic(novelty_module) -> None:
    candidate = novelty_module.CandidateSpec
    candidates = [
        candidate("z", ("a",), ("same",), 3),
        candidate("a", ("b",), ("same",), 3),
        candidate("other", ("c",), ("other",), 3),
    ]

    first = [item.label for item in novelty_module.NoveltyScheduler.order(candidates)]
    second = [item.label for item in novelty_module.NoveltyScheduler.order(candidates)]

    assert first == second


def test_attack_algorithm_runs_end_to_end_with_fixture_trace(novelty_module) -> None:
    class FakeEnv:
        def __init__(self) -> None:
            self.messages: list[str] = []
            self.completed_attempts: list[tuple[str, ...]] = []

        def reset(self) -> None:
            if self.messages:
                self.completed_attempts.append(tuple(self.messages))
            self.messages = []

        def interact(self, message: str) -> None:
            self.messages.append(message)

        def snapshot(self) -> tuple[str, ...]:
            return tuple(self.messages)

        def restore(self, snapshot: tuple[str, ...]) -> None:
            if self.messages:
                self.completed_attempts.append(tuple(self.messages))
            self.messages = list(snapshot)

        def export_trace_dict(self) -> dict[str, list[dict[str, object]]]:
            events: list[dict[str, object]] = []
            for message in self.messages:
                if "Read" in message:
                    events.append(
                        {
                            "tool_name": "fs.read",
                            "arguments": {"path": "fixture.txt"},
                            "status": "success",
                        }
                    )
                if "Post" in message:
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
                if any(word in message for word in ("Email", "Forward", "Notify", "Inform")):
                    events.append(
                        {
                            "tool_name": "email.send",
                            "arguments": {"to": "fixture@company.invalid", "body": "fixture"},
                            "status": "success",
                        }
                    )
            return {"events": events}

    novelty_module.eval_predicates = lambda trace: bool(trace["events"])
    environment = FakeEnv()
    config = SimpleNamespace(time_budget_s=10_000)
    algorithm = novelty_module.AttackAlgorithm()
    algorithm.max_findings_per_signature = 1

    findings = algorithm.run(environment, config)

    assert len(findings) == 4
    assert all(hasattr(finding, "user_messages") for finding in findings)
    first_mechanisms = environment.completed_attempts[:4]
    assert "Post" in first_mechanisms[0][0]
    assert "Notify" in first_mechanisms[1][0]
    assert "Read the file secret.txt" in first_mechanisms[2][0]
    assert "Read the weekly_report.txt" in first_mechanisms[3][0]
