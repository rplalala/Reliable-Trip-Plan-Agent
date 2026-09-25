# V3 design

## Final engineering checkpoint — 2026-09-25

Current closeout status: **V3 ENGINEERING CLOSED — FINAL ENGINEERING CHECKPOINT RECORDED**. The [closeout record](v3_closeout.md) supersedes
earlier current-state claims below; dated checkpoints remain historical. Shared mixed transport,
five-round Repair, minimum coverage, same-round component partial adoption and two final TRANSIT
legs have artifact-confirmed bounded live observations. Prompt13 budget scope and the latest
content-filter UI mapping remain offline-only. Benchmark Frozen: NO; Formal Evaluation: NOT STARTED.


V3 adds application validation, bounded targeted Repair and revalidation to the shared
V2 primary flow. V0/V1/V2 remain independently runnable. The product default is unchanged.
The mixed-transport/component revision is **implemented + offline-validated**; no new live evidence
or version freeze is implied. [Development history](v3_development.md) preserves dated
implementation, tests, capacity decisions and historical live observations.
[Milestone status](v3_milestone.md) separates current delivery from historical evidence.

## Request flow and ownership

The default-disabled post-primary hook in the shared graph runs after primary identity/date
checks and before one final Nearby stage. V3 does not rerun interpretation, initial discovery
or primary generation. Request resources, caches, send/failure records and the request
entry deadline are shared. Repair counters and its deadline start once per stage.
The immutable draft, original report, fairly reassessed draft, component proposals and
latest adopted itinerary remain distinct. Nearby references never supplement primary counts.

## Validation, targets and permissions

The existing validator distinguishes diagnostics, CONFIRMED conflicts, NEEDS_REVIEW and
UNKNOWN. Applicable Google operating windows and route estimates support their specific
checks; admission, ticketing and future-real-world guarantees remain separate uncertainties.
Quantity, repetition and overfull reviews default off. Confirmed operating/transfer conflicts
are automatic targets. Confirmed/hard obligations precede activated compensation and reviews;
deferred targets cannot drive current acquisition, authorization or projection.

A supplies fixed occupancy, authorized elastic free-time consumption and real-place adjacency.
B supplies coverage, repetition, overfull, satisfaction-based REQUIRED protection, adjacent
moves and scoped compensation. C supplies evidence-backed operating/transfer repair.
The same validator and business comparison protect identities, sources, dates, required and
excluded obligations, duration, fixed time, coverage and confirmed conflicts throughout.

## Per-leg mixed transport

`repair_transport.py` uses the soft WALK, TRANSIT, DRIVE preference. Supported explicit
requirements restrict allowed modes. No raw preference or note keywords are interpreted.
Existing applicable evidence for any allowed mode is examined before sending another query;
existing DRIVE can be used without a ceremonial TRANSIT call. Sent failures retain their
request key; a failed TRANSIT query can be followed by a distinct allowed DRIVE query.

| Mode | Automatic selection window | Occupancy |
| --- | --- | --- |
| WALK | Provider distance <=3 km and duration <=45 min | Provider duration |
| TRANSIT | Applicable provider total duration <=45 min | Provider total, without duplicate access walking |
| DRIVE | Provider driving duration <=30 min | Provider duration plus 10 min application reserve |

These values come from runtime.yaml, not user statements. The 2 km WALK / 5 km motor
geographic prefilters support discovery and missing-route screening; applicable provider
options proceed to temporal, burden and detour checks. They are not permanent place labels.
Missing routes permit only the existing conservative WALK <=1 km / 45-minute reservation;
no driving estimate is inferred from coordinates. All chosen legs must fit one continuous
available interval, respect fixed occupancy and both adjacent visits, and preserve the
stage-original daily added traffic limit of 90 itinerary minutes. DRIVE reserves count.
No comparable original route means no invented baseline credit.

