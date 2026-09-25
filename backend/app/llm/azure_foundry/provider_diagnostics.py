"""Bounded internal provider facts; never a preference classifier or public API payload."""

import json
import re

from backend.app.observability.run_trace import redact_secrets

# Privacy bounds, not model or acquisition budgets.
TEXT_LIMIT = 1024
FIELD_LIMIT = 256
_HEADER = re.compile(
    r"(?im)(?:authorization|proxy-authorization|api[-_]key|x-api-key|cookie|set-cookie)"
    r"\s*[:=]\s*[^\r\n]+"
)
_REQUEST_CODES = frozenset(
    {
        "invalid_json_schema",
        "invalid_schema",
        "invalid_parameter",
        "unsupported_parameter",
        "missing_required_parameter",
        "invalid_request_error",
        "DeploymentNotFound",
    }
)


def normalize(*, metadata=None, content=None, usage=None, response_id=None, error=None, secrets=()):
    """Allowlist metadata and scalar error fields, with explicit missing/truncated state."""
    metadata = metadata or {}
    truncated = []

    def bounded(value, key, limit=FIELD_LIMIT):
        if not isinstance(value, str):
            return None
        for secret in secrets:
            if secret:
                for representation in (secret, json.dumps(secret)[1:-1]):
                    value = value.replace(representation, "[REDACTED]")
        value = _HEADER.sub("[REDACTED HEADER]", str(redact_secrets(value)))
        if len(value) > limit:
            truncated.append(key)
        return value[:limit]

    body = getattr(error, "body", None)
    body = body if isinstance(body, dict) else {}
    outer_usage = body.get("usage")
    # SDK errors may unwrap `error`, dropping top-level usage. Read only an already
    # buffered, small response; never perform I/O or retain the raw error document.
    response = getattr(error, "response", None)
    if outer_usage is None and response is not None:
        try:
            raw = response.content
            if len(raw) <= 16384:
                envelope = json.loads(raw)
                if isinstance(envelope, dict):
                    outer_usage = envelope.get("usage")
        except (AttributeError, ValueError, RuntimeError):
            pass
    body = body.get("error", body)
    body = body if isinstance(body, dict) else {}
    detail = metadata.get("incomplete_details")
    detail = detail if isinstance(detail, dict) else {}
    blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content
    refusal = (
        any(b.get("type") == "refusal" for b in blocks if isinstance(b, dict))
        if isinstance(blocks, list)
        else None
    )
    # Tokens only: neither arbitrary usage extensions nor reasoning content are retained.
    usage = usage if isinstance(usage, dict) else body.get("usage", outer_usage)
    allowed_usage = (
        {
            key: value
            for key, value in (usage or {}).items()
            if key in {"input_tokens", "output_tokens", "total_tokens"}
            and type(value) is int
            and value >= 0
        }
        if isinstance(usage, dict)
        else {}
    )
    result = {
        "version": "provider_diagnostics_1",
        "http_status": getattr(error, "status_code", None),
        "provider_error_code": bounded(body.get("code"), "provider_error_code"),
        "provider_error_type": bounded(body.get("type"), "provider_error_type"),
        "provider_error_message": bounded(
            body.get("message"), "provider_error_message", TEXT_LIMIT
        ),
        "provider_request_id": bounded(
            getattr(error, "request_id", None) or metadata.get("request_id"), "provider_request_id"
        ),
        "provider_response_id": bounded(response_id, "provider_response_id"),
        "response_status": bounded(metadata.get("status"), "response_status"),
        "incomplete_reason": bounded(detail.get("reason"), "incomplete_reason"),
        "structured_refusal": refusal,
        "text_present": any(b.get("text") for b in blocks if isinstance(b, dict))
        if isinstance(blocks, list)
        else None,
        "ordinary_text_refusal": "not_semantically_classified",
        "usage": allowed_usage or None,
        "usage_availability": "available" if allowed_usage else "unavailable",
        "capture_completeness": "allowlisted_partial",
        "truncated_fields": truncated,
    }
    result["unavailable_fields"] = [key for key, value in result.items() if value is None]
    return result


def failure_category(diagnostics):
    """Only machine-readable codes establish request-contract attribution."""
    status = diagnostics["http_status"]
    if status == 400:
        if diagnostics["provider_error_code"] in _REQUEST_CODES:
            return "configuration_failure"
        return "provider_request_rejected"
    if status in (401, 403):
        return "provider_request_rejected"
    return "transport_failure"
