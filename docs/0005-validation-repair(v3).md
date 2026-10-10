# Structured validation and targeted repair

Status: Implemented V3 architecture, consolidated 2026-10-03.

## Validation is a separate stage

V3 consumes the shared V2 primary result, normalized evidence and source-linked requirements.
The validator produces structured findings with evidence/applicability boundaries. Confirmed
contradictions, missing facts and optional quality observations are not interchangeable.
UNKNOWN never becomes PASS simply because a model offers a plausible explanation.

Validation includes supported requirement, schedule, coverage, repetition and factual
consistency policies. Applicability depends on available evidence and declared scope.
This is planner-internal validation, not the independent evaluator's ground truth.

### Supported findings and factual limits

[Validation](../backend/app/versions/v3/validation.py) emits `PASS`, `CONFIRMED`,
`NEEDS_REVIEW` or `UNKNOWN`; only `CONFIRMED` is a violation. A finding or improvement
target is distinct from the later operation permission. Its supported boundaries are:

| Finding family | Current scope |
| --- | --- |
| Named/semantic and primary policy | Source-bound named inclusion/count/date obligations, supported semantic count/date goals and primary-role/exception policy; arbitrary open text remains unassessed. See [shared semantics](0002-requirements-evidence.md#semantic-qualification-and-multiplicity). |
| Overlap, repetition and coverage | Supported schedule conflicts, unauthorized canonical repeats and minimum coverage; optional quantity/overfull review remains separate. See [counting](0003-itinerary-transport.md#generation-diagnostics-and-counting-contract). |
| Opening | Complete visit containment in adopted structured intervals, with selected-hours provenance and outside-hours magnitude; this is not admission or ticket verification. |
| Route | Actual directed transition bindings and applicable evidence; missing mode/departure/binding remains UNKNOWN. |
| Visitor suitability and budget | Admission eligibility, reservation/ticket possession, special-area access and verified whole-trip affordability remain UNKNOWN. Reported conditions are context, not certified fulfillment. |

[Opening selection](../backend/app/evidence/opening_hours.py) prefers applicable adopted
official date/range facts, then request-window current Places periods and eligible regular
weekly periods. Conflicting, invalid or missing applicable material retains UNKNOWN.
Without an explicit visit binding, the application uses the recorded `obey_place_hours`
scheduling policy. An explicit exterior/non-entry binding cannot acquire an entry-hours
PASS. A missing venue timezone may use the single recognized timezone of related scheduled
places; this is planner context, not the evaluator's independent timezone evidence.
The selected intervals may cover overnight visits; older whole-venue/date-only limitations
in records describe their earlier checkpoints. Even an hours PASS establishes only that
adopted-hours condition, not real-world access or independent factual completeness.

## Authority precedes editing

Target selection and operation permissions are application-owned. Hard protections,
required/excluded identity obligations, fixed time and existing accepted state constrain
each proposed patch. Optional quantity review is recorded separately from minimum daily
coverage. A sparse or overfull day alone does not grant unrestricted rescheduling.

Confirmed opening/route conflicts can authorize duration-preserving retiming of affected
main visits and policy-bounded moves. Delete/replace requires the existing dispensable-visit
and sourced count/date/access protections; the application does not shorten a visit merely
to fit hours. Removed-obligation progress stays distinct from verified resolution, and
retained route endpoints require applicable checks of the actual changed chain.

Repair receives compact current context, canonical candidates, target worksheets, allowed
operations, route options and bounded feedback. It proposes edits and target dispositions;
it cannot author provider evidence or expand its own operation scope. Invalid structured
output fails before adoption; partial malformed JSON is not salvaged as an itinerary.

## Components, adoption and fallback

The [joint component contract](#joint-repair-and-component-atomicity) defines dependencies,
ordering, adoption and safe fallback. Independent rejected components preserve earlier
accepted improvements; missing facts never become a successful repair claim.

## Transport and resource boundaries

Changed real adjacencies require both neighboring legs to be considered at applicable
departure times. Representative route preparation is not insertion feasibility. Fixed
occupancy, required visits, daily burden and separately represented application reserves
remain binding. Missing evidence permits only the explicitly coded conservative fallback,
not fabricated driving or transit estimates.

Rounds, per-stage work and total request deadlines are bounded by runtime configuration.
The V3 runner establishes the whole-request deadline before owned retrieval setup; later
stages cannot reset it. Exhaustion, cancellation, no authorized target, rejected proposal
and accepted repair are separate recorded outcomes. Final Nearby runs after final primary
selection and cannot modify the accepted primary plan.

Retrieval initialization is lazy. If the request expires before its factory runs, no
runtime exists to release. A factory-created runtime is released once on timeout or
cancellation; a caller-owned runtime remains caller-owned. Offline deadline regressions
must establish which phase was reached before asserting its resource lifecycle, rather
than relying on a short wall-clock delay to select that phase.

Accepted draft and final selection use the shared
[source-fact ownership boundary](0003-itinerary-transport.md#scheduled-activities-and-references).
Final selection includes original supply and the verified Repair whitelist, so retaining
or retiming a visit preserves its provider name and complete address just as add/replace
does. This application normalization requires no extra model/Google call and does not
make the read-only validator mutate its input or certify independent ground truth.

## Soft pace objective

V3 Repair aims for zero soft pace deductions under the existing daily-density table.
Zero is an optimization objective, not output validity or a failure gate. The
`quantity_review_enabled` flag enables this optional quantity optimization; opting out
preserves hard Repair. A resolved pace policy supersedes the generic 2-5 quantity
target on that date. Minimum daily coverage and hard visit protections remain separate.

Read-only validation counts primary visit occurrences, including assessed visits that
the model labels as generic; Nearby, transport and unlinked filler do not count.
`soft_pace` findings retain source-linked policy, count, penalty and zero-penalty counts.
Positive known penalties are review targets, never CONFIRMED violations; unavailable
policy/roles/counts remain diagnostic uncertainty without guessed edit authority.
The numeric curves live in `backend/pace_policy.py`; independent evaluation retains
its own reviewed input policies and evidence rather than consuming planner interpretation.

The application permits bounded additions or removal/movement of dispensable visits,
then reuses existing mandatory count/date/time, role, coverage, route/occupancy and
budget checks. A strict reduction can be accepted without reaching zero. A pace patch
cannot increase another comparable date's penalty or replace it with uncertainty.
No role relabeling is an edit operation. At a budget/opportunity stop, keep the latest
accepted legal itinerary or untouched draft; retained penalties do not fail V3 generation.
`soft_pace` summaries in V3 outcome and stage result expose before/after days and mean,
`reached`/`residual`/`unavailable` state and `is_failure_constraint=false`. Existing
round patches, stop reasons and actual usage remain authoritative. V0-V2 and V3 draft
acceptance gain no zero-penalty condition; independent evaluation still scores all normally.

Offline tests exercise authorization, regressions, component interactions, rejection and
fallback with controlled evidence. Bounded historical live repairs demonstrate only their
observed paths. They do not establish universal improvement or factual completeness, and
do not retroactively validate later code. V0/V1/V2 retain independent paths without this
repair stage.

Implementation owners: [runner](../backend/app/versions/v3/runner.py),
[validation](../backend/app/versions/v3/validation.py),
[acceptance](../backend/app/versions/v3/repair_acceptance.py),
[components](../backend/app/versions/v3/repair_components.py) and
[service](../backend/app/versions/v3/repair_service.py).

## Request flow and ownership

The default-disabled post-primary hook in the shared graph runs after primary identity/date
checks and before one final Nearby stage. V3 does not rerun interpretation, initial discovery
or primary generation. Request resources, caches, send/failure records and the request
entry deadline are shared. Repair counters and its deadline start once per stage.
The immutable draft, original report, fairly reassessed draft, component proposals and
latest adopted itinerary remain distinct. Nearby references never supplement primary counts.

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

## Limits

No global transport optimizer, vehicle-location/parking state, rideshare pricing, detailed
transit navigation, semantic evaluator or arbitrary public-access inference is introduced.
The nearest-anchor preparation is provisional, not exhaustive; exact final TRANSIT departure
may need a fresh bounded query. Conservative same-date components can reject more edits than
a finer proven dependency partition. Budget exhaustion can leave legitimate goals unresolved.
Offline evidence does not prove real provider availability, model throughput or quality gains.

## Target priority and stage accounting

Confirmed/hard obligations precede activated compensation and optional review. Minimum
coverage gaps precede optional quantity review but do not override hard protections.
Unauthorized repeats are automatic policy targets; historical unassessed multiplicity is
not proof that deletion is safe. Deferred targets cannot drive current acquisition or edits.
Dependent deduplication/compensation can remain unpublished until its whole group is accepted.
Only the narrowly authorized removal exceptions permit partial deletion without compensation.

All rounds share the stage counters, evidence cache, actual-send/failure history and deadline.
Preparation leaves configured reserves for model/recheck/finalization and final Nearby;
unused preparation allowance can serve proposals. Reviews/Profile and official web are not
new Repair acquisitions. Input overflow, terminal model failure and no material opportunity
stop at their declared boundary. The final stage summary compares original and adopted plans,
not a rejected proposal. Transport thresholds above are configurable policy, not user facts.

## Pending compensation and publishable state

Deduplication cannot evade counting by moving a visit to another date or changing its role.
The Repair model chooses the retained occurrence using sourced obligations, actual windows
and route context; the application does not always keep the first. Explicit count/date-bound
copies remain protected. The minimum-one rule does not replace the existing conditional
coverage floor merely to permit a deletion.

An otherwise valid deduplication group awaiting coverage compensation may be retained as a
bounded unpublished proposal. The pending group carries affected dates, base-state fingerprint,
edits and proposal days; only a matching current base can reactivate it. Descendant edits stay
in the same atomic group, while independent accepted edits remain publishable. Completion
rechecks the combined group against the current adopted state. Exhaustion discards pending
dependent windows/transfers without reverting independent improvements or waiving coverage.
Residual repetition/coverage remains explicit incomplete output. Confirmed excluded or
unexecutable-visit removal retains its separately authorized partial-removal policy.

Already assessed candidates may be reused after the semantic preparation budget is exhausted;
new ADD/REPLACE candidates require shared qualification before authorization. Budgets are
request-wide, not reset per round. Terminal semantic model/contract failures remain failures,
not a successful generic Repair fallback. Final Nearby occurs once only after normal finalization,
with no continuation after terminal failure, cancellation or an exhausted request deadline.
Implementation: [pending groups](../backend/app/versions/v3/repair_pending.py).
