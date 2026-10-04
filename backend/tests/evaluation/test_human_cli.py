"""Local package rendering and exact answer/report CLI replay."""

import json

from backend.evaluation.human_cli import main, render_human_html
from backend.evaluation.human_tasks import build_human_package, prepare_human_material
from backend.tests.evaluation.test_human_answers import answer, bundle
from backend.tests.evaluation.test_human_tasks import config, review

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def test_static_html_escapes_hostile_source_text_without_private_mapping(batch):
    _, results, write, _, _ = batch
    results["v0"]["itinerary"]["days"][0]["activities"][0]["notes"] = (
        "</script><script>window.injected=true</script>"
    )
    path = write("v0")
    material = build_human_package(path, config(), review(prepare_human_material(path, config())))
    html = render_human_html(
        material["public"], 'document.body.dataset.ready="yes";', "body{color:black}"
    )
    assert "\\u003c/script>" in html
    assert "<script>window.injected" not in html
    assert "connect-src" in html and "default-src 'none'" in html
    assert "run-v0" not in html and "private" not in html and "v0.json" not in html


def test_cli_preparation_package_import_and_report_are_separate_local_outputs(batch, capsys):
    _, _, write, _, root = batch
    path = write()
    cfg = root / "config.json"
    cfg.write_text(json.dumps(config()))
    assert main(["prepare", str(path), str(cfg)]) == 0
    preparation = json.loads(capsys.readouterr().out)
    reviewed = root / "review.json"
    reviewed.write_text(json.dumps(review(preparation)))
    js, css = root / "renderer.js", root / "renderer.css"
    js.write_text('document.body.dataset.ready="yes";')
    css.write_text("body{color:black}")
    out, mapping = root / "public", root / "private.json"
    assert (
        main(
            [
                "package",
                str(path),
                str(cfg),
                str(reviewed),
                "--out",
                str(out),
                "--private-out",
                str(mapping),
                "--renderer-js",
                str(js),
                "--renderer-css",
                str(css),
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert sorted(p.name for p in out.iterdir()) == ["presentation.json", "review.html"]
    public = json.loads((out / "presentation.json").read_text())
    answers = root / "answers.json"
    answers.write_text(json.dumps(bundle(answer(public))))
    assert (
        main(
            [
                "report",
                str(out / "presentation.json"),
                str(mapping),
                str(answers),
                "--generated-at",
                "2026-10-02T10:00:00+10:00",
            ]
        )
        == 0
    )
    report = json.loads(capsys.readouterr().out)
    assert report["main_task_count"] == 1
    assert main(["import", str(out / "presentation.json"), str(mapping), str(answers)]) == 0
    assert json.loads(capsys.readouterr().out)["effective"][0]["answer_revision"] == 1
