"""Opt-in local development capture, disabled for normal runtime."""




import json
import os
from pathlib import Path
from uuid import uuid4


class DevelopmentRequirementCapture:
    """Explicit caller opt-in; use a private directory under ignored logs.

    Files use owner-only permissions on POSIX and inherited directory ACLs on Windows.
    Text can contain personal data. This is neither normal telemetry nor a PII anonymizer.
    """

    def __init__(self, directory: Path, *, scenario_id: str, secrets=()):
        self.directory = Path(directory)
        self.scenario_id = scenario_id
        self.secrets = tuple(s for s in secrets if s)
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        (self.directory / ".gitignore").write_text("*\n", encoding="utf-8")

    def record(self, call_id, stage, payload, *, secrets=()):
        # Unique immutable artifacts per call/stage. Never overwrite an earlier response.
        def sanitize(value):
            if isinstance(value, str):
                for secret in (*self.secrets, *secrets):
                    if secret:
                        for representation in (secret, json.dumps(secret)[1:-1]):
                            value = value.replace(representation, "[REDACTED]")
                return value
            if isinstance(value, dict):
                return {k: sanitize(v) for k, v in value.items()}
            if isinstance(value, (list, tuple)):
                return [sanitize(v) for v in value]
            return value

        content = json.dumps(
            sanitize(
                {
                    "call_id": call_id,
                    "scenario_id": self.scenario_id,
                    "validation_stage": stage,
                    **payload,
                }
            ),
            ensure_ascii=True,
            indent=2,
        )
        path = self.directory / f"{uuid4().hex}.json"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
        except OSError:
            # Diagnostic storage must not change interpretation or cause another model call.
            return None
        return path