Preparation rotates active addition opportunities by target, using a nearest real anchor
and directed options rather than fetching the whole pool in three modes. This provisional
anchor/time is explicitly not insertion feasibility. Retime/delete and other actual changed
chains obtain necessary routes after legal patch construction. Final binding checks every
changed real adjacency, including both sides, with its actual departure. TRANSIT remains
exact-time-sensitive; basic DRIVE and WALK retain their provider-estimate evidence basis.

## Joint repair and component atomicity

`repair_input_2` uses projection revision `mixed_transport_components_1`: canonical catalog,
separate operation authorizations, protected/current context, compact target worksheet,
transport options, adopted transfers, constraints and bounded feedback. A strict model result
contains edits and target dispositions. Model explanations are not evidence. The application
selects allowed per-leg modes and reserves; the model cannot write provider facts.

`repair_components.py` partitions a maximum of 50 parsed edits using concrete dependencies:
activity, source identity obligation, affected dates/adjacency/elastic roots/daily burden,
protected cost association, parent compensation and shared target. Same-date edits are
conservatively atomic. Common validator kind alone does not link unrelated dates.
New-identity competition across independent dates is resolved sequentially, not by accepting
a duplicate. Malformed structured output fails before partition; no partial JSON salvage.

Components run once in deterministic confirmed/compensation/review order with a stable edit
index tie-break. Each uses the latest working itinerary and runs authorization, schedule,
route acquisition/binding, occupancy adjustment, spatial policy, validator and business
comparison. Dependent deletion and compensation stay together, except existing narrowly
authorized EXCLUDED/unexecutable-visit partial-removal policies. Every accepted component
must measurably improve an authorized goal. A rejected independent component leaves earlier
accepted components intact. Final global checks reject an illegal combination; the minimal
safe fallback is the round input if the final combination cannot be justified. There is no
exponential subset search. Actual sends, obtained evidence and failure history never roll back.

Remaining goals continue from the latest accepted state. Compact component decisions and
localized failures enter existing material feedback. Presentation is not qualification;
a rejected component does not taint unedited candidates. Fingerprints include actual
transport options/bindings and permissions, not just a round number.

## Shared output and frontend

The optional shared `Itinerary.transfers` array defaults empty for historical/V0-V2 outputs.
V3 publishes adopted pair/activity/canonical IDs, mode/source, departure/arrival, provider
seconds/metres, separate application reserve, routing preference, evidence references,
calculation basis, validation state and unknowns. Final presentation uses the same binding
and route selector as validation. It does not create visits, expense commitments or transit
stations. Car transport must be arranged; cost/availability are not inferred.
The existing frontend renderer displays estimates and reserves separately. Product V3/API
selection and other previously deferred frontend features remain outside this revision.

## Effective limits and lifecycle

`config/runtime.yaml` is authoritative; [configuration reference](../config/README.md)
describes every leaf. Current Repair limits: 5 rounds/calls, 360 stage seconds, at most70
model seconds, 252000 engineering input tokens, 16384 output tokens, 32 input identity union,
120 activities. Preparation is at most45 runtime seconds, shortened dynamically for model,
recheck/finalization and the original request deadline. Nearby reserves its existing budget.
A 600-second development request still requires the existing explicit override.

Stage acquisition: Google6 (ordinary5 plus fallback1), canonical30, Details30,
embedding1/retrieval1 Top-K10, Routes16 requests/32 elements. Route preparation allowance is
16 minus reserved4 =12; all rounds/modes share these counters. Unused preparation sends may
serve proposals. Cache hits are free; actual failed sends count; same-key hidden retries are
prohibited. Reviews/Profile and Official Web are not newly acquired by Repair.
Input overflow, terminal model failure or no material opportunity stop safely; cancellation
propagates and request owners release self-created resources.

## Limits

