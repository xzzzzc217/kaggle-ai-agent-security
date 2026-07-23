"""Static checks that do not require the competition-only SDK."""

import ast
import re
from pathlib import Path
from urllib.parse import urlparse

BASELINE = Path("baselines/official_starter_v17/attack.py")
URL_PATTERN = re.compile(r"https?://[^\s'\"),]+")
EMAIL_PATTERN = re.compile(r"\b[^@\s]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")


def test_baseline_is_valid_python() -> None:
    ast.parse(BASELINE.read_text(encoding="utf-8"))


def test_attack_contract_symbols_exist() -> None:
    tree = ast.parse(BASELINE.read_text(encoding="utf-8"))
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}

    attack = classes["AttackAlgorithm"]
    methods = {node.name for node in attack.body if isinstance(node, ast.FunctionDef)}
    assert "run" in methods


def test_attack_prompts_only_use_reserved_network_hosts() -> None:
    """Prevent accidental real-world hosts from entering executable attack prompts."""
    tree = ast.parse(BASELINE.read_text(encoding="utf-8"))
    prompt_literals: list[str] = []

    for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
        function_name = (
            call.func.id
            if isinstance(call.func, ast.Name)
            else call.func.attr
            if isinstance(call.func, ast.Attribute)
            else ""
        )
        if function_name not in {"try_attack", "interact"}:
            continue
        prompt_literals.extend(
            node.value
            for argument in call.args
            for node in ast.walk(argument)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        )

    assert prompt_literals
    for prompt in prompt_literals:
        for match in URL_PATTERN.findall(prompt):
            hostname = urlparse(match).hostname
            assert hostname == "example.com" or hostname.endswith(".example.com")
        for domain in EMAIL_PATTERN.findall(prompt):
            assert domain.endswith(".invalid")
