"""Tests for the unit-test network isolation safeguard."""

import socket

import pytest


def test_external_network_connections_are_blocked() -> None:
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with pytest.raises(
            AssertionError,
            match="External network access is not allowed in unit tests",
        ):
            connection.connect(("192.0.2.1", 80))
    finally:
        connection.close()