No global transport optimizer, vehicle-location/parking state, rideshare pricing, detailed
transit navigation, semantic evaluator or arbitrary public-access inference is introduced.
The nearest-anchor preparation is provisional, not exhaustive; exact final TRANSIT departure
may need a fresh bounded query. Conservative same-date components can reject more edits than
a finer proven dependency partition. Budget exhaustion can leave legitimate goals unresolved.
Offline evidence does not prove real provider availability, model throughput or quality gains.


## Shared first-generation mixed transport (current offline checkpoint)

V1/V2/V3 now use shared baseline routing, bounded pre-generation mixed-mode options,
one primary generation, and actual-adjacency/time transfer binding before the version's
post-primary step. V1/V2 report conflicts and UNKNOWN without repairing activities.
V3 reuses the same evidence and adopted transfers in its existing validator and Repair.
V0 remains tool-free. This is a shared baseline upgrade, not V3-exclusive mechanism value.

The normal planning supply is unchanged: this does not rediscover omitted POIs, increase K,
or add a second discovery pass. Default WALK preference permits evidence-supported TRANSIT
and DRIVE alternatives; explicit supported requirements remain restrictive. Representative
TRANSIT never inherits final-time PASS. Provider duration and DRIVE application reserve are
separate. The primary projection retains all directed baseline facts in a compact catalogue;
it drops redundant wrappers, not inconvenient facts. No selective fact omission is performed.
Unbound actual adjacencies remain in application-owned `route_diagnostics`, including
per-mode facts and unresolved alternatives; absent transfers do not erase obligations.

Primary input is 252000, output 16384. Supplementary totals are 32 directed pairs / 32 sends /
64 requested elements; post-generation reservations are 16 / 16 / 32 within those totals.
Baseline remains 7 / 400 / 64. Cumulative route-work wall time is 120 seconds with 30 seconds
reserved for post-generation, always inside the original request deadline. Other acquisition,
Repair and Nearby limits are unchanged. Common transport policy now belongs to `transport`
in runtime.yaml; Repair-only authority and added-burden policy remain version-specific.

Implementation and tests are recorded in `docs/v1_development.md`. This checkpoint has only
offline evidence; historical development live records are unchanged and do not validate it.
No new live, evaluation, freeze, commit or push is implied.


## Shared preference input gate checkpoint (2026-09-25)

Implemented + offline-validated only. All V0-V3 entries reuse the existing single preference
interpretation call to assess request-level input issues before travel acquisition. Application
policy checks exact provenance and returns rewrite/clarification or dedicated safety outcomes;
VALID does not certify feasibility or override hard-requirement/capability checks. Empty input
still skips interpretation. Model contract/provider failures remain system failures. Product
engine selection and travel budgets are unchanged. Historical live runs were not retroactively
validated with this feature. See [shared preference input checkpoint](shared_preference_input.md)
for contracts, compatibility, API/UI behavior, actual test chronology and serializer limits.


### Minimum daily coverage update (2026-09-25)

Shared output now reports the one-primary-visit minimum independently of 2-5 review
quantity guidance. V0-V2 remain diagnostic-only; V3 prioritizes confirmed minimum gaps
below hard protections and above optional reviews. Explicit source-linked full-day time
protections support exemptions; uncertain applicability remains unknown. Product output
includes coverage status without research metadata or source quotations. The primary
prompt, default engine and budgets are unchanged. See [shared minimum coverage](shared_minimum_daily_coverage.md)
for counting, compatibility, exemption and partial-result boundaries, and the V3 development
checkpoint for offline and live evidence. This does not retroactively validate historical runs.


Minimum coverage live checkpoint (2026-09-25): the single authorized Honolulu run
`f9bd621d-0eb5-47d7-8af8-03825d57524b` repaired three zero-main-visit dates in round1;
all nine days meet the minimum, while one ordinary quantity review remains. Five actual
Repair calls retained eight additions (10 -> 18 main visits), exit0. This supplies limited
live evidence for the observed path only; exemptions/review-off remain offline-tested.
See `docs/v3_development.md` and the complete run report for counters, UNKNOWNs and limits.
No freeze or formal evaluation is implied.
