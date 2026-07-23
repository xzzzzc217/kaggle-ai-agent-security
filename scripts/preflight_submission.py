"""Static preflight checks for a Kaggle attack.py submission.

The checker is deliberately SDK-independent so it can run before competition data is
available. It validates the entry-point contract, catches accidental real-world
destinations, identifies direct network libraries, and records a reproducible digest.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

URL_PATTERN = re.compile(r"https?://[^\s'\"),]+")
EMAIL_PATTERN = re.compile(r"\b[^@\s]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
PROMPT_CALLS = frozenset({"CandidateSpec", "interact", "try_attack"})
DIRECT_NETWORK_IMPORTS = frozenset(
    {
        "aiohttp",
        "httpx",
        "requests",
        "socket",
        "urllib3",
        "websocket",
        "websockets",
    }
)


@dataclass(frozen=True)
class PreflightIssue:
    severity: str
    code: str
    message: str
    line: int | None = None


@dataclass(frozen=True)
class PreflightReport:
    path: str
    sha256: str
    size_bytes: int
    issues: tuple[PreflightIssue, ...]

    @property
    def errors(self) -> tuple[PreflightIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "error")

    @property
    def warnings(self) -> tuple[PreflightIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "warning")

    @property
    def passed(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "passed": self.passed,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "issues": [asdict(issue) for issue in self.issues],
        }


def _call_name(call: ast.Call) -> str:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return ""


def _dotted_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _dotted_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _prompt_literals(tree: ast.AST) -> list[tuple[str, int | None]]:
    literals: list[tuple[str, int | None]] = []
    for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
        if _call_name(call) not in PROMPT_CALLS:
            continue
        arguments = [*call.args, *(keyword.value for keyword in call.keywords)]
        for argument in arguments:
            literals.extend(
                (node.value, getattr(node, "lineno", None))
                for node in ast.walk(argument)
                if isinstance(node, ast.Constant) and isinstance(node.value, str)
            )
    return literals


def _validate_contract(tree: ast.Module) -> list[PreflightIssue]:
    issues: list[PreflightIssue] = []
    attack_classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "AttackAlgorithm"
    ]
    if len(attack_classes) != 1:
        message = (
            f"expected exactly one top-level AttackAlgorithm class, found {len(attack_classes)}"
        )
        issues.append(
            PreflightIssue(
                "error",
                "attack_class_count",
                message,
            )
        )
        return issues

    attack_class = attack_classes[0]
    base_names = {_dotted_name(base) for base in attack_class.bases}
    if not any(name.endswith("AttackAlgorithmBase") for name in base_names):
        issues.append(
            PreflightIssue(
                "error",
                "attack_base",
                "AttackAlgorithm must inherit from AttackAlgorithmBase",
                attack_class.lineno,
            )
        )

    run_methods = [
        node
        for node in attack_class.body
        if isinstance(node, ast.FunctionDef) and node.name == "run"
    ]
    if len(run_methods) != 1:
        issues.append(
            PreflightIssue(
                "error",
                "run_method_count",
                f"expected exactly one run method, found {len(run_methods)}",
                attack_class.lineno,
            )
        )
        return issues

    run_method = run_methods[0]
    positional = [*run_method.args.posonlyargs, *run_method.args.args]
    argument_names = [argument.arg for argument in positional]
    if len(argument_names) < 3 or argument_names[:3] != ["self", "env", "config"]:
        issues.append(
            PreflightIssue(
                "error",
                "run_signature",
                "run must begin with positional arguments (self, env, config)",
                run_method.lineno,
            )
        )
    return issues


def _validate_imports(tree: ast.Module) -> list[PreflightIssue]:
    issues: list[PreflightIssue] = []
    imported_roots: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.extend(
                (alias.name.split(".", 1)[0], node.lineno) for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                issues.append(
                    PreflightIssue(
                        "error",
                        "relative_import",
                        "submission must not depend on repository-relative imports",
                        node.lineno,
                    )
                )
            elif node.module:
                imported_roots.append((node.module.split(".", 1)[0], node.lineno))

    for root, line in imported_roots:
        if root in DIRECT_NETWORK_IMPORTS:
            issues.append(
                PreflightIssue(
                    "error",
                    "direct_network_import",
                    f"direct network library '{root}' is out of scope for the offline evaluator",
                    line,
                )
            )
        elif root not in sys.stdlib_module_names and root != "aicomp_sdk":
            issues.append(
                PreflightIssue(
                    "warning",
                    "third_party_import",
                    f"verify Kaggle image or notebook provisioning for third-party import '{root}'",
                    line,
                )
            )
    return issues


def _validate_prompt_destinations(tree: ast.Module) -> list[PreflightIssue]:
    issues: list[PreflightIssue] = []
    for prompt, line in _prompt_literals(tree):
        for match in URL_PATTERN.findall(prompt):
            hostname = urlparse(match).hostname
            if hostname is None or not (
                hostname == "example.com" or hostname.endswith(".example.com")
            ):
                issues.append(
                    PreflightIssue(
                        "error",
                        "non_reserved_url",
                        f"executable prompt contains non-reserved URL host: {hostname or match}",
                        line,
                    )
                )
        for domain in EMAIL_PATTERN.findall(prompt):
            if not domain.endswith(".invalid"):
                issues.append(
                    PreflightIssue(
                        "error",
                        "non_reserved_email",
                        f"executable prompt contains non-reserved email domain: {domain}",
                        line,
                    )
                )
    return issues


def validate_attack(path: Path) -> PreflightReport:
    resolved = path.resolve()
    try:
        payload = resolved.read_bytes()
    except OSError as exc:
        issue = PreflightIssue("error", "read_error", str(exc))
        return PreflightReport(str(resolved), "", 0, (issue,))

    digest = hashlib.sha256(payload).hexdigest()
    try:
        source = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        issue = PreflightIssue("error", "utf8", str(exc))
        return PreflightReport(str(resolved), digest, len(payload), (issue,))

    try:
        tree = ast.parse(source, filename=str(resolved))
    except SyntaxError as exc:
        issue = PreflightIssue("error", "syntax", exc.msg, exc.lineno)
        return PreflightReport(str(resolved), digest, len(payload), (issue,))

    issues = [
        *_validate_contract(tree),
        *_validate_imports(tree),
        *_validate_prompt_destinations(tree),
    ]
    issues.sort(key=lambda issue: (issue.severity != "error", issue.line or 0, issue.code))
    return PreflightReport(str(resolved), digest, len(payload), tuple(issues))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attack_file", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = validate_attack(args.attack_file)
    if args.as_json:
        print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))
    else:
        status = "PASS" if report.passed else "FAIL"
        print(f"{status} {report.path}")
        print(f"sha256={report.sha256} size={report.size_bytes}")
        for issue in report.issues:
            location = f":{issue.line}" if issue.line else ""
            print(f"{issue.severity.upper()} {issue.code}{location} {issue.message}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
