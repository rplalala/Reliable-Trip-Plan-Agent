"""Mapped pair outcomes and duplicate consistency are separate descriptive tracks."""

from backend.evaluation.human_report import build_human_report
from backend.evaluation.human_tasks import build_human_package, prepare_human_material
from backend.tests.evaluation.test_human_answers import answer, bundle
from backend.tests.evaluation.test_human_tasks import config, expand, review

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def test_duplicate_consistency_uses_versions_and_never_adds_main_outcome_weight(batch):
    path = expand(batch, 3)
    cfg = config(
        [{"group_id": g} for g in ("g", "g1", "g2")] + [{"group_id": "g", "duplicate_of": 0}]
    )
    material = build_human_package(path, cfg, review(prepare_human_material(path, cfg)))
    public, private = material["public"], material["private"]
    records = []
    for i, mapping in enumerate(private["tasks"]):
        labels = {v: label for label, v in mapping["labels"].items()}
        groups = [[labels["v0"], labels["v1"]], [labels["v2"]], [labels["v3"]]]
        records.append(answer(public, groups=groups, task=i))
    result = build_human_report(
        public, private, [bundle(*records)], generated_at="2026-10-02T10:00:00+10:00"
    )
    assert result["main_task_count"] == 3
    assert result["aggregates"]["preference"]["v0_vs_v1"] == {
        "win": 0,
        "tie": 3,
        "loss": 0,
        "available": 3,
    }
    assert result["aggregates"]["pace"]["v0_vs_v2"]["win"] == 3
    assert result["duplicate_consistency"][0]["dimensions"]["usefulness"] == {
        "agreeing_pairs": 6,
        "comparable_pairs": 6,
        "agreement": 1.0,
    }
    records[-1]["responses"] = {d: {"status": "unable_to_judge"} for d in public["dimensions"]}
    missing = build_human_report(
        public, private, [bundle(*records)], generated_at="2026-10-02T10:00:00+10:00"
    )
    assert missing["duplicate_consistency"][0]["dimensions"]["pace"]["agreement"] is None
    assert missing["main_task_count"] == 3
