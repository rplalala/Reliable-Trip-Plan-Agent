# Shared itinerary output

## Product and model roles

Final itinerary_2 contains dated/timed primary activities and zero to three optional unplanned
references. References have no time, cost or booking status; associated dates must be in the trip.
They neither satisfy REQUIRED nor count as scheduled visits or planned costs. Empty is valid.
V0 generates both roles once as model knowledge with null external identities. V1/V2 use a
primary-only model DTO, followed by application-attached Nearby references. There is no same-pool
model fallback or extra recommendation LLM.

## Three ledgers and role summary

Main source_place_id resolves against main supply evidence. Truly generic activities may be null;
do not fuzzy-match missing identities. Anchors must be actual scheduled, locatable identities.
Reference identities resolve against independent successful Nearby results, possibly outside
supply. The application supplies source_ref, name/address and attribution. An address does not
prove a separately confirmed locality. Main identity validation is not relaxed for new references.
output_role_summary distinguishes scheduled identities, unlinked activities, unused supply,
references and unarranged REQUIRED. References are not a partition of unused supply. A previously
unused candidate may qualify only after independent Nearby discovery. Deduplicate scheduled and
reference identities; do not silently delete invalid model items to manufacture acceptance.

## Invariance and uncertainty

Post-primary work changes only references and related sources/role diagnostics, never primary
dates, times, order, identity, costs/cost diagnostics or REQUIRED decisions. Ordinary reference
failure preserves primary success; cancellation propagates. Search mechanics belong to
[V1 design](v1_design.md). A supplied place need not be scheduled; the default daily
target below is not an unconditional quota or a requirement to fill every hour. Unknown prices remain unknown. Date/identity checks are
not V3 feasibility validation. Straight-line proximity is not measured walking or accessibility.


## Baseline closure: structural order and evaluation metric contract

The shared V0/V1/V2 output-source boundary stably sorts activities within each existing day by
start_time, preserving original order for ties. It does not reorder day groups or modify any
activity field, reference, identity, note or cost. Cost-projection diagnostic paths follow the
same activities after permutation. This happens before Nearby; Nearby still cannot reorder the
primary itinerary. Raw model DTOs and historical captures remain unchanged. Standalone schema
construction is not the normalization boundary. No overlap or feasibility repair is performed.

Baseline responsibilities are valid structured input, bounded candidate supply, structural
normalization, provenance and truthful uncertainty. Future V3 owns whole-itinerary validation,
violation detection, targeted repair and re-validation. It remains unimplemented.

The following is a metric contract only, not an evaluator implementation or benchmark result.
References are excluded throughout. Use the inclusive requested date set; a missing day counts
as empty. Record raw-model and normalized ordering separately to avoid hiding model errors.

| Metric | Definition and limits |
| --- | --- |
| trip_days / days_with_activity | Inclusive requested dates / distinct requested dates containing primary activities |
| empty_day_count / empty_day_rate | trip_days minus days_with_activity / divide by trip_days; not automatically a violation |
| chronological_order_violations | Adjacent start-time inversions within each day; ties are valid; report raw and final separately |
| scheduled_activity_count | All primary activity instances, including repeated visits and unlinked activities |
| unique_canonical_poi_count | Distinct non-null linked canonical IDs; unavailable for V0, not zero verified places |
| repeated_canonical_visit_count | Linked activity count minus unique linked IDs; descriptive, not necessarily unreasonable |
| duplicate_visit_ratio | repeated_canonical_visit_count / linked activity count; unavailable with no linked identity |
| supply_count / scheduled_unique_supply_count | Distinct supplied IDs / intersection with scheduled IDs; not applicable to V0 |
| unused_supply_count / utilization_ratio | Supply minus scheduled intersection / intersection divided by supply; zero supply means unavailable ratio |
| required_total / required_scheduled / required_unscheduled | Distinct resolved REQUIRED IDs / intersection with primary IDs / difference; unresolved identities reported separately |
| V0 required-place observation | Separate name-based/manual observation, never canonical satisfaction inferred by fuzzy matching |
| activities_with_known_cost / activities_with_unknown_cost | Reliable, scope-compatible activity costs versus missing, unsupported, conflicting or incompatible costs |
| cost_evidence_coverage | Known-cost activities / all primary activities; no activities means unavailable ratio |
| known_total_cost | Sum only reliable, nonoverlapping costs normalized to the same currency, party and time scope; empty sum is explicitly a known subtotal, not a zero trip cost |
| budget_status | FAIL if reliable nonnegative known costs already exceed the budget; PASS only if complete comparable evidence covers the declared budget scope and total is within budget; otherwise UNKNOWN |

