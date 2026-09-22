"""Explicitly synthetic evidence shared by payload diagnostics and offline tests."""
from datetime import UTC, date, datetime, timedelta

from backend.app.evidence.models import (
    EvidenceAvailability,
    NonWalkablePairEvidence,
    NonWalkableTrigger,
    OpeningHoursEvidence,
    PlaceCandidate,
    PlaceEvidence,
    RouteElementEvidence,
    RouteElementEvidenceType,
    RouteEvidence,
    RouteEvidenceBundle,
    RouteEvidencePurpose,
)

START = date(2026, 9, 12)
END = START + timedelta(days=9)
RETRIEVED = datetime(2026, 9, 11, tzinfo=UTC)

def _places(count=16) -> tuple[list[PlaceCandidate], list[PlaceEvidence]]:
    candidates = []
    places = []
    current = OpeningHoursEvidence(
        applicability="provider_current_window",
        valid_from=START,
        valid_through=START + timedelta(days=6),
        weekday_descriptions=[
            f"{name}: 09:00-17:00"
            for name in (
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            )
        ],
    )
    regular = OpeningHoursEvidence(
        applicability="regular_weekly_pattern",
        weekday_descriptions=[
            f"{name}: 09:00-17:00"
            for name in (
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            )
        ],
    )
    for index in range(count):
        place_id = f"poi-{index:02d}"
        name = f"Museum {index:02d}"
        candidates.append(
            PlaceCandidate(
                place_id=place_id,
                name=name,
                latitude=-33.8 + index / 1000,
                longitude=151.2 + index / 1000,
                business_status="OPERATIONAL",
                source_query="Sydney museums",
                category="museum",
                provider_rank=index,
            )
        )
        places.append(
            PlaceEvidence(
                place_id=place_id,
                name=name,
                latitude=-33.8 + index / 1000,
                longitude=151.2 + index / 1000,
                business_status="OPERATIONAL",
                opening_hours=current,
                current_opening_hours=current,
                regular_opening_hours=regular,
                timezone_id="Australia/Sydney",
                rating=4.9,
                website_uri=f"https://museum{index:02d}.example.org",
                availability=EvidenceAvailability.AVAILABLE,
                retrieved_at=RETRIEVED,
                source_ref=f"google_places:{place_id}",
            )
        )
    return candidates, places


def _route_element(origin: str, destination: str) -> RouteElementEvidence:
    return RouteElementEvidence(
        origin_place_id=origin,
        destination_place_id=destination,
        evidence_type=RouteElementEvidenceType.PROVIDER_OBSERVED,
        status="OK",
        condition="ROUTE_EXISTS",
        distance_meters=10000,
        duration_seconds=7200,
        availability=EvidenceAvailability.AVAILABLE,
    )


def _routes(ids: list[str]) -> RouteEvidenceBundle:
    baseline = RouteEvidence(
        travel_mode="WALK",
        mode_reason="default_walk",
        availability=EvidenceAvailability.AVAILABLE,
        elements=[_route_element(origin, destination) for origin in ids for destination in ids],
        retrieved_at=RETRIEVED,
        source_ref="google_routes:baseline",
    )
    alternatives = [
        RouteEvidence(
            travel_mode="TRANSIT",
            mode_reason="selective_transit_for_non_walkable_pair",
            purpose=RouteEvidencePurpose.NON_WALKABLE_ALTERNATIVE,
            availability=EvidenceAvailability.AVAILABLE,
            elements=[
                _route_element(ids[0], ids[index + 1]),
                _route_element(ids[index + 1], ids[0]),
            ],
            retrieved_at=RETRIEVED,
            source_ref=f"google_routes:alternative:{index}",
        )
        for index in range(8)
    ]
    pairs = [
        NonWalkablePairEvidence(
            place_id_a=ids[left],
            place_id_b=ids[right],
            trigger_reasons=[NonWalkableTrigger.DISTANCE_THRESHOLD],
        )
        for left in range(len(ids))
        for right in range(left + 1, len(ids))
    ]
    return RouteEvidenceBundle(
        baseline=baseline, alternatives=alternatives, non_walkable_pairs=pairs
    )
