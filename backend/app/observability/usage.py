"""Opt-in request-local numeric observations; never budgets or planner decisions."""

import asyncio
import json
import math
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import UTC, datetime
from functools import wraps
from time import monotonic
from urllib.parse import urlsplit
from uuid import uuid4

current_usage = ContextVar("usage_ledger", default=None)
_stage = ContextVar("usage_stage", default=())


def tokens(raw):
    if hasattr(raw, "model_dump"):
        raw = raw.model_dump()
    raw = raw if isinstance(raw, dict) else {}
    result = {}
    for name, alternate in (
        ("input_tokens", "prompt_tokens"),
        ("output_tokens", "completion_tokens"),
        ("total_tokens", "total_tokens"),
    ):
        value = raw.get(name, raw.get(alternate))
        result[name] = value if type(value) is int and value >= 0 else None
    derived = False
    if result["total_tokens"] is None and all(
        result[k] is not None for k in ("input_tokens", "output_tokens")
    ):
        result["total_tokens"] = result["input_tokens"] + result["output_tokens"]
        derived = True
    return {
        **result,
        "total_status": "derived"
        if derived
        else "reported"
        if result["total_tokens"] is not None
        else "missing",
    }


class UsageLedger:
    """One attempt, no cumulative trace ingestion and no prompts/URLs/credentials."""

    def __init__(self, *, clock=monotonic):
        self.clock = clock
        self.models = {}
        self.providers = {}
        self.cache = []
        self.stages = []
        self.diagnostics = []
        self.active = True
        self.hook_cleanups = []

    def begin(self, kind, provider, operation, *, event_id=None, **fields):
        event_id = event_id or uuid4().hex
        rows = self.models if kind == "model" else self.providers
        if not self.active or event_id in rows:
            return event_id
        stack = _stage.get()
        rows[event_id] = {
            "event_id": event_id,
            "provider": provider,
            "operation": operation,
            "stage": stack[-1][0] if stack else "unattributed",
            "round_id": next((r for _, r in reversed(stack) if r is not None), None),
            "repair": any(s in ("repair", "repair_round") for s, _ in stack),
            "started": self.clock(),
            "outcome": "incomplete",
            **fields,
        }
        return event_id

    def finish(self, kind, event_id, *, outcome="completed", usage=None, **fields):
        row = (self.models if kind == "model" else self.providers).get(event_id)
        if row is None or not self.active or row["outcome"] != "incomplete":
            return
        row.update(outcome=outcome, elapsed_seconds=max(0, self.clock() - row["started"]), **fields)
        if kind == "model":
            row.update(tokens(usage))

    def snapshot(self):
        def copy(rows):
            return [{k: v for k, v in row.items() if k != "started"} for row in rows]

        models = copy(self.models.values())
        for row in models:
            for key, value in tokens(None).items():
                row.setdefault(key, value)
        providers = copy(self.providers.values())
        return {
            "model_calls": models,
            "provider_events": providers,
            "cache_events": list(self.cache),
            "stage_summaries": list(self.stages),
            "repair_summary": {
                "observed_rounds": len(
                    {
                        row["round_id"]
                        for row in self.stages
                        if row["stage"] == "repair_round" and row["round_id"] is not None
                    }
                ),
                "model_event_ids": [r["event_id"] for r in models if r["repair"]],
                "provider_event_ids": [r["event_id"] for r in providers if r["repair"]],
            },
            "missing_fields": [
                "stage_attribution"
                if any(r["stage"] == "unattributed" for r in models + providers)
                else None,
                "provider_usage" if any(r["total_tokens"] is None for r in models) else None,
            ],
            "diagnostics": list(self.diagnostics),
        }


@contextmanager
def usage_stage(name, round_id=None):
    ledger = current_usage.get()
    if ledger is None:
        yield
        return
    started = ledger.clock()
    token = _stage.set((*_stage.get(), (name, round_id)))
    outcome = "completed"
    try:
        yield
    except BaseException as exc:
        outcome = "cancelled" if isinstance(exc, asyncio.CancelledError) else "failed"
        raise
    finally:
        ledger.stages.append(
            {
                "stage": name,
                "round_id": round_id,
                "outcome": outcome,
                "elapsed_seconds": max(0, ledger.clock() - started),
                "scope": "inclusive_not_additive",
            }
        )
        _stage.reset(token)


def staged(name):
    def decorate(fn):
        @wraps(fn)
        async def wrapped(*args, **kwargs):
            with usage_stage(name, kwargs.get("round_index")):
                if args and current_usage.get() is not None:
                    root = getattr(getattr(args[0], "_chat_model", None), "root_async_client", None)
                    install_http_hooks(
                        getattr(root, "_client", None), "azure_foundry", "model_http"
                    )
                return await fn(*args, **kwargs)

        return wrapped

    return decorate


