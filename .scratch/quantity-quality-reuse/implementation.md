# Quantity comparison-pool reuse: offline implementation

Status: Implemented and offline-validated; subsequent live quantity pilot passed with limitations.
Date: 2026-09-26

Subsequent authorized pilot: D quantity review completed once with all three new-sample
gaps resolved (15 -> 18 canonical visits) and complete capture. See
`artifacts/poi_semantics_acceptance/20260926_D_quantity_review/report.md`. The offline
checkpoint below is preserved historically. The pilot supports quantity/reuse but does
not resolve same-site parent/exhibit overlap or UNKNOWN factual conditions.

Closeout decision: the user declined further Penguin Beach / London Zoo diagnosis or
repair. The exhibit/parent relationship alone does not establish a defect. No issue or
follow-up is opened for it; factual UNKNOWNs remain as previously recorded.

## Outcome

The existing enriched-plus-admitted comparison-pool path already works. No change was
needed to candidate selection, admission, operation permissions, adoption, budgets or
production defaults. A quantity-enabled graph test demonstrates that the actual Repair
model input includes canonical candidates outside the original selected supply.

The new development-only `--capture-repair` option writes one pre-Repair-stage snapshot
under `<case-output>/repair/`. Capture also runs when Repair is skipped, retaining the
actual review-off scope. It records typed enriched and admitted candidates separately,
the original itinerary, validation context (including effective evidence and routes),
scope/windows, request remaining time, untouched stage-entry Repair ledger/limits,
request-wide semantic usage and exact-key cache, provider cache/attempt identity hashes,
runtime configuration/hash and semantic/Repair prompt hashes.

The acceptance wrapper knows the actual CLI request allowance and records elapsed and
remaining time. Direct custom capture adapters without that allowance explicitly report
the missing request limit/elapsed fields; remaining time is still required and never reset.
Provider cache payloads are not serialized. Their hashes are audit-only: values absent
from normalized context/pool cannot be reconstructed by replay.

Capture uses existing secret redaction, immutable creation and a 4 MiB total cap. A
second capture is rejected, including after a failed/partial write. Overflow or storage
failure is explicit in `execution.json`; planning outcomes are not rewritten. A failed
request that never reaches the stage reports `repair_snapshot_not_reached` instead of
claiming a complete snapshot. Capture is off by default.

The existing CLI quantity-review Boolean override now passes through the acceptance
wrapper. Omission preserves runtime configuration; explicit true/false is recorded as
`explicit_override`. No configuration file or other review flag is changed.

## Replay scope and limitations

Run offline from the repository root:

```powershell
.venv/Scripts/python.exe -m tools.validation.repair_replay --snapshot <case-output>/repair/<artifact>.json --output <new-output>.json
```

Replay validates the versioned typed snapshot and runtime hash, recomputes operation
scope, reconstructs insertion windows, and runs existing candidate preparation over the
same pool merge. Only exact semantic input fingerprints can grant eligibility. Missing
or stale judgments are reported, not reassessed. Existing semantic calls/time and saved
request/Repair time remain consumed; insufficient stage time stops preparation.

This is evidence-only stage-scope analysis. It does not invoke providers, retrieval or
models, localize a Repair round, generate a patch, or replay adoption. It does not
reconstruct missing cached provider values. UNKNOWN routes/hours remain UNKNOWN; a
candidate opportunity is not verified itinerary feasibility. Prompt drift is reported.
Synthetic artifacts are explicitly labeled. New capture cannot restore D's lost pool,
and no new live quantity-improvement claim is made.

## Offline validation map

New `backend/tests/versions/v3/test_quantity_replay.py` covers:

- complete typed pool roundtrip/deduplication, nonselected reuse and missing Details;
- actual graph-to-Repair full-pool input with review on, and skipped behavior with review off;
- one/three/five sparse dates, no invented movement/revisit permissions;
- real semantic-service cache reuse at exhausted calls/time, stale prompt misses;
- missing snapshot fields and exhausted stage time, deterministic replay, blocked sockets;
- capture failure isolation, redaction, byte cap and duplicate-stage prevention;
- acceptance CLI default/true/false pass-through and incomplete pre-stage failures.

Existing tests, rerun rather than duplicated:

| Requirement | Existing V3 test evidence |
| --- | --- |
| Distinct identity capacity and repeat rejection | `test_repair.py::test_multi_target_links_remain_but_supply_and_patch_cannot_double_count`; `test_material_feedback.py::test_independent_matching_counts_unknown_identity_once` |
| Date eligibility, future opening and retained unknowns | `test_repair.py::test_date_exclusion_preserves_other_date_and_unknown_is_not_excluded` |
| Real opening/window intersections | `test_material_feedback.py::test_hours_window_opportunity_has_no_minimum_duration_and_keeps_unknown`; `test_b_targets.py::test_default_window_rejects_outside_hours_and_unknown_timezone` |
| Geography and applicable transport evidence | `test_api_evidence_policy.py::test_existing_api_route_bypasses_radius_in_preparation_and_acceptance`; `test_material_feedback.py::test_applicable_leg_policy_can_block_all_positions_without_blocking_unknown_routes`; `test_multiround.py::test_geographic_policy_rejects_far_addition_even_with_large_time_gap` |
| Unauthorized edits and regression protection | `test_repair.py::test_unauthorized_operations_rejected_before_post_routes`; `test_repair.py::test_new_conflict_is_rejected`; `test_repair.py::test_scheduled_and_ledger_only_identity_cannot_be_added` |
| Budget/reserve preservation | `test_multiround.py::test_budget_settings_control_sends_and_nearby_reserve_without_round_reset` |
| Semantic non-main policy | `test_semantic_repair.py::test_primary_role_policy_replacement_uses_real_validator_scope_and_stage` |

TDD sequence: the first test failed because the replay module did not exist; implementing
it exposed a synthetic fixture that claimed Details while retaining NOT_ATTEMPTED state.
The fixture was corrected to the real acquired-with-missing-rating state. Capture tests
then failed for the missing observer/wrapper, and CLI tests failed for absent status;
each passed after its slice. A network-denial test initially blocked Windows asyncio's
internal loop socketpair; the guard now starts inside the running loop, still forbidding
all replay connections. No production policy was relaxed to make tests pass.

The focused V3 suite passed: 421 tests. The final full backend suite passed with 1640
passed and 9 skipped in 75.77 seconds. Ruff, changed-file compilation and diff whitespace
checks passed. Two-axis review found no blocking Standards or Spec findings after the
quantity-on graph assertion was added. No live run, commit, P3 work or freeze was performed.

The offline CLI also successfully read a real serialized synthetic artifact at
`artifacts/poi_semantics_acceptance/quantity_reuse_offline/0dc9ea82072b41e1b8acba404cc982ce.json`
and wrote `replay.json` beside it. The deduplicated pool contains `z` and `pending`;
one detailed nonselected candidate is reused, the saved semantic call count stays one,
and missing Details remain pending. Internal canonical/input counters are not provider
sends. This synthetic sample is not evidence about London's actual inventory.

At the offline checkpoint, the recommended next step was to approve a quantity-enabled D pilot
with requirement, semantic and Repair capture, preserving the existing budget and stop
rules. That pilot was subsequently approved and completed as recorded above.
