"""Semantic query embedding and database retrieval remain separate service boundaries."""

from pathlib import Path

from backend.app.tripworld.database.search import PostgresSearch
from backend.app.tripworld.database.vectors import SPACE, validate_space
from tools.data.tripworld.embedding_build import encode_resumable
from tools.data.tripworld.embedding_config import production_config
from tools.data.tripworld.estimation import tokenizer
from tools.data.tripworld.openai_adapter import OpenAIEmbeddingAdapter
from tools.data.tripworld.search import DiscoveryIntent


class RetrievalService:
    def __init__(self, conn, root: Path, *, provider_factory=OpenAIEmbeddingAdapter):
        self.search = PostgresSearch(conn)
        self.root = root
        self.provider_factory = provider_factory

    def retrieve(self, text, scope, top_k=10, *, lexical=False):
        text = DiscoveryIntent(semantic_query=text).query_text()
        if not isinstance(top_k, int) or not 1 <= top_k <= 1000:
            raise ValueError("Top-K must be between 1 and 1000")
        if lexical:
            return {
                "query": text,
                "mode": "normalized_exact_name_or_alias",
                "results": self.search.lexical(text, scope, top_k),
            }
        validate_space(self.search.conn)
        provider = self.provider_factory(production_config())
        try:
            vectors, usage = encode_resumable(
                [text],
                provider,
                self.root / "artifacts/phase5/query_checkpoints",
                query=True,
                token_counts=[len(tokenizer().encode_ordinary(text))],
            )
        finally:
            provider.close()
        return {
            "query": text,
            "scope": scope.model_dump(),
            "embedding_space": SPACE,
            "query_usage": usage,
            "results": self.search.search(vectors[0], scope, top_k),
        }
