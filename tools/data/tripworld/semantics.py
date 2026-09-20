"""Deterministic category semantics and retrieval-document formatting."""

import json
import re
import unicodedata
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SemanticRule(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rule_id: str = Field(pattern=r"^[a-z0-9_]+$")
    match_terms: tuple[str, ...] = Field(min_length=1)
    direct_semantics: tuple[str, ...] = ()
    inferred_semantics: tuple[str, ...] = ()
    eligibility_hint: Literal["eligible", "ineligible", "unknown"] = "unknown"


class CategorySemanticMapping(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    mapping_version: str = Field(min_length=1)
    description_version: str = Field(min_length=1)
    rules: tuple[SemanticRule, ...]

    @model_validator(mode="after")
    def unique_rules_and_terms(self) -> "CategorySemanticMapping":
        rule_ids = [rule.rule_id for rule in self.rules]
        if len(rule_ids) != len(set(rule_ids)):
            raise ValueError("Category semantic rule IDs must be unique")
        terms: list[str] = []
        for rule in self.rules:
            terms.extend(_match_key(term) for term in rule.match_terms)
        if len(terms) != len(set(terms)):
            raise ValueError("Category semantic match terms must be unique")
        return self


class SemanticEnrichment(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    normalized_fsq_categories: tuple[str, ...]
    normalized_google_categories: tuple[str, ...]
    semantic_rule_ids: tuple[str, ...]
    direct_semantics: tuple[str, ...]
    inferred_semantics: tuple[str, ...]
    semantic_eligibility_hints: tuple[str, ...]
    retrieval_description: str
    retrieval_text: str


_WHITESPACE = re.compile(r"\s+")
_MATCH_SEPARATORS = re.compile(r"[_\-/]+")
_MATCH_PUNCTUATION = re.compile(r"[^\w\s]+", re.UNICODE)


def clean_text(value: object) -> str | None:
    if value is None:
        return None
    cleaned = _WHITESPACE.sub(" ", unicodedata.normalize("NFKC", str(value))).strip()
    return cleaned or None


def _deduplicate(values: list[str]) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.casefold()
        if value and key not in seen:
            seen.add(key)
            result.append(value)
    return tuple(result)


def normalize_fsq_categories(values: object) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        return ()
    normalized: list[str] = []
    for value in values:
        text = clean_text(value)
        if not text:
            continue
        segments = [clean_text(segment) for segment in text.split(">")]
        normalized.append(" > ".join(segment for segment in segments if segment))
    return _deduplicate(normalized)


def normalize_google_categories(values: object) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        return ()
    normalized: list[str] = []
    for value in values:
        text = clean_text(value)
        if not text:
            continue
        expanded = [text]
        if text.startswith("[") and text.endswith("]"):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
                    expanded = parsed
            except json.JSONDecodeError:
                pass
        for item in expanded:
            cleaned = clean_text(item)
            if cleaned:
                normalized.append(
                    _WHITESPACE.sub(" ", cleaned.replace("_", " ")).strip()
                )
    return _deduplicate(normalized)


def _match_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = _MATCH_SEPARATORS.sub(" ", normalized)
    normalized = _MATCH_PUNCTUATION.sub("", normalized)
    return _WHITESPACE.sub(" ", normalized).strip()


def _category_match_keys(
    fsq_categories: tuple[str, ...],
    google_categories: tuple[str, ...],
) -> set[str]:
    keys: set[str] = set()
    for category in fsq_categories:
        keys.add(_match_key(category))
        keys.update(_match_key(segment) for segment in category.split(" > "))
    keys.update(_match_key(category) for category in google_categories)
    return keys


def load_semantic_mapping(path: Path) -> CategorySemanticMapping:
    return CategorySemanticMapping.model_validate_json(path.read_text(encoding="utf-8"))


def build_retrieval_description(
    direct_semantics: tuple[str, ...],
    inferred_semantics: tuple[str, ...],
) -> str:
    parts: list[str] = []
    if direct_semantics:
        parts.append("Category associations: " + "; ".join(direct_semantics) + ".")
    if inferred_semantics:
        parts.append(
            "Potential travel uses inferred from category types: "
            + "; ".join(inferred_semantics)
            + "."
        )
    return " ".join(parts)


def build_retrieval_text(
    row: dict[str, object],
    *,
    fsq_categories: tuple[str, ...],
    google_categories: tuple[str, ...],
    retrieval_description: str,
) -> str:
    fsq_name = clean_text(row.get("fsq_name"))
    google_name = clean_text(row.get("google_name"))
    primary_name = fsq_name or google_name
    alternative_name = (
        google_name
        if google_name and primary_name and google_name.casefold() != primary_name.casefold()
        else None
    )
    lines: list[str] = []
    if primary_name:
        lines.append(f"Name: {primary_name}")
    if alternative_name:
        lines.append(f"Alternative name: {alternative_name}")
    location = _deduplicate(
        [
            value
            for key in ("fsq_locality", "fsq_region", "fsq_country")
            if (value := clean_text(row.get(key)))
        ]
    )
    if location:
        lines.extend(("", "Location:", ", ".join(location)))
    category_lines: list[str] = []
    if fsq_categories:
        category_lines.append("FSQ: " + "; ".join(fsq_categories))
    if google_categories:
        category_lines.append("Google: " + "; ".join(google_categories))
    if category_lines:
        lines.extend(("", "Categories:", *category_lines))
    if retrieval_description:
        lines.extend(("", "Description:", retrieval_description))
    return "\n".join(lines)


def enrich_row(
    row: dict[str, object],
    mapping: CategorySemanticMapping,
) -> SemanticEnrichment:
    fsq_categories = normalize_fsq_categories(row.get("fsq_category_labels"))
    google_categories = normalize_google_categories(row.get("google_categories"))
    category_keys = _category_match_keys(fsq_categories, google_categories)
    matched_rules = [
        rule
        for rule in mapping.rules
        if any(_match_key(term) in category_keys for term in rule.match_terms)
    ]
    direct = _deduplicate(
        [value for rule in matched_rules for value in rule.direct_semantics]
    )
    inferred = _deduplicate(
        [value for rule in matched_rules for value in rule.inferred_semantics]
    )
    description = build_retrieval_description(direct, inferred)
    return SemanticEnrichment(
        normalized_fsq_categories=fsq_categories,
        normalized_google_categories=google_categories,
        semantic_rule_ids=tuple(rule.rule_id for rule in matched_rules),
        direct_semantics=direct,
        inferred_semantics=inferred,
        semantic_eligibility_hints=_deduplicate(
            [rule.eligibility_hint for rule in matched_rules]
        ),
        retrieval_description=description,
        retrieval_text=build_retrieval_text(
            row,
            fsq_categories=fsq_categories,
            google_categories=google_categories,
            retrieval_description=description,
        ),
    )


def semantic_mapping_payload(mapping: CategorySemanticMapping) -> dict[str, object]:
    return json.loads(mapping.model_dump_json())
