"""Two-pass request-local evidence reuse and bounded new-success acquisition."""

import asyncio
from time import perf_counter

from backend.app.evidence.selection_normalization import normalize_place_details_for_selection
from backend.app.integrations.dispatch import ProviderNotSentError
from backend.app.integrations.google.places import PLACES_DETAILS_FIELD_MASK
from backend.app.integrations.models import PlaceDetailsRequest
from backend.app.policies.poi_funnel import opening_dates_compatible
from backend.app.policies.poi_selection import evaluate_poi_eligibility
from backend.app.runtime.budget import ToolBudgetExceededError, ToolBudgetKey
from backend.app.runtime.config_models import AcquisitionConfig


async def acquire_candidate_details(acq, admitted, trip_end, target, *, adequate=None):
    runtime_config = getattr(acq, "runtime_config", None)
    config = runtime_config.acquisition if runtime_config else AcquisitionConfig()
    ends = perf_counter() + config.details_deadline_seconds
    rich, failures, attempted, pending = {}, [], [], []
    report = {
        "capacity": len(admitted),
        "new_success_target": target,
        "new_successes": 0,
        "cache_qualified": 0,
        "stop": "queue_exhausted",
    }
    before = acq._budget.summary()[ToolBudgetKey.PLACE_DETAIL_CALLS.value]["used"]

    def remaining():
        return max(0.0, ends - perf_counter())

    def qualify(original, details):
        try:
            item = normalize_place_details_for_selection(original, details)
            if item.details_opening_date and any(
                not opening_dates_compatible(item.details_opening_date, d)
                for d in item.search_opening_date_observations
            ):
                item = item.model_copy(update={"opening_date_conflict": True})
            gate = evaluate_poi_eligibility(item, trip_end=trip_end, require_details=True)
            if gate.eligible:
                rich[item.candidate.place_id] = item
                return True
            failures.append((original.candidate.place_id, gate.reason))
        except ValueError:
            failures.append((original.candidate.place_id, "invalid_details"))
        return False

    processed = set()
    try:
        # Complete the compatible-cache pass before any paid ordinary acquisition.
        for original in admitted:
            if remaining() <= 0:
                report["stop"] = "deadline"
                break
            pid = original.candidate.place_id
            request = PlaceDetailsRequest(place_id=pid, field_mask=PLACES_DETAILS_FIELD_MASK)
            key = acq._place_details_cache_key(request)
            cached, hit = acq._cache.lookup(key)
            if hit or acq._cache.terminal_attempt(key):
                processed.add(pid)
                if hit and cached.value is not None:
                    attempted.append(pid)
                    report["cache_qualified"] += int(qualify(original, cached.value))
                else:
                    failures.append((pid, "previous_sent_unavailable"))
            else:
                pending.append((original, request, key))
            await asyncio.sleep(0)
        if report["stop"] != "deadline":
            for original, request, key in pending:
                pid = original.candidate.place_id
                if remaining() <= 0:
                    report["stop"] = "deadline"
                    break
                if report["new_successes"] >= target:
                    if adequate is None or await adequate(list(rich.values()), ends):
                        report["stop"] = "new_success_target"
                        break
                    # Resume this queue, preserving the original deadline and counters.
                    target = min(len(admitted), target + runtime_config.poi_semantics.batch_size)
                    report["continued_for_semantic_supply"] = True
                if len(rich) >= len(admitted):
                    report["stop"] = "comparison_capacity"
                    break
                cached, hit = acq._cache.lookup(key)
                if hit:
                    processed.add(pid)
                    if cached.value is not None:
                        report["cache_qualified"] += int(qualify(original, cached.value))
                    else:
                        failures.append((pid, "previous_sent_unavailable"))
                    continue
                if acq._budget.remaining(ToolBudgetKey.PLACE_DETAIL_CALLS) <= 0:
                    report["stop"] = "send_budget"
                    break
                timer = asyncio.timeout(min(config.details_timeout_seconds, remaining()))
                try:
                    async with timer:
                        result = await acq._get_place_details(request)
                except ToolBudgetExceededError:
                    report["stop"] = "send_budget"
                    break
                except ProviderNotSentError:
                    report["stop"] = "pre_send_unavailable"
                    break
                except TimeoutError:
                    processed.add(pid)
                    attempted.append(pid)
                    failures.append((pid, "details_timeout"))
                    if remaining() <= 0:
                        report["stop"] = "deadline"
                        break
                    continue
                processed.add(pid)
                attempted.append(pid)
                if result.value is None:
                    failures.append((pid, result.error_type or "unavailable"))
                elif pid not in rich and qualify(original, result.value):
                    report["new_successes"] += 1
    except asyncio.CancelledError:
        report["stop"] = "caller_cancelled"
        raise
    finally:
        report["ordinary_sends"] = (
            acq._budget.summary()[ToolBudgetKey.PLACE_DETAIL_CALLS.value]["used"] - before
        )
        report["qualified_count"] = len(rich)
        report["unprocessed_ids"] = [
            p.candidate.place_id for p in admitted if p.candidate.place_id not in processed
        ]
        report["elapsed_seconds"] = config.details_deadline_seconds - remaining()
        acq._tracer.event("ordinary_details_completed", report)
        acq.details_report = report
    return list(rich.values()), failures, attempted
