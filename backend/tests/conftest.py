"""Test safeguards shared by the backend test suite."""

import socket
from collections.abc import Generator
from ipaddress import ip_address

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(autouse=True)
def offline_semantic_tokenizer(monkeypatch):
    """Unit tests mock tokenization; real offline sizing uses the dedicated script.

    This keeps a clean checkout independent of downloaded tokenizer assets. The fake
    tests structural/call-limit behavior only and is not a payload measurement.
    """
    from backend.app.runtime import token_counting

    class FakeEncoding:
        def encode_ordinary(self, text):
            return range((len(text.encode("utf-8")) + 3) // 4)

    monkeypatch.setattr(token_counting, "tokenizer", lambda: FakeEncoding())


@pytest.fixture(autouse=True)
def block_network_access(monkeypatch: MonkeyPatch) -> Generator[None]:
    """Fail every unit test that attempts to open a network connection."""

    original_create_connection = socket.create_connection
    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex

    def is_loopback(address: object) -> bool:
        if not isinstance(address, tuple) or not address:
            return True
        try:
            return ip_address(address[0]).is_loopback
        except ValueError:
            return False

    def guarded_create_connection(address, *args, **kwargs):
        if not is_loopback(address):
            raise AssertionError("External network access is not allowed in unit tests")
        return original_create_connection(address, *args, **kwargs)

    def guarded_connect(instance, address):
        if not is_loopback(address):
            raise AssertionError("External network access is not allowed in unit tests")
        return original_connect(instance, address)

    def guarded_connect_ex(instance, address):
        if not is_loopback(address):
            raise AssertionError("External network access is not allowed in unit tests")
        return original_connect_ex(instance, address)

    monkeypatch.setattr(socket, "create_connection", guarded_create_connection)
    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    monkeypatch.setattr(socket.socket, "connect_ex", guarded_connect_ex)
    yield
