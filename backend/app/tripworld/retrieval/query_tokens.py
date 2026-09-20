"""Embedding tokenizer from verified local vocabulary; never download at runtime."""

import base64
import hashlib
from functools import lru_cache
from pathlib import Path

import tiktoken

ROOT = Path(__file__).resolve().parents[4] / "data/tripworld"
URL = "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"
SHA256 = "223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7"


@lru_cache(maxsize=1)
def tokenizer():
    content = (ROOT / "tokenizer_cache" / hashlib.sha1(URL.encode()).hexdigest()).read_bytes()
    if hashlib.sha256(content).hexdigest() != SHA256:
        raise ValueError("Embedding tokenizer checksum mismatch")
    ranks = {
        base64.b64decode(token): int(rank)
        for token, rank in (line.split() for line in content.splitlines() if line)
    }
    return tiktoken.Encoding(
        name="cl100k_base_local",
        pat_str=r"'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}++|\p{N}{1,3}+| ?[^\s\p{L}\p{N}]++[\r\n]*+|\s++$|\s*[\r\n]|\s+(?!\S)|\s",  # noqa: E501
        mergeable_ranks=ranks,
        special_tokens={},
    )
