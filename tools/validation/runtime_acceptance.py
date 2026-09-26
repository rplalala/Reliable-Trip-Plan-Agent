"""Development-only session ownership and non-intrusive acceptance telemetry."""

import asyncio
import json
from contextlib import contextmanager
from contextvars import ContextVar
from time import perf_counter
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from openai import DefaultAsyncHttpxClient, DefaultHttpxClient

from backend.app.services import preference_interpretation as _bootstrap  # noqa: F401
from backend.app.versions.v0.runner import create_foundry_client
from tools.validation.requirement_capture import DevelopmentRequirementCapture


class SharedDependencyFailure(RuntimeError):
    """Local acceptance dependency is unusable; no further cases may start."""


class ResponseObserver(BaseCallbackHandler):
    """Capture LangChain output before business DTO conversion, without changing it."""

    def __init__(self, session):
        self.session = session

    def on_llm_end(self, response, **kwargs):
        for batch in response.generations:
            for generation in batch:
                message = getattr(generation, "message", None)
                if message is not None:
                    self.session.record("langchain_response", message.model_dump(mode="json"))


class AcceptanceSession:
    """Single-loop, sequential cases borrow one model; only this owner closes it.

    Explicit transport injection bypasses LangChain's global client caches. The scoped
    constructor adapter invokes the existing project factory without production edits.
    Caller-supplied clients are borrowed and are never closed by this session.
    """

    def __init__(self, *, settings=None, client=None, transport=None, directory=None, capture=True):
        if (settings is None) == (client is None):
            raise ValueError("Supply settings for ownership or an explicitly borrowed client")
        self.settings, self.client, self.transport = settings, client, transport
        self.directory, self.capture_enabled = directory, capture
        self.owned = client is None
        self.session_id = uuid4().hex
        self.call = ContextVar(f"acceptance_{self.session_id}", default=None)
        self.case_id = None
        self.calls, self.events, self.capture_errors = {}, [], []
        self.used_cases = set()
        self.broken = None
        self.close_count = 0
        self._entered = False

    async def __aenter__(self):
        if self._entered:
            raise SharedDependencyFailure("A session cannot be re-entered")
        self._entered = True
        self.loop = asyncio.get_running_loop()
        self.http = self.sync_http = None
        try:
            if self.owned:
                options = {} if self.transport is None else {"transport": self.transport}
                self.http = DefaultAsyncHttpxClient(**options)
                self.sync_http = DefaultHttpxClient()

                def construct(**kwargs):
                    return ChatOpenAI(
                        **kwargs, http_async_client=self.http, http_client=self.sync_http
                    )

                with patch("backend.app.llm.azure_foundry.client.ChatOpenAI", construct):
                    self.client = create_foundry_client(self.settings)
            self.chat = self.client._chat_model
            self.sdk = self.chat.root_async_client
            self.http = self.sdk._client
            self.original_callbacks = self.chat.callbacks
            self.callback = ResponseObserver(self)
            self.original_process = self.sdk._process_response
            self.hook = self._request_hook
            self.response_hook = self._response_hook
            if self.capture_enabled:
                if self.original_callbacks is not None and not isinstance(
                    self.original_callbacks, list
                ):
                    raise SharedDependencyFailure("Unsupported existing callback manager")
                self.chat.callbacks = [*(self.original_callbacks or []), self.callback]
                self.http.event_hooks["request"].append(self.hook)
                self.http.event_hooks["response"].append(self.response_hook)
                self.sdk._process_response = self._process_response
            self.capture = None
            if self.directory is not None and self.capture_enabled:
                try:
                    self.capture = DevelopmentRequirementCapture(
                        self.directory / self.session_id,
                        scenario_id=self.session_id,
                        secrets=getattr(self.client, "_capture_secrets", ()),
                    )
                except Exception as exc:
                    self.capture_errors.append(type(exc).__name__)
            return self
        except BaseException:
            await self.__aexit__(None, None, None)
            raise

    async def __aexit__(self, *args):
        if hasattr(self, "original_process"):
            if self.sdk._process_response == self._process_response:
                self.sdk._process_response = self.original_process
            if isinstance(self.chat.callbacks, list) and self.callback in self.chat.callbacks:
                self.chat.callbacks.remove(self.callback)
                if self.chat.callbacks == (self.original_callbacks or []):
                    self.chat.callbacks = self.original_callbacks
            if self.hook in self.http.event_hooks["request"]:
                self.http.event_hooks["request"].remove(self.hook)
            if self.response_hook in self.http.event_hooks["response"]:
                self.http.event_hooks["response"].remove(self.response_hook)
        if self.owned and not self.close_count:
            self.close_count += 1
            try:
                if self.http is not None and not self.http.is_closed:
                    await self.http.aclose()
            finally:
                if self.sync_http is not None and not self.sync_http.is_closed:
                    self.sync_http.close()

    def ready(self):
        if asyncio.get_running_loop() is not self.loop:
            raise SharedDependencyFailure("Acceptance session belongs to a different event loop")
        if self.broken or self.capture_errors or self.http.is_closed:
            raise SharedDependencyFailure(self.broken or "Closed client or unhealthy capture")
        if self.sdk._client is not self.http or self.chat.root_async_client is not self.sdk:
            raise SharedDependencyFailure("Model transport changed during the session")

    def begin_case(self, case_id):
        self.ready()
        if case_id in self.used_cases:
            raise SharedDependencyFailure("A case cannot be dispatched twice")
        self.used_cases.add(case_id)
        self.case_id = case_id

    def record(self, layer, payload):
        if not self.capture_enabled:
            return
        call_id = self.call.get()
        entry = {"case_id": self.case_id, "call_id": call_id, "layer": layer, "payload": payload}
        self.events.append(entry)
        if call_id in self.calls and layer == "sdk_response":
            payload["attempt"] = self.calls[call_id]["http_sends"]
            key = (payload["attempt"], payload.get("response_id"))
            if any(
                (v["attempt"], v.get("response_id")) == key
                for v in self.calls[call_id]["responses"]
            ):
                return
            # One response observation per actual send. Usage is counted here ONLY;
            # callbacks and HTTP observations are corroboration, never summed again.
            self.calls[call_id]["responses"].append(payload)
        try:
            if self.capture is not None:
                path = self.capture.record(call_id or uuid4().hex, layer, entry)
                if path is None:
                    self.capture_errors.append("artifact_write_failed")
        except Exception as exc:
            self.capture_errors.append(type(exc).__name__)

    async def _request_hook(self, request):
        call_id = self.call.get()
        if call_id in self.calls:
            self.calls[call_id]["http_sends"] += 1
        self.record("http_send", {"method": request.method, "path": request.url.path})

    async def _response_hook(self, response):
        payload = {
            "status_code": response.status_code,
            "request_id": response.headers.get("x-request-id"),
        }
        call_id = self.call.get()
        if call_id in self.calls:
            self.calls[call_id]["http_responses"].append(payload)
        self.record("http_response", payload)

    async def _process_response(self, **kwargs):
        response = kwargs["response"]
        try:
            # Non-streaming SDK responses are already buffered here. Never consume SSE.
            payload = response.json() if not kwargs["stream"] else None
            self.record(
                "sdk_response",
                {
                    "request_id": response.headers.get("x-request-id"),
                    "response_id": payload.get("id") if isinstance(payload, dict) else None,
                    "usage": payload.get("usage") if isinstance(payload, dict) else None,
                    "status": payload.get("status") if isinstance(payload, dict) else None,
                    "model": payload.get("model") if isinstance(payload, dict) else None,
                    "raw_response": payload,
                },
            )
        except Exception as exc:
            self.capture_errors.append(type(exc).__name__)
        return await self.original_process(**kwargs)

    @contextmanager
    def observe_provider_http(self, http, provider):
        """Borrow either HTTP family; preserve hooks and never read response bodies."""
        pending = {}

        async def request_hook(request):
            attempt = uuid4().hex
            pending[id(request)] = attempt
            self.record(
                "provider_send",
                {
                    "provider": provider,
                    "attempt_id": attempt,
                    "method": request.method,
                    "path": request.url.path,
                },
            )

        async def response_hook(response):
            self.record(
                "provider_response",
                {
                    "provider": provider,
                    "attempt_id": pending.pop(id(response.request), None),
                    "status_code": response.status_code,
                },
            )

        http.event_hooks["request"].append(request_hook)
        http.event_hooks["response"].append(response_hook)
        try:
            yield
        finally:
            http.event_hooks["request"].remove(request_hook)
            http.event_hooks["response"].remove(response_hook)

    @property
    def last_call_metadata(self):
        return getattr(self.client, "last_call_metadata", None)

    @contextmanager
    def observe_json_transport(self, *, transport=None):
        """Observe project JSON clients without replacing a global HTTP client type.

        The project adapter still creates and closes each real client. Optional
        transport injection is for offline tests only. SDK HTTP family detection
        continues to see the original httpx module and class.
        """
        from backend.app.integrations import http as adapter

        original = adapter.httpx
        pending = {}

        async def on_request(request):
            attempt = uuid4().hex
            pending[id(request)] = (attempt, perf_counter())
            body = None
            if request.content:
                try:
                    body = json.loads(request.content)
                except (ValueError, UnicodeDecodeError):
                    pass
            self.record(
                "external_http_send",
                {
                    "attempt_id": attempt,
                    "method": request.method,
                    "host": request.url.host,
                    "path": request.url.path,
                    "field_mask": request.headers.get("x-goog-fieldmask"),
                    "body": body,
                },
            )

        async def on_response(response):
            attempt, started = pending.pop(id(response.request), (None, None))
            self.record(
                "external_http_response",
                {
                    "attempt_id": attempt,
                    "status": response.status_code,
                    "seconds": None if started is None else perf_counter() - started,
                },
            )

        def create_client(**kwargs):
            hooks = kwargs.pop("event_hooks", {}) or {}
            kwargs["event_hooks"] = {
                **hooks,
                "request": [*hooks.get("request", []), on_request],
                "response": [*hooks.get("response", []), on_response],
            }
            if transport is not None:
                kwargs["transport"] = transport
            return original.AsyncClient(**kwargs)

        local_http = SimpleNamespace(AsyncClient=create_client, HTTPError=original.HTTPError)
        with patch.object(adapter, "httpx", local_http):
            yield

    def capture_requirement_outcome(self, draft, error=None):
        return self.client.capture_requirement_outcome(draft, error)

    async def generate_structured(self, **kwargs):
        # Per-case readiness runs before acquisition. Do not turn a mid-case capture
        # write failure into an application failure; stop at the next case boundary.
        call_id = uuid4().hex
        token = self.call.set(call_id)
        row = {
            "case_id": self.case_id,
            "http_sends": 0,
            "http_responses": [],
            "responses": [],
            "mapped": False,
        }
        self.calls[call_id] = row
        method = kwargs.pop("_method", "generate_structured")
        capture_input = {k: v for k, v in kwargs.items() if k != "usage_callback"}
        capture_input["response_schema"] = kwargs["response_schema"].__name__
        if capture_input.get("_generation_config") is not None:
            capture_input["_generation_config"] = capture_input["_generation_config"].model_dump(
                mode="json"
            )
        self.record("model_input", capture_input)
        try:
            if method != "generate_structured":
                kwargs.pop("response_schema")
            result = await getattr(self.client, method)(**kwargs)
            row["mapped"] = True
            self.record("domain_output", result.model_dump(mode="json"))
            return result
        finally:
            self.call.reset(token)

    def save_result(self, payload):
        self.record("case_result", payload)

    async def generate_primary_structured(self, *, generation_config, **kwargs):
        """Keep session capture and ownership for configured primary generation."""
        return await self.generate_structured(**kwargs, _generation_config=generation_config)

    async def generate_poi_semantics_structured(self, **kwargs):
        from backend.app.schemas.poi_semantics import SemanticAssessmentBatch

        return await self.generate_structured(
            **kwargs,
            response_schema=SemanticAssessmentBatch,
            _method="generate_poi_semantics_structured",
        )


def failure_kind(exc, session):
    """Classify wrapped errors without natural-language exception matching."""
    from openai import APIConnectionError, APIStatusError

    from backend.app.schemas.requirement_boundary import RequirementBoundaryError

    if session.http.is_closed or isinstance(exc, SharedDependencyFailure):
        return "shared_dependency_failure"
    current, seen = exc, set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(current, TypeError):
            # A development invocation/configuration fault must not spend another case.
            return "shared_dependency_failure"
        if isinstance(current, APIStatusError):
            return (
                "shared_dependency_failure"
                if current.status_code in (400, 401, 403, 404)
                else "provider_failure"
            )
        if isinstance(current, APIConnectionError):
            return "provider_failure"
        if isinstance(current, RequirementBoundaryError):
            if current.category == "configuration_failure":
                return "shared_dependency_failure"
        current = current.__cause__ or current.__context__
    return "content_or_business_failure"
