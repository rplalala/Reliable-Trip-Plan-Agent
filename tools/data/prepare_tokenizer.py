"""Explicitly download a checksum-pinned public vocabulary; no paid/model calls."""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.app.runtime.token_counting import VOCAB_CACHE, VOCAB_SHA256, VOCAB_URL  # noqa: E402


def main():
    import httpx

    target = VOCAB_CACHE / hashlib.sha1(VOCAB_URL.encode()).hexdigest()
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == VOCAB_SHA256:
        print("Tokenizer vocabulary already verified.")
        return
    response = httpx.get(VOCAB_URL, timeout=30)
    response.raise_for_status()
    if hashlib.sha256(response.content).hexdigest() != VOCAB_SHA256:
        raise ValueError("Tokenizer checksum mismatch")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.content)
    print("Tokenizer vocabulary prepared; no model/provider calls were made.")


if __name__ == "__main__":
    main()
