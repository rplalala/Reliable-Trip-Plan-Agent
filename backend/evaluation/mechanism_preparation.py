"""Immutable selected-result and optional-channel preparation without planner imports."""

import hashlib
import json
from pathlib import Path

from .intake import _artifact, _constant, _float, _pairs, _read, load_batch
from .records import IntakeResult, MaterialError, canonical_digest, freeze, require, thaw

LINK_FIELDS = ("group_id", "run_id", "version", "input_sha256", "result_sha256")
CHANNELS = ("capture", "trace", "usage", "independent")


def _validate_observation(observation, run, selection_sha256):
    require(linkage(observation) == linkage(run), "observations", "Stale/foreign linkage")
    content = observation["content"]
    require(isinstance(content, dict), "observations", "Object envelope required")
    require(
        canonical_digest(content) == observation["content_sha256"],
        "observations",
        "Observation content hash mismatch",
    )
    channel = observation["channel"]
    if channel in ("capture", "usage"):
        fields = LINK_FIELDS if channel == "capture" else LINK_FIELDS[:-2] + ("result_sha256",)
        require(
            all(content.get(k) == run[k] for k in fields),
            "observations",
            "Inner envelope linkage mismatch",
        )
    elif channel == "independent":
        schema = content.get("schema_version")
        require(
            schema
            in (
                "rtpeval_v3_pair_report_1",
                "rtpeval_v3_pair_report_2",
                "rtpeval_controlled_report_1",
            )
            and run["version"] == "v3"
            and content.get("status") == "complete",
            "independent",
            "Complete independent V3 report required",
        )
        require(
            content.get("content_hash")
            == canonical_digest(
                {k: v for k, v in content.items() if k not in ("generated_at", "content_hash")}
            ),
            "independent",
            "Independent report hash mismatch",
        )
        field = "intake" if schema.startswith("rtpeval_v3_pair_report_") else "preparation"
        require(
            content["source_hashes"][field] == selection_sha256,
            "independent",
            "Report does not bind the selected source preparation",
        )


def value_dict(value):
    return value.to_dict() if hasattr(value, "to_dict") else thaw(value)


def linkage(row):
    return {key: row[key] for key in LINK_FIELDS}


def diagnostic(exc):
    return (
        exc.diagnostic
        if isinstance(exc, MaterialError)
        else {
            "reason": "material_invalid",
            "explanation": str(exc),
        }
    )


def unique_rows(rows, identity, pointer):
    """Exact copies retain provenance; conflicting identities are not silently selected."""
    indexed = {}
    for index, row in enumerate(rows):
        key = identity(row)
        require(key is not None, pointer, "Observation identity is missing")
        if key in indexed:
            require(indexed[key]["value"] == row, pointer, "Conflicting observation identity")
            indexed[key]["source_refs"].append(f"{pointer}/{index}")
        else:
            indexed[key] = {"value": row, "source_refs": [f"{pointer}/{index}"]}
    return list(indexed.values())


