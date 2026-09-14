"""V1-only projection of optional planner costs at the Foundry DTO boundary."""

import re
from decimal import Decimal, InvalidOperation, localcontext

from pydantic import ValidationError

from backend.app.llm.azure_foundry.dto import FoundryItineraryDTO, FoundryMoneyDTO
from backend.app.llm.azure_foundry.mapping import map_foundry_itinerary
from backend.app.schemas.request import Money
from backend.app.schemas.v1_itinerary import (
    EstimatedCostProjectionDiagnostic,
    V1Itinerary,
)

_RANGE_PATTERN = re.compile(
    r"(?P<lower>[0-9]+(?:\.[0-9]+)?)[ \t]*-[ \t]*(?P<upper>[0-9]+(?:\.[0-9]+)?)\Z"
)
_CURRENCY_PATTERN = re.compile(r"[A-Z]{3}\Z")


def project_v1_estimated_cost(
    value: FoundryMoneyDTO | None, *, field_path: str
) -> tuple[FoundryMoneyDTO | None, EstimatedCostProjectionDiagnostic]:
    """Preserve a point, derive a clear range midpoint, or discard only this cost."""

    if value is None:
        return None, EstimatedCostProjectionDiagnostic(field_path, "explicit_null")

    currency_valid = _CURRENCY_PATTERN.fullmatch(value.currency) is not None
    if currency_valid:
        try:
            point = Money(amount=value.amount, currency=value.currency)
        except ValidationError:
            pass
        else:
            if point.amount.is_finite():
                return value, EstimatedCostProjectionDiagnostic(
                    field_path, "exact_point", currency=value.currency
                )

    range_match = _RANGE_PATTERN.fullmatch(value.amount)
    if range_match is not None and currency_valid:
        try:
            lower = Decimal(range_match.group("lower"))
            upper = Decimal(range_match.group("upper"))
        except InvalidOperation:
            pass
        else:
            if lower.is_finite() and upper.is_finite() and 0 <= lower <= upper:
                precision = max(len(lower.as_tuple().digits), len(upper.as_tuple().digits)) + 2
                with localcontext() as context:
                    context.prec = precision
                    midpoint = (lower + upper) / Decimal(2)
                try:
                    Money(amount=midpoint, currency=value.currency)
                except ValidationError:
                    pass
                else:
                    return FoundryMoneyDTO(
                        amount=str(midpoint), currency=value.currency
                    ), EstimatedCostProjectionDiagnostic(
                        field_path,
                        "midpoint_from_range",
                        currency=value.currency,
                        lower_bound=str(lower),
                        upper_bound=str(upper),
                        midpoint=str(midpoint),
                    )

    return None, EstimatedCostProjectionDiagnostic(
        field_path,
        "invalid_set_null",
        error_category="invalid_currency" if not currency_valid else "unsupported_amount",
    )


def map_foundry_v1_itinerary(value: FoundryItineraryDTO) -> V1Itinerary:
    """Change only optional costs, then reuse the strict shared itinerary mapping."""

    diagnostics: list[EstimatedCostProjectionDiagnostic] = []
    projected_days = []
    for day_index, day in enumerate(value.days):
        projected_activities = []
        for activity_index, activity in enumerate(day.activities):
            cost, diagnostic = project_v1_estimated_cost(
                activity.estimated_cost,
                field_path=f"days[{day_index}].activities[{activity_index}].estimated_cost",
            )
            diagnostics.append(diagnostic)
            projected_activities.append(activity.model_copy(update={"estimated_cost": cost}))
        projected_days.append(day.model_copy(update={"activities": projected_activities}))

    projected = value.model_copy(update={"days": projected_days})
    mapped = map_foundry_itinerary(projected)
    itinerary = V1Itinerary.model_validate(mapped.model_dump())
    itinerary.set_cost_projections(tuple(diagnostics))
    return itinerary
