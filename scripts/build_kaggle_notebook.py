"""Build a reproducible Kaggle notebook bundle for an attack.py submission.

The generated notebook follows the competition's official starter structure:
it writes the selected attack module to ``/kaggle/working/attack.py`` and then
starts the competition-owned JED inference server.  The bundle is private by
default and records the exact attack digest and Git commit used to build it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from scripts.preflight_submission import validate_attack

COMPETITION_SLUG = "ai-agent-security-multi-step-tool-attacks"
SDK_VERSION = "3.1.2"
KERNEL_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+/[a-z0-9][a-z0-9-]*$")

SETUP_SOURCE = """\
import glob
import sys
from pathlib import Path

# Prevent argparse conflicts inside Kaggle notebooks.
sys.argv = [sys.argv[0]]

# The competition input contains kaggle_evaluation/ and aicomp_sdk/ at its root.
for candidate in glob.glob("/kaggle/input/**/kaggle_evaluation", recursive=True):
    dataset_root = str(Path(candidate).parent)
    if dataset_root not in sys.path:
        sys.path.insert(0, dataset_root)
    print(f"Dataset root: {dataset_root}")
    break
else:
    raise RuntimeError("Competition SDK input was not found")
"""

SERVER_SOURCE = """\
import csv
import os
from pathlib import Path

if os.getenv("KAGGLE_IS_COMPETITION_RERUN"):
    import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server

    server = kaggle_evaluation.jed_attack_134815.jed_attack_inference_server
    server.JEDAttackInferenceServer().serve()
else:
    # Code Competition submissions require this output to exist on the committed
    # notebook version. The hidden gateway overwrites it with real rerun scores.
    rows = (
        "gpt_oss_public",
        "gpt_oss_private",
        "gemma_public",
        "gemma_private",
    )
    output_path = Path("/kaggle/working/submission.csv")
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("Id", "Score"))
        writer.writerows((row_id, 0.0) for row_id in rows)
    print("placeholder submission.csv written")
"""


@dataclass(frozen=True)
class SubmissionManifest:
    experiment_id: str
    competition: str
    kernel_id: str
    title: str
    notebook_file: str
    attack_source: str
    attack_sha256: str
    attack_size_bytes: int
    sdk_version: str
    git_commit: str
    is_private: bool
    enable_gpu: bool


def _source_lines(source: str) -> list[str]:
    lines = source.splitlines(keepends=True)
    return lines or [""]


def _cell_id(prefix: str, source: str) -> str:
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def _markdown_cell(source: str) -> dict[str, Any]:
    return {
        "cell_type": "markdown",
        "id": _cell_id("markdown", source),
        "metadata": {},
        "source": _source_lines(source),
    }


def _code_cell(source: str) -> dict[str, Any]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": _cell_id("code", source),
        "metadata": {},
        "outputs": [],
        "source": _source_lines(source),
    }


def build_notebook(
    attack_source: str,
    *,
    experiment_id: str,
    attack_sha256: str,
    git_commit: str,
) -> dict[str, Any]:
    write_attack_source = (
        "from pathlib import Path\n\n"
        f"ATTACK_SOURCE = {json.dumps(attack_source, ensure_ascii=False)}\n"
        'Path("/kaggle/working/attack.py").write_text(ATTACK_SOURCE, encoding="utf-8")\n'
        'print("attack.py written")\n'
    )
    provenance = (
        "# AI Agent Security submission\n\n"
        f"- Experiment: `{experiment_id}`\n"
        f"- Attack SHA-256: `{attack_sha256}`\n"
        f"- Source commit: `{git_commit}`\n"
        f"- Competition SDK: `{SDK_VERSION}`\n"
    )
    return {
        "cells": [
            _markdown_cell(provenance),
            _code_cell(SETUP_SOURCE),
            _code_cell(write_attack_source),
            _code_cell(SERVER_SOURCE),
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build_kernel_metadata(
    *,
    kernel_id: str,
    title: str,
    notebook_file: str,
    is_private: bool,
    enable_gpu: bool,
) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "id": kernel_id,
        "title": title,
        "code_file": notebook_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": is_private,
        "enable_gpu": enable_gpu,
        "enable_tpu": False,
        "enable_internet": False,
        "keywords": [],
        "dataset_sources": [],
        "kernel_sources": [],
        "competition_sources": [COMPETITION_SLUG],
        "model_sources": [],
    }
    if enable_gpu:
        metadata["machine_shape"] = "NvidiaTeslaT4"
    return metadata


def _slugify_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _current_git_commit(worktree: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=worktree,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def build_bundle(
    attack_file: Path,
    output_dir: Path,
    *,
    experiment_id: str,
    kernel_id: str,
    title: str,
    is_private: bool = True,
    enable_gpu: bool = True,
    worktree: Path | None = None,
) -> SubmissionManifest:
    if not KERNEL_ID_PATTERN.fullmatch(kernel_id):
        raise ValueError("kernel id must use the form username/lowercase-hyphenated-slug")
    kernel_slug = kernel_id.split("/", 1)[1]
    title_slug = _slugify_title(title)
    if title_slug != kernel_slug:
        raise ValueError(
            f"title resolves to slug '{title_slug}', but kernel id uses '{kernel_slug}'"
        )

    preflight = validate_attack(attack_file)
    if not preflight.passed:
        messages = "; ".join(f"{issue.code}: {issue.message}" for issue in preflight.errors)
        raise ValueError(f"attack preflight failed: {messages}")

    resolved_attack = attack_file.resolve()
    attack_bytes = resolved_attack.read_bytes()
    attack_source = attack_bytes.decode("utf-8")
    attack_sha256 = hashlib.sha256(attack_bytes).hexdigest()
    worktree = (worktree or Path.cwd()).resolve()
    git_commit = _current_git_commit(worktree)

    notebook_file = f"{kernel_slug}.ipynb"
    output_dir.mkdir(parents=True, exist_ok=True)

    notebook = build_notebook(
        attack_source,
        experiment_id=experiment_id,
        attack_sha256=attack_sha256,
        git_commit=git_commit,
    )
    kernel_metadata = build_kernel_metadata(
        kernel_id=kernel_id,
        title=title,
        notebook_file=notebook_file,
        is_private=is_private,
        enable_gpu=enable_gpu,
    )
    manifest = SubmissionManifest(
        experiment_id=experiment_id,
        competition=COMPETITION_SLUG,
        kernel_id=kernel_id,
        title=title,
        notebook_file=notebook_file,
        attack_source=str(resolved_attack),
        attack_sha256=attack_sha256,
        attack_size_bytes=len(attack_bytes),
        sdk_version=SDK_VERSION,
        git_commit=git_commit,
        is_private=is_private,
        enable_gpu=enable_gpu,
    )

    (output_dir / notebook_file).write_text(
        json.dumps(notebook, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "kernel-metadata.json").write_text(
        json.dumps(kernel_metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "submission-manifest.json").write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attack_file", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--kernel-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument(
        "--public",
        action="store_true",
        help="Create public kernel metadata. Bundles are private by default.",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Disable the GPU in kernel metadata.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    manifest = build_bundle(
        args.attack_file,
        args.output_dir,
        experiment_id=args.experiment_id,
        kernel_id=args.kernel_id,
        title=args.title,
        is_private=not args.public,
        enable_gpu=not args.cpu,
    )
    print(f"Built {args.output_dir.resolve() / manifest.notebook_file}")
    print(f"attack_sha256={manifest.attack_sha256}")
    print(f"git_commit={manifest.git_commit}")
    print("kernel_visibility=private" if manifest.is_private else "kernel_visibility=public")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
