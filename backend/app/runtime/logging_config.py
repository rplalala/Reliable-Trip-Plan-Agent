"""Small standard-library console logging setup from validated YAML policy."""

import logging

from backend.app.observability.run_trace import redact_secrets
from backend.app.runtime.config_models import LoggingConfig

_OWNED_HANDLER_NAME = "reliable-trip-plan-console"


class _RedactingLogFilter(logging.Filter):
    """Prevent credentials in provider URLs or messages reaching console logs."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact_secrets(record.getMessage())
        record.args = ()
        return True


def configure_logging(config: LoggingConfig) -> None:
    """Apply project logging without replacing handlers owned by the host."""

    root = logging.getLogger()
    root.setLevel(config.level)
    owned = next((h for h in root.handlers if h.get_name() == _OWNED_HANDLER_NAME), None)
    if config.console and owned is None:
        handler = logging.StreamHandler()
        handler.set_name(_OWNED_HANDLER_NAME)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        handler.addFilter(_RedactingLogFilter())
        root.addHandler(handler)
    elif config.console and owned is not None and not any(
        isinstance(item, _RedactingLogFilter) for item in owned.filters
    ):
        owned.addFilter(_RedactingLogFilter())
    elif not config.console and owned is not None:
        root.removeHandler(owned)
        owned.close()