def prepare_sources(selection, sources, *, observations=()):
    """Bind exact saved bytes to an accepted batch or genuine Ticket 11 V3-only selection.

    Optional observation rows are {linkage, channel, content, content_sha256}; the content
    digest is canonical JSON, while artifact_sha256 (if present) preserves saved-file bytes.
    Optional-channel failures are local and never mutate independent quality preparation.
    """
    selection, sources = value_dict(selection), value_dict(sources)
    require(selection.get("status") == "accepted", "selection", "Accepted selection required")
    if "batch_id" in sources:
        require(
            (sources["batch_id"], sources["batch_revision"])
            == (selection["batch_id"], selection["revision"]),
            "sources",
            "Foreign selection",
        )
    source_index = {}
    for item in unique_rows(sources["records"], lambda r: (r["group_id"], r["run_id"]), "sources"):
        source_index[(item["value"]["group_id"], item["value"]["run_id"])] = item
    runs = []
    selected_keys = set()
    for group in selection["inventory"]:
        for version, run in group["runs"].items():
            context = run["final"]["context"]
            key = (group["group_id"], context["run_id"])
            selected_keys.add(key)
            link = {
                "group_id": key[0],
                "run_id": key[1],
                "version": version,
                "input_sha256": group["input_sha256"],
                "result_sha256": context["artifact_sha256"],
            }
            record = {
                **link,
                "result": None,
                "result_raw_utf8": None,
                "source_refs": [],
                "diagnostics": [],
                "channels": {
                    name: {"status": "unavailable", "records": [], "diagnostics": []}
                    for name in CHANNELS
                },
            }
            try:
                item = source_index.get(key)
                require(item is not None, "sources", "Selected result source is absent")
                row = item["value"]
                require(
                    all(
                        row.get(k, version if k == "version" else None) == v
                        for k, v in link.items()
                    ),
                    "sources",
                    "Source linkage mismatch",
                )
                raw = row["raw_utf8"].encode("utf-8")
                require(
                    hashlib.sha256(raw).hexdigest() == link["result_sha256"],
                    "sources",
                    "Result byte hash mismatch",
                )
                result = json.loads(
                    row["raw_utf8"],
                    object_pairs_hook=_pairs,
                    parse_constant=_constant,
                    parse_float=_float,
                )
                require(
                    isinstance(result, dict) and result.get("system_version") == version,
                    "sources",
                    "Source version mismatch",
                )
                record.update(
                    result=result, result_raw_utf8=row["raw_utf8"], source_refs=item["source_refs"]
                )
            except (ValueError, TypeError, KeyError) as exc:
                record["diagnostics"].append(diagnostic(exc))
            runs.append(record)
    require(set(source_index) <= selected_keys, "sources", "Foreign result sources")
    run_index = {(r["group_id"], r["run_id"]): r for r in runs}
    optional_diagnostics = []
    for observation in observations:
        require(isinstance(observation, dict), "observations", "Observation row must be an object")
        key = (observation.get("group_id"), observation.get("run_id"))
        if (
            observation.get("channel") not in CHANNELS
            or not all(isinstance(v, str) for v in key)
            or key not in run_index
        ):
            optional_diagnostics.append(
                {
                    "reason": "foreign_optional_observation",
                    "channel": observation.get("channel"),
                    "run_id": key[1],
                }
            )
            continue
        run = run_index[key]
        channel = run["channels"][observation["channel"]]
        try:
            _validate_observation(observation, run, canonical_digest(selection))
            channel["records"].append(dict(observation))
            channel["status"] = "available"
        except (ValueError, TypeError, KeyError) as exc:
            channel["diagnostics"].append(diagnostic(exc))
    for run in runs:
        for channel in run["channels"].values():
            if channel["diagnostics"]:
                channel.update(status="needs_material_correction", records=[])
    return IntakeResult(
        "accepted",
        freeze(
            {
                "schema_version": "rtpeval_mechanism_preparation_1",
                "batch_id": selection["batch_id"],
                "revision": selection["revision"],
                "selection_sha256": canonical_digest(selection),
                "runs": runs,
                "optional_diagnostics": optional_diagnostics,
            }
        ),
    )


def read_batch_sources(manifest_path, *, observations=()):
    """Read the existing four-version batch contract and its selected exact result bytes."""
    path = Path(manifest_path).resolve()
    selection = load_batch(path)
    require(selection.status == "accepted", "manifest", "Batch requires material correction")
    manifest, _ = _read(path)
    rows, optional = [], list(observations)
    for group in manifest["groups"]:
        for version, run in group["selected_runs"].items():
            _, digest = _artifact(path.parent, run["result_ref"])
            raw = (path.parent / run["result_ref"]["path"]).read_bytes()
            require(
                hashlib.sha256(raw).hexdigest() == digest, "result", "Result changed during read"
            )
            link = {
                "group_id": group["group_id"],
                "run_id": run["run_id"],
                "version": version,
                "input_sha256": group["input_ref"]["sha256"],
                "result_sha256": digest,
            }
            rows.append({**link, "raw_utf8": raw.decode("utf-8")})
            usage, usage_hash = _artifact(path.parent, run["usage_ref"], "rtpeval_usage_1")
            optional.append(
                {
                    **link,
                    "channel": "usage",
                    "content": usage,
                    "content_sha256": canonical_digest(usage),
                    "artifact_sha256": usage_hash,
                }
            )
    return prepare_sources(selection, {"records": rows}, observations=optional)


def validated_preparation(value):
    prepared = value_dict(value)
    require(
        prepared.get("schema_version") == "rtpeval_mechanism_preparation_1",
        "preparation",
        "Mechanism preparation required",
    )
    for run in prepared["runs"]:
        if run["result"] is not None:
            try:
                raw = run["result_raw_utf8"]
                require(
                    hashlib.sha256(raw.encode("utf-8")).hexdigest() == run["result_sha256"],
                    "result",
                    "Saved result byte hash mismatch",
                )
                parsed = json.loads(
                    raw, object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_float
                )
                require(
                    parsed == run["result"] and parsed["system_version"] == run["version"],
                    "result",
                    "Prepared result differs from exact source",
                )
            except (ValueError, TypeError, KeyError) as exc:
                run["result"] = None
                run["diagnostics"].append(diagnostic(exc))
        for name, channel in run["channels"].items():
            if channel["status"] == "available":
                try:
                    for record in channel["records"]:
                        require(
                            record["channel"] == name, "channel", "Observation channel mismatch"
                        )
                        _validate_observation(record, run, prepared["selection_sha256"])
                except (ValueError, TypeError, KeyError) as exc:
                    channel.update(status="needs_material_correction", records=[])
                    channel["diagnostics"].append(diagnostic(exc))
    return prepared
