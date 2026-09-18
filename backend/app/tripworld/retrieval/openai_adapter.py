"""Explicit OpenAI Embeddings API adapter; no Azure, Luna, or local-model fallback."""

import base64
import os
import random
import time
from collections.abc import Callable, Sequence

import numpy as np
from openai import APIConnectionError, APIStatusError, OpenAI

from backend.app.tripworld.retrieval.embedding import (
    EmbeddingConfig,
    EncodedBatch,
    validate_vectors,
)


class OpenAIEmbeddingError(RuntimeError):
    """Sanitized API failure with no secrets or source text in the message."""


class OpenAIEmbeddingAdapter:
    def __init__(
        self,
        config: EmbeddingConfig,
        *,
        client: OpenAI | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        self.config = config
        self.sleep = sleep
        if client is None:
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise OpenAIEmbeddingError(
                    "Set OPENAI_API_KEY in the process environment before live embedding access"
                )
            # Endpoint is deliberate; ignore unrelated Azure or OPENAI_BASE_URL settings.
            client = OpenAI(
                api_key=key,
                base_url="https://api.openai.com/v1",
                timeout=config.timeout_seconds,
                max_retries=0,
            )
        self.client = client

    def close(self) -> None:
        self.client.close()

    def encode(self, texts: Sequence[str], *, query: bool = False) -> EncodedBatch:
        from backend.app.tripworld.retrieval.estimation import tokenizer

        config = self.config
        if not texts or len(texts) > config.max_batch_inputs or any(not t.strip() for t in texts):
            raise ValueError("Invalid embedding input count or empty text")
        encoding = tokenizer()
        counts = [len(encoding.encode_ordinary(text)) for text in texts]
        if max(counts) > config.max_input_tokens or sum(counts) > config.max_batch_tokens:
            raise ValueError("Embedding API token budget exceeded")
        for attempt in range(1, config.max_attempts + 1):
            try:
                response = self.client.embeddings.create(
                    model=config.model_name,
                    input=list(texts),
                    encoding_format="base64",
                    # Default dimensions; no custom shortening and no query/passage prefix.
                )
                break
            except (APIConnectionError, APIStatusError) as exc:
                status = getattr(exc, "status_code", None)
                body = getattr(exc, "body", None)
                code = body.get("code") if isinstance(body, dict) else None
                retryable = status in (None, 408, 409, 429) or (
                    status is not None and status >= 500
                )
                if code == "insufficient_quota":
                    retryable = False
                if not retryable or attempt == config.max_attempts:
                    raise OpenAIEmbeddingError(
                        f"OpenAI embeddings failed: status={status}, attempts={attempt}; "
                        "check API key, project model access, billing, or network"
                    ) from None
                delay = min(30.0, 2 ** (attempt - 1) + random.random())
                if isinstance(exc, APIStatusError):
                    try:
                        delay = min(
                            30.0, max(delay, float(exc.response.headers.get("retry-after", 0)))
                        )
                    except ValueError:
                        pass
                self.sleep(delay)
        items = sorted(response.data, key=lambda item: item.index)
        if [item.index for item in items] != list(range(len(texts))):
            raise ValueError("Embedding response indices mismatch")
        if response.model != config.model_name:
            raise ValueError("Embedding response model mismatch")
        # Base64 avoids multi-megabyte decimal JSON responses for production batches.
        # It transports the same float32 vectors; the model/vector-space contract is unchanged.
        values = [
            np.frombuffer(base64.b64decode(item.embedding, validate=True), dtype="<f4")
            if isinstance(item.embedding, str)
            else item.embedding
            for item in items
        ]
        vectors = np.asarray(values, dtype=np.float32)
        if vectors.shape != (len(texts), config.dimension) or not np.isfinite(vectors).all():
            raise ValueError("Embedding response shape/value mismatch")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        if (norms <= 0).any():
            raise ValueError("Embedding response contains zero vector")
        vectors /= norms
        validate_vectors(vectors, len(texts), config.dimension)
        return EncodedBatch(
            vectors,
            response.usage.prompt_tokens,
            response.usage.total_tokens,
            response.model,
            getattr(response, "_request_id", None),
            attempt,
        )
