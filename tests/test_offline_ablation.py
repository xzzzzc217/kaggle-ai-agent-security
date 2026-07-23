"""Assertions for the deterministic cross-variant ablation harness."""

from scripts.offline_ablation import run_matrix


def rows_by_key() -> dict[tuple[str, str], dict]:
    report = run_matrix()
    return {(row["scenario"], row["variant"]): row for row in report["rows"]}


def test_ablation_matrix_is_deterministic() -> None:
    assert run_matrix() == run_matrix()


def test_adaptive_scheduler_uses_more_of_tight_budget() -> None:
    rows = rows_by_key()
    baseline = rows[("tight_budget_all_replayable", "official_starter_v17")]
    adaptive = rows[("tight_budget_all_replayable", "adaptive_budget_v1")]

    assert adaptive["interactions"] > baseline["interactions"]
    assert adaptive["findings"] > baseline["findings"]
    assert adaptive["remaining_s"] >= 0


def test_novelty_scheduler_preserves_mechanism_coverage() -> None:
    rows = rows_by_key()
    adaptive = rows[("tight_budget_all_replayable", "adaptive_budget_v1")]
    novelty = rows[("tight_budget_all_replayable", "novelty_scheduler_v1")]

    assert novelty["unique_mechanisms"] >= adaptive["unique_mechanisms"]
    assert novelty["findings"] <= adaptive["findings"]


def test_snapshot_archive_eliminates_unreplayable_findings() -> None:
    rows = rows_by_key()
    scenario = "snapshot_discovery_not_replayable"
    baseline = rows[(scenario, "official_starter_v17")]
    adaptive = rows[(scenario, "adaptive_budget_v1")]
    novelty = rows[(scenario, "novelty_scheduler_v1")]
    snapshot = rows[(scenario, "snapshot_archive_v1")]

    assert baseline["unreplayable_findings"] > 0
    assert adaptive["unreplayable_findings"] > 0
    assert novelty["unreplayable_findings"] > 0
    assert snapshot["unreplayable_findings"] == 0
    assert snapshot["findings"] > 0
