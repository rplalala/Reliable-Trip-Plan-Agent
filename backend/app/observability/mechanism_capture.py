"""Caller-owned best-effort mechanism capture; no additional planner/provider calls."""

import asyncio
import hashlib
import logging

from .mechanism_observation import MechanismRecorder, current_mechanism

LOGGER = logging.getLogger(__name__)


async def capture_attempt(
    invoke,
    *,
    group_id,
    run_id,
    version,
    input_sha256,
    serialize,
    sink,
    max_bytes=1_000_000,
):
    """Use the exact saved-result serializer; preserve invocation return and exception.

    The sink receives local normalized accepted claims and projections, never raw prompts.
    Sink failures cannot be written to that failed sink and are intentionally nonfatal.
    Coverage concerns instrumented application seams, not provider receipt or model attention.
    """
    if current_mechanism.get() is not None:
        raise ValueError("Nested mechanism capture is not supported")
    if version not in ("v0", "v1", "v2", "v3") or not group_id or not run_id:
        raise ValueError("Invalid mechanism identity")
    if (
        not isinstance(input_sha256, str)
        or len(input_sha256) != 64
        or any(c not in "0123456789abcdef" for c in input_sha256)
    ):
        raise ValueError("Mechanism capture requires the original input SHA-256")
    if not isinstance(max_bytes, int) or max_bytes < 1:
        raise ValueError("Capture capacity must be positive")
    recorder = MechanismRecorder(max_bytes)
    token = current_mechanism.set(recorder)
    result = None
    outcome = "failed"
    try:
        result = await invoke()
        outcome = "completed"
        return result
    except BaseException as exc:
        outcome = "cancelled" if isinstance(exc, asyncio.CancelledError) else "failed"
        raise
    finally:
        current_mechanism.reset(token)
        result_hash = None
        if outcome == "completed":
            try:
                raw = serialize(result)
                result_hash = hashlib.sha256(
                    raw.encode("utf-8") if isinstance(raw, str) else raw
                ).hexdigest()
            except (Exception, asyncio.CancelledError) as exc:
                recorder.diagnostics.append(
                    {"reason": "result_hash_unavailable", "error_type": type(exc).__name__}
                )
        missing = []
        if result_hash is None:
            missing.append("result_sha256")
        if version != "v0" and not recorder.catalog_observed:
            missing.append("accepted_catalog")
        if any(not row["submitted"] for row in recorder.prepared_calls):
            missing.append("submission_observation")
        if version == "v3" and not recorder.rules_observed:
            missing.append("rule_selection_observation")
        envelope = {
            "schema_version": "rtpeval_mechanism_capture_1",
            "group_id": group_id,
            "run_id": run_id,
            "version": version,
            "input_sha256": input_sha256,
            "result_sha256": result_hash,
            "outcome": outcome,
            "collection_status": "partial" if missing or recorder.diagnostics else "available",
            "coverage": {
                "model_submission": "instrumented_default_adapter_only",
                "rule_selection": "actual_v3_opening_only",
                "provider_receipt_or_attention": "not_observed",
            },
            "missing_fields": missing,
            "diagnostics": recorder.diagnostics,
            "catalog": recorder.catalog,
            "prepared_calls": recorder.prepared_calls,
            "occurrences": recorder.occurrences,
        }
        try:
            sink(envelope)
        except (Exception, asyncio.CancelledError) as exc:
            LOGGER.warning("Mechanism capture sink failed: %s", type(exc).__name__)
