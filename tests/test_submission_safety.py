"""Safety invariants shared by every executable competition attack variant."""

import ast
import re
from pathlib import Path
from urllib.parse import urlparse

import pytest

ATTACK_FILES = sorted(Path("baselines").glob("*/attack.py"))
URL_PATTERN = re.compile(r"https?://[^\s'\"),]+")
EMAIL_PATTERN = re.compile(r"\b[^@\s]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
GOEXPLORE_MODULE = "aicomp_sdk.attacks.baselines.attacker_goexplore"
GOEXPLORE_SOURCE = Path(
    "data/competition/extracted/aicomp_sdk/attacks/baselines/attacker_goexplore.py"
)


def _sdk_goexplore_prompts(tree: ast.Module) -> list[str]:
    delegated_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    if GOEXPLORE_MODULE not in delegated_modules:
        return []

    sdk_tree = ast.parse(GOEXPLORE_SOURCE.read_text(encoding="utf-8"))
    prompts: list[str] = []
    for assignment in (
        node for node in sdk_tree.body if isinstance(node, ast.AnnAssign | ast.Assign)
    ):
        target_names: set[str] = set()
        if isinstance(assignment, ast.AnnAssign) and isinstance(assignment.target, ast.Name):
            target_names.add(assignment.target.id)
        elif isinstance(assignment, ast.Assign):
            target_names.update(
                target.id for target in assignment.targets if isinstance(target, ast.Name)
            )
        if not any(name.endswith("PROMPT_BANK") for name in target_names):
            continue
        prompts.extend(
            node.value
            for node in ast.walk(assignment.value)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        )
    return prompts


def _named_template_prompts(tree: ast.Module) -> list[str]:
    """Collect prompt banks that are passed to interact through a local variable."""
    prompts: list[str] = []
    for assignment in (node for node in tree.body if isinstance(node, ast.AnnAssign | ast.Assign)):
        target_names: set[str] = set()
        if isinstance(assignment, ast.AnnAssign) and isinstance(assignment.target, ast.Name):
            target_names.add(assignment.target.id)
        elif isinstance(assignment, ast.Assign):
            target_names.update(
                target.id for target in assignment.targets if isinstance(target, ast.Name)
            )
        if not any(name.endswith("TEMPLATES") for name in target_names):
            continue
        prompts.extend(
            node.value
            for node in ast.walk(assignment.value)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        )
    return prompts


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

    if not prompt_literals:
        prompt_literals.extend(_sdk_goexplore_prompts(tree))
    if not prompt_literals:
        prompt_literals.extend(_named_template_prompts(tree))

    assert prompt_literals
    for prompt in prompt_literals:
        for match in URL_PATTERN.findall(prompt):
            hostname = urlparse(match).hostname
            assert hostname is not None
            assert hostname == "example.com" or hostname.endswith(".example.com")
        for domain in EMAIL_PATTERN.findall(prompt):
            assert domain.endswith(".invalid")
