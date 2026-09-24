"""Standalone single-round repair service. No runner, graph, Nearby or client factory."""

import asyncio
import json
from time import monotonic

from backend.app.observability.run_trace import redact_secrets
from backend.app.versions.v3.repair_acceptance import (
    apply_patch,
    assess,
    compare,
    inclusion_ids,
    validate_scope,
)
from backend.app.versions.v3.repair_budget import RepairBudget
from backend.app.versions.v3.repair_candidates import prepare_candidates
from backend.app.versions.v3.repair_models import RepairPatch, RepairResult, TargetProgress
from backend.app.versions.v3.repair_projection import build_repair_input
from backend.app.versions.v3.repair_routes import acquire_transitions, bind_transitions
from backend.app.versions.v3.repair_schedule import check_time_permissions, consume_windows


async def run_repair_once(
    original,
    context,
    scope,
    *,
    model,
    request_deadline,
    pool=(),
    places_provider=None,
    routes_provider=None,
    intent_ids=(),
    rag=None,
    geographic_scope=None,
    cache=None,
    clock=monotonic,
    tracer=None,
    audit_max_bytes=1000000,
    budget=None,
    policy=None,
    nearby_reserve=None,
    stage_original=None,
    feedback=None,
    round_index=1,
    round_deadline=None,
    runtime_config=None,
):
    """All collaborators are injected. Optional acquisition failures are local stops.

    Inputs must be an accepted V2 primary snapshot. Cancellation is always propagated.
    No result from a rejected patch becomes the final itinerary.
    """
    budget = (
        budget
        if budget is not None
        else RepairBudget(
            request_deadline,
            clock=clock,
            cache=cache,
            policy=policy,
            nearby_reserve=nearby_reserve,
            runtime_config=runtime_config,
        )
    )
    policy = budget.policy
    timing = policy.timing
    stage_original = stage_original if stage_original is not None else original
    round_deadline = min(round_deadline or budget.deadline, budget.deadline)

    def remaining():
        return min(budget.remaining(), max(0, round_deadline - budget.clock()))

    snapshot = original.model_copy(deep=True)
    context = context.model_copy(deep=True)
    initial = assess(snapshot, context)
    whitelist, extra, progress, losses, regressions = (), (), (), (), ()
    reassessed = after = None
    sizing = {}
    attempted = False
    preparation = patch = proposed = comparison = None
    model_returned = False
    spatial = {}
    proposed_schedule = context.schedule
    window_adjustments = ()
    usage = {}
    model_timeout = None

    def audit(value):
        if value is None:
            return None, "not_constructed"
        data = redact_secrets(value)
        size = len(json.dumps(data, ensure_ascii=True).encode("utf-8"))
        if size > audit_max_bytes:
            return None, f"truncated:{size}_bytes"
        return data, "recorded"

    def result(status, reason, final=None):
        selected = final if final is not None else snapshot
        budget.used["repair_input_candidates"] = sizing.get("candidate_count", 0)
        budget.used["final_scheduled_unique"] = len(
            {a.source_place_id for d in selected.days for a in d.activities if a.source_place_id}
        )
        if preparation is not None:
            scheduled = {
                a.source_place_id for d in selected.days for a in d.activities if a.source_place_id
            }
            budget.used["repair_input_unused"] = len(
                {c.place.place_id for c in preparation.input_candidates} - scheduled
            )
            budget.used["original_supply_unused"] = len(
                set(context.original_supply_ids) - scheduled
            )
        budget.used["final_main_visits"] = sum(
            a.activity_kind == "main_poi" for d in selected.days for a in d.activities
        )
        audit_patch, patch_status = audit(patch)
        audit_proposed, proposed_status = audit(proposed)
        from backend.app.versions.v3.repair_targets import related_progress

        record = RepairResult(
            related_targets=related_progress(
                snapshot, proposed if proposed is not None else snapshot, scope, proposed_schedule
            ),
            schedule=proposed_schedule if final is not None else context.schedule,
            window_adjustments=window_adjustments,
            status=status,
            reason=reason,
            model_attempted=attempted,
            original=snapshot,
            final=selected,
            original_report=initial,
            reassessed_original_report=reassessed,
            proposed_report=after,
            target_progress=progress
            or tuple(
                TargetProgress(
                    finding_id=f.finding_id,
                    check=f.check,
                    outcome="unknown" if f.status == "UNKNOWN" else "unresolved",
                    before=None,
                    after=None,
                )
                for f in initial.findings
                if f.finding_id in scope.target_ids
            ),
            acquired_routes=extra,
            original_supply_ids=context.original_supply_ids,
            repair_whitelist=whitelist,
            final_place_ids=tuple(
                sorted(
                    {
                        a.source_place_id
                        for d in selected.days
                        for a in d.activities
                        if a.source_place_id
                    }
                )
            ),
            main_visits_lost=losses,
            coverage_regressions=regressions,
            counters=dict(budget.used),
            stops=tuple(budget.stops),
            sizing=sizing,
            candidate_preparation=preparation,
            scope=scope,
            spatial=spatial,
            effective_policy=policy.model_dump(mode="json"),
            usage=usage,
            usage_status="reported" if usage else "unavailable" if attempted else "not_called",
            timing={
                "stage_started": budget.started,
                "stage_deadline": budget.deadline,
                "round_deadline": round_deadline,
                "request_deadline": request_deadline,
                "preparation_or_route_deadline": budget.io_deadline,
                "model_timeout_seconds": model_timeout,
                "stage_remaining_seconds": budget.remaining(),
            },
            parsed_patch=audit_patch,
            proposed=audit_proposed,
            comparison=comparison,
            artifact_status={
                "patch": (
                    patch_status
                    if patch is not None
                    else "not_parsed"
                    if model_returned
                    else "model_no_return"
                    if attempted
                    else "not_executed"
                ),
                "proposal": proposed_status,
                "comparison": "recorded" if comparison is not None else "not_executed",
            },
        )

        if tracer is not None:
            # Separate compact artifacts survive truncation of the full V3 outcome.
            for name, value in (
                ("schedule", proposed_schedule),
                ("window_adjustments", window_adjustments),
                ("scope", scope),
                ("candidates", preparation),
                ("patch", audit_patch),
                ("proposal", audit_proposed),
                ("comparison", comparison),
                ("related_targets", record.related_targets),
                ("spatial", spatial),
            ):
                data, state = audit(value)
                if name == "patch":
                    state = record.artifact_status["patch"]
                if name == "proposal":
                    state = proposed_status
                tracer.event(
                    f"v3_repair_{name}",
                    {"round_index": round_index, "artifact_status": state, "value": data},
                )
            tracer.event(
                "v3_repair_decision",
                {"status": status, "reason": reason, "artifact_status": record.artifact_status},
            )
        return record

    try:
        validate_scope(snapshot, initial, scope)
        if scope.unsupported_explicit_mode and not scope.permissions:
            return result("SKIPPED", "explicit_transport_mode_not_supported")
        if remaining() <= 0:
            return result("SKIPPED", "phase_or_request_deadline")
        async with asyncio.timeout(remaining()):
            # Optional preparation cannot consume the model/recheck allocation.
            budget.io_deadline = min(
                budget.clock() + timing.preparation_seconds,
                round_deadline - timing.minimum_model_seconds - timing.recheck_reserve_seconds,
            )
            preparation = await prepare_candidates(
                context,
                scope,
                budget,
                original=snapshot,
                pool=pool,
                provider=places_provider,
                intent_ids=intent_ids,
                rag=rag,
                geographic_scope=geographic_scope,
            )
            whitelist = preparation.ledger
            if not scope.permissions and not preparation.authorizations:
                return result("SKIPPED", "no_executable_candidate_operation")
            all_places = {p.place_id: p for p in context.places}
            all_places.update({c.place.place_id: c.place for c in whitelist})
            original_bindings = bind_transitions(
                snapshot,
                None if scope.unsupported_explicit_mode else (scope.travel_mode or "WALK"),
                scope.routing_preference,
                context.schedule,
            )
            extra = await acquire_transitions(
                snapshot,
                scoped_bindings(snapshot, scope, original_bindings),
                context.route_evidence,
                tuple(all_places.values()),
                routes_provider,
                budget,
                context.schedule,
            )
            system, user, sizing = build_repair_input(
                snapshot,
                initial,
                scope,
                context,
                preparation,
                relevant_routes(
                    snapshot, scope, (*context.route_evidence, *extra), context.schedule
                ),
                policy=policy,
                feedback=feedback,
            )
            import hashlib

            fingerprint = hashlib.sha256((system + user).encode()).hexdigest()
            if fingerprint in getattr(budget, "input_fingerprints", set()):
                return result("SKIPPED", "duplicate_effective_input")
            budget.input_fingerprints = getattr(budget, "input_fingerprints", set()) | {fingerprint}
            timeout = min(timing.model_seconds, remaining() - timing.recheck_reserve_seconds)
            if timeout < timing.minimum_model_seconds:
                return result("SKIPPED", "insufficient_time_for_model_and_rechecks")
            model_timeout = timeout
            budget.charge(model=1)
            attempted = True
            from langchain_core.callbacks import UsageMetadataCallbackHandler

            callback = UsageMetadataCallbackHandler()
            try:
                async with asyncio.timeout(timeout):
                    raw = await model.generate_repair_structured(
                        system_prompt=system,
                        user_prompt=user,
                        output_tokens=policy.input.output_tokens,
                        usage_callback=callback,
                    )
            finally:
                usage = dict(callback.usage_metadata)
            model_returned = True
            patch = RepairPatch.model_validate(raw)
            required, excluded = inclusion_ids(context)
            proposed, losses = apply_patch(
                snapshot,
                patch,
                scope,
                preparation,
                required,
                excluded,
                id_prefix=f"repair_r{round_index}_new",
                context=context,
            )
            check_time_permissions(snapshot, proposed, context.schedule)
            budget.io_deadline = round_deadline - timing.finalization_reserve_seconds
            # Reject unauthorized patches BEFORE any post-repair provider work.
            if remaining() <= 0:
                return result("REJECTED", "phase_deadline")
            proposed_bindings = bind_transitions(
                proposed,
                None if scope.unsupported_explicit_mode else (scope.travel_mode or "WALK"),
                scope.routing_preference,
                context.schedule,
            )
            later = await acquire_transitions(
                proposed,
                scoped_bindings(
                    proposed, scope, proposed_bindings, previous=snapshot, schedule=context.schedule
                ),
                (*context.route_evidence, *extra),
                tuple(all_places.values()),
                routes_provider,
                budget,
                context.schedule,
            )
            extra = (*extra, *later)
            proposed, proposed_schedule, window_adjustments = consume_windows(
                snapshot,
                proposed,
                scope,
                context.schedule,
                tuple(all_places.values()),
                (*context.route_evidence, *extra),
                policy.spatial,
                prefix=f"repair_r{round_index}",
            )
            if sum(len(d.activities) for d in proposed.days) > policy.input.activity_capacity:
                raise ValueError("repair_activity_capacity_after_window_split")
            proposed_context = context.model_copy(update={"schedule": proposed_schedule})
            # Preserve initial observation; compare both arrangements on the augmented evidence.
            reassessed = assess(snapshot, context, whitelist, extra, original_bindings)
            after = assess(proposed, proposed_context, whitelist, extra, proposed_bindings)
            comparison = compare(
                snapshot, proposed, initial, reassessed, after, scope, proposed_schedule, context
            )
            from backend.app.versions.v3.repair_spatial import check_addition_layout

            spatial = check_addition_layout(
                stage_original,
                proposed,
                tuple(all_places.values()),
                (*context.route_evidence, *extra),
                scope.travel_mode,
                policy.spatial,
                required,
                routing_preference=scope.routing_preference,
                schedule=proposed_schedule,
            )
            spatial["mode_basis"] = scope.mode_source or spatial["mode_basis"]
            if scope.unsupported_explicit_mode and any(
                e.operation in {"add", "replace"} for e in patch.edits
            ):
                spatial["accepted"] = False
                spatial["reasons"].append("explicit_transport_mode_not_supported")
            if not spatial["accepted"]:
                comparison = comparison.model_copy(
                    update={
                        "accepted": False,
                        "reason": comparison.reason + "; " + "; ".join(spatial["reasons"]),
                    }
                )
            progress, regressions = comparison.progress, comparison.coverage_regressions
            if not comparison.accepted:
                return result("REJECTED", comparison.reason)
            if remaining() <= 0:
                return result("REJECTED", "phase_deadline")
            from backend.app.versions.v3.repair_targets import related_progress

            linked = related_progress(snapshot, proposed, scope, proposed_schedule)
            complete = all(p.outcome == "resolved" for p in progress) and all(
                r.status == "resolved" for r in linked
            )
            return result(
                "ACCEPTED_COMPLETE" if complete else "ACCEPTED_PARTIAL",
                "authorized_targets_complete" if complete else "partial_target_improvement",
                proposed,
            )
    except asyncio.CancelledError:
        raise
    except TimeoutError:
        return result("REJECTED" if attempted else "SKIPPED", "repair_timeout")
    except Exception as exc:
        if hasattr(exc, "counts"):
            sizing = exc.counts
        return result("REJECTED" if attempted else "SKIPPED", f"{type(exc).__name__}:{exc}")


