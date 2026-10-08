"""Opt-in local HTTP evidence; observe owned hooks without consuming extra bytes."""

import hashlib
import json
import os
import re
from contextlib import aclosing, contextmanager
from contextvars import ContextVar
from http.cookies import SimpleCookie
from urllib.parse import parse_qsl, urlsplit

current_raw_capture = ContextVar("current_raw_capture", default=None)
BODY_LIMIT = 10_000_000
_SENSITIVE = re.compile(r"key|authorization|credential|password|secret|token|cookie", re.I)
_HEADERS = {
    "content-type",
    "content-encoding",
    "content-length",
    "x-goog-fieldmask",
    "x-request-id",
    "request-id",
    "apim-request-id",
}


def redact_known_credentials(value):
    """Filter ambient known values, including unlabelled provider echoes."""
    capture = current_raw_capture.get()
    if capture is None:
        return value
    if isinstance(value, str):
        for secret in sorted(capture.secrets, key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]")
        return value
    if isinstance(value, dict):
        return {k: redact_known_credentials(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact_known_credentials(v) for v in value]
    return value


class RawCapture:
    def __init__(self, directory):
        self.directory = directory
        self.events = []
        self.diagnostics = []
        self.secrets = set()
        for key, value in os.environ.items():
            if _SENSITIVE.search(key):
                self.remember(value)

    def remember(self, value):
        if isinstance(value, str) and value:
            self.secrets.add(value)
            if value.lower().startswith("bearer "):
                self.secrets.add(value[7:])

    def learn(self, value):
        if isinstance(value, dict):
            for key, item in value.items():
                if _SENSITIVE.search(str(key)) and isinstance(item, str):
                    self.remember(item)
                else:
                    self.learn(item)
        elif isinstance(value, list):
            for item in value:
                self.learn(item)

    def body(self, row, kind, content, *, complete=True, encoding=None, form="request_content"):
        row[f"{kind}_body_form"] = form
        if not complete:
            row[f"{kind}_body_status"] = "incomplete"
            return
        if len(content) > BODY_LIMIT:
            row[f"{kind}_body_status"] = "omitted_size_limit"
            return
        if encoding and encoding.lower() not in ("identity",):
            row[f"{kind}_body_status"] = "omitted_content_encoding"
            return
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            row[f"{kind}_body_status"] = "omitted_non_utf8"
            return
        try:
            value = json.loads(text)
        except ValueError:
            value = text
        self.learn(value)
        row[f"{kind}_body_status"] = "complete"
        row[f"_{kind}_body"] = value
        row[f"{kind}_observed_body_sha256"] = hashlib.sha256(content).hexdigest()

    def request(self, request, event_id):
        url = str(request.url)
        parts = urlsplit(url)
        for key, value in parse_qsl(parts.query, keep_blank_values=True):
            self.learn({key: value})
        for key, value in request.headers.items():
            if _SENSITIVE.search(key):
                self.remember(value)
            if key.lower() == "cookie":
                cookie = SimpleCookie()
                cookie.load(value)
                for item in cookie.values():
                    self.remember(item.value)
        self.remember(parts.password)
        row = {
            "event_id": event_id,
            "method": request.method,
            "url": url,
            "request_headers": self.headers(request),
            "response_body_status": "missing",
        }
        self.events.append(row)
        try:
            content = request.content
        except Exception:
            row["request_body_status"] = "unread_stream"
        else:
            self.body(row, "request", content)

    @staticmethod
    def headers(message):
        return {k: v for k, v in message.headers.items() if k.lower() in _HEADERS}

    def response(self, response, event_id):
        row = next((r for r in reversed(self.events) if r["event_id"] == event_id), None)
        if row is None:
            return
        row.update(status_code=response.status_code, response_headers=self.headers(response))
        try:
            content = response.content
        except Exception:
            row["response_body_status"] = "incomplete"
            original_raw, original_bytes = response.aiter_raw, response.aiter_bytes
            decoding = False

            async def observed(iterator, *, encoding=None, enabled=True, form="decoded_content"):
                data = bytearray()
                oversized = False
                completed = False
                try:
                    async with aclosing(iterator):
                        async for chunk in iterator:
                            if enabled:
                                if not oversized and len(data) + len(chunk) <= BODY_LIMIT:
                                    data.extend(chunk)
                                else:
                                    oversized = True
                                    data.clear()
                            yield chunk
                    completed = True
                finally:
                    if not enabled:
                        pass
                    elif oversized:
                        row["response_body_status"] = "omitted_size_limit"
                    else:
                        try:
                            self.body(
                                row,
                                "response",
                                bytes(data),
                                complete=completed,
                                encoding=encoding,
                                form=form,
                            )
                        except Exception as exc:
                            row["response_body_status"] = "capture_failed"
                            self.diagnostics.append(
                                {"reason": "body_capture_failed", "error_type": type(exc).__name__}
                            )

            async def raw_stream(*args, **kwargs):
                async with aclosing(
                    observed(
                        original_raw(*args, **kwargs),
                        encoding=response.headers.get("content-encoding"),
                        enabled=not decoding,
                        form="raw_content",
                    )
                ) as stream:
                    async for chunk in stream:
                        yield chunk

            async def decoded_stream(*args, **kwargs):
                nonlocal decoding
                decoding = True
                try:
                    async with aclosing(observed(original_bytes(*args, **kwargs))) as stream:
                        async for chunk in stream:
                            yield chunk
                finally:
                    decoding = False

            response.aiter_raw, response.aiter_bytes = raw_stream, decoded_stream
        else:
            self.body(row, "response", content, form="decoded_content")

    def finish(self):
        from .run_trace import redact_secrets

        for number, row in enumerate(self.events):
            for kind in ("request", "response"):
                body = row.pop(f"_{kind}_body", None)
                if row.get(f"{kind}_body_status") != "complete":
                    continue
                try:
                    name = f"evidence/wire/{number:04d}-{kind}.json"
                    path = self.directory / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(
                        (
                            json.dumps(
                                {
                                    "representation": "credential_filtered_utf8",
                                    "body": redact_secrets(body),
                                },
                                ensure_ascii=True,
                                indent=2,
                            )
                            + "\n"
                        ).encode()
                    )
                    row[f"{kind}_body_ref"] = name
                except Exception as exc:
                    row[f"{kind}_body_status"] = "write_failed"
                    self.diagnostics.append(
                        {"reason": "wire_write_failed", "error_type": type(exc).__name__}
                    )
        self.events = redact_secrets(self.events)


@contextmanager
def capture_raw(directory):
    from backend.app.tripworld.retrieval.diagnostics import current_vector_capture_directory

    recorder = RawCapture(directory)
    token = current_raw_capture.set(recorder)
    vector_token = current_vector_capture_directory.set(directory / "evidence/vectors")
    try:
        yield recorder
    finally:
        try:
            recorder.finish()
        finally:
            current_vector_capture_directory.reset(vector_token)
            current_raw_capture.reset(token)


def observe_request(request, event_id):
    recorder = current_raw_capture.get()
    if recorder:
        try:
            recorder.request(request, event_id)
        except Exception as exc:
            recorder.diagnostics.append(
                {"reason": "request_capture_failed", "error_type": type(exc).__name__}
            )


def observe_response(response, event_id):
    recorder = current_raw_capture.get()
    if recorder:
        try:
            recorder.response(response, event_id)
        except Exception as exc:
            recorder.diagnostics.append(
                {"reason": "response_capture_failed", "error_type": type(exc).__name__}
            )
