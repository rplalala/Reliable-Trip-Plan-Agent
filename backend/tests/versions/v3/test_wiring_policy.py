"""Narrow application permissions reuse existing findings without semantic inference."""

from backend.app.versions.v3.wiring import operation_scope
from backend.tests.versions.v3.test_validation import DAY, activity, binding, contract, draft, run


def test_required_omission_allows_addition_without_deleting_existing_visits():
    original = draft([activity(pid="b")])
    report = run(
        itinerary=original, requirements=contract("REQUIRED"), named_resolutions=(binding(),)
    )
    scope = operation_scope(original, report)
    assert scope.add_dates == (DAY,)
    assert not scope.permissions and not scope.allow_coverage_regression


def test_excluded_identity_grants_only_its_explicit_delete_permission():
    original = draft([activity(), activity("other", "b", "12:00", "13:00")])
    report = run(
        itinerary=original, requirements=contract("EXCLUDED"), named_resolutions=(binding(),)
    )
    scope = operation_scope(original, report)
    assert len(scope.permissions) == 1
    assert scope.permissions[0].activity_id == "one"
    assert scope.permissions[0].operations == {"delete"}
    assert not scope.permissions[0].allow_duration_change
    assert not scope.allow_coverage_regression
    assert scope.coverage_permissions[0].allow_partial
    assert scope.coverage_permissions[0].reason == "excluded_removal"
    assert scope.add_dates == scope.dates


def test_repetition_and_unknown_opening_grant_no_operations():
    original = draft([activity(), activity("repeat", "a", "12:00", "13:00")])
    report = run(itinerary=original)
    assert any(f.check == "repetition" for f in report.findings)
    assert operation_scope(original, report) is None