A numeric estimated_cost is not by itself verified evidence. A range midpoint remains an estimate,
not an official price. Activity coverage alone cannot prove compliance with a whole-trip budget
when transport, accommodation or other in-scope costs remain unobserved. No baseline budget_status
validator currently exists. Null is preserved; the UI omits a null cost rather than displaying zero.
Free-text model claims are not mechanically verified by these contracts.

Future feasibility observations should identify run/version, activity IDs/date, violation kind,
evidence refs, evidence availability, assessment (confirmed conflict / no conflict / UNKNOWN),
and rationale. Kinds include opening-hours conflict, route/time conflict, unreasonable repeated
experience, visitor-access uncertainty and factual contradiction. Missing evidence is not failure;
repeated identity is not proof of duplicate experience. No repair or new acquisition is authorized
by this metric definition.

## Evaluation checkpoint governance

This checkpoint locks the core mechanism differences used for version comparison, not permanent
implementation immutability. Shared correctness, contract and infrastructure bugs remain fixable
in shared implementation and must affect every dependent version, including future V3. Do not
reserve ordinary shared fixes for a higher version to manufacture an advantage. No per-case,
version-specific prompt/budget tuning or ad-hoc repair is part of this baseline.

For a shared change that materially affects completed evaluation, record the old/new checkpoint,
change scope and impacted versions/cases, then explicitly decide which evaluations require reruns.
V3's added mechanism remains explicit post-generation validation, targeted repair and re-validation;
ordinary shared maintenance is not a V3 capability. This task does not declare a formal re-freeze
or complete evaluation acceptance.

## First-generation roles and diagnostics

All three generators share the default objective: cover the full requested date range,
normally 2-5 distinct main POIs per normal full day, without concentrating all visits
at the start. Explicit rest/pace, long REQUIRED visits and evidence availability take
precedence over quota filling. No fabricated places, filler or repeats to inflate counts.

New model DTOs require activity_kind: main_poi, generic_activity, transport, free_time,
or unknown. Historical domain inputs without the field default to unknown. The role
is model-declared, not verified place suitability; no keyword inference or fuzzy matching.
A REQUIRED cafe may be a main visit. Nearby is never counted as a scheduled main visit.

PlanningResult.generation_diagnostics is application-owned and optional for historical
results. V0 computes it after existing date validation; the shared V1/V2 graph computes
it after identity/date checks and before Nearby, which cannot change it or the draft.
It records every requested date, including absent days. Per-day fields are date,
day_present, applicability, count_basis, main_activity_count, distinct_main_poi_count,
repeated_main_poi_count, generic_activity_count, transport_activity_count,
free_time_activity_count, unclassified_activity_count, target_status and empty_day.

V1/V2 count only declared main_poi visits with IDs in the validated supply. V0 uses only
NFKC Unicode, whitespace and case normalization of main place names (name_proxy), not
canonical identity. Missing roles/identities are unclassified, never inferred. The
same-day remaining-hours case is not_assessable. Other days are measured against the
default target; this does not certify full-day availability or adjudicate pace exceptions.
Any unclassified activity makes that day's target status not_assessable; partial known
counts remain visible. Zero known main POIs does not prove zero real visits when roles
are unknown. Empty means no activities, which is distinct from zero counted main POIs.

Trip fields summarize within/below/above/unassessable days, empty days, zero-known-main
days, scheduled_unique_supply, unused_supply and cross_day_repeated_visits. Supply
counts use distinct counted main IDs; V0 supply counts are null (not applicable), not
zero. Within-day repeated count is counted visits minus distinct IDs/names; cross-day
repeated count counts a distinct key once per subsequent day, independent of same-day
multiplicity. The existing output_role_summary continues reporting all linked activities;
these two metrics deliberately have different denominators. Related semantic requirement
IDs remain available for traceability; no new language interpretation is performed.

Diagnostics only observe. A below-target result can still be a successful legal draft.
No search, refill, second generation, repair or activity mutation follows these counters.
The 160000 engineering input guard and 16384 output-token allowance remain unchanged.
