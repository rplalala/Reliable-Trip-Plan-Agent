"""Small standard-library console logging setup from validated YAML policy."""

import logging

from backend.app.runtime.config_models import LoggingConfig

_OWNED_HANDLER_NAME = "reliable-trip-plan-console"


def configure_logging(config: LoggingConfig) -> None:
    """Apply project logging without replacing handlers owned by the host."""

    root = logging.getLogger()
    root.setLevel(config.level)
    owned = next((h for h in root.handlers if h.get_name() == _OWNED_HANDLER_NAME), None)
    if config.console and owned is None:
        handler = logging.StreamHandler()
        handler.set_name(_OWNED_HANDLER_NAME)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        root.addHandler(handler)
    elif not config.console and owned is not None:
        root.removeHandler(owned)
        owned.close()
