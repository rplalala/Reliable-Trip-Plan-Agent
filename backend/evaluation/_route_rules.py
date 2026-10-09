"""Frozen rule values shared by route interpretation and report hashes."""

NANOSECOND = 1000000000
CAPS = {"WALK": 2700, "TRANSIT": 2700, "DRIVE": 1800}
DURATION_TOLERANCE_SECONDS = 300
NEXT_VISIT_TOLERANCE_SECONDS = 300
HARD_BOUNDARY_TOLERANCE_SECONDS = 0
DRIVE_RESERVE_SECONDS = 600
WALK_DISTANCE_CAP_METERS = 3000
DISTANCE_TOLERANCE_METERS = 0
QUERY_TIMESTAMP_FRACTION_DIGITS = 6
DEFAULT_OPTIONS = {
    "WALK": {"time_basis": "time_independent", "routing_options": {}},
    "TRANSIT": {"time_basis": "explicit_departure", "routing_options": {}},
    "DRIVE": {
        "time_basis": "time_independent",
        "routing_options": {"routing_preference": "TRAFFIC_UNAWARE"},
    },
}
RULES = {
    "version": "rtpeval_route_rules_2",
    "duration_caps_seconds": CAPS,
    "duration_cap_tolerance_seconds": DURATION_TOLERANCE_SECONDS,
    "walk_distance_cap_meters": WALK_DISTANCE_CAP_METERS,
    "distance_tolerance_meters": DISTANCE_TOLERANCE_METERS,
    "drive_reserve_seconds": DRIVE_RESERVE_SECONDS,
    "hard_boundary_tolerance_seconds": HARD_BOUNDARY_TOLERANCE_SECONDS,
    "next_visit_tolerance_seconds": NEXT_VISIT_TOLERANCE_SECONDS,
    "default_departure": "longest_continuous_fragment_then_earliest",
    "duration_precision": "integer_nanoseconds",
    "query_timestamp_fraction_digits": QUERY_TIMESTAMP_FRACTION_DIGITS,
    "default_query_options": DEFAULT_OPTIONS,
    "transport": "v0_activity_v1_v3_transfer",
    "unbound_v0_transport": "declared_activity_clock_establishes_occupancy_without_route_identity",
    "partial_proven_failure": "FAIL",
    "conditional_compliance": "PASS/(PASS+FAIL)",
}
