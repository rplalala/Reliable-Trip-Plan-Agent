"""Guard application/tool separation and offline CLI entry points."""

import ast
import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


def test_application_does_not_import_tools_tests_or_retired_experiments():
    retired = {"semantic_evaluator", "semantic_evaluation", "semantic_projection",
               "semantic_set_selection", "semantic_poi_pipeline"}
    for path in (ROOT / "backend/app").rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            modules = ([node.module or ""] if isinstance(node, ast.ImportFrom)
                       else [a.name for a in node.names] if isinstance(node, ast.Import) else [])
            for module in modules:
                assert not module.startswith(("tools", "scripts", "backend.tests")), path
                assert not (set(module.split(".")) & retired), (path, module)


@pytest.mark.parametrize("version", ["v0", "v1", "v2"])
def test_current_runner_imports(version):
    module = importlib.import_module(f"backend.app.versions.{version}.runner")
    assert callable(getattr(module, f"run_{version}"))


@pytest.mark.parametrize("module", [
    "tools.data.prepare_tripworld", "tools.data.tripworld_database",
    "tools.data.tripworld_retrieval", "tools.validation.requirement_acceptance",
    "tools.diagnostics.retrieval_performance", "tools.diagnostics.itinerary_payload",
    "tools.diagnostics.candidate_supply",
])
def test_tool_help_has_no_execution_side_effects(module, tmp_path):
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    result = subprocess.run(
        [sys.executable, "-m", module, "--help"], cwd=tmp_path, env=env,
        capture_output=True, text=True, timeout=20, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout.lower()
    assert list(tmp_path.iterdir()) == []