def relevant_routes(itinerary, scope, evidence, schedule=None):
    """Project only existing adjacency dependencies touching the authorized dates."""
    pairs = set()
    for day in itinerary.days:
        if day.date not in scope.dates:
            continue
        from backend.app.versions.v3.repair_schedule import ordered_activities

        ordered = ordered_activities(day, schedule)
        pairs.update(
            (a.source_place_id, b.source_place_id)
            for a, b in zip(ordered, ordered[1:], strict=False)
        )
    return tuple(
        r.model_copy(
            update={
                "elements": [
                    e for e in r.elements if (e.origin_place_id, e.destination_place_id) in pairs
                ]
            }
        )
        for r in evidence
        if any((e.origin_place_id, e.destination_place_id) in pairs for e in r.elements)
    )


async def run_repair_stage(
    original,
    context,
    scope,
    *,
    request_deadline,
    policy=None,
    nearby_reserve=None,
    cache=None,
    clock=monotonic,
    runtime_config=None,
    **kwargs,
):
    """One resource ledger and latest-adopted state across explicit feedback iterations."""
    from backend.app.versions.v3.repair_acceptance import finding_key
    from backend.app.versions.v3.repair_models import RepairRoundRecord

    budget = RepairBudget(
        request_deadline,
        policy=policy,
        nearby_reserve=nearby_reserve,
        cache=cache,
        clock=clock,
        runtime_config=runtime_config,
    )
    policy = budget.policy
    initial = assess(original, context)
    original_keys = {
        finding_key(f): f.finding_id for f in initial.findings if f.finding_id in scope.target_ids
    }
    current = original.model_copy(deep=True)
    current_schedule = context.schedule
    active_related = scope.active_related
    ledger = {c.place.place_id: c for c in context.identity_ledger}
    routes, records, feedback = (), [], None
    patch_fingerprints = set()
    completed = set()
    stop = "model_budget_disabled" if not policy.max_model_calls else "round_limit"
    last = None
    for index in range(1, min(policy.max_rounds, policy.max_model_calls) + 1):
        effective = context.model_copy(
            update={
                "schedule": current_schedule,
                "active_related": active_related,
                "identity_ledger": tuple(ledger.values()),
                "route_evidence": (*context.route_evidence, *routes),
                "transitions": bind_transitions(
                    current,
                    None if scope.unsupported_explicit_mode else (scope.travel_mode or "WALK"),
                    scope.routing_preference,
                    current_schedule,
                ),
            }
        )
        report = assess(current, effective)
        authorized = {t.finding_id for t in report.improvement_targets}
        remaining_targets = tuple(
            f.finding_id
            for f in report.findings
            if (
                finding_key(f) in original_keys
                or f.finding_id in {r.permission.target_id for r in active_related}
            )
            and finding_key(f) not in completed
            and f.finding_id in authorized
        )
        if not remaining_targets:
            stop = "authorized_targets_complete"
            break
        confirmed_ids = {
            f.finding_id
            for f in report.findings
            if f.finding_id in remaining_targets and f.status == "CONFIRMED"
        }
        deferred = (
            tuple(i for i in remaining_targets if i not in confirmed_ids) if confirmed_ids else ()
        )
        if confirmed_ids:
            remaining_targets = tuple(i for i in remaining_targets if i in confirmed_ids)
        remaining_findings = [f for f in report.findings if f.finding_id in remaining_targets]
        addition_dates = {day for f in remaining_findings for day in (f.dates or scope.add_dates)}
        activity_ids = {aid for f in remaining_findings for aid in f.activity_ids}
        activity_ids.update(
            a.activity_id
            for d in current.days
            for a in d.activities
            if any(f.check == "overfull" and d.date in f.dates for f in remaining_findings)
        )
        excluded_targets = {
            pid
            for f in remaining_findings
            if f.reason == "excluded_identity_scheduled"
            for pid in f.place_ids
        }
        activity_ids.update(
            a.activity_id
            for d in current.days
            for a in d.activities
            if a.source_place_id in excluded_targets
        )
        round_scope = scope.model_copy(
            update={
                "target_ids": remaining_targets,
                "deferred_review_target_ids": deferred,
                "active_related": active_related,
                "add_dates": tuple(
                    d
                    for d in scope.add_dates
                    if d in addition_dates
                    or any(
                        r.permission.date == d and r.status != "resolved" for r in active_related
                    )
                ),
                "revisits": tuple(r for r in scope.revisits if r.date in addition_dates),
                "permissions": tuple(p for p in scope.permissions if p.activity_id in activity_ids),
            }
        )
        timing = policy.timing
        if budget.remaining() < timing.minimum_model_seconds + timing.recheck_reserve_seconds:
            stop = "insufficient_stage_time"
            break
        affordable = max(
            1,
            min(
                policy.max_rounds - index + 1,
                int(budget.remaining() // timing.round_reference_seconds),
            ),
        )
        allocation = min(timing.round_seconds, budget.remaining() / affordable)
        before = current.model_copy(deep=True)
        result = await run_repair_once(
            current,
            effective,
            round_scope,
            request_deadline=request_deadline,
            budget=budget,
            stage_original=original,
            feedback=feedback,
            round_index=index,
            round_deadline=clock() + allocation,
            **kwargs,
        )
        last = result
        ledger.update({c.place.place_id: c for c in result.repair_whitelist})
        routes = (*routes, *result.acquired_routes)
        accepted = result.status.startswith("ACCEPTED")
        if accepted:
            current = result.final
            current_schedule = result.schedule
            active_related = result.related_targets
            by_id = {f.finding_id: f for f in report.findings}
            completed.update(
                finding_key(by_id[p.finding_id])
                for p in result.target_progress
                if p.outcome == "resolved" and p.finding_id in by_id
            )
        serialized_patch = result.parsed_patch.model_dump_json() if result.parsed_patch else None
        repeated = serialized_patch is not None and serialized_patch in patch_fingerprints
        if serialized_patch is not None:
            patch_fingerprints.add(serialized_patch)
        terminal_failure = result.model_attempted and result.parsed_patch is None
        stop = (
            "duplicate_failed_patch"
            if repeated and not accepted
            else "model_failed_no_retry"
            if terminal_failure
            else "authorized_targets_complete"
            if set(original_keys) <= completed
            and all(r.status == "resolved" for r in active_related)
            else result.reason
            if result.status == "SKIPPED"
            else "feedback_iteration"
        )
        new_feedback = round_feedback(result, accepted)
        if len(json.dumps(new_feedback, ensure_ascii=True)) > policy.input.feedback_characters:
            stop = "feedback_capacity_exceeded"
        records.append(
            RepairRoundRecord(
                round_index=index,
                target_links={
                    f.finding_id: original_keys.get(finding_key(f), f.finding_id)
                    for f in remaining_findings
                },
                input_itinerary=before,
                result=result,
                adopted=current.model_copy(deep=True),
                feedback=feedback,
                continuation_reason=stop,
                usage=result.usage,
            )
        )
        if kwargs.get("tracer") is not None:
            # Existing trace size/redaction remains authoritative for the full artifacts.
            kwargs["tracer"].event(
                "v3_repair_round",
                {
                    "round_index": index,
                    "status": result.status,
                    "continuation_reason": stop,
                    "cumulative_counters": dict(budget.used),
                    "usage": result.usage,
                },
            )
        if stop != "feedback_iteration":
            break
        feedback = new_feedback
        budget.explore_feedback = bool(result.spatial.get("reasons"))
    else:
        stop = "round_or_model_limit"
    if last is None:
        return RepairResult(
            status="SKIPPED",
            reason=stop,
            model_attempted=False,
            original=original,
            final=current,
            original_report=initial,
            original_supply_ids=context.original_supply_ids,
            final_place_ids=tuple(
                sorted(
                    {
                        a.source_place_id
                        for d in current.days
                        for a in d.activities
                        if a.source_place_id
                    }
                )
            ),
            effective_policy=policy.model_dump(mode="json"),
            usage_status="not_called",
            scope=scope,
        )
    # Final progress is measured against the original targets, never the last rejected proposal.
    reassessed = assess(
        original,
        context,
        tuple(ledger.values()),
        routes,
        bind_transitions(
            original,
            None if scope.unsupported_explicit_mode else (scope.travel_mode or "WALK"),
            scope.routing_preference,
            current_schedule,
        ),
    )
    final_report = assess(
        current,
        context.model_copy(update={"schedule": current_schedule, "active_related": active_related}),
        tuple(ledger.values()),
        routes,
        bind_transitions(
            current,
            None if scope.unsupported_explicit_mode else (scope.travel_mode or "WALK"),
            scope.routing_preference,
            current_schedule,
        ),
    )
    summary = compare(
        original, current, initial, reassessed, final_report, scope, current_schedule, context
    )
    any_accepted = any(r.result.status.startswith("ACCEPTED") for r in records)
    status = (
        (
            "ACCEPTED_COMPLETE"
            if all(p.outcome == "resolved" for p in summary.progress)
            and all(r.status == "resolved" for r in active_related)
            else "ACCEPTED_PARTIAL"
        )
        if any_accepted
        else last.status
    )
    cumulative_usage = {}
    for record in records:
        for model_name, values in record.usage.items():
            target = cumulative_usage.setdefault(model_name, {})

            def accumulate(source, destination):
                for key, value in source.items():
                    if isinstance(value, dict):
                        accumulate(value, destination.setdefault(key, {}))
                    elif isinstance(value, (int, float)):
                        destination[key] = destination.get(key, 0) + value

            accumulate(values, target)
    return last.model_copy(
        update={
            "schedule": current_schedule,
            "related_targets": active_related,
            "window_adjustments": tuple(
                a
                for r in records
                if r.result.status.startswith("ACCEPTED")
                for a in r.result.window_adjustments
            ),
            "status": status,
            "reason": stop,
            "usage": cumulative_usage,
            "usage_status": "not_called"
            if not any(r.result.model_attempted for r in records)
            else "reported"
            if all(r.result.usage for r in records if r.result.model_attempted)
            else "partial_or_unavailable",
            "original": original,
            "final": current,
            "original_report": initial,
            "reassessed_original_report": reassessed,
            "target_progress": summary.progress,
            "repair_whitelist": tuple(ledger.values()),
            "acquired_routes": routes,
            "rounds": tuple(records),
            "counters": dict(budget.used),
            "stops": tuple(budget.stops),
            "scope": scope,
            "final_place_ids": tuple(
                sorted(
                    {
                        a.source_place_id
                        for d in current.days
                        for a in d.activities
                        if a.source_place_id
                    }
                )
            ),
            "model_attempted": any(r.result.model_attempted for r in records),
            "adopted_report": final_report,
        }
    )


def scoped_bindings(itinerary, scope, bindings, *, previous=None, schedule=None):
    """Fetch only incident authorized legs, or actually changed post-patch dependencies."""
    ids = {a.activity_id for d in itinerary.days if d.date in scope.dates for a in d.activities}
    editable = {p.activity_id for p in scope.permissions}
    selected = [b for b in bindings if b.from_activity_id in ids and b.to_activity_id in ids]
    if previous is None:
        return tuple(
            b for b in selected if not editable or {b.from_activity_id, b.to_activity_id} & editable
        )
    prior = {a.activity_id: a for d in previous.days for a in d.activities}
    current = {a.activity_id: a for d in itinerary.days for a in d.activities}
    from backend.app.versions.v3.repair_schedule import ordered_activities

    pairs = {
        (a.activity_id, b.activity_id)
        for d in previous.days
        for rows in [ordered_activities(d, schedule)]
        for a, b in zip(rows, rows[1:], strict=False)
    }
    return tuple(
        b
        for b in selected
        if (b.from_activity_id, b.to_activity_id) not in pairs
        or any(
            i not in prior
            or current[i].source_place_id != prior[i].source_place_id
            or current[i].start_time != prior[i].start_time
            or current[i].end_time != prior[i].end_time
            for i in (b.from_activity_id, b.to_activity_id)
        )
    )


def round_feedback(result, accepted):
    """Compact prior business feedback; no provider response or reasoning history."""
    return {
        "previous_status": result.status,
        "reason": result.reason,
        "previous_patch": result.parsed_patch.model_dump(mode="json")
        if result.parsed_patch
        else None,
        "comparison": result.comparison.model_dump(mode="json") if result.comparison else None,
        "spatial": result.spatial,
        "adjustment": (
            "Use different authorized candidate/time placement; preserve accepted improvements."
        )
        if not accepted
        else "Address only remaining targets on the adopted itinerary.",
    }
