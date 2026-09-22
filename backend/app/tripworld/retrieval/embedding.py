"""Shared vector shape, dtype, finiteness and normalization validation."""








import numpy as np


def validate_vectors(vectors: np.ndarray, rows: int, dimension: int) -> None:
    if vectors.shape != (rows, dimension) or vectors.dtype != np.float32:
        raise ValueError("Embedding shape/dtype mismatch")
    if not np.isfinite(vectors).all():
        raise ValueError("Embedding contains nonfinite values")
    if not np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-5):
        raise ValueError("Embedding vectors must be L2-normalized")
