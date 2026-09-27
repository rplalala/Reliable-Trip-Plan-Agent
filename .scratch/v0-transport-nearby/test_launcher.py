"""Offline one-shot and frozen-input gates for the authorized V0 smoke."""

import importlib.util
import subprocess
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

spec = importlib.util.spec_from_file_location("v0_smoke", Path(__file__).with_name("run_once.py"))
packet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packet)


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    monkeypatch.setattr(packet, "OUTPUT", tmp_path / "evidence")
    monkeypatch.setattr(packet, "head", lambda: "offline-frozen-revision")
    settings = SimpleNamespace(
        azure_openai_api_key=SimpleNamespace(get_secret_value=lambda: "offline-secret-value")
    )
    monkeypatch.setattr(packet, "local_preflight", lambda: (date(2026, 9, 28), settings))
    packet.prepare()
    return packet.OUTPUT


def test_input_is_identical_to_original_berlin():
    assert packet.REQUEST.read_bytes() == packet.ORIGINAL.read_bytes()


def test_one_shot_execution_and_unchanged_independent_cli(prepared, monkeypatch):
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        assert kwargs["timeout"] == 660
        assert command[1].endswith("run_v0.py")
        assert "--runtime-config" not in command
        return SimpleNamespace(stdout=b"{}", stderr=b"", returncode=0)

    monkeypatch.setattr(packet.subprocess, "run", run)
    packet.execute()
    with pytest.raises(FileExistsError):
        packet.execute()
    assert len(calls) == 1


def test_source_drift_blocks_before_attempt(prepared, monkeypatch):
    monkeypatch.setattr(packet, "hashes", lambda: {"different": "hash"})
    with pytest.raises(ValueError, match="changed"):
        packet.execute()
    assert not (prepared / "started.json").exists()


def test_timeout_is_recorded_without_retry(prepared, monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 660)

    monkeypatch.setattr(packet.subprocess, "run", timeout)
    packet.execute()
    assert packet.read(prepared / "execution.json")["outer_timeout"]
    with pytest.raises(FileExistsError):
        packet.execute()
