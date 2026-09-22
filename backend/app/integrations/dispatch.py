"""Request-local send boundary; no global client mutation or resource ownership."""

from contextvars import ContextVar

send_observer = ContextVar("provider_send_observer", default=None)


def mark_provider_send():
    """Charge and mark immediately before the transport starts its one send."""
    callback = send_observer.get()
    if callback is not None:
        callback()


class ProviderNotSentError(RuntimeError):
    """Pre-send dependency failure, not a place fact or a terminal attempt."""
