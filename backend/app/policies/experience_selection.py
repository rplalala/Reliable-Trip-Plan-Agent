"""Controlled V1-A experience preferences and deterministic selection adjustments."""

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from itertools import product

from backend.app.evidence.experience_models import (
    ExperienceConfidence,
    ExperienceDimension,
    ExperienceProfile,
    ExperienceValue,
)
from backend.app.evidence.models import EvidenceAvailability
from backend.app.evidence.selection_models import SearchIntentKind
from backend.app.schemas.request import TravelRequirements
from backend.app.schemas.trip_intent import ExperiencePreference, ExperiencePreferenceIntent

PREFERENCE_DIMENSION: dict[ExperiencePreference, ExperienceDimension] = {
    ExperiencePreference.AVOID_CROWDS: ExperienceDimension.CROWDING,
    ExperiencePreference.PREFER_LESS_WALKING: ExperienceDimension.WALKING_INTENSITY,
    ExperiencePreference.PREFER_ACCESSIBLE: ExperienceDimension.ACCESSIBILITY,
    ExperiencePreference.PREFER_FAMILY_FRIENDLY: ExperienceDimension.FAMILY_FRIENDLINESS,
    ExperiencePreference.PREFER_SHORT_VISIT: ExperienceDimension.VISIT_DURATION,
    ExperiencePreference.PREFER_LONG_VISIT: ExperienceDimension.VISIT_DURATION,
}

_PATTERNS: dict[ExperiencePreference, tuple[str, ...]] = {
    ExperiencePreference.AVOID_CROWDS: (
        r"\bavoid (?:the )?crowds?\b",
        r"\bavoid crowded (?:places?|attractions?|areas?)\b",
        r"\b(?:less|not too|not very) crowded\b",
    ),
    ExperiencePreference.PREFER_LESS_WALKING: (
        r"\b(?:less|minimal|limited) walking\b",
        r"\bnot too much walking\b",
        r"\bavoid (?:long|much) walk(?:s|ing)?\b",
    ),
    ExperiencePreference.PREFER_ACCESSIBLE: (
        r"\b(?:prefer|need|require|want) (?:wheelchair )?accessible\b",
        r"\baccessible (?:places?|experiences?|attractions?)\b",
        r"\bwheelchair accessibility\b",
        r"\baccessibility (?:is )?(?:important|required)\b",
    ),
    ExperiencePreference.PREFER_FAMILY_FRIENDLY: (
        r"\b(?:family|kid|child)[ -]friendly\b",
        r"\b(?:suitable|good) for (?:families|children|kids)\b",
    ),
    ExperiencePreference.PREFER_SHORT_VISIT: (
        r"\b(?:prefer|want|need) (?:a )?(?:short|brief|quick) visits?\b",
        r"\bshort visits?\b",
        r"\bquick stops?\b",
    ),
    ExperiencePreference.PREFER_LONG_VISIT: (
        r"\b(?:prefer|want|need) (?:a )?(?:long|extended) visits?\b",
        r"\blong visits?\b",
        r"\b(?:half|full)[ -]day visits?\b",
    ),
}

_NEGATED_CONCEPTS = (
    r"\b(?:not|no|avoid)\s+(?:family|kid|child)[ -]friendly\b",
    r"\bnot\s+(?:suitable|good) for (?:families|children|kids)\b",
    r"\b(?:not|no|avoid)\s+(?:wheelchair )?accessible\b",
    r"\b(?:not|no|avoid)\s+(?:short|brief|quick|long|extended) visits?\b",
    r"\b(?:do not|don't)\s+(?:want|need|prefer)?\s*avoid crowds?\b",
)


@dataclass(frozen=True)
class ExplicitExperienceNeed:
    preference: ExperiencePreference
    dimension: ExperienceDimension
    source_kind: SearchIntentKind
    source_text: str

    @property
    def importance(self) -> Decimal:
        return self.source_kind.weight


@dataclass(frozen=True)
class ExperienceNeedExtraction:
    needs: tuple[ExplicitExperienceNeed, ...]
    ambiguities: tuple[str, ...]


@dataclass(frozen=True)
class ExperienceContribution:
    preference: ExperiencePreference
    dimension: ExperienceDimension
    value: ExperienceValue | None
    confidence: ExperienceConfidence | None
    amount: Decimal
    review_refs: tuple[str, ...]


@dataclass(frozen=True)
class ExperienceScoreResult:
    total: Decimal
    contributions: tuple[ExperienceContribution, ...]


_MATCH_CONFLICT: dict[ExperiencePreference, tuple[ExperienceValue, ExperienceValue]] = {
    ExperiencePreference.AVOID_CROWDS: (ExperienceValue.LOW, ExperienceValue.HIGH),
    ExperiencePreference.PREFER_LESS_WALKING: (ExperienceValue.LIGHT, ExperienceValue.HIGH),
    ExperiencePreference.PREFER_ACCESSIBLE: (
        ExperienceValue.ACCESSIBLE,
        ExperienceValue.LIMITED,
    ),
    ExperiencePreference.PREFER_FAMILY_FRIENDLY: (
        ExperienceValue.FAMILY_FRIENDLY,
        ExperienceValue.NOT_FAMILY_FRIENDLY,
    ),
    ExperiencePreference.PREFER_SHORT_VISIT: (ExperienceValue.SHORT, ExperienceValue.LONG),
    ExperiencePreference.PREFER_LONG_VISIT: (ExperienceValue.LONG, ExperienceValue.SHORT),
}


