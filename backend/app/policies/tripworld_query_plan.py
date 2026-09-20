"""Use interpreted discovery opportunities without parsing user language."""

import unicodedata

from backend.app.schemas.tripworld_discovery import RetrievalQuery
from backend.app.tripworld.retrieval.query_tokens import tokenizer

STRENGTH = {"hard": 0, "high": 1, "medium": 2, "low": 3}


def query_plan(contract, config=None):
    from backend.app.versions.v2.config import RAGConfig

    config = config or RAGConfig()
    requirements = {r.requirement_id: r for r in contract.semantic_requirements}
    grouped, omitted = {}, []
    for intent in sorted(
        contract.discovery_intents,
        key=lambda i: (
            min(STRENGTH[requirements[r].strength] for r in i.requirement_refs),
            i.intent_id,
        ),
    ):
        refs = tuple(r for r in intent.requirement_refs if requirements[r].polarity == "favor")
        if not refs:
            omitted.append({"intent_id": intent.intent_id, "reason": "no_positive_link"})
            continue
        text = " ".join(unicodedata.normalize("NFKC", intent.query_text).split())
        if not text or len(text) > 200 or len(tokenizer().encode_ordinary(text)) > 512:
            omitted.append({"intent_id": intent.intent_id, "reason": "invalid_query_bounds"})
            continue
        key = text.casefold()
        if key not in grouped and len(grouped) == config.max_queries:
            omitted.append({"intent_id": intent.intent_id, "reason": "query_limit"})
            continue
        entry = grouped.setdefault(key, {"text": text, "intents": set(), "refs": set()})
        entry["intents"].add(intent.intent_id)
        entry["refs"].update(refs)
    queries = tuple(
        RetrievalQuery(
            query_id=f"rag_{n}",
            text=g["text"],
            origin="user",
            intent_ids=tuple(sorted(g["intents"])),
            requirement_refs=tuple(sorted(g["refs"])),
        )
        for n, g in enumerate(grouped.values(), 1)
    )
    if not queries:
        queries = (
            RetrievalQuery(
                query_id="rag_default_1", text="top attractions", origin="system_default"
            ),
        )
    counts = [len(tokenizer().encode_ordinary(q.text)) for q in queries]
    if any(n > 512 for n in counts) or sum(counts) > config.total_query_tokens:
        raise ValueError("Total query token bound exceeded")
    return queries, omitted
