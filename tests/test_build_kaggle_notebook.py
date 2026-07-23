from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from scripts.build_kaggle_notebook import (
    COMPETITION_SLUG,
    SDK_VERSION,
    build_bundle,
)

ATTACK_PATH = Path("baselines/official_starter_v17/attack.py")


def _embedded_attack_source(notebook: dict) -> str:
    write_cell = "".join(notebook["cells"][2]["source"])
    tree = ast.parse(write_cell)
    assignment = next(
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "ATTACK_SOURCE" for target in node.targets
        )
    )
    return ast.literal_eval(assignment.value)


def test_build_bundle_embeds_exact_attack_and_private_metadata(tmp_path: Path) -> None:
    manifest = build_bundle(
        ATTACK_PATH,
        tmp_path,
        experiment_id="B000",
        kernel_id="heralces/ai-agent-security-b000",
        title="AI Agent Security B000",
        worktree=Path.cwd(),
    )

    notebook = json.loads((tmp_path / manifest.notebook_file).read_text(encoding="utf-8"))
    metadata = json.loads((tmp_path / "kernel-metadata.json").read_text(encoding="utf-8"))
    recorded = json.loads((tmp_path / "submission-manifest.json").read_text(encoding="utf-8"))

    assert _embedded_attack_source(notebook) == ATTACK_PATH.read_text(encoding="utf-8")
    assert metadata["is_private"] is True
    assert metadata["enable_internet"] is False
    assert metadata["competition_sources"] == [COMPETITION_SLUG]
    assert metadata["code_file"] == manifest.notebook_file
    assert recorded["attack_sha256"] == manifest.attack_sha256
    assert recorded["sdk_version"] == SDK_VERSION
    assert manifest.attack_size_bytes == ATTACK_PATH.stat().st_size
    assert len({cell["id"] for cell in notebook["cells"]}) == len(notebook["cells"])


def test_build_bundle_rejects_invalid_kernel_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="kernel id"):
        build_bundle(
            ATTACK_PATH,
            tmp_path,
            experiment_id="B000",
            kernel_id="missing-owner",
            title="Invalid",
        )


def test_build_bundle_rejects_title_slug_mismatch(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="title resolves to slug"):
        build_bundle(
            ATTACK_PATH,
            tmp_path,
            experiment_id="B000",
            kernel_id="heralces/ai-agent-security-b000",
            title="AI Agent Security B000 Official Baseline",
        )


def test_notebook_starts_competition_inference_server(tmp_path: Path) -> None:
    manifest = build_bundle(
        ATTACK_PATH,
        tmp_path,
        experiment_id="B000",
        kernel_id="heralces/ai-agent-security-b000",
        title="AI Agent Security B000",
    )
    notebook = json.loads((tmp_path / manifest.notebook_file).read_text(encoding="utf-8"))
    server_cell = "".join(notebook["cells"][3]["source"])

    assert "JEDAttackInferenceServer().serve()" in server_cell
    assert 'os.getenv("KAGGLE_IS_COMPETITION_RERUN")' in server_cell
    assert 'Path("/kaggle/working/submission.csv")' in server_cell
    assert '"gpt_oss_public"' in server_cell
    assert '"gemma_private"' in server_cell
    assert "/kaggle/working/attack.py" in "".join(notebook["cells"][2]["source"])