def cache_hit(operation, *, kind="cache_hit"):
    ledger = current_usage.get()
    if ledger is not None and ledger.active:
        ledger.cache.append(
            {
                "event_id": uuid4().hex,
                "operation": str(operation),
                "stage": _stage.get()[-1][0] if _stage.get() else "unattributed",
                "outcome": kind,
            }
        )


async def observe_sdk(call, *, usage_operation, usage_provider, **kwargs):
    ledger = current_usage.get()
    if ledger is None:
        return await call(**kwargs)
    with usage_stage(usage_operation):
        sdk = getattr(getattr(call, "__self__", None), "_client", None)
        install_http_hooks(getattr(sdk, "_client", None), usage_provider, usage_operation)
        eid = ledger.begin(
            "model",
            usage_provider,
            usage_operation,
            model=kwargs.get("model"),
            source="sdk_response_usage",
        )
        try:
            result = await call(**kwargs)
        except BaseException as exc:
            ledger.finish(
                "model",
                eid,
                outcome="cancelled" if isinstance(exc, asyncio.CancelledError) else "failed",
                error_type=type(exc).__name__,
            )
            raise
        raw = result.get("usage") if isinstance(result, dict) else getattr(result, "usage", None)
        ledger.finish("model", eid, usage=raw)
        return result


def http_operation(request):
    """Categorize without retaining host, URL, body, headers or user-supplied keys."""
    parsed = urlsplit(str(request.url))
    host, path = parsed.hostname or "", parsed.path
    if host == "places.googleapis.com":
        return "google", "places_search" if ":search" in path else "place_details"
    if host == "routes.googleapis.com":
        return "google", "route_matrix"
    if host.endswith("open-meteo.com"):
        return "open_meteo", "weather"
    return "external", "http_request"


def install_http_hooks(client, provider=None, operation=None):
    """Attach once to an owned client's documented hook lists; inactive outside capture."""
    ledger = current_usage.get()
    if ledger is None or not ledger.active:
        return
    if not isinstance(getattr(client, "event_hooks", None), dict):
        return
    registration = getattr(client, "_rtpeval_usage_hooks", None)
    if isinstance(registration, dict):
        if ledger in registration["users"]:
            return
        registration["users"].add(ledger)
        ledger.hook_cleanups.append(lambda: release_http_hooks(client, ledger))
        return
    client._rtpeval_usage_hooks = {"users": {ledger}}
    ledger.hook_cleanups.append(lambda: release_http_hooks(client, ledger))

    async def sent(request):
        ledger = current_usage.get()
        if ledger is None or not ledger.active:
            return
        p, op = http_operation(request)
        elements = None
        if op == "route_matrix":
            try:
                body = json.loads(request.content)
                elements = len(body["origins"]) * len(body["destinations"])
            except (ValueError, KeyError, TypeError, AttributeError):
                pass
        eid = ledger.begin(
            "provider",
            provider or p,
            operation or op,
            send_status="transport_entered",
            element_count=elements,
            source="http_request_hook",
        )
        request.extensions["rtpeval_usage_event"] = (ledger, eid)

    async def received(response):
        pair = response.request.extensions.pop("rtpeval_usage_event", None)
        if pair:
            ledger, eid = pair
            ledger.finish(
                "provider",
                eid,
                outcome="completed" if response.status_code < 400 else "failed",
                status_code=response.status_code,
            )

    client.event_hooks["request"].append(sent)
    client.event_hooks["response"].append(received)
    client._rtpeval_usage_hooks.update(request=sent, response=received)


def release_http_hooks(client, ledger):
    registration = getattr(client, "_rtpeval_usage_hooks", None)
    if not isinstance(registration, dict):
        return
    registration["users"].discard(ledger)
    if registration["users"]:
        return
    for kind in ("request", "response"):
        callback = registration.get(kind)
        if callback in client.event_hooks[kind]:
            client.event_hooks[kind].remove(callback)
    del client._rtpeval_usage_hooks


def finish_attempt(ledger, started, started_at, outcome):
    elapsed = ledger.clock() - started
    if not math.isfinite(elapsed) or elapsed < 0:
        raise ValueError("Invalid monotonic duration")
    ledger.active = False
    for cleanup in ledger.hook_cleanups:
        cleanup()
    ledger.hook_cleanups.clear()
    data = ledger.snapshot()
    data["missing_fields"] = [v for v in data["missing_fields"] if v]
    data["timing"] = {
        "scope": "selected_invocation_through_cleanup",
        "started_at": started_at,
        "finished_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": elapsed,
        "status": "measured",
    }
    data["outcome"] = outcome
    return data
