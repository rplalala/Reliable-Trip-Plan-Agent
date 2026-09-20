"""Offline o200k engineering counts; missing vocabulary never triggers networking."""

import base64
import hashlib
from functools import lru_cache
from pathlib import Path

import tiktoken

VOCAB_URL = "https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken"
VOCAB_SHA256 = "446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d"
VOCAB_CACHE = Path(__file__).resolve().parents[3] / ".cache" / "tokenizer"
# o200k_base pre-tokenization from the installed tiktoken distribution (MIT).
PATTERN = "|".join(
    [
        r"[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]*[\p{Ll}\p{Lm}\p{Lo}\p{M}]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?",  # noqa: E501
        r"[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]+[\p{Ll}\p{Lm}\p{Lo}\p{M}]*(?i:'s|'t|'re|'ve|'m|'ll|'d)?",  # noqa: E501
        r"\p{N}{1,3}",
        r" ?[^\s\p{L}\p{N}]+[\r\n/]*",
        r"\s*[\r\n]+",
        r"\s+(?!\S)",
        r"\s+",
    ]
)


@lru_cache(maxsize=1)
def tokenizer() -> tiktoken.Encoding:
    cache_file = VOCAB_CACHE / hashlib.sha1(VOCAB_URL.encode()).hexdigest()
    if not cache_file.is_file():
        raise RuntimeError(
            "Tokenizer vocabulary missing; run tools/data/prepare_tokenizer.py"
        )
    content = cache_file.read_bytes()
    if hashlib.sha256(content).hexdigest() != VOCAB_SHA256:
        raise RuntimeError("Tokenizer vocabulary checksum mismatch")
    ranks = {
        base64.b64decode(token): int(rank)
        for token, rank in (line.split() for line in content.splitlines() if line)
    }
    return tiktoken.Encoding(
        name="o200k_base",
        pat_str=PATTERN,
        mergeable_ranks=ranks,
        special_tokens={"<|endoftext|>": 199999, "<|endofprompt|>": 200018},
    )


def count_tokens(text: str) -> int:
    return len(tokenizer().encode_ordinary(text))
