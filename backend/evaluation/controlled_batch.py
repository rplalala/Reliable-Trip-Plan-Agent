"""Declared controlled inventory; missing reports never disappear from denominators."""

from datetime import datetime
from pathlib import Path

from .intake import _artifact
from .records import MaterialError, canonical_digest, require, text


def build_controlled_batch(manifest, root, *, generated_at):
    base = {
        "schema_version": "rtpeval_controlled_batch_report_1",
        "generated_at": generated_at,
        "batch_id": manifest.get("batch_id"),
        "revision": manifest.get("revision"),
        "status": "needs_material_correction",
        "cases": [],
        "diagnostics": [],
    }
    inventory = manifest.get("cases", [])
    base["counts"] = {
        "expected_cases": len(inventory) if isinstance(inventory, list) else None,
        "expected_targets": None,
        "resolved_targets": 0,
        "unavailable_cases": 0,
    }
    try:
        require(
            manifest.get("schema_version") == "rtpeval_controlled_batch_1"
            and text(manifest.get("batch_id"))
            and text(manifest.get("revision")),
            "manifest",
            "Invalid controlled batch",
        )
        require(
            datetime.fromisoformat(generated_at).utcoffset() is not None,
            "generated_at",
            "Offset required",
        )
        require(
            isinstance(inventory, list) and bool(inventory),
            "cases",
            "Declared case inventory required",
        )
        ids = [r["case_id"] for r in inventory]
        require(
            len(ids) == len(set(ids)) and all(text(i) for i in ids),
            "cases",
            "Unique case IDs required",
        )
        for row in inventory:
            goals = row.get("expected_goal_ids")
            require(
                row.get("role") in {"target", "control"}
                and isinstance(goals, list)
                and all(text(g) for g in goals)
                and len(goals) == len(set(goals)),
                "cases",
                "Invalid case/goal inventory",
            )
        base["counts"].update(
            expected_targets=sum(len(r["expected_goal_ids"]) for r in inventory),
            target_cases=sum(r["role"] == "target" for r in inventory),
            control_cases=sum(r["role"] == "control" for r in inventory),
        )
        for row in inventory:
            entry = {
                "case_id": row["case_id"],
                "role": row["role"],
                "expected_goal_ids": row["expected_goal_ids"],
                "status": "unavailable",
            }
            base["cases"].append(entry)
            try:
                report, digest = _artifact(
                    Path(root).resolve(), row["report"], "rtpeval_controlled_report_1"
                )
                require(
                    report.get("content_hash")
                    == canonical_digest(
                        {
                            k: v
                            for k, v in report.items()
                            if k not in {"content_hash", "generated_at"}
                        }
                    ),
                    "report",
                    "Controlled report content hash mismatch",
                )
                require(
                    (report["case_id"], report["role"]) == (row["case_id"], row["role"])
                    and {t["goal_id"] for t in report["targets"]} == set(row["expected_goal_ids"]),
                    "report",
                    "Foreign/stale case or target inventory",
                )
                entry.update(status=report["status"], report=report, file_sha256=digest)
                if report["status"] == "complete":
                    base["counts"]["resolved_targets"] += sum(
                        t["independent_outcome"] == "resolved" for t in report["targets"]
                    )
            except (MaterialError, ValueError, TypeError, KeyError, OSError) as exc:
                entry["diagnostics"] = [
                    exc.diagnostic if isinstance(exc, MaterialError) else {"explanation": str(exc)}
                ]
        base["counts"]["unavailable_cases"] = sum(r["status"] != "complete" for r in base["cases"])
        base["status"] = (
            "complete" if not base["counts"]["unavailable_cases"] else "needs_material_correction"
        )
    except (MaterialError, ValueError, KeyError, TypeError, OSError) as exc:
        base["diagnostics"] = [
            exc.diagnostic if isinstance(exc, MaterialError) else {"explanation": str(exc)}
        ]
    base["source_hashes"] = {"manifest": canonical_digest(manifest)}
    base["content_hash"] = canonical_digest({k: v for k, v in base.items() if k != "generated_at"})
    return base
