"""Safety invariants shared by every executable competition attack variant."""

import ast
import re
from pathlib import Path
from urllib.parse import urlparse

import pytest

ATTACK_FILES = sorted(Path("baselines").glob("*/attack.py"))
URL_PATTERN = re.compile(r"https?://[^\s'\"),]+")
EMAIL_PATTERN = re.compile(r"\b[^@\s]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")


@pytest.mark.parametrize("attack_file", ATTACK_FILES, ids=lambda path: path.parent.name)
def test_executable_prompts_only_use_reserved_destinations(attack_file: Path) -> None:
    tree = ast.parse(attack_file.read_text(encoding="utf-8"))
    prompt_literals: list[str] = []

    for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
        function_name = (
            call.func.id
            if isinstance(call.func, ast.Name)
            else call.func.attr
            if isinstance(call.func, ast.Attribute)
            else ""
        )
        if function_name not in {"try_attack", "interact", "CandidateSpec"}:
            continue
        arguments = [*call.args, *(keyword.value for keyword in call.keywords)]
        prompt_literals.extend(
            node.value
            for argument in arguments
            for node in ast.walk(argument)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        )

    assert prompt_literals
    for prompt in prompt_literals:
        for match in URL_PATTERN.findall(prompt):
            hostname = urlparse(match).hostname
            assert hostname is not None
            assert hostname == "example.com" or hostname.endswith(".example.com")
        for domain in EMAIL_PATTERN.findall(prompt):
            assert domain.endswith(".invalid")
