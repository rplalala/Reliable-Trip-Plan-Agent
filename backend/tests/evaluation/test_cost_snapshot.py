"""Native oracle snapshots reuse their verified attempt and raw hash boundary."""

import asyncio
import json

import pytest

from backend.evaluation.cost_report import build_cost_report
from backend.evaluation.cost_snapshot import snapshot_usage
from backend.evaluation.intake import load_batch
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_identity_plan,
)
from backend.tests.evaluation.test_cost_report import prices

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def test_snapshot_counts_actual_attempts_without_copying_payloads(batch, tmp_path):
    plan = build_identity_plan(load_batch(batch[2]()))

    async def transport(request):
        return Response(200, b'{"places":[]}')

    directory = tmp_path / "oracle"
    asyncio.run(acquire_snapshot(plan, directory, transport, AcquisitionPolicy(max_sends=2)))
    source = snapshot_usage(directory)
    assert source["usage"]["namespace"] == "oracle"
    assert len(source["usage"]["provider_events"]) == 2
    assert "payload" not in json.dumps(source["usage"]["provider_events"])
    catalog = prices()
    catalog["rows"] = [
        {
            **catalog["rows"][1],
            "valid_from": "2020-01-01",
            "valid_until": "2100-01-01",
            "match": {"kind": "provider", "provider": "google", "operation": "places_search"},
            "rates": {"requests": "35"},
        }
    ]
    assert build_cost_report([source], catalog)["runs"][0]["estimated_total"] == "0.07"
    with pytest.raises(ValueError, match="Duplicate"):
        build_cost_report([source, source], catalog)
    manifest = json.loads((directory / "manifest.json").read_bytes())
    raw = directory / manifest["records"][0]["attempts"][0]["raw"]["path"]
    raw.write_bytes(b"changed")
    with pytest.raises(ValueError, match="hash"):
        snapshot_usage(directory)
