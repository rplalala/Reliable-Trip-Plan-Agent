"""Pinned TripWorld source download and validation."""

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

import httpx
import pyarrow as pa
import pyarrow.parquet as pq

from backend.app.tripworld.manifest import TripWorldManifest, validate_source_schema


class SourceValidationError(ValueError):
    """A local TripWorld source does not match its pinned manifest."""


class SourceDownloadError(RuntimeError):
    """The pinned TripWorld source could not be downloaded or validated."""


@dataclass(frozen=True)
class SourceValidation:
    path: Path
    size_bytes: int
    sha256: str
    row_count: int


@dataclass(frozen=True)
class DownloadResult:
    validation: SourceValidation
    downloaded: bool


def sha256_file(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def validate_source_file(path: Path, manifest: TripWorldManifest) -> SourceValidation:
    if not path.is_file():
        raise SourceValidationError(f"TripWorld source file does not exist: {path}")
    actual_size = path.stat().st_size
    if actual_size != manifest.dataset.size_bytes:
        raise SourceValidationError(
            f"TripWorld source size mismatch: expected {manifest.dataset.size_bytes}, "
            f"got {actual_size}"
        )
    actual_hash = sha256_file(path)
    if actual_hash != manifest.dataset.sha256:
        raise SourceValidationError(
            f"TripWorld source checksum mismatch: expected {manifest.dataset.sha256}, "
            f"got {actual_hash}"
        )
    try:
        parquet = pq.ParquetFile(path)
    except (pa.ArrowException, OSError) as exc:
        raise SourceValidationError(f"TripWorld source is not valid Parquet: {exc}") from exc
    if parquet.metadata.num_rows != manifest.dataset.row_count:
        raise SourceValidationError(
            f"TripWorld source row-count mismatch: expected {manifest.dataset.row_count}, "
            f"got {parquet.metadata.num_rows}"
        )
    validate_source_schema(parquet.schema_arrow, manifest)
    return SourceValidation(path, actual_size, actual_hash, parquet.metadata.num_rows)


def download_source(
    manifest: TripWorldManifest,
    destination: Path,
    *,
    transport: httpx.BaseTransport | None = None,
) -> DownloadResult:
    """Download the single pinned source atomically, or reuse a valid local copy."""

    if destination.exists():
        try:
            return DownloadResult(validate_source_file(destination, manifest), downloaded=False)
        except SourceValidationError:
            pass

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.unlink(missing_ok=True)
    try:
        timeout = httpx.Timeout(connect=30.0, read=120.0, write=30.0, pool=30.0)
        with httpx.Client(
            follow_redirects=True,
            timeout=timeout,
            transport=transport,
        ) as client:
            with client.stream("GET", manifest.dataset.download_url) as response:
                response.raise_for_status()
                with temporary.open("wb") as handle:
                    for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                        handle.write(chunk)
        validation = validate_source_file(temporary, manifest)
        os.replace(temporary, destination)
        return DownloadResult(
            SourceValidation(
                destination,
                validation.size_bytes,
                validation.sha256,
                validation.row_count,
            ),
            downloaded=True,
        )
    except (httpx.HTTPError, OSError, SourceValidationError) as exc:
        temporary.unlink(missing_ok=True)
        raise SourceDownloadError(
            f"Pinned TripWorld source download failed: {type(exc).__name__}: {exc}"
        ) from exc