def extract_experience_needs(requirements: TravelRequirements) -> ExperienceNeedExtraction:
    """Map only explicit controlled wording in existing extracted requirement fields."""

    found: dict[ExperiencePreference, ExplicitExperienceNeed] = {}
    for texts, kind in (
        (requirements.required_activities, SearchIntentKind.EXPLICIT_REQUIREMENT),
        (requirements.preferences, SearchIntentKind.NORMAL_PREFERENCE),
    ):
        for text in texts:
            normalized = " ".join(text.casefold().split())
            if any(re.search(pattern, normalized) for pattern in _NEGATED_CONCEPTS):
                continue
            for preference, patterns in _PATTERNS.items():
                if preference in found or not any(
                    re.search(pattern, normalized) for pattern in patterns
                ):
                    continue
                found[preference] = ExplicitExperienceNeed(
                    preference=preference,
                    dimension=PREFERENCE_DIMENSION[preference],
                    source_kind=kind,
                    source_text=text,
                )
    ambiguities: tuple[str, ...] = ()
    if {
        ExperiencePreference.PREFER_SHORT_VISIT,
        ExperiencePreference.PREFER_LONG_VISIT,
    } <= found.keys():
        found.pop(ExperiencePreference.PREFER_SHORT_VISIT)
        found.pop(ExperiencePreference.PREFER_LONG_VISIT)
        ambiguities = ("contradictory_visit_duration_preferences",)
    return ExperienceNeedExtraction(tuple(found.values()), ambiguities)


def experience_needs_from_intents(
    intents: Sequence[ExperiencePreferenceIntent],
) -> ExperienceNeedExtraction:
    """Map typed user preferences to the unchanged deterministic score inputs."""

    found: dict[ExperiencePreference, ExplicitExperienceNeed] = {}
    for intent in sorted(intents, key=lambda item: -item.importance.weight):
        found.setdefault(
            intent.preference,
            ExplicitExperienceNeed(
                preference=intent.preference,
                dimension=PREFERENCE_DIMENSION[intent.preference],
                source_kind=intent.importance,
                source_text=intent.source_text,
            ),
        )
    ambiguities: tuple[str, ...] = ()
    if {
        ExperiencePreference.PREFER_SHORT_VISIT,
        ExperiencePreference.PREFER_LONG_VISIT,
    } <= found.keys():
        found.pop(ExperiencePreference.PREFER_SHORT_VISIT)
        found.pop(ExperiencePreference.PREFER_LONG_VISIT)
        ambiguities = ("contradictory_visit_duration_preferences",)
    return ExperienceNeedExtraction(tuple(found.values()), ambiguities)


def _clamp(value: Decimal) -> Decimal:
    return max(Decimal(-15), min(Decimal(10), value))


def score_experience(
    profile: ExperienceProfile | None, needs: Sequence[ExplicitExperienceNeed]
) -> ExperienceScoreResult:
    """Only cited, supported Profile signals can change E_exp."""

    by_dimension = (
        {item.dimension: item for item in profile.signals}
        if profile is not None and profile.availability is not EvidenceAvailability.UNAVAILABLE
        else {}
    )
    contributions: list[ExperienceContribution] = []
    for need in needs:
        signal = by_dimension.get(need.dimension)
        amount = Decimal(0)
        if signal is not None and signal.review_refs:
            match_value, conflict_value = _MATCH_CONFLICT[need.preference]
            if signal.value == match_value:
                amount = Decimal(5)
            elif signal.value == conflict_value:
                amount = Decimal(-10)
            if signal.confidence is ExperienceConfidence.LOW:
                amount /= 2
        contributions.append(
            ExperienceContribution(
                preference=need.preference,
                dimension=need.dimension,
                value=signal.value if signal is not None else None,
                confidence=signal.confidence if signal is not None else None,
                amount=amount,
                review_refs=signal.review_refs if signal is not None else (),
            )
        )
    return ExperienceScoreResult(
        total=_clamp(sum((item.amount for item in contributions), Decimal(0))),
        contributions=tuple(contributions),
    )


def reachable_experience_values(
    needs: Sequence[ExplicitExperienceNeed],
) -> tuple[Decimal, ...]:
    """Enumerate finite taxonomy/confidence outcomes; no synthetic Profile is made."""

    dimensions = {need.dimension for need in needs}
    if not dimensions:
        return (Decimal(0),)
    if len(dimensions) != len(needs):
        raise ValueError("Only one explicit preference per experience dimension is supported")
    options = (Decimal(-10), Decimal(-5), Decimal(0), Decimal("2.5"), Decimal(5))
    return tuple(
        sorted({_clamp(sum(items, Decimal(0))) for items in product(options, repeat=len(needs))})
    )


def experience_score_map(
    profiles: Mapping[str, ExperienceProfile], needs: Sequence[ExplicitExperienceNeed]
) -> dict[str, Decimal]:
    if any(place_id != profile.place_id for place_id, profile in profiles.items()):
        raise ValueError("Profile Place IDs must match score-map keys")
    return {
        place_id: score_experience(profile, needs).total for place_id, profile in profiles.items()
    }
