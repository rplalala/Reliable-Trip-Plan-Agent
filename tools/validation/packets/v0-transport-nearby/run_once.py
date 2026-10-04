"""One authorized V0 prompt smoke; local preparation makes no provider requests."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from dotenv import dotenv_values  # noqa: E402

from backend.app.policies.trip_dates import (  # noqa: E402
    create_trip_date_window,
    validate_requested_trip_dates,
)
from backend.app.schemas.request import PlanningRequest  # noqa: E402
from backend.app.versions.v0.config import V0Settings  # noqa: E402

PACKET = Path(__file__).resolve().parent
REQUEST = PACKET / "request.json"
ORIGINAL = ROOT / "tools/validation/packets/berlin-six-day-smoke/request.json"
OUTPUT = ROOT / "logs/v0_transport_nearby_20260928"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=True, indent=2)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def hashes():
    files = {Path(__file__), REQUEST, ORIGINAL, ROOT / "pyproject.toml", ROOT / "uv.lock"}
    for folder in ("backend/app", "scripts"):
        files.update((ROOT / folder).rglob("*.py"))
    files.update((ROOT / "config").glob("*.yaml"))
    if (ROOT / ".env").is_file():
        files.add(ROOT / ".env")
    return {str(p.relative_to(ROOT)): digest(p) for p in sorted(files)}


def environment_hash():
    values = {
        k: v
        for k, v in os.environ.items()
        if k.upper().startswith(
            ("AZURE_", "OPENAI_", "APP_", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")
        )
    }
    return hashlib.sha256(json.dumps(values, sort_keys=True).encode()).hexdigest()


def local_preflight():
    settings = V0Settings()
    if REQUEST.read_bytes() != ORIGINAL.read_bytes():
        raise ValueError("Input differs from the original Berlin request")
    trip = PlanningRequest.model_validate(read(REQUEST))
    today = datetime.now(ZoneInfo("Australia/Sydney")).date()
    validate_requested_trip_dates(trip.start_date, trip.end_date, create_trip_date_window(today))
    if trip.start_date <= today:
        raise ValueError("Future dates required; never backdate")
    return today, settings


def prepare():
    today, _ = local_preflight()
    OUTPUT.mkdir(parents=True, exist_ok=False)
    write(
        OUTPUT / "manifest.json",
        {
            "prepared_date": today.isoformat(),
            "git_head": head(),
            "hashes": hashes(),
            "environment_sha256": environment_hash(),
            "version": "v0",
            "authorized_attempts": 1,
            "outer_seconds": 660,
            "request_sha256": digest(REQUEST),
        },
    )
    print("Prepared offline; no provider constructed or called.")


def preflight():
    today, settings = local_preflight()
    manifest = read(OUTPUT / "manifest.json")
    if (
        manifest["git_head"] != head()
        or manifest["hashes"] != hashes()
        or manifest["environment_sha256"] != environment_hash()
    ):
        raise ValueError("Frozen revision, source, input, config or environment changed")
    if (OUTPUT / "started.json").exists() or (OUTPUT / "execution.json").exists():
        raise FileExistsError("Single attempt already consumed; no reset or retry")
    return today, settings


def execute():
    today, settings = preflight()
    write(
        OUTPUT / "started.json",
        {
            "started_at": datetime.now(ZoneInfo("Australia/Sydney")).isoformat(),
            "reference_date": today.isoformat(),
            "attempt": 1,
        },
    )
    command = [
        sys.executable,
        str(ROOT / "scripts/run_v0.py"),
        "--input-json",
        str(REQUEST),
        "--reference-date",
        today.isoformat(),
    ]
    status = {"application_exit_code": None, "outer_timeout": False}
    try:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=660, check=False)
        stdout, stderr = process.stdout, process.stderr
        status["application_exit_code"] = process.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = exc.stdout or b"", exc.stderr or b""
        status["outer_timeout"] = True
    except OSError as exc:
        stdout, stderr = b"", type(exc).__name__.encode()
        status["launch_error"] = type(exc).__name__
    (OUTPUT / "result.json").write_bytes(stdout)
    (OUTPUT / "stderr.log").write_bytes(stderr)
    secrets = [settings.azure_openai_api_key.get_secret_value()]
    values = {**dotenv_values(ROOT / ".env"), **os.environ}
    secrets.extend(
        v
        for k, v in values.items()
        if v
        and len(v) >= 8
        and any(word in k.upper() for word in ("KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL"))
    )
    status["secret_exposure"] = any(s.encode() in stdout + stderr for s in secrets)
    status["finished_at"] = datetime.now(ZoneInfo("Australia/Sydney")).isoformat()
    status["assessment"] = "pending_output_review"
    write(OUTPUT / "execution.json", status)
    print(json.dumps(status))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "check", "execute"))
    action = parser.parse_args().action
    if action == "prepare":
        prepare()
    elif action == "check":
        preflight()
        print("Frozen preflight passed; no live attempt started.")
    else:
        execute()
