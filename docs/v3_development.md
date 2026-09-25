# V3 development record

## Final engineering checkpoint — 2026-09-25

Current closeout status: **V3 ENGINEERING CLOSED — FINAL ENGINEERING CHECKPOINT RECORDED**. The [closeout record](v3_closeout.md) supersedes
earlier current-state claims below; dated checkpoints remain historical. Shared mixed transport,
five-round Repair, minimum coverage, same-round component partial adoption and two final TRANSIT
legs have artifact-confirmed bounded live observations. Prompt13 budget scope and the latest
content-filter UI mapping remain offline-only. Benchmark Frozen: NO; Formal Evaluation: NOT STARTED.


This file preserves the chronological checkpoints formerly held in v3_design.md.
Statements of future scope, budgets and evidence inside a dated checkpoint describe that
checkpoint, not necessarily the current implementation. Historical runs are unchanged.
See [current design](v3_design.md) and [milestone status](v3_milestone.md).

# Original roadmap and checkpoint record

Status: The historical three-day run provides bounded live evidence for the V3 path
without entering Repair. The historical seven-day run provides bounded live evidence
for a real Repair call, rejection and fallback. These records do not validate later
capabilities retroactively.

The original [C operating/transfer checkpoint](#c-operating-and-transfer-checkpoint-2026-09-24)
is **implemented + offline-validated**, building on the accepted B target/operation and
[A elastic-time checkpoint](#a-elastic-time-and-real-adjacency-checkpoint-2026-09-24). The later historical multi-round Tokyo run
`cc5c3a29-ee2b-477e-b4da-d93ed7223b23` contains three rejected proposals; it does not
validate the later A/B/C corrections. Earlier checkpoints retain their original evidence boundaries.
No new live run, formal evaluation, production acceptance or version freeze is implied.


Current checkpoint: [Active-target locality and capacity follow-up](#active-target-locality-and-capacity-follow-up-2026-09-25).
Material feedback has offline evidence plus a subsequent one-round Tokyo live
(4b0b018e-92ae-4563-a401-83f303d8c9cb); no real no-op recovery was exercised. The preceding
[Google API evidence adoption](#google-api-evidence-adoption-checkpoint-2026-09-24) gained bounded
live evidence in run `29b2a5f7-c6fa-45b8-9eba-31b9e89e3ea4`: ten final opening PASS, five WALK
transfer PASS, and one accepted quantity addition; C confirmed-conflict repair was not triggered.
The later feedback correction is not retroactively attributed to that run. Separately, saved ABC run
`759ee785-05c6-44e6-9ef7-9a812a6e21bb` demonstrated one accepted deduplication replacement,
coverage protection, WALK layout and final Nearby. It did not validate this later evidence-policy
revision, all C scenarios or every UNKNOWN dimension. Historical records below are unchanged.

## Research mechanism and non-goals

V3 = V2 initial draft -> explicit post-generation feasibility validation -> structured
violations -> targeted repair -> re-validation. Its independent variable is the
post-generation loop, not a new selector, ranking system, larger supply, more first-pass
search, or a more elaborate first-generation prompt. Shared correctness fixes must
apply to every dependent version and be recorded as baseline checkpoint changes.

The shared 2-5 default full-day target, K20 support, role-aware diagnostics, stable
chronological sorting and PostgreSQL connection tolerance are baseline improvements,
not V3 contributions. They do not guarantee feasibility or implement repair.

## Motivation and evidence limits

The [accepted V2 checkpoint](v2_milestone.md#current-implementation-acceptance-2026-09-20)
and [joint smoke record](development_record.md#v2-current-checkpoint-acceptance) retain
the original Tokyo/Sydney observations. Sydney V2 left the final four requested dates
empty despite successful acquisition; Sydney V1 repeated canonical visits, and an MCA
visit ended after the closure time stated in its own note. A note alone is not verified
opening evidence. Distinct IDs can also refer to subvenues in one complex.

The later [London/shared improvement record](development_record.md#first-generation-coverage-20260920)
records four main visits followed by three empty dates, with RAG stopping at connection
establishment. Those are separate mechanisms: a connection timeout does not prove the
reason for the generator's distribution. Historical outputs are not rewritten after
baseline changes. Development smoke is motivation, not a formal comparative benchmark.

## Future validation inputs

Reuse the PlanningRequest form facts, interpreted semantic requirements and subjects,
REQUIRED/OPTIONAL/EXCLUDED canonical bindings, final supply, initial itinerary and declared
activity_kind. Consume existing generation diagnostics directly for counting/coverage;
do not call an LLM to recount identities. Diagnostics are observations, not violations.

Evidence inputs are normalized Places/current Details, Weather, directional Routes,
ExperienceProfile, accepted Official-current evidence, available cost evidence and
their provenance, dates, scopes and UNKNOWN/unavailable/conflict states. Preserve
the original draft, evidence snapshot and requirement linkage. TripWorld static priors
remain discovery semantics, not verified opening, visitor-access or experience facts.
V0 name proxies must never be treated as V2 canonical evidence.

## Violation and uncertainty categories

| ID | Scope | Evidence and decision boundary | Potential repair scope |
| --- | --- | --- | --- |
| V3-1 | Coverage / temporal distribution | Requested dates, empty dates, zero main POIs, early concentration and unusual under-filled days. Distinguish default-target miss from repair-worthy under-planning using explicit rest/pace, long REQUIRED visits and available evidence. Fewer than two is not automatically a violation. | Affected day/segment, initially using unused supply |
| V3-2 | Duplicate / redundant experience | Same ID may be an intentional revisit; different IDs may share parent/subvenue or experience. Combine purpose, intent, date/time and supported relationships; do not infer guaranteed redundancy from identity alone. | Remove/replace only unjustified repetition |
| V3-3 | Opening / availability | Compare visit interval to reliable date-applicable evidence. Regular hours do not guarantee special-date access; unavailable hours are UNKNOWN. | Time or venue with justified availability |
| V3-4 | Route / transition | Previous end + applicable directional travel duration + approved buffer <= next start. Route mode, representative departure and mirrored estimates matter; absence is not proof of impossibility. Buffer policy remains undecided. | Adjacent visits or affected day |
| V3-5 | Schedule overlap | Shared sorting changes array order only. Activity start < end is already a shared schema invariant; cross-activity overlap and incompatible windows need post-generation checks. Do not rebrand the existing schema check as new V3 behavior. | Conflicting windows |
| V3-6 | Visitor suitability | Operational office/firm/service records do not establish public access or prohibit it. Flag uncertainty; assert conflict only with reliable evidence. | Prefer justified visitor-facing unused candidates where available |
| V3-7 | Cost / budget | Aggregate reliable applicable costs with explicit party/unit/currency scope. A known lower bound above budget can establish a conflict; incomplete prices otherwise leave overall feasibility UNKNOWN. Never map null to zero. | Affected paid visits, without invented prices |
| V3-8 | Generated factual contradiction | Claims/notes versus date-specific hours, place, route or cost evidence. Model prose is not itself official evidence. Distinguish internal inconsistency from evidence-backed falsity. | Specific claim/time/activity |

Required omission and excluded inclusion must also be checked as global requirement
invariants. Default counts cannot justify deleting REQUIRED or reintroducing EXCLUDED.
Weather/provider unavailability remains uncertainty rather than a fabricated safe result.

## Original conceptual findings (superseded by Step 1 contract below)

Each future finding should express violation_id, violation_type, severity/priority if
needed, affected date, activity IDs, place IDs, related requirement IDs, evidence refs,
status (confirmed, probable, unknown/insufficient_evidence), repairability and suggested
repair scope. UNKNOWN entries should be findings of uncertainty, not confirmed violations.
The Step 1 section below defines the implemented names and evidence limits.
Repair authorization remains a separate future application decision.

UNKNOWN != PASS != FAIL. Do not convert model belief or absent evidence into verification.
The validator may retain uncertainty, surface it, or choose a better-supported alternative
when justified. An LLM-assisted semantic judgment must remain distinguishable from a
deterministic finding and an accepted provider fact.

## Targeted repair and invariants

Initial draft -> findings -> repair planner -> change only affected portion -> revalidate
repaired findings and global invariants. Prefer unused existing supply, time adjustment,
movement between days, removal of unreasonable duplication or substitution of an existing
candidate. Limited day/segment generation or additional candidate/evidence acquisition
may be justified only under separately approved repair policy/budgets. Do not regenerate
the whole itinerary by default.

Protect unaffected content and provenance. REQUIRED feasibility conflicts must remain
explicit; do not silently drop the visit to satisfy density. EXCLUDED cannot re-enter
through repair. New identities must pass the normal candidate/evidence boundary.

Nearby remains unscheduled reference material and never fills a main-visit count.
Promoting a reference requires formal identity/evidence/candidate processing. Repairs
that change anchors may make references stale; future orchestration must explicitly
decide their handling and budget, not silently retain mismatched references or rerun
Nearby without accounting. No such mechanism exists now.

## Bounded work and stopping

The Step 1 execution contract below records finite development ceilings for future
repair and evidence acquisition; none are activated by the offline validator.
Reuse compatible evidence and
record failed attempts; no hidden retry or unlimited search to fill a quota.
Propagate user cancellation. Preserve the initial draft and return partially repaired
with remaining findings when budgets, evidence or repairability prevent completion.

## Re-validation

Re-check repaired findings and global date, identity, REQUIRED/EXCLUDED, duplicate,
opening, route, overlap, coverage and budget invariants. A repair is not success until
the applicable checks are rerun. Retain unresolved UNKNOWN and record new conflicts
introduced by repair. Exact dependency-based recheck scope is still a design task.

## Roadmap (original tasks; Step 1 status is detailed below)

| ID | Task | Completion evidence required later |
| --- | --- | --- |
| V3-T01 | Define structured findings/violation contract | Scope, statuses and provenance tests |
| V3-T02 | Deterministic validators where evidence is sufficient | True conflict / unknown / pass fixtures |
| V3-T03 | Bound any necessary LLM-assisted semantic validation | Responsibility and evidence limits, no duplicated interpretation |
| V3-T04 | Coverage and distribution validation | Explicit rest and long REQUIRED exceptions |
| V3-T05 | Repetition and redundant-experience validation | Intentional revisit and subvenue counterexamples |
| V3-T06 | Opening/date-specific availability validation | Date/zone/exception/UNKNOWN fixtures |
| V3-T07 | Route, transition and cross-activity overlap validation | Directional evidence, buffers and missing-route cases |
| V3-T08 | Cost/budget validation | Currency, unit/party scope and incomplete coverage |
| V3-T09 | Visitor-suitability uncertainty handling | Public/private/unknown evidence without type blacklist |
| V3-T10 | Define targeted repair contract | Unaffected-field and requirement protection |
| V3-T11 | Bounded candidate reuse/additional acquisition | Identity, provenance, exclusion and cache accounting |
| V3-T12 | Limited repair model/prompt where needed | Segment scope and no full-draft replacement by default |
| V3-T13 | Repair budgets, cancellation and stop rules | Exhaustion/partial output/no hidden retries |
| V3-T14 | Re-validation and new-conflict detection | Repaired and global invariants |
| V3-T15 | Independent V3 runner/graph wiring | V0/V1/V2 mechanism isolation |
| V3-T16 | Prepare V2-draft versus V3-repaired evaluation | Separate future authorization; same shared checkpoint/evidence accounting |

## Current limits and checkpoint discipline

V2 acceptance does not mean every output is feasible. Below-target/empty days, repeated
or redundant visits, hours/route conflicts, visitor-access and price uncertainty and
generated contradictions remain possible. See [known issues](known_issues.md#first-draft-and-v3-boundary).
The new baseline supplies better first-draft objectives/capacity/observability only.
Record future shared changes and decide whether affected completed evaluations must
be rerun; never fix a shared bug only in V3 to manufacture a version advantage.

## Shared baseline update (2026-09-22)

Open-Meteo Weather and the 14-selectable-date/10-travel-day input boundary are shared V0/V1/V2
baseline changes (V0 still fetches no weather). This checkpoint is implemented + bounded
development-live-validated. Offline checks passed; the Tokyo smoke exercised the shared date
contract, and V1 and the separately authorized normal V2 run each obtained all five requested
weather fields for all ten trip dates with matching planner projection. The initial degraded
V2 attempt remains a separate historical result. See the
[Tokyo execution record](development_record.md#tokyo-weather-window-live-20260922) and
[Profile closeout](development_record.md#weather-date-closeout-profile-20260922).

This evidence does not guarantee future weather completeness, resolve itinerary-quality issues,
or constitute formal evaluation or re-freeze. Future V3 inherits this shared capability without
treating it as its contribution. V3 runtime and repair budget enforcement remain unimplemented.
No database reproduction/export work is included.

## Step 1 execution contract (2026-09-22)

This section supersedes the earlier undecided execution boundaries. Only the offline
report and validator are implemented in this step. The accepted mechanism remains:
V2 draft and existing checks -> snapshot -> deterministic findings -> bounded candidate
preparation -> at most one Repair LLM -> application acceptance and re-validation ->
one Nearby stage after the final primary itinerary. No global Semantic Evaluator.

### Implemented contracts and shared preconditions

`backend/app/versions/v3/models.py` defines `Finding`, `ImprovementTarget`,
`PlaceUseObservation`, `ValidationPolicy`, and `ValidationReport` (`v3_validation_1`).
`backend/app/versions/v3/validation.py::validate_draft` is a synchronous pure function
over the existing itinerary, interpreted contract, original supply IDs, Details,
named resolutions, effective evidence and optional route bundle. It accepts no client,
database handle, model, tracer or callback. It performs no acquisition or repair.

The caller supplies application-owned snapshots, not model-authored effective facts.
Inputs are not cryptographically authenticated; source refs are traceability, not proof
that an arbitrary caller is trustworthy. No alternative evidence extraction is added.
`validate_output_sources` runs on a detached primary-only copy, and its normalized
return is discarded. `validate_itinerary_dates` remains the shared date boundary.
Schema/source/date failures still raise shared errors, not new V3 findings. Nearby
references are ignored and do not satisfy REQUIRED or inflate counts. The original
business fields, order and private cost projection metadata remain untouched.

`observe_generation` supplies the existing canonical diagnostics unchanged. Counts,
duplicate occurrence and provider primary types are observations. No text matching
against preferences, names, notes, hours descriptions or model explanations is added.

| Result | Meaning |
| --- | --- |
| CONFIRMED | An evidence-backed conflict within an implemented check; only this status sets `is_violation=true` |
| NEEDS_REVIEW | A reviewable observation, not a confirmed violation |
| UNKNOWN | Unsupported or insufficient evidence; neither PASS nor FAIL |
| PASS | A narrowly scoped named identity inclusion check only; never whole-trip validity |

Improvement targets are separate references to findings. Default policy proposes only
confirmed conflicts. Explicit `ValidationPolicy.review_targets` may opt coverage,
repetition and opening review findings into improvement proposals without changing
their status. Targets authorize no edits and cannot waive requirements.

Implemented checks and conservative limits:

- Coverage: below/above default or unassessable days retain shared diagnostics; default
  misses are NEEDS_REVIEW. Same-day/unknown roles remain UNKNOWN. There is no executable
  rest/pace exception predicate in the current contract. A long REQUIRED visit, rest
  day or intentional revisit is never declared a violation merely from counts.
- Repetition: repeated main canonical IDs are NEEDS_REVIEW; intent and distinct-ID
  experience equivalence are not inferred. No automatic removal is authorized.
- Overlap: compare all scheduled interval pairs, including nested/cross-day pairs;
  positive interval intersection is CONFIRMED, touching endpoints are not conflicts.
  Cross-day mixed timezone awareness is UNKNOWN. Within-day mixed awareness is rejected
  by existing shared sorting before V3; this step neither bypasses nor changes it.
  Naive timestamps use the shared local schedule
  convention; there is no sub-party/concurrent-activity contract to establish exceptions.
- Named requirements: reuse canonical requirements and `NamedPlaceResolution` linked
  by search intent ID, exact supplied place text and source quote. REQUIRED omission
  and EXCLUDED scheduling are CONFIRMED only with an unambiguous resolved binding.
  Missing/inconsistent bindings are UNKNOWN; foreign requirement links are rejected.
  EXCLUDED lookup's existing OPTIONAL resolver role does not erase the canonical
  exclusion. PASS means identity presence/absence only, not the requested visit mode.
- Opening: consume resolver output only. Date-specific whole-venue closure or explicit
  daily time-window mismatch is NEEDS_REVIEW because `Activity` has no indoor/exterior
  visit-mode binding. Offset-aware times are converted through Details' IANA zone.
  Conflicting, partial, regular weekly, unparsed Places, scoped sub-area, missing zone,
  overnight or non-applicable evidence remains UNKNOWN. Matching hours do not prove
  admission. This step deliberately does not claim confirmed visit-access conflicts.
- Visitor suitability: record provider primary type separately; public access remains
  UNKNOWN. An office/service category proves neither a visitor attraction nor a ban.
  Offices, exterior viewing, public galleries and events cannot be distinguished by
  the current activity contract. Architecture preferences confer no access evidence.
- Routes: UNKNOWN in Step 1 because no per-leg planned mode/departure binding exists.
  Retain route source refs; direct, reverse-mirrored or representative evidence alone
  does not validate the scheduled leg. No new typed assertion of applicability is fabricated.
- Budget: UNKNOWN. Model estimated costs/private projection diagnostics are not verified
  party/unit/currency-scoped expenditure. The existing official amount evidence does
  not establish comprehensive party pricing or a sound aggregate lower bound.
- Open semantic requirements, prose contradictions, weather feasibility and visit-purpose
  equivalence remain unsupported/UNKNOWN. No new interpretation or semantic judge.

### Future repair acceptance (not implemented)

The application must check legal structure/identity, unchanged unauthorized fields,
REQUIRED/EXCLUDED protection, and no added or worsened confirmed hard conflict. At
least one authorized target must have a verifiable improvement. Reject no-op patches,
notes-only claims of success, role changes used to evade counts, lost evidence, and
CONFIRMED -> UNKNOWN downgrades presented as resolution. Preserve original findings
and evidence for comparison even if an activity is replaced. Recheck dependencies and
global invariants, not just targets the model says it fixed.

Visit-mode changes must be explicit and require rechecking linked requirements; exterior
viewing cannot satisfy an explicit indoor visit. A future visit-mode contract is required
before implementing those acceptance checks. Repair explanations are not independent
fact evidence. `REPAIRED` means accepted improvement under this round's targets and
applicable checks, never comprehensive trip correctness. No such status is emitted now.

### Future candidate ledgers and acquisition accounting (not implemented)

Use, in order: unused qualified original supply; qualified comparison-pool Details;
already discovered candidates requiring normal evidence acquisition; necessary bounded
new discovery. Every candidate must cross the existing canonical identity, exclusion,
Details and evidence boundaries before entering the application repair whitelist.

Keep three distinct records: immutable original supply ledger, repair allowed-identity
ledger with provenance, and actual final scheduled identities. New qualified IDs need
not belong to original K20. Future repair validation must use the repair ledger rather
than applying the original generation supply restriction to new legitimate identities.
This is not permission for model-created or arbitrary IDs.

Count separately: existing qualified candidate reuse; new canonical processing attempts;
actual Details sends; distinct candidates projected into Repair input; final scheduled
identities/visits. Each processing attempt consumes its attempt slot before work, even
if failed or duplicate. Repeated discovery hits do not become distinct candidates or
reset budgets; keep raw hit/attempt accounting. Cached qualified reuse does not consume
a network-send slot. Every actual Details dispatch counts, including failures. Reuse
is deduplicated by canonical ID; candidate input cap includes retained scheduled IDs.

New discovery reuses `DiscoveryIntent`, its requirement links and destination area,
targeting an actual gap. Do not reinterpret the entire request, rerun all initial
queries, infer queries from raw preference keywords or hide another model call in
"programmatic discovery". Returning old IDs is allowed; implicit retries are not.

### Future development ceilings (not active configuration)

| Resource | Ceiling |
| --- | --- |
| Repair rounds / Repair LLM calls | 1 / 1 |
| New Google discovery sends | 2, including at most 1 fallback |
| New RAG query / retrieval / Top-K | 1 / 1 / 10 |
| Query embedding | At most 1 batch, only when needed |
| New canonical processing attempts / Details sends | 8 / 8; failures count |
| Distinct Repair input candidates | 28 total, not 28 additional; original K20 plus at most 8 alternatives |
| New Reviews/Profile / Official Web | 0 / 0 |
| Additional Routes | 4 requests and 32 billable elements total, shared before and after Repair |
| Retries | 0 |
| Repair input engineering ceiling | 64,000 tokens, including system/user/schema and 2,048 framing reserve |
| Repair output ceiling | 16,384 tokens, matching current primary output protection |
| Single Repair model timeout | 90 seconds, further clamped by remaining phase/request time |
| Entire repair phase | 180 seconds |
| Weather / Nearby | Reuse Weather; once-only final Nearby stage with existing independent budget |

28 is a projection cap, not a supply enlargement or permission to acquire 28 places.
64k is a conservative development guard below the current primary 160k ceiling, not
a measured provider context limit or proof every repair fits. Bound each projected
candidate/evidence field, select only affected-day and protected-context dependencies,
and include only needed directional route pairs. Never serialize the full comparison
pool/matrix. If a faithful bounded projection cannot fit, skip Repair with an explicit
resource outcome; do not silently truncate constraints or evidence. These budgets do
not promise complete recovery of a severely under-filled ten-day draft.

The 180-second monotonic phase starts immediately after validated V2 draft/evidence
snapshot, before V3 findings and candidate preparation; it ends after acceptance and
re-validation, including any post-Repair Routes. It is nested within the existing
whole-request deadline and never extends it. Reserve the current Nearby stage's up to
10 seconds when computing the repair deadline: min(phase start + 180s, request deadline
- Nearby reserve). Exhausted time means skip/stop repair, not a fresh 180s allocation.
Nearby is still bounded by remaining request time and its own three-request/10-second
budget. A 600-second request remains explicit development-only authorization.
Propagate cancellation normally; never catch it as ordinary repair failure and continue
to tools/Nearby. A model timeout must not consume time reserved for required rechecks;
future integration must reserve/recompute that time before dispatch.

### Future route evidence after Repair (not implemented)

Prepare necessary pairs before Repair where useful. Once a patch is structurally
admissible, compute actual newly required directed adjacency pairs and acquire missing
applicable routes using the same 4-request/32-element ledger. This is not a second
Repair LLM. Count actual billable matrix elements and failed sends; cache reuse must
match direction, travel mode and temporal applicability. A mirrored reverse estimate
cannot silently replace a provider-observed forward leg. Representative departure
time is not automatically applicable to a different date/time, especially transit.
If scope is missing, evidence conflicts, or time/budget is exhausted, retain UNKNOWN;
do not declare route feasibility or route-target improvement. Initial feasibility uses
zero extra buffer only as an explicit minimum transition check; any positive comfort
buffer needs a separately documented policy and must not be invented from prose.

### Step 1 verification record

Final focused regression: **154 passed**, including **55 V3 tests**, in 5.66 seconds.
The command selected `backend/tests/versions/v3`, shared generation diagnostics/date/
official-evidence policy tests, `test_v1_itinerary.py`, V0/V1 graph tests and the V2
runner tests. No full-suite repeat was warranted by isolated, unconnected additions.
Ruff check/format passed for the added modules/tests; `git diff --check` passed.

The first run had 48 passing V3 cases and one failing test that expected mixed within-day
timezones to reach V3. Existing shared sorting instead raises TypeError. The test and
scope documentation were corrected; no shared behavior was bypassed. Initial Ruff
issues (default constructor and formatting) were corrected before the final run.

Tests explicitly guard socket connect (including loopback), HTTP sends, OpenAI chat and
embedding calls, and sync/async PostgreSQL connections while exercising validation.
They compare complete itinerary JSON, activity order and private cost projections before
and after. Other cases cover canonical bindings, exclusion lookup provenance, Nearby,
long REQUIRED/rest/revisit non-violations, structured-hours scopes and cancellation
propagation. No actual external call, database acquisition or live run occurred.

Current sizing uses
the actual primary prompt/DTO serializer and cached offline o200k tokenizer on synthetic
3-day/K12 and 10-day/K20 fixtures. This is a shared serialization reference only: the
Repair DTO, prompt and serializer do not exist, and final Repair payload acceptance is
explicitly **not established**. The 28-candidate/64k design must be checked again using
the real bounded Repair projection before model integration.

| Synthetic primary fixture | System | User | DTO schema | Framing | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| 3 days / K12 / 80 preference characters | 1,180 | 39,317 | 792 | 2,048 | 43,337 |
| 10 days / K20 / 80 preference characters | 1,180 | 102,110 | 792 | 2,048 | 106,130 |
| 10 days / K20 / 24,000 preference characters | 1,180 | 127,968 | 792 | 2,048 | 131,988 |

All fit the current 160k primary ceiling; the latter two exceed the proposed 64k Repair
ceiling. This supports bounded projection rather than copying the primary payload.
These are fabricated development fixtures, not live captures or worst-case proofs.
Reproduce without credentials/captures by loading `config/runtime.yaml`, calling
`tools.diagnostics.itinerary_payload.fixtures(days, K, long_text)` for `(3,12,False)`,
`(10,20,False)`, `(10,20,True)`, then `measure(ITINERARY_GENERATION_SYSTEM_PROMPT, prompt,
config.main_generation, metadata)` outside pytest (whose tokenizer fixture is mocked).
The real offline tokenizer fails rather than fetching a missing vocabulary.

T01 is implemented; T02/T04-T09 are partially supported with the limits above. T03 does
not authorize a Semantic Evaluator. T10-T15 remain future work. T16 needs separate
formal-evaluation authorization. No V3 milestone completion or freeze is claimed.

## Step 2 standalone repair checkpoint

The subsequently approved Step 2 is implemented without graph/runner/runtime assembly.
The following describes actual behavior, superseding the earlier planned implementation
statuses and the Step 1-only route limitations where explicit bindings now exist.

### Contracts, modules and responsibilities

All new runtime modules live under `backend/app/versions/v3/`:

| Module | Implemented responsibility |
| --- | --- |
| `repair_models.py` | RepairScope, ActivityPermission, RepairEdit/Patch, RepairCandidate, TransitionBinding, ValidationContext, TargetProgress and RepairResult |
| `repair_acceptance.py` | Shared validation invocation, operation authorization, detached patch application, stable finding comparison and acceptance |
| `repair_projection.py` | Actual strict FoundryRepairPatchDTO, Repair prompt, serializer, candidate/field limits and token preflight |
| `repair_candidates.py` | Original supply and qualified comparison reuse, normal Details qualification, bounded Google discovery and optional RAG adapter |
| `repair_budget.py` | Independent repair counters, request-cache reuse, send accounting, local stops and phase deadline |
| `repair_routes.py` | Explicit transition bindings, directed evidence applicability and necessary route requests |
| `repair_service.py` | Injected `run_repair_once`; no clients, graph, Nearby or runtime factories are created |

`validation.py` remains the single validator. Optional route evidence/bindings add scoped
route findings with `magnitude` (transfer deficit seconds); absent/partial bindings retain
UNKNOWN. Step 1 calls remain compatible. Shared schema/source/date checks are unchanged.

The shared Foundry client adds only `generate_repair_structured`, using the new DTO and
per-call 16,384 output ceiling. Primary methods/options are unchanged. GoogleRoutesProvider
exposes its existing transport send-boundary capability through a property; its HTTP
request, normalization and existing V1/V2 budget path are unchanged.

### Operation scope and result semantics

Application-owned scope explicitly permits retime, replace, delete and/or additions by
date, and separately permits duration changes. Being on an editable date is insufficient
to authorize deletion. Existing activities keep IDs, roles, names, notes and costs during
retiming. Replacements are restricted to non-REQUIRED main visits and qualified identities;
the application constructs their fields, retaining old evidence in the original snapshot.
REQUIRED deletion/replacement and EXCLUDED additions are rejected. New IDs are allocated
by the application. Cross-day edits, arbitrary notes/role edits and visit-mode changes
are not supported. No minimum visit duration or preference-keyword rules are introduced.

Patch output is at most 50 explicit edits. Draft projection supports at most 120 existing
activities; both are engineering guards, not promises of full-trip repair. Unaffected
activities and original array positions are preserved; changed chronological ordering is
expressed by timestamps. Cost-projection paths are remapped for retained costs after
authorized removal. Original private projections remain on the preserved snapshot.

Report states are SKIPPED, REJECTED, ACCEPTED_PARTIAL and ACCEPTED_COMPLETE. The last two
mean the patch was accepted; COMPLETE means all *authorized targets* resolved, not a
fully verified trip. Other confirmed findings and UNKNOWN can remain in proposed_report.
Each target independently records resolved, improved, unresolved or unknown, with before/
after measures. A 1,800 -> 600 second overlap is improved and remains CONFIRMED.

Comparison uses check/scope/activity/requirement identities rather than sequential
finding_id equality. Measurable targets currently include overlap, bound named identity,
coverage distance from the default 2-5 range, and supported route deficit. Repetition and
opening-review semantics are not independently credited as arrangement improvement.
No-op/evidence-only gains cannot qualify. Existing confirmed evidence cannot be weakened
during baseline reassessment or downgraded to uncertainty in the proposed result. New or
worsened confirmed conflicts reject the patch. At least one target must measurably improve.

Authorized deletions/replacements record lost original main visits. Reduced distinct daily
coverage is rejected unless scope explicitly allows it, and is always recorded when
accepted. Improving an authorized default-count target is a default-target improvement,
not proof of visitor suitability. Generic/transport/free-time roles cannot inflate counts.

The result preserves original_report, separately records reassessed_original_report using
augmented evidence, and records proposed_report. It also retains acquired routes, original
supply IDs, repair whitelist/provenance, final arranged IDs, losses, counters and local stops.
Rejected proposals never replace the final itinerary. Invalid caller snapshots remain
shared validation precondition errors; ordinary failures inside repair return the snapshot.

### Candidate preparation and local stopping

No additions/replacements permitted means no candidate acquisition is needed. Existing
primary supply remains application-trusted; comparison-pool and newly acquired candidates
must pass normal `evaluate_poi_eligibility` with Details, identity, exclusion and opening-date
consistency boundaries. Normal eligibility does not prove public visitor access.

Reuse precedes new processing. New Details use existing normalization/cache keys. Google
queries select at most two existing DiscoveryIntents, with destination/location scope.
Optional RAG consumes one existing intent, one batch, one search with Top-K 10, and reuses
the existing Google-backed TripWorld identity resolver/attachment logic; it does not call
the initial `extend()` pipeline or reinterpret preferences. The RAG port must already be
prepared by a future caller; runtime creation/preparation/lifecycle are deliberately not
assembled here. There is no new Reviews/Profile or Official Web acquisition.

Caps remain Google2 (fallback1 included), embedding batch1, retrieval1, canonical attempts8,
Details sends8 and distinct Repair input candidates28. Existing qualified reuse, canonical
attempts, actual Details sends, raw/duplicate discovery hits, cache hits, projected candidates
and final arranged identities/main visits are separate counters. Repeated failed request
keys cannot retry. Existing compatible request-cache wrappers are retained.

Place/Routes production adapters expose the actual transport send hook: failures before
send do not consume sends, while sent failures do. Non-observing fixture/port dispatch is
conservatively counted as an attempt, not advertised as observed HTTP transmission. RAG
embedding/retrieval caps apply to port invocations; their runtime performs no hidden retry.

Exhausting or failing one optional acquisition category stops that work only. The service
still repairs using retained material where possible. It does not require a new candidate
for retiming and does not interpret unavailable evidence as feasible to continue.

### Route and time boundaries

Transitions require explicit application mode plus activity endpoints and departure time;
no mode is extracted from notes. Direction, mode, routing preference, directly observed
available duration and exact departure applicability must match. Conflicting durations,
mirrored reverse estimates, missing bindings and mismatched representative departure remain
UNKNOWN. Additional requests currently use directed one-origin/one-destination matrices;
they do not automatically batch a full comparison matrix. The common ledger enforces both
4 requests and 32 billable elements, with atomic accounting of matrix Cartesian products.

TRANSIT/DRIVE requests can supply explicit departure. The current repair adapter does not
send new WALK matrices because it does not establish a provider-supported temporal binding
for them; ordinary undated WALK baseline evidence remains UNKNOWN. This is a stated limit,
not a claim that walking cannot be feasible. No route-missing case becomes PASS by default.
Existing explicit compatible evidence can be evaluated without acquisition.

Only structurally/operationally legal patches reach post-patch route acquisition. New
adjacencies/departures use the same pre/post ledger. Both original and proposed arrangements
are assessed on accumulated evidence. Route fetch success itself is not repair success.

The service requires an explicit absolute monotonic request deadline. The 180-second phase
starts on entry before initial validation/snapshot work and ends after acceptance/rechecks;
its deadline is min(start+180, request deadline-10). Optional preparation is bounded earlier
to reserve up to 90 seconds for the one model call plus 20 seconds for rechecks. If less
time is available, optional I/O stops first; model timeout is min(90, remaining-20).
Post-patch I/O leaves at least one second for synchronous final checking, followed by a
deadline check before acceptance. These are scheduling guards, not latency guarantees.
No missing deadline is silently replaced with a 600-second development allowance.

Input overflow, no measurable improvement, invalid model output, deadline exhaustion and
acceptance failure preserve the initial draft, with explicit result reasons. Calls do not
retry. CancelledError propagates, including after a send; it cannot produce a normal
fallback followed by more work. Nearby remains outside this service and its reserved
budget never extends the caller's request deadline.

### Actual Repair payload sizing

Reproduce with `.venv/Scripts/python.exe -m tools.diagnostics.repair_payload`. This uses the
actual Repair system/user serializer and actual output DTO JSON schema with the cached real
offline o200k tokenizer, outside pytest's mocked tokenizer fixture. It creates no clients.

| Synthetic fixture | System | User | Schema | Framing | Total | Outcome |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 day / 3 candidates | 133 | 1,185 | 322 | 2,048 | 3,688 | Fits |
| 10 days / 28 candidates, minimal evidence | 133 | 8,314 | 322 | 2,048 | 10,817 | Fits |
| 10 days / 28 candidates, adversarial long fields | 133 | 115,642 | 322 | 2,048 | 118,145 | Rejected before model |
| 10 days / 28 candidates, 24 requirements and conflicting hours | 133 | 74,202 | 322 | 2,048 | 76,705 | Rejected before model |

The 50-edit synthetic DTO output serializes to 2,956 tokens. This is an output-size example,
not a completion guarantee within 16,384 tokens. Candidate objects are bounded to 12,000
serialized characters; excess fields/evidence/requirements are never silently truncated.
Only affected-date directed adjacency elements are projected, even if given a full matrix.
Complex valid evidence can exceed 64k; current behavior is an explicit skip retaining the
draft, not raising the limit or discarding evidence. These fixtures do not establish a
universal sufficient budget or live model/provider compatibility. The earlier primary
payload measurements remain a separate historical reference, not Repair acceptance.

### Offline execution record (actual order)

1. Initial implementation Ruff check found 31 unused-import/style/default issues. Corrections
   and formatting passed; the existing Step 1 V3 tests passed **55/55** (2.77s).
2. First new repair tests passed **32/32** (2.57s), covering operation scope, local acquisition
   exhaustion, partial acceptance, whitelist additions and route applicability.
3. Initial real sizing produced 3,688/10,817 tokens and rejected the long-field sample. Later
   sizing exposed the rejected sample's actual 118,145 count. Test/tool formatting issues
   were corrected during these additions; no runtime behavior was changed to fit a sample.
4. Expanded repair tests passed **45/45** (2.62s), adding deadline, send accounting,
   cancellation, RAG mock resolution, post-patch Routes and evidence-only rejection.
5. First affected regression: **164 passed, 1 failed**, 2 warnings (7.21s). The new strict
   no-network test blocked Windows asyncio's event-loop-initialization socketpair before
   repair ran, producing cleanup/unawaited-coroutine warnings. The test now starts the loop
   first, then blocks all connects (including loopback), HTTP and DB access during repair.
6. Corrected guard test passed **1/1** (3.10s). Ruff passed. The affected regression then
   passed **165/165** (4.88s), including V3, Foundry client/V1 itinerary, Google adapters,
   request cache/budget and TripWorld discovery tests, without those warnings.
7. Added explicit UNKNOWN for unbound legs and direct serializer matrix filtering. V3 tests
   passed **104/104** (4.69s). The enriched sizing harness initially stopped on the expected
   overflow instead of reporting it; its reporting handler was corrected, preserving the
   runtime rejection. Final real sizing records all four outcomes above. Ruff and tracked
   `git diff --check` passed. No formal evaluation or full-suite mechanical rerun occurred.

All model/provider/embedding/retrieval operations in tests use mocks or fixtures. No live
service, database acquisition/reproduction, Weather, SQL or primary-generation budget change.
No staging, commit, push, thesis archive update, version freeze or V3 milestone completion.
Next approval is required for independent V3 graph/runner wiring, runtime instance lifecycle,
final-primary Nearby placement and subsequently a separately authorized bounded live run.


## Step 3: independent offline integration checkpoint

Implemented under separate authorization after acceptance of Steps 1/2. No V3 live,
database startup/reproduction, formal evaluation, vector/artifact change or freeze.

### Entry and adopted output

`scripts/run_v3.py` dispatches `versions/v3/runner.py::run_v3`. The shared tools graph
has a default-off `post_primary` hook, optional state schema and reference node. V3
uses those hooks in `versions/v3/graph.py`; it does not call `run_v2`, duplicate its
nodes, regenerate the draft, reinterpret preferences or repeat initial discovery.
Existing clarification, no-candidate, identity/date and generation failure exits remain
before V3. A legal primary draft is required before validation, repair or Nearby.

`V3State` adds `v3_outcome`. `V3PlanningResult.v3` records the detached draft, original
ValidationReport, effective quantity policy and operation scope, optional RepairResult,
adopted primary, final report, final allowed identity IDs/Details and original/final cost
projection records. RepairResult still distinguishes original findings, augmented-evidence
draft reassessment, proposed findings and partial/complete target progress. Rejected
proposed findings never become the final report. Final checks run the same validator
against the adopted arrangement and accumulated compatible evidence.

The original `planning_supply` is unchanged. Final source validation uses the union of
original supply identities and application-qualified repair candidates, not arbitrary
model IDs. The repair whitelist and actual final scheduled set remain separately visible.
The common source normalizer retains canonical names, chronological ordering and remapped
cost paths on the adopted copy. `generation_diagnostics`, output role summary and final
cost associations refer to that adopted output. The original report/diagnostics, original
cost records and initial RAG fate snapshot remain historical observations. RAG's final
fate describes original discovery origins against the adopted output; repair-only origins
are recorded in the repair whitelist rather than fabricated into initial discovery.

Final identity/date validation happens before Nearby. One Nearby service invocation uses
the final primary's actual scheduled identities and coordinates, with the existing own
request budget (up to three sends). Its returned references have a separate ledger. After
attachment, only reference identity/projection checks and primary/cost invariance run;
there is no second primary generation, repair or source normalization. References cannot
satisfy REQUIRED, change primary counts or become planned expenses.

### Effective operation policy

`wiring.py::operation_scope` consumes existing findings; no text/keyword interpretation
or new visitor/cost validator is introduced:

- Confirmed overlaps authorize retiming of the implicated activities, preserving duration.
- Canonically resolved REQUIRED omissions authorize additions on available itinerary dates.
- Explicit resolved EXCLUDED conflicts authorize deleting only those visits, with the
  existing visit-loss and coverage-regression records. This does not bypass initial source
  filtering: a model identity already rejected by the primary boundary never reaches repair.
- `quantity_review_enabled=False` is the API default. CLI opt-in is
  `--repair-quantity-review`. The effective value is retained in the outcome and policy
  trace. When enabled, below-target dates may authorize additions; overfull dates do not
  gain deletion rights. Counts remain NEEDS_REVIEW, not confirmed violations.
- Repetition, opening doubts, public access UNKNOWN and route-only uncertainty do not
  grant additional operations. No replacements, duration changes or general deletions
  are automatically authorized by this first wiring policy.

No authorized scope means no Repair model call. Candidate preparation can reuse supply,
qualified comparison candidates and admitted candidates still needing normal Details.
Only quantity shortages select at most two existing discovery intents; REQUIRED-only
additions do not start unrelated discovery. No new natural-language query interpreter.
Per-leg bindings use the existing structured transport decision as an explicit uniform
application policy, never activity notes. Only already supported exact direction/mode/
departure evidence applies. TRANSIT/DRIVE necessary route requests share the existing
4-request/32-element pre/post ledger; WALK acquisition remains unsupported. Route-only
findings remain visible even when this narrow operation policy grants no repair target.

### Request lifecycle and shared correctness fixes

One explicit `development_timeout_seconds` (positive, at most the configured 600 ceiling)
is mandatory for V3. The absolute monotonic deadline starts at the async request entry;
the CLI supplies its earlier entry timestamp, including local dependency preparation.
The outer request timeout and borrowed client `DeadlinePort` guards share that same deadline.
No graph or repair entry grants a new whole-request allowance. Expiry prevents further
provider/model work; cancellation propagates, including LangGraph's wrapped node cancellation.
Resource cleanup still runs. An exhausted request is not converted to a successful fallback
followed by Nearby. A local repair skip/failure can retain the draft and run permitted
post-work only while whole-request time remains. Repair input overflow remains a repair
result, never `invalid_planning_input`.

Repair keeps its existing min(start+180, request deadline-10) stage boundary, 90-second
maximum model wait, early optional-I/O stop and recheck reserve. Nearby's independent
10-second phase is clipped to the remaining request time. Candidate 28, input 64k, output
16,384, single model call and all acquisition limits are unchanged; no retries or enlarged
first-generation budgets are added.

`resources.py::RequestRetrieval` lazily enters/prepares a factory-created runtime once.
Initial TripWorld discovery borrows it; its context exit no longer closes the request's
resource. Repair borrows the same prepared runtime, cached vectors, raw clients and
compatible evidence. RuntimeRetrieval retains per-operation config, not discovery's
`ends` deadline; Repair uses its own stage limits. Phase-tagged operation records and
copied initial diagnostics prevent later work rewriting initial observations.
Initialization failure blocks restart. Failed embedding texts and failed retrieval vector/
region keys persist across phases, including attempts to change Top-K. RAG query text
normalization matches the initial query planner. Successful retrieval cache keys retain
Top-K as before. Shared RequestCache provider attempts, including prior pre-send failures,
block same-key Repair retries without pretending that unsent attempts consumed send budget.
Optional failure/exhaustion still permits improvement with retained candidates/material.

The owner closes factory-created resources once after planning, errors or cancellation.
Externally injected `retrieval_runtime` and client ports remain caller-owned. Cleanup errors
are recorded without hiding cancellation. Google/Weather HTTP and page transport clients
retain their per-call context-managed lifetimes.

Two narrow shared ownership corrections are baseline fixes, not V3 mechanism contributions:
RuntimeRetrieval reuses its embedding SDK client/hooks across repeated calls (V2/V3 adapter),
and the common V1/V2/V3 CLI closes only its own Foundry/Web/reasoner adapters, including
partial dependency assembly failure. Supplied adapters are not recreated or closed. Primary
client defaults, prompts, K, tool budgets, Weather and SQL are unchanged. V0 stays tool-free,
V1 initializes no RAG, V2 executes no Repair, and product/developer defaults remain V0.

### Step 3 offline execution record (actual order)

1. Initial static check found two line-length issues; formatting corrected them. First
   integration run: **12 passed, 4 failed, 1 warning (7.00s)**. Fixture supply count was
   wrongly assumed to be 10 rather than 9; the new-identity fixture had no out-of-supply
   candidate; notes used a list instead of a string; and LangGraph wrapped a dependency's
   CancelledError. Fixtures were corrected and V3 restored caller-facing cancellation.
2. Second integration run: **15 passed, 1 failed (3.72s)**. The larger pool changed which
   identities were supplied, so the fake primary had an invalid identity. The fake model
   now chooses from its actual input supply. New-identity targeted rerun: **1 passed (2.74s)**.
3. Wiring plus initial lifecycle tests: **22 passed (4.70s)**. Intermediate Ruff checks
   found import-order/line-length issues during additions; these were corrected by formatting.
4. Expanded wiring/lifecycle run: **31 passed, 1 failed (5.31s)**. The Nearby response fixture
   omitted required provider_rank; provider failure was correctly kept optional. Corrected
   attachment, strict no-network and lifecycle targeted run: **11 passed (3.48s)**.
5. Affected regression: **290 passed (6.91s)**. Scope: new wiring/resources, affected standalone
   repair, V1/V2 versions, V0 graph, Nearby/TripWorld services, runtime/cache, Foundry adapters,
   planning service and product API. No full repository suite or live calls.
6. Final ownership audit added partial CLI-assembly cleanup and explicit scope-policy tests.
   Targeted lifecycle/policy/V3 CLI/V1 runner regression: **18 passed (3.51s)**.
7. Added actual TRANSIT pre/post route wiring cases. Initial **2 failed (4.84s)** before
   execution because the fixture used preferred_mode instead of the real mode field.
   Corrected targeted rerun: **2 passed (3.80s)**. Success uses two necessary directed
   elements at different departure times; optional failure retains route UNKNOWN while
   accepting independently verifiable overlap improvement. Initial/reassessed/final reports
   are checked separately.
8. Final new wiring/lifecycle/policy suite: **43 passed (4.27s)**. Ruff passed on all
   changed Python modules/tests; `git diff --check` passed. The290-test affected regression
   was not mechanically repeated after the targeted CLI ownership fix. All acquisition
   boundaries used fixtures/mocks; the actual V3 chain also passed strict HTTP/socket/DB
   blocking after Windows event-loop creation. No live service was contacted.

The Step 2 real serializer/sizing results above are unchanged and were not rerun: no Repair
DTO, prompt, schema or input ceiling was expanded. Mock tokenizer integration tests prove
control flow, not real token sufficiency. No primary-payload sizing is relabeled as Repair
acceptance. The long/conflicting-evidence stress samples remain legitimate overflow skips.

Before any separately authorized live: verify credentials/deployment strict-output support,
explicit whole-request allowance and trusted reference date, retained corpus compatibility,
read-only DB/embedding prerequisites, provider availability and effective quantity policy.
This checkpoint does not start a database or verify those live conditions. Indoor/exterior
access semantics, complete verified costs, new WALK evidence and universal repair coverage
remain unsupported. Live validation and any formal evaluation need separate authorization.


## Targeted addition candidate revision (2026-09-22)

Implemented and offline-validated only. This local revision does not establish the complete
cause of the historical seven-day REJECTED result. The accepted three-day observation exercised
no Repair; the separate seven-day observation exercised a real model return, proposal checking,
rejection and fallback, not successful acceptance. Both historical captures remain unchanged.
No live or provider/database request was performed for this revision.

### Contracts and execution

`CandidatePreparation` separates the application identity ledger from presented candidates,
target/date/operation authorizations and selection decisions. `RepairScope.revisits` defaults
empty and refers only to already scheduled identities and authorized addition dates. Automatic
quantity policy does not grant revisits. No cross-day moving capability was added.

`repair_input_2` sends compact protected activities (including names, identities and schedule),
editable activities, `addition_candidates`, and `other_operation_candidates`. It does not send
the full ledger. All original scheduled identities count toward the unchanged 28-distinct-ID
union, together with presented operation candidates. More than 28 protected identities fails
closed before a model call; protection is not truncated. The existing 120-activity, per-object,
64000 input and 16384 output ceilings remain. REQUIRED options cannot be displaced by exploration.

An add operation must satisfy the legal ledger, actual input membership, target/date candidate
authorization and scope. Scheduled identities are not addition options without an explicit
revisit authorization. Duplicate additions of an identity across targets are rejected unless
that revisit is explicitly authorized. Other retime/replace/delete permissions remain separate.

### Preparation policy

1. Lock the original itinerary and identify scheduled identities.
2. Inspect unused original supply and qualified comparison-pool candidates with the same factual
   gate used for new candidates. Record pending Details separately from ineligibility. Target-date
   future-opening conflicts use existing structured Places opening-date evidence and are local
   to that date. Office type, name keywords and model explanations never establish access facts.
3. For each authorized quantity deficit, use two distinct alternatives as a preparation reference.
   A bipartite matching calculation prevents a candidate associated with several dates from
   counting as several independent options. Associations themselves remain available for all
   eligible dates; the preparation calculation does not lock a candidate to one day.
4. Exploration is justified by an alternatives shortfall or missing place-specific applicable
   hours across the target's options. Provider weekly/datetime hours presence is a material
   indicator, not verified visit feasibility. Capability-only visitor access, costs or WALK
   UNKNOWN never triggers exploration. Unknown options remain eligible.
5. Complete bounded pending Details work first, then recompute material sufficiency. Where new
   discovery is available, retain up to two of the existing eight canonical/Details attempts
   for discovery (at most six old pending attempts). This is a subdivision, not extra budget.
   Acquiring Details for an old discovered identity does not count as new-discovery exploration.
6. If still needed, use existing intents with the existing Google and RAG adapters. Scheduled,
   EXCLUDED and known target-ineligible identities are filtered when known, including after
   fallback canonical selection and before unnecessary Details. Request cache and terminal
   failure state are reused; no stage-based retry opportunity is introduced.
7. Reserve at most two input opportunities for the entire round, not per day/deficit. Qualified
   new results can take those positions; empty discovery backfills with old candidates. This is
   an exploration opportunity, not a source score bonus. Other selection considers distinct
   target opportunity coverage, applicable-hours presence, existing intent links, target links
   and stable ID ties under the same rules for old and new candidates.
8. Stop acquisition when old materials suffice, there is no input opportunity, local budgets/time
   expire, or bounded exploration has supplied its reserved opportunities and reached the
   preparation reference or full input capacity. Do not consume budget simply to fill it.
   No second exploration/Repair cycle exists. Fewer than two alternatives does not block an
   otherwise usable single Repair attempt. The single model call occurs after preparation.

The current revision does not decide public visitor access, execute arbitrary date-opening
semantics, prove budget coverage, or acquire temporally verified WALK routes. Evidence strengths
and UNKNOWN stay visible. A candidate need not satisfy every soft preference of the whole trip.

### Comparison, audit and statistics

`compare()` returns `RepairComparison` before the service decides acceptance. Existing identity,
protected-content and confirmed-conflict guards remain. No improvement still rejects, while
progress and business values (including distinct-POI before/after and deficit before/after)
survive rejection. Parsed patch and successfully merged proposal are stored in `RepairResult`;
invalid/missing outputs are explicitly not parsed/not constructed, never reconstructed.

Separate `v3_repair_scope`, `candidates`, `patch`, `proposal`, `comparison` and `decision` events
use the existing redactor and configured size ceiling. Oversized artifact content is omitted
with explicit truncation/byte-count status; the enclosing v3_finalized event also has a visible
size marker rather than duplicating an unbounded payload. Raw provider responses and internal
reasoning remain disabled. Audit redaction affects saved proposal copies, not business drafts.

Identity validation still accepts the application-managed union. Generation diagnostics use
that union to count actual primary activities, but original `unused_supply` and
`scheduled_unique_supply` retain the original planning_supply denominator. Independent counters
record Repair input unused candidates and original supply unused identities. Ledger growth is
not an arrangement improvement and never changes the original supply record.

### Offline execution record (chronological)

1. First V3 regression: 137 passed, 10 failed. Failures included a new-conflict comparison
   continuing with a missing baseline, old exception/DTO assertions, and old mixed-candidate
   fixture consumers. Corrected the comparison control flow and migrated affected fixtures.
2. Targeted repair/wiring regression: 74 passed, 4 failed. Remaining assertions expected the
   former unconditional RAG acquisition despite sufficient old materials.
3. First Ruff check: 37 import/line-format findings; corrected formatting/imports.
4. Added candidate regression cases: 80 passed, 9 failed. New fixture intents violated the
   actual contract; multi-day scope fixtures omitted dates; one old cache expectation remained.
5. Fixture corrections: 88 passed, 1 failed. Remaining assertion compared different itinerary
   Python subclasses rather than equal business data; corrected to compare model dumps.
6. Targeted repair/wiring regression: 89 passed.
7. Actual revised serializer sizing completed offline; results are below.
8. Expanded checks found one import-order issue; corrected it.
9. V3 plus affected generation diagnostics, trip dates and trace regression: 198 passed.
10. Distinguished old pending Details from new discovery and added a bounded-reserve test:
    repair service regression 67 passed; Ruff passed.
11. Wiring/operation policy regression: 32 passed; git diff --check passed.
12. Added enclosing trace size markers and narrowed explicit revisit identities: wiring
    regression 30 passed. Targeted actual trace-marker/revisit checks then passed 2 tests.

All model, HTTP, embedding and database collaborators in tests use mocks/fixtures. Existing
service no-network guards and cancellation/budget checks remain in the selected regression.
No full-repository rerun, live, SQL/database reproduction, vector changes or formal evaluation.

### Actual Repair sizing

Measured with the revised DTO, prompt, strict patch schema, serializer and local checksum-checked
o200k tokenizer. Every case has system=164, schema=322 and framing=2048 tokens. Component counts
below tokenize separate JSON projections; they need not add exactly to the user message count.
These are engineering measurements, not provider usage or a model completion guarantee.

| Synthetic case | Identity union | Options | Context | Candidates | Evidence | Requirements/findings | User | Total | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Retime only | 2 | 0 | 264 | 10 | 9 | 484 | 771 | 3305 | fits |
| One addition date | 28 | 27 | 133 | 5816 | 9 | 468 | 6430 | 8964 | fits |
| Three addition dates | 28 | 25 | 307 | 8786 | 9 | 803 | 9909 | 12443 | fits |
| Ten-day other operations | 28 | 28 | 2257 | 5891 | 9 | 2135 | 10296 | 12830 | fits |
| Long text | 28 | 28 | 46977 | 68499 | 9 | 2135 | 117624 | 120158 | rejected |
| 24 requirements/conflicting hours | 28 | 28 | 2257 | 5891 | 63234 | 4798 | 76184 | 78718 | rejected |

The 50-edit synthetic patch is 2956 tokens. Neither pressure case was made to fit by deleting
protected information or enlarging ceilings. Primary-generation sizing is not Repair acceptance.

This revision needs separately authorized live observation. It does not prove that the historical
seven-day proposal would now be accepted or that a future accepted addition improves overall
quality or satisfies the user's relaxed intent. No commit, push, freeze or next stage is implied.


## Bounded feedback rounds and spatial policy (2026-09-22)

Status: implemented and offline-validated. This supersedes the single-call development limit
for the current implementation, not the historical three-day/seven-day live records. No new
live/provider/model/database run was executed. This does not establish the complete cause or
resolution of the historical seven-day REJECTED result, quality improvement or a benchmark.

### Implementation and configuration ownership

`runtime.config_models.V3RepairConfig` parses the new `v3_repair` group in the existing
`config/runtime.yaml`. Nested acquisition/timing/input/spatial objects are immutable, strict,
finite and range/relationship validated; they do not carry independent numeric defaults.
`config/README.md` documents all 118 YAML leaf paths and current values, applicability, counts,
zero behavior, bounds, CLI overrides and loading. A documentation test checks every path/value.
Existing versions keep their configuration values and execution paths; no product-default,
primary prompt, K, supply, Weather, calendar or SQL change accompanies this work.

`runner.run_v3` resolves quantity-review YAML/explicit Boolean CLI override once and propagates
the effective runtime snapshot. It records source, base/effective hashes, review provenance,
entry deadline and the existing Nearby reservation. Both `--repair-quantity-review` and
`--no-repair-quantity-review` are supported; absence preserves the YAML false default. The
explicit development timeout remains mandatory for V3 and never starts again inside graph.
`wiring.V3PostPrimary` calls `run_repair_stage` at the existing post-primary hook. Primary work
is not repeated and Nearby still executes only after the final adopted output is validated.

`repair_service.run_repair_stage` owns one `RepairBudget`, immutable stage-original itinerary,
original findings/targets, growing identity/evidence context and latest adopted itinerary.
`run_repair_once` remains its injected round operation. `RepairResult.rounds` holds each
input/adopted itinerary, scope, candidates, patch/proposal/comparison, target links, usage,
cumulative counters, timing and continuation reason. Original targets are linked by existing
finding business keys, not transient enumeration IDs. Activity IDs contain the stage round.
The stage result includes `adopted_report`; a final rejected proposal remains a proposal only.

`repair_candidates` retains the context/options/ledger separation and original-supply statistics.
It reclassifies accepted additions as scheduled context each round. The same fact/authorization
rules apply to old/new options. Geographic filtering is target-scoped; search-known clearly
out-of-range additions can stop before Details. Existing target anchors bias bounded discovery;
coordinate-compatible candidate-pair/date associations are projected for blank-day grouping.
The first available target anchor currently determines the RAG region; this is not a complete
multi-region optimization. No anchor/hotel is invented for a blank day. The selected candidate
pair projection is bounded by the actual 28-ID input, not the complete comparison pool.

`repair_projection` still serializes `repair_input_2`, actual strict DTO schema, necessary
protected context/coordinates, scoped candidates and only the latest compact business feedback.
`repair_acceptance` retains atomic application and existing comparison semantics.
`repair_spatial` adds application layout/compactness assessment alongside that same validator;
its policy rejection is not a new CONFIRMED visitor-access fact or a second semantic evaluator.
The Azure Foundry Repair-only method receives per-call output tokens and an additive usage
callback. Primary client defaults are unchanged. Actual per-round callback values are summed
without adding them again to an outer callback total; unavailable usage stays explicit.
No new shared correctness bug/fix is claimed. Earlier shared client-lifecycle corrections
remain separately attributed to all affected versions.

### Effective iteration and acquisition policy

Defaults are at most three rounds and three total model calls, one call per round. First-round
no improvement permits a different feedback-conditioned arrangement with existing options.
An unchanged failed patch stops further iterations; identical effective serialized inputs are
not sent. Invalid/unreturned model output and provider-level model failure stop without retry.
Partial acceptance advances the adopted itinerary; later failure, rejection, input overflow or
phase exhaustion preserves that adoption. Scopes only narrow the original permissions and
remaining target associations. Newly added activities receive no automatic retime/delete rights.
Completed target permissions do not silently reopen. No executable candidate operation means
no model call; unsupported explicit transport cannot silently become WALK/default addition.

Two alternatives per quantity gap remain a preparation reference, not an eligibility or
acceptance requirement. Two exploration positions are reused inside each input union without
increasing stage tool allowances. Missing general hours/access/cost facts do not automatically
trigger discovery. Actual alternative shortages or concrete previous arrangement feedback may
justify bounded exploration. No presentation opportunity and no useful acquisition purpose
stops that work. Feedback exploration is not restarted just because UNKNOWN remains. Reuse,
unknown facts, capacity omission and applicable exclusion continue to be distinct audit states.

Stage totals remain Google 2 (including fallback 1), embedding 1 batch, retrieval 1 with Top-K10,
canonical 8 processing attempts, Details 8 sends, Routes 4 requests/32 requested elements.
Reviews/Profile/Official Web additions remain unsupported. Successful cache reuse costs no new
send allowance; terminal failures and canonical attempts survive rounds. Phase/round names do
not create retry keys. Local budget exhaustion does not terminate other feasible repair work.

### Time and spatial evidence

Defaults: stage 300 seconds; round cap 120; model cap 70; optional preparation cap 30; model
startup minimum 30; recheck reserve 20; affordable-round reference 60; finalization reserve 1.
The existing Nearby `reference_discovery.deadline_seconds` supplies its reservation (currently
10 seconds), rather than a second Repair default. The stage deadline is the earlier of start
plus 300 and request deadline minus that reservation. Remaining stage time is divided among
remaining affordable rounds, with round/model/preparation caps applied. The explicit full-request
600-second ceiling is not extended. Cancellation propagates and request exhaustion prevents
new postwork; request-owned cleanup remains active. Model limits are maxima, not allocations
that every round is guaranteed to receive.

Application defaults: WALK/unspecified coordinate range 2 km, explicit motor range 5 km,
automatic leg burden 45 itinerary minutes, insertion detour increment at most max(1 km,
0.5 times original direct distance), stage-cumulative added daily burden 90 itinerary minutes.
Two-sided insertion checks both adjacent legs and the original-anchor detour. Blank-day groups
also receive a diameter check. REQUIRED remote visits are exempt from automatic compactness
removal, but not from confirmed constraints.

Evidence layers remain separate:

- Exact directed/mode/routing-preference/departure-compatible observed Routes may support the
  existing minimum-transfer PASS/CONFIRMED check.
- Observed untimed WALK matrices omit `departureTime`; their directed durations support layout
  and burden. Future-time feasibility remains UNKNOWN. The existing generic matrix transport
  can serialize this request; provider acceptance/quality has not been live-validated here.
- Missing compatible Routes can use a <=1 km WALK/application-default coordinate layout with
  at least 45 minutes of schedule reserve. This is a policy reserve, not an estimated provider
  duration. Explicit motor requirements, observed obstacles and applicable hard conflicts
  cannot be bypassed by it. Reversed/estimated observations do not become measured evidence.

Every proposal recomputes stage-added/identity-replaced transfer burden against stage-original
activities. Earlier accepted additions remain stage-added. Removed original adjacent edges earn
credit only with comparable observed evidence of the same basis; unknown baseline travel earns
no invented credit. Unsupported comparisons are marked, and conservative gross added load may
reject an arrangement even when its true increment might be lower. Transport itinerary minutes
are separate from service runtime seconds. Baseline credits currently cover insertion chains
between retained original adjacent anchors; unsupported replacement/deletion comparisons use
conservative gross load. Splitting an existing CONFIRMED route dependency requires verified
replacement legs; removing the old adjacency cannot hide that conflict behind UNKNOWN.
The current single-pair route adapter can exhaust
four requests before using all 32 elements; it does not promise complete route coverage.

### Actual offline execution record

Chronological pytest runs during this task (no live and no full-repository sweep):

| Order | Scope | Actual first result / follow-up |
| --- | --- | --- |
| 1 | Repair + wiring, stop after 8 failures | 45 passed, 8 failed; old unconditional-hours discovery and 180-second assertions |
| 2 | Wiring, stop after 6 failures | 3 passed, 6 failed; old one-call assumptions and obscured overflow summary |
| 3 | New multi-round/spatial tests | 24 passed |
| 4 | Repair + wiring | 75 passed, 22 failed; remaining old invocation/deadline/discovery fixtures |
| 5 | Repair + wiring after fixture migration | 96 passed, 1 failed; duplicate canonical attempt now correctly counted once |
| 6 | Multi-round + Repair + wiring | 121 passed |
| 7 | Expanded multi-round/config/graph tests | 30 passed, 1 failed; test observed a nonexistent module function instead of ReferenceDiscoveryService.discover |
| 8 | Corrected expanded tests + documentation coverage | 32 passed |
| 9 | Added actual callback, shared-route-budget and unsupported-mode checks | 35 passed |
| 10 | All V3 tests + runtime config + V0/V1/V2 runner regression | 249 passed in 8.31 seconds |
| 11 | Unsupported transport pre-call stop and configured stage deadline | 35 passed |
| 12 | Runtime source/CLI/YAML targeted checks | 5 passed, 60 deselected |
| 13 | Final usage/missing-usage, unsupported-mode and documentation checks | 3 passed, 32 deselected |
| 14 | Confirmed-route chain protection + Repair/multi-round tests | 103 passed |
| 15 | Directed replacement-chain check after allowing verified reversed order | 1 passed, 35 deselected |

Static checks initially reported 49 import/format/unused/zip findings; targeted formatting/import
fixes followed. Later checks found two long lines, then one unused loop target; those were fixed.
Final changed-code Ruff and Git diff whitespace checks passed (existing CRLF notices only).
These are not silently represented as an uninterrupted green first run. Tests use injected
models, provider fixtures and retrieval fakes; no real HTTP/embedding/database call was made.
Coverage includes fair evidence reassessment, protected content, partial rollback boundary,
unique cross-round IDs, actual graph feedback and one Nearby phase, cancellation/ownership,
UNKNOWN additions, WALK measurement versus missing-route reserve, two-sided detour, cumulative
burden and no fictional baseline credit, YAML/CLI propagation and unchanged earlier runners.

### Actual Repair serializer sizing

Uses the modified DTO, system prompt, strict schema, serializer, compact feedback helper,
coordinate candidate-pair projection and offline o200k tokenizer. Synthetic fixtures are sizing
inputs, not model executions or empirical evidence that the limits suffice. Second/third-round
fixtures represent only the latest feedback, not concatenated history. An initial sizing run
used the same feedback specimen for both later labels; the final third-round specimen uses a
distinct partial-acceptance feedback envelope. No limit was enlarged to pass a stress sample.

System = 232, schema = 322, framing = 2048 tokens in every row below. Component counts are
independently serialized measurements and need not add exactly to the combined user payload.

| Fixture | ID union / candidates | Context | Candidates | Evidence/spatial/feedback | Requirements/findings | User | Total | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Retime only | 2 / 0 | 318 | 10 | 93 | 484 | 918 | 3520 | Fits |
| Single-date addition | 28 / 27 | 171 | 5816 | 13432 | 468 | 19900 | 22502 | Fits |
| Three-target addition | 28 / 25 | 377 | 8786 | 15694 | 803 | 25673 | 28275 | Fits |
| Ten-day other operations | 28 / 28 | 2599 | 5891 | 1158 | 2135 | 11796 | 14398 | Fits |
| Long text | 28 / 28 | 47319 | 68499 | 1158 | 2135 | 119124 | 121726 | Rejected |
| 24 requirements/conflicting hours | 28 / 28 | 2599 | 5891 | 64383 | 4798 | 77684 | 80286 | Rejected |
| Round 2 compact feedback | 28 / 25 | 377 | 8786 | 15799 | 803 | 25778 | 28380 | Fits |
| Round 3 compact feedback | 28 / 25 | 377 | 8786 | 15800 | 803 | 25779 | 28381 | Fits |

The synthetic 50-edit output measured 2956 tokens against 16384. This is not a completion
length guarantee. Input overflow preserves the latest adoption; necessary protection and
facts are not deleted to force a pass. Full public-access semantics, complete costs, all-mode
routing, global route optimization and empirical multi-round success remain unsupported or
unvalidated. Any new live run requires separate authorization; no automatic rerun is scheduled.


## A elastic time and real adjacency checkpoint (2026-09-24)

Status: implemented and offline-validated only. A is complete; B/C remain approved directions,
not implemented in this checkpoint. Historical live records remain unchanged. This work does
not establish the complete root cause of any historical seven-day rejection.

### Shared contract adaptation, separate from V3 mechanism

`TimeProtectionDraft` / `TimeProtection` add destination-local dates, same-day start/end,
fixed/unresolved status, reason and canonical source references. Empty dates mean all requested
dates. The existing single preference interpretation call emits this additive dimension;
Foundry transport mapping, domain validation and canonical source/date validation enforce it.
`preference_prompt_6` / captured `preference_draft_4` distinguish the new interpreter boundary.
The canonical envelope remains `interpreted_requirements_3` with an additive nullable field.

`time_protections=null` or missing historical domain fields mean unassessed, never proven absence.
An empty array is an explicit assessment with no fixed reservation; empty user text takes the
existing no-model branch with that assessment. Old strict-wire capture re-expression tests add
explicit null; original capture files are not migrated. Unresolved restrictions keep their date
scope and reason. Ambiguous overnight/time-zone restrictions are not guessed. A relaxed soft
preference is retained and is not converted into a whole-afternoon reservation. No keyword or
regex interpretation, second interpretation call, primary-generation prompt change, or B/C
visit-count/access-mode contract was introduced. V0-V3 share the interpretation/mapping change;
this is not counted as a V3-specific gain.

### Application-owned schedule view and atomic application

`repair_schedule.py` builds a request-owned `ScheduleState` only from the primary-generation
snapshot and assessed requirements. Eligible roots must originally be `free_time`, locationless,
aware in time, and without a monetary amount or an unsafe meaningful cost projection. Missing
or scoped unresolved provenance keeps them protected. Fixed time is subtracted from usable
windows; unrelated soft semantics do not freeze them. Destination time zones must be unambiguous
in the supplied Places evidence to bind fixed local time; otherwise the affected dates stay
unresolved. Explicit non-null/unsafe costs are conservatively retained. Null/invalid-to-null
cost observations alone do not create financial obligations.

`RepairScope.window_roots` grants application consumption on specific existing dates and original
intervals. Direct model edits to free-time activities are rejected regardless of claimed role.
Candidate preparation and `repair_input_2` expose the same residual elastic windows; protected
activities no longer contradict that permission. Identity/date/operation validation and fixed-time
checks precede optional post-proposal Routes. On a detached proposal the application subtracts
only changed visits and necessary affected transfer intervals, creates uniquely identified
fragments, then runs the existing full overlap, source/date, requirement, route, spatial and
business comparisons. Acceptance adopts visits and fragments together; rejection retains the
previous itinerary and schedule state. Placeholder edits alone never supply quantity improvement.

Fragments retain root lineage, original authorized bounds and generation provenance in the
schedule/audit sidecar; non-time activity fields remain intact. Retained cost projections are
reindexed by activity identity; consumed null placeholder paths are removed without cloning a
cost onto new visits. The original itinerary and original cost observations remain immutable.
Each accepted round carries the residual state forward; rejected rounds cannot enlarge it or
roll back previous adoption. Stage output aggregates accepted window adjustments and preserves
individual rejected proposals in their round records.

### One adjacency view, without imaginary endpoints

Candidate windows, projection, relevant-route filtering, acquisition, revalidation, confirmed-route
replacement-chain checks and spatial burden use the shared schedule view. Authorized locationless
placeholders are not geography nodes. An insertion between A and C tests A->B and B->C. Fixed
occupancy is subtracted from transfer windows and cannot be credited as travel. Applicable timed
routes, untimed WALK measurements and no-route policy reserves remain distinct. A route tied to
an earlier departure is not reused as if it certified a later departure after fixed rest.

Unknown real activities and unbound explicit transport remain occupancy/location barriers. The
current Activity/TransitionBinding contract has no transport-activity-to-endpoints binding: A does
not infer one from notes or silently credit that duration. Such cases may remain unrepairable.
Existing confirmed real route conflicts and true distant/short-gap arrangements remain checked.
No hotel, origin or minimum visit duration is invented. Unchanged adopted transfer reservations cannot be
reused by a later visit. Superseded adjacency reservations stay in prior-round audit and are
replaced by the new real legs, not counted as simultaneous travel. This does not enlarge or
recreate consumed free-time fragments. Generic/private activities within fixed time remain
UNKNOWN in their semantic relationship and protected against unsafe retiming or deletion.
Nearby still runs once over the final adopted primary, with the existing main-invariance and
cost-association boundary.

No new runtime tuning values were needed. Existing `v3_repair` limits apply, including 28 input
identities, 120 projected activities (also enforced after splitting), 64k/16384 tokens, shared
acquisition budgets, three rounds and existing deadlines/spatial thresholds. Fixed-time protection
and lineage are contract invariants, not switches. The input ceiling remains fail-closed without
truncating protection data.

### Historical fixture evidence and limitations

`backend/tests/fixtures/v3/historical_free_time.json` extracts the draft, three parsed patches and
relevant Places from the recorded result, with run ID and source SHA-256. The tests explicitly add
**synthetic** `time_protections=[]`; the historical run did not observe that new assessment.
Recorded route matrices are not included, so this is a minimal regression, not an exact live
replay or evidence that the same provider response would occur today.

| Historical patch | Offline result under the explicit synthetic context |
| --- | --- |
| 1 | Rejected: insufficient unoccupied transfer window (30-minute gap versus existing 45-minute no-route reserve). No successful fully adjusted proposal is claimed. |
| 2 | Rejected after atomic placeholder adjustment and revalidation: `no_route_fallback_distance`. No confirmed free-time overlap in the adjusted proposal. |
| 3 | Rejected after atomic placeholder adjustment and revalidation: `no_route_fallback_distance`. No confirmed free-time overlap in the adjusted proposal. |

The elastic-placeholder endpoint obstruction is removed; the remaining spatial/time rejections
are retained. No historical patch, input, evidence or log was rewritten to make it pass.

### Actual offline execution sequence

| Order | Run | Result and follow-up |
| --- | --- | --- |
| 1 | Repair/wiring/multi-round + Foundry client/boundary | 177 passed, 1 failed: historical re-expression lacked the new strict DTO field. Added explicit unassessed null in the test adapter only. |
| 2 | New A tests + requirement boundary | 42 passed, 11 failed: ten invalid zero-duration test fixtures and one missing accepted-window summary audit. Fixed fixtures and stage audit aggregation. |
| 3 | A tests | 15 passed. |
| 4 | Shared time contract + A + strict DTO | 33 passed. |
| 5 | Expanded A adjacency/authorization tests | 19 passed. |
| 6 | Offline historical result inspection | Three rejections retained, with reasons above; real offline tokenizer, fixture model only. |
| 7 | Changed-code Ruff | Initially 49 findings, 10 automatically fixed; formatting then left three ambiguous local names; renamed and checks passed. |
| 8 | Actual Repair serializer sizing | Eleven inputs measured; nine fit and two stress inputs rejected. See below. |
| 9 | V3 + affected V0/V1/V2 + Foundry + shared interpretation | 491 passed, 1 failed: acceptance-tool prompt-version marker was stale. Updated that marker and its assertion. |
| 10 | Request-wide preference + requirement acceptance harness | 35 passed. |
| 11 | A/Repair/multi-round/wiring + time contract | 164 passed, including additional relaxed, unsafe cost and confirmed-real-route tests. |
| 12 | A + read-only validator after private-activity protection | 78 passed. |
| 13 | A + multi-round + graph after superseded-reservation protection | 90 passed. |

Tests inject all external boundaries; the test network guard prevents non-loopback sockets.
No model/provider/embedding/database service was called. Unit tokenizer fixtures are not used
as real sizing evidence. Tests cover actual graph/Repair/final diagnostics/Nearby integration,
source identity, fixed/rest protection, atomic rollback, residual windows, cost paths and resource
closure. Only relevant tests and affected version regressions were run, not the whole repository.
The final static pass initially identified two import-order findings in the newly added tests;
those imports were fixed. Final changed-code Ruff and tracked Git diff whitespace checks pass
(existing CRLF conversion notices only). The historical result hash matches the fixture provenance.
Branch remains `feature/v3`, HEAD `05ef226b46123883aa9bbc681382baeb4724a984`; no paths are staged.
The workspace still includes the pre-existing dirty/untracked work. No commit, push, live run,
configuration change, `.gitignore` edit or thesis-note edit was made by A.

### Actual serializer sizing

The real Repair DTO, schema, prompt, serializer and installed offline o200k tokenizer were used.
Each row includes system 263, schema 322 and framing 2048 tokens. Component columns are separately
serialized and need not add exactly to combined user tokens. All A samples use the 28-identity
union; later samples use an actual application split and only compact previous-round feedback.

| A fixture | Context | Candidates | Evidence/spatial/feedback | Requirements/findings | User | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Fixed time and elastic window | 600 | 5816 | 13432 | 532 | 20393 | 23026 |
| Later residual split | 875 | 5601 | 12549 | 526 | 19564 | 22197 |
| Later multi-target, 24 soft requirements | 1855 | 8435 | 14551 | 3526 | 28380 | 31013 |

Other totals: retime 3574; single-date 22556; three-target 28329; ten-day operations 14452;
round-2 feedback 28434; round-3 feedback 28435. Long text 121780 and conflicting-hours/24-requirement
stress 80340 both raise `repair_input_overflow`. No protection was truncated and no limit raised.
The synthetic 50-edit output is 2956 tokens versus 16384; this is not a completion guarantee.

### Deferred B/C and live boundary

Deduplication/overfull review switches (approved default off), adjacent-date moves with explicit
source/target activity permissions, associated targets, REQUIRED-copy protection, opening/route
target expansion and visit/access semantics remain B/C. The approved configurable 09:00-18:00
blank/missing-day default is not implemented here; existing activity days are not clipped to it.
Quantity review stays default off. This A checkpoint adds no new live evidence, benchmark result
or quality guarantee. Further implementation and live execution require separate authorization.


## B target and operation checkpoint (2026-09-24)

Status: **implemented + offline-validated**. No new live evidence. C opening/route-conflict
repair targets and access-mode semantics remain unimplemented. Historical Tokyo records,
including the three rejected patches, retain their original outcomes and evidence boundaries.

### Contracts and execution

- `validation.py`, `models.py`, `wiring.py`: quantity review covers assessable zero/one-POI,
  empty and missing dates; independent repetition and overfull switches are default false.
  Repetition is still an observation/review, not a confirmed inappropriate revisit. Overfull
  counts distinct main POIs and permits exactly five under the current application policy.
  Unknown roles/identities are not converted to zero visits. Shared generation diagnostics
  remain the original 2..5 observation, separately from configurable Repair target thresholds.
- `repair_targets.py` implements executable visit satisfaction, residual insertion windows,
  blank-date windows and conditional coverage progress. Reliable consistent Places timezone
  plus assessed time protections are required for the blank-date default. Missing dates also
  receive relevant fixed/unresolved protection records. Existing days use their actual occupancy
  and calendar gaps, not a new 09:00..18:00 boundary. A elastic roots remain unchanged.
- `repair_models.py`, `repair_acceptance.py`: move carries the existing activity ID, null place ID,
  destination date and timestamps. Original source and explicit neighboring destinations are
  application permissions. Identity, duration, other fields and cost association are retained.
  A moved activity cannot be moved again from a new source to escape its original authorization.
  A repetition group may cover more than two dates; the adjacency restriction is per move.
- `repair_service.py`: current adopted draft and remaining original/activated targets drive each
  round. The phase budget, deadline, identity ledger, unique activity IDs, caches and failure
  records are not recreated per target or child. Rejected/failed later rounds retain the latest
  accepted draft. Nearby remains outside the phase and executes once on the final primary.
- `repair_candidates.py`, `repair_projection.py`: existing context, addition options and identity
  ledger remain separate. Replacement associations use the affected target/activity, not an
  arbitrary first target. Discovery opportunities choose a deficient target date, prefer an
  unserved date, and use that date's real anchor or existing destination scope. Records include
  attempted/cached scope and unserved reasons. Google/RAG/Details budgets remain phase totals;
  some dates can receive no discovery opportunity. UNKNOWN candidates remain eligible under
  the existing identity/fact/spatial gates. Replacement inputs may include identities needed for
  authorized existing operations; this does not grant ordinary addition/revisit permission.

### Satisfaction, conditional targets and acceptance

`CoveragePermission` binds a stable child ID to parent target, trigger activities, date, count
floor and reason. `RelatedTarget` records real activating changes, affected adjacency, baseline,
current count and resolved/unresolved/unknown state. The application activates children only when
an actual authorized deletion/replacement/move changes the parent visit. Model additions alone
cannot activate permission or expand to an unrelated date.

Review proposals must preserve the minimum of prior distinct count and the configured lower
reference; compensation is atomic. Moving a visit cannot create/worsen an overfull neighboring
date. Repetition progress counts total excess visits, so concentrating duplicates on one date
cannot fake improvement. Explicitly required revisit counts/dates remain protected. REQUIREMENT
satisfaction cannot decrease, even when deleting an extra copy is allowed.

EXCLUDED deletion has a narrowly scoped exception: only distinct prohibited identities actually
removed can justify lost coverage on that authorized date. It cannot waive optional losses.
An unmet child remains in the final report/result and makes completion partial; the prohibited
identity cannot be reintroduced. The legacy `allow_coverage_regression` field remains readable
for compatibility but has no authorization effect. All edits, A placeholder changes and cost
reindexing remain one atomic proposal. Existing confirmed conflict, route and spatial guards run
normally; input legality or reduced repetition alone does not imply acceptance.

The final graph reassessment carries active children as well as the adopted schedule, so a last
rejected proposal cannot replace the final report. B review flags are included in `V3Outcome`;
full effective configuration remains in the existing request snapshot. Related-target artifacts
join the existing bounded/redacted scope, candidates, patch, proposal and comparison trace events.
Missing/truncated artifacts retain their existing explicit status semantics.

### Shared contract adaptation, not a V3 mechanism gain

`VisitRequirementDraft` / `VisitRequirement` and strict Foundry DTO add minimum total visits,
mandatory dates, executable/unresolved status, reason and source quotes/references tied to exactly
one canonical named requirement. The same single preference interpretation path serves V0..V3;
no second interpretation or text heuristic was introduced. Canonicalization checks exact named
identity, request date range and quote provenance (including canonical casefold references).
`None` remains legacy/unassessed; an explicit empty list means assessed without visit-count/date
obligations. Unbound explicit requirements and unassessed visit dimensions do not grant destructive
review scope. Unresolved dimensions stay visible; soft preferences do not become per-POI hard gates.

The interpreter markers are `preference_prompt_7` and `preference_draft_5`; canonical envelope
version remains additive-compatible. Historical strict-wire re-expression fixtures explicitly
supply null, without altering historical logs. The primary itinerary prompt, supply K, acquisition,
weather, date policy, SQL and vector artifacts are unchanged. No new shared client lifecycle fix
was made in B; earlier lifecycle corrections retain their separate attribution.

### Configuration and capacity

See `config/runtime.yaml` and `config/README.md`: new independent review flags false/false,
`daily_main_min=2`, `daily_main_max=5`, `move_max_days=1` (0 disables), blank local hours 9..18.
New review flags are YAML-only; existing quantity CLI override behavior is unchanged. Values load
once into the effective runtime snapshot with type/range/relationship validation.

All targets share the existing three rounds/calls, 300-second phase, at most 70 seconds/model,
64k input, 16384 output, 28 input-identity union and unchanged tool totals. New child targets do
not replenish them. No required context is truncated to force a fit.

### Actual offline execution sequence

The following is the actual order, including fixture and implementation failures. No provider,
model, embedding or database service was called; pytest external boundaries are mocked/guarded.

| Order | Run | Result / action |
| --- | --- | --- |
| 1 | A schedule, wiring policy, shared time | 35 passed, 1 failed: obsolete blanket EXCLUDED-waiver assertion migrated to scoped permission. |
| 2 | First B service tests | 6 passed, 5 failed: two malformed hour fixtures and missing child-result aggregation; corrected. |
| 3 | B service retest | 11 passed. |
| 4 | V3, shared time, strict DTO | 246 passed, 9 failed: config documentation, old waiver/cost assertions, rejection wording, explicit revisit guard and unassessed synthetic graph context; corrected without expanding budgets. |
| 5 | Expanded B, Repair, wiring/policy, multiround | 151 passed, 2 failed: duplicate-date fixture and remaining old waiver assertion. |
| 6 | B plus waiver test | 17 passed, 1 failed: comparison used pre-normalized fixture instead of unchanged normalized primary; corrected. |
| 7 | Selected-run command | No tests ran: wrong config test path; corrected to `backend/tests/runtime/test_config.py`. |
| 8 | B/shared visit, Repair, graph, runtime config | 156 passed, 1 failed: strict DTO test supplied Python tuples instead of JSON arrays. |
| 9 | Static checks/formatting | Initial 115 findings; follow-up new changes yielded 117 findings (6 import fixes), formatting reduced to 3; loop binding/line length corrected. |
| 10 | B and shared visit tests | 27 passed. |
| 11 | Actual serializer sizing | 15 synthetic inputs measured; 13 fit, 2 pressure samples rejected. |
| 12 | Expanded B tests | 25 passed, 2 failed: primary fixture referenced identities outside supply and imported a nonexistent free-time helper. |
| 13 | Graph diagnostic rerun | 1 failed, confirming the fixture's primary identity boundary. |
| 14 | Two targeted fixtures | 1 passed, 1 failed: graph fixture accidentally included overlaps, so overfull completion correctly remained partial. |
| 15 | Corrected graph fixture | 1 passed; six valid supplied identities, nonoverlapping visits, reduction to five. |
| 16 | V3 and shared time/visit | 270 passed, 1 failed: synthetic 28-way overlap capacity test now projected many real target associations and hit the input ceiling. Narrowed that capacity-only test to one explicit target; no production limit changed. |
| 17 | Targeted capacity plus shared Foundry/interpreter/V0/V1/V2/config regression | 220 passed. |
| 18 | V3 plus shared time/visit, including missing-date rest protection | 272 passed. Static check had one new test import-order finding, subsequently fixed. |
| 19 | Final serializer sizing | Same 15 sample categories; later-round B sample now includes adopted compensation, retained child audit and remaining repetition. Results below. |

The actual graph tests exercise default-off and enabled review paths, real Repair patch application,
final diagnostics, cost association, Nearby and resource closure. Service tests additionally cover
blank/missing dates, fixed rest, explicit visit obligations, multi-date groups, atomic compensation,
EXCLUDED partial/next-round completion, later failure preservation, adjacent move, prohibited move
chaining, A elastic consumption, per-date geography, and effective/invalid B configuration.

### Actual Repair serializer sizing

Measured using the real `repair_input_2` payload, prompt, strict patch schema and offline o200k
serializer/tokenizer. System 330, schema 325 and framing reserve 2048 tokens are included in totals.
Component columns are independently tokenized diagnostics; JSON composition adds its own framing.

| Input | Context | Candidates | Evidence | Requirements/findings | User | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dedup + conditional compensation, union 28 | 1227 | 21045 | 13649 | 580 | 36511 | 39214 |
| Adjacent two-day move, union 28 | 2005 | 6411 | 7345 | 566 | 16337 | 19040 |
| Missing date, union 28 | 508 | 5965 | 12475 | 565 | 19523 | 22226 |
| Later adopted compensation + child audit + remaining target, union 28 | 1771 | 7249 | 10649 | 573 | 20252 | 22955 |
| A residual split / later round | 1091 | 5601 | 12555 | 532 | 19792 | 22495 |
| Long time/requirements context | 2433 | 8435 | 14557 | 3532 | 28970 | 31673 |

Other passing totals: retime 3700; single addition 22664; three-target addition 28437; ten-day
operations 14740; elastic/fixed 23324; prior round-2/3 feedback 28542/28543. Long text 122068 and
conflicting-hours evidence 80628 reject with `repair_input_overflow`. Synthetic 50-edit output is
2956 tokens, not a completion guarantee. These are synthetic serializer measurements, not live
model usage, evidence that all 28-identity inputs fit, or proof of real-world repair quality.

### Remaining limits and stop boundary

C remains deferred: no automatic opening/route-conflict repair target expansion, access-mode
adaptation, complete public access/cost checking or different-ID experience deduplication.
Missing reliable timezone or unassessed relevant obligations can prevent blank/destructive scope;
UNKNOWN facts are not upgraded. Discovery opportunity is bounded and may not serve every target.
Real route/spatial policy may still reject validly authorized edits, including historical proposals.
No new live or formal evaluation is authorized by this checkpoint. B does not establish that the
historical seven-day rejection's complete cause has been solved.

Final changed-code/test Ruff and tracked `git diff --check` pass. The historical source result
SHA-256 still matches the A regression fixture provenance. Git remains on `feature/v3` at
`05ef226b46123883aa9bbc681382baeb4724a984`, with prior and new uncommitted changes; the index is
empty. No stage, commit, push, historical-record edit, `.gitignore` edit, thesis-note edit or
source snapshot was performed for B.


## C operating and transfer checkpoint (2026-09-24)

Status: **implemented + offline-validated**. No new live run or formal evaluation. Historical
Tokyo outcomes are unchanged; C does not establish that the old seven-day rejection is solved.

### Supported evidence and explicit limits

`VisitBinding` is application-owned activity/canonical/whole-venue intent with source references,
not an operational claim. A uniquely bound named visit can inherit explicit `venue_entry` or
`exterior` intent from the canonical shared requirement. Duplicate copies are not arbitrarily
assigned an interior visit by the interpreter mapping. Explicit per-activity bindings may be
provided by the application; Repair output cannot create or alter them. Missing access mode,
ambiguous copy assignment and unsupported subvenue/mixed semantics remain unassessed/unresolved.

Opening confirmation currently supports the existing effective resolver's whole-venue,
explicit-date/range daily hours, and traceable date-specific closure with matching authoritative
closure provenance. It requires reliable identity, recognized venue timezone, aware activity
timestamps, entry intent, valid applicable dates and no relevant unresolved evidence conflict.
Business magnitude is seconds of the visit outside supported hours; a closed day loses the whole
visit duration. An hours PASS means only the bound hours condition passed; public access,
admission/tickets and price remain separate UNKNOWN dimensions.

Ordinary Places prose, generic recurring hours, business type, titles/notes and exterior viewing
do not establish a future indoor closure conflict. Missing/conflicting scope, timezone, authority
or date does not become CONFIRMED. Overnight windows, sub-area/product hours, general public
access eligibility and complete cost verification remain unsupported. No new official-page,
Reviews or Profile acquisition was introduced.

Transfer confirmation reuses A `ordered_activities` and available occupancy. It requires exact
origin/destination, structured mode, routing preference, departure time and provider-observed
available duration. Conflicting durations, mirrored estimates and absent/mismatched times remain
UNKNOWN. Untimed WALK can guide layout, but cannot certify a future transfer. The existing
no-route and spatial policies are unchanged and may reject otherwise authorized proposals.

### Automatic scope, comparison and stage priority

`wiring.operation_scope` now grants confirmed opening/route targets without any review switch.
Affected main visits get duration-preserving retime permissions (which can reorder them), optional
adjacent moves, and conditional deletion/replacement only when B visit-satisfaction protection
permits that copy to be removed. Explicit required entry cannot be replaced by an exterior copy.
A fixed/rest, original move bounds, date/count protection, canonical authorization and EXCLUDED
rules remain enforced over the complete atomic patch. The application still does not shorten a
visit merely to fit opening hours.

`repair_obligations.py` records whether an old visit/transfer obligation truly disappeared due to
an authorized deletion, identity replacement or separation onto different dates. Same-visit
opening comparisons use stable activity/canonical identity across date moves. Retained route
endpoints require a verified actual new chain; dropping the adjacency record or inserting an
unverified intermediate stop does not remove that obligation. A changed direction is checked
in its actual new order. A genuinely removed optional visit does not require a nonexistent old
leg to PASS, but the new schedule still faces route/spatial/confirmed-conflict checks.

`repair_acceptance.py` compares opening violation seconds and transfer deficit seconds; partial
improvement retains CONFIRMED residuals. Removed-obligation progress is explicitly labeled
`conflict_obligation_removed_not_new_facts_verified`, rather than treating an UNKNOWN replacement
as factually verified. Notes-only, role changes, evidence weakening and access-mode substitution
remain invalid repair paths. Fair re-assessment uses shared evidence for both arrangements.

`confirmed_visit_removal` extends B coverage permission with the exact removable identity set,
parent, date and trigger. Only actual loss of those identities can justify coverage regression.
It does not authorize unrelated optional deletion. Conditional children survive later failures;
completion remains partial until active children are resolved. The model cannot activate a child
by simply adding a visit. Source loss, costs and adopted diagnostics retain existing audit rules.

`repair_service.py` prioritizes remaining CONFIRMED targets before review goals and records
`deferred_review_target_ids` in each effective scope. No per-target/round budget is allocated.
Pre-proposal route requests are limited to incident authorized activities (addition-only scopes
retain their existing bounded date context); post-proposal requests select actually changed
adjacency/identity/time dependencies. Missing coordinates stop that optional request without
inventing a waypoint. Actual sends/elements, cache and failure keys share the existing 4/32 total.
No new provider probes or SDK retries were added. Final Nearby remains once after the adopted
primary; no per-round Nearby work is introduced.

### Shared adaptation and output provenance

The shared `VisitRequirementDraft`/canonical requirement and strict Foundry DTO add nullable
`access_mode` (venue_entry/exterior). The same one-pass interpreter sources it from explicit user
text; the primary itinerary generation prompt is unchanged. This is a shared V0..V3 contract
adaptation, not a V3-only mechanism benefit. Legacy absence stays null. Prompt/wire markers are
`preference_prompt_8` / `preference_draft_6`; the additive canonical envelope stays version 3.

RepairInput remains `repair_input_2` and now includes application visit bindings. Patch operations
and strict edit schema are unchanged. Application-generated schedule-note handling affects only
changed retained/replaced activities: old note text is preserved under a historical,
not-revalidated label, with the unmodified text also available on the original audit snapshot.
This avoids presenting an old timing description as current without using semantic heuristics or
discarding embedded warnings. It does not rewrite unknown title/description semantics or claim
the historical note's facts have been rechecked. Complete model/provider raw reasoning is not
captured.

C adds no runtime tuning values. `config/README.md` documents reuse of current YAML policy;
review defaults, K, initial acquisition, Weather/date/SQL/vector behavior and all budget values
are unchanged. No shared client lifecycle change was included.

### Offline execution sequence

| Order | Run | Actual outcome / follow-up |
| --- | --- | --- |
| 1 | Initial obligation/acceptance static check | 17 findings (1 import fix); formatting followed. |
| 2 | First C evidence/scope/service tests | 12 passed, 1 failed: replacement lacked the TRANSIT route demanded by existing spatial policy. |
| 3 | Targeted failed-case inspection | 1 failed with `explicit_motor_mode_requires_route_evidence`; policy retained. Test supplies mock new-leg evidence and asserts other replacement facts remain UNKNOWN. |
| 4 | C with actual runner/graph and note boundary | 15 passed. Real graph uses fixture model/provider boundaries with automatic route finding/scope/patch/revalidation, final Nearby and resource closure. |
| 5 | V3 plus shared time/visit regression | 287 passed after incident/changed-leg acquisition adaptation. |
| 6 | Expanded C plus shared visit contract | 31 passed: reordered direction, partial conflict, move plus compensation, fixed rest, sourced intent and priority. |
| 7 | Expanded static pass | 38 findings (3 import fixes); formatting and targeted cleanup without threshold changes. |
| 8 | Serializer extension / actual sizing | Sizing-tool static pass had 8 findings (1 import fix), then formatting. 19 synthetic inputs: 17 within ceiling, 2 pressure inputs rejected. |
| 9 | C/B/shared visit after satisfaction integration | 60 passed; required-copy eligibility uses B satisfaction rather than unconditional canonical locking. |
| 10 | Additional static pass and V3/shared time/visit | 10 formatting findings corrected; 298 tests passed, including entry-vs-exterior protection, exhausted Routes and closure provenance counterexamples. |
| 11 | Affected shared interpreter/Foundry/V0/V1/V2/config regression | 220 passed. No full-repository run. |
| 12 | Final inspection and C/read-only validator tests | One interpreter-prompt line-length finding corrected. Inspection aligned business magnitude with the same date-specific usable fact filter as confirmation, preventing a general baseline from supplying a contradictory magnitude; 81 passed. |


All external model/HTTP/embedding/database boundaries were fixtures/mocks. No live behavior is
claimed from these tests. Representative facts are created through the existing evidence resolver,
not by constructing a CONFIRMED finding as the trigger. Existing route direction/mode/time,
A historical-patch, rollback/cancellation/cache, B compensation and scope regressions were reused.

### Actual serializer sizing

Real DTO/prompt/schema/serializer and offline o200k; system 377, schema 325, framing 2048 tokens.
Component columns are diagnostic independent tokenizations; total includes the complete JSON.

| Sample | Context | Candidates | Evidence | Requirements/findings | User | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Opening retime, two context identities | 795 | 10 | 665 | 566 | 2046 | 4796 |
| Timed route reorder/options, union 28 | 916 | 14744 | 13196 | 562 | 29428 | 32178 |
| Opening replacement/compensation and adjacent move scope, union 28 | 886 | 14744 | 13041 | 566 | 29247 | 31997 |
| C scope plus later-round compact feedback, union 28 | 886 | 14744 | 13146 | 566 | 29352 | 32102 |

These are input scenarios and capacity checks, not successful model completions. Long-text input
122127 and conflicting-evidence input 80687 reject above 64000, without dropping protection data.
Synthetic 50-edit output is 2956 tokens versus the unchanged 16384 ceiling. The later-round sizing
uses compact synthetic feedback, not a replay or estimate of live model usage.

### Live boundary

Real interpreter access-mode extraction, provider date-specific evidence coverage, new route
acquisition and actual model C patch behavior still require separately authorized live validation.
Unbound normal visits can remain UNKNOWN/review and will not trigger C merely because their notes
mention hours. No claim is made that all required visits are executable, all UNKNOWN facts are
resolved, every confirmed conflict can be repaired within the budgets, or historical Tokyo output
is repaired. This checkpoint stops at offline implementation and validation.

Final targeted baseline-magnitude test: 1 passed after using the actual `current_general_policy`
enum in the negative fixture. Final changed-code Ruff and tracked Git diff whitespace checks pass.
Git remains `feature/v3` at `05ef226b46123883aa9bbc681382baeb4724a984`, dirty with prior and current
work, and no staged changes. The historical multi-round result SHA-256 still matches the A fixture
provenance. No stage/commit/push, `.gitignore` or thesis-note edit, source copy or new live run was
performed. This C checkpoint is ready for user review; further live work requires approval.


## Google API evidence adoption checkpoint (2026-09-24)

Status: implemented + offline-validated; no new live/model/provider/database calls. Source baseline
is feature/v3 at 9d429cde7ef4d75442f7f63876a123cfe0a91c3b; this checkpoint is uncommitted.
No budget, model deployment, primary prompt, K, Weather, date policy, SQL or vector artifact changed.

### Shared correctness and V3 integration

Shared Places normalization retains periods presence (missing/present/invalid/legacy-unmapped),
raw structured endpoints, dates/weekdays/truncation, separate special-day dates, request/retrieval
time and timezone. Current windows remain tied to the original request-local date. Structured
selection handles daily segments, overnight periods, 24-hour sentinel, explicit empty closure,
and clipped current windows. Text descriptions remain descriptive, never parsed into intervals.
Known special-date gaps prevent regular fallback; a special-day marker with usable periods does
not prevent evaluation. Applicable existing date-specific special evidence retains precedence.
Conflicts and unparseable facts stay UNKNOWN. Unsupported official non-daily/overnight contracts
are not reinterpreted; Places structured overnight periods are supported.

Shared Routes normalization accepts successful protobuf status `{}` and code zero, distinguishes
missing/invalid/error status, checks condition, preserves indexes, fallback/static duration and
per-element request/retrieval timestamps (including merged baseline chunks). Invalid/negative/nonfinite
seconds are unavailable; positive fractional seconds round upward and legitimate zero is retained.
The field mask adds only staticDuration/fallbackInfo, not a wildcard. These fixes affect V1/V2/V3;
V0 has no new tools. Shared evidence content is richer even though primary prompt text is unchanged.

V3 opening assessment, magnitude, candidate preparation and projection share selected_hours /
assess_opening. Unbound ordinary visits adopt application_default hours policy. Explicit exterior
intent is not overwritten; public access is not inferred. Timezone borrowing is limited to unique
reliable related scheduled context; unrelated pool timezones cannot freeze local dates.
Opening PASS means complete interval compliance, CONFIRMED means seconds outside adopted hours,
and UNKNOWN identifies missing/conflicting/inapplicable evidence. Date-closed candidates are excluded
only for their target date. Ordinary unknown candidates remain usable.

One route selector serves baseline/new evidence, validator, layout and comparison. Directed valid
WALK and basic-drive estimates are usable without future-time equality; TRANSIT/traffic-aware
estimates retain exact-time scope, including fallback calculation semantics. Conflicting applicable
no-route observations do not become PASS. Evidence selection precedes gap testing; insufficient
valid routes cannot masquerade as missing routes. Actual A occupancy and fixed-time exclusions remain.

Visitor suitability now independently records scheduling policy, reported admission/ticket/reservation
conditions and unverified eligibility/completion/special-area questions. Absence of a restriction
is not evidence of universal access. These uncertainties do not contaminate opening or route checks.

### Local gates, capacity and audit

The unchanged 2/5 km radii guide discovery and no-route filtering. Existing applicable routes bypass
radius rejection in preparation and acceptance, but still face 45-minute legs, insertion detour,
and stage-cumulative 90-minute daily addition policy. Candidate-linked existing routes can reach the
real input projection; unrelated matrix elements do not. No new routes are fetched merely for projection.
Same-activity-ID replacement edges receive comparable old-edge credit using real canonical endpoints;
unknown baseline routes receive none. Unresolved named binding protection is limited only when trusted
candidate/date scope exists; otherwise protection remains. Canonical/Details/ledger authorization,
REQUIRED/EXCLUDED, fixed time, review status, children, local acquisition stops and real cost protection
are preserved, not rewritten.

repair_input_2 has a canonical candidate catalog and referenced operation groups, retaining all
per-target/date/operation permissions. Projection revision is canonical_catalog_api_evidence_1.
The duplicated legacy opening_hours alias is omitted from candidate input only; source evidence is
retained. No empty route shells are serialized. Findings retain selected compact hours/route elements,
source/time/scope, calculation policy, available gap and outcome, including considered unusable routes.
Existing draft/reassessment/proposal/final reports and bounded audit truncation rules remain in use.

The saved ABC WALK observation is extracted into backend/tests/fixtures/v3/api_walk_observation.json with run
provenance. It is normalized historical evidence, not a raw provider response. The six unsaved baseline
legs and twelve missing historical periods were not reconstructed. New periods tests are synthetic.

### Actual test and correction sequence

1. Initial evidence/V3 regression: 78 passed, stopped after 12 failures. Old group payload consumers,
   unbound-hours expectations and route fixtures without status needed explicit migration.
2. Retest: 273 passed / 13 failed. Further old semantic expectations and cancellation patch location
   changed; the graph's contiguous visits now exposed real API route deficits. Complete mock repairs
   were changed to preserve duration and leave transfer time; C-authorized deletion is tested as partial
   with an unresolved coverage child, not disguised as a rejected overlap-only action.
3. New test collection failed due to Windows text encoding; converted that test to UTF-8.
4. Retest: 231 passed / 1 failed, correcting a test's zero-send counter lookup.
5. Targeted evidence/C tests: 50 passed / 1 failed; descriptive planning output was retained alongside
   explicit structured status, without using descriptions as executable facts.
6. Added edge tests: 30 passed / 2 failed, fixing synthetic TimeProtection.required reason and the
   dataclass resolution fixture API. Targeted retest: 32 passed.
7. Shared/V1/V2/V3 integration run: 458 passed / 2 failed. Fixed a new graph patch fixture that shortened
   a two-hour visit and updated the expected minimal Routes mask. Focused retest: 2 passed.
8. A later combined run produced no completion and was interrupted; it is not a pass. Targeted rerun:
   26 passed / 2 failed, identifying duplicate adopted_evidence keyword construction in route audit.
   Corrected the implementation. The affected combined suite then passed 461 tests in 9.15 seconds.
9. Final special-day projection check: 32 passed / 1 failed. Migrated the old expectation that a known
   special-day gap may fall back to regular when timezone is missing. Final targeted run: 33 passed.

Changed-file Ruff initially reported formatting/import/closure-binding issues; those were corrected.
Tests include real provider-shape normalization -> validator -> automatic scope -> repair -> adoption,
and actual run_v3 graph, Nearby and resource closure with mocked external boundaries. No second model
or remote probe was used. This is targeted engineering validation, not a formal benchmark/full-repo run.

### Actual serializer sizing

Command: `.venv/Scripts/python.exe -m tools.diagnostics.repair_payload --api-policy-comparison`.
Real DTO, prompt, schema, serializer and offline tokenizer. System 408, schema 325, framing 2048;
input 64000 and output 16384 unchanged. Component tokenizations are diagnostic, not additive totals.

| Synthetic sample | Context | Candidate groups/catalog | Evidence | Requirements/findings | User | Total | Group-only saving | New-field delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Retime | 390 | 14 | 259 | 505 | 1192 | 3973 | -4 | 168 |
| Overlapping groups, 28 identities | 936 | 7765 | 2539 | 888 | 12152 | 14933 | 2747 | 2604 |
| C route/options, 28 identities | 990 | 32453 | 15207 | 983 | 49654 | 52435 | 3283 | 2646 |
| Structured weekly periods, 28 identities | 936 | 13589 | 3947 | 888 | 19384 | 22165 | 7323 | 8520 |
| Same periods plus compact later feedback | 936 | 13589 | 3976 | 888 | 19413 | 22194 | 7323 | 8520 |
| Long-text pressure, 28 identities | 47553 | 69309 | 3603 | 2228 | 122717 | 125498 | not measured | not measured |

Group-only saving compares identical candidate content/permissions using inline groups versus a
catalog; it does not include removal of the legacy hours alias. New-field delta is a controlled field
ablation on the same new payload, not a reproduction of the old serializer or live usage. Retime pays
four tokens for the empty catalog. Richer evidence costs tokens; no claim of universally smaller inputs.
Pressure fails closed above 64000, without deleting protection or enlarging limits. Earlier and final
comparison runs were consistent; C route coverage was added to the final comparison set.

### Limitations and next boundary

No new live evidence exists for this policy. Source data can be missing, conflicting or invalid;
explicit sub-area/exterior access, reservation completion, tickets and complete costs remain limited.
Traffic-sensitive routes retain strict applicability. No ability guarantees completion within three
rounds. The historical ABC deduplication improvement remains its original result; new API-based
validation coverage is not another itinerary repair, nor proof that all twelve historical opening
checks or seven legs now pass. Further implementation changes or live runs require separate approval.

Final changed-file Ruff check and Git diff whitespace check passed. Staging remains empty;
HEAD is unchanged. The original .gitignore modification and historical live artifacts are untouched.


## Material feedback checkpoint (2026-09-24)

Status: implemented + offline-validated. No new model/provider/database/live calls. No commit,
push, threshold change or evaluation. This checkpoint corrects feedback preparation inside V3;
it does not change shared interpretation, V0/V1/V2, Google evidence policy or primary generation.

### Control flow and contracts

`repair_feedback.py` owns compact feedback classification, semantic input fingerprints,
presentation memory and attributable conflict records. `repair_candidates.py` reuses A insertion
windows, selected opening evidence and the existing route selector. `repair_models.py` adds
opportunity/audit fields; `repair_service.py` connects them to the existing stage budget and
latest-adopted state. `repair_projection.py` retains repair_input_2 and
canonical_catalog_api_evidence_1, with compact arrangement constraints and authorized opportunity
windows. No second candidate catalog, validator, ranking model or deterministic scheduler is added.

Candidate-target edges are TRYABLE when a potential authorized range remains; UNRESOLVED when
preparation cannot establish relevant conditions; BLOCKED only for an existing eligibility boundary
or a provable whole-opportunity obstruction. Missing schedule contracts, hours, coordinates, access
and price are not converted to facts. Known hours are intersected with authorized windows without
inventing a minimum visit duration. Time-independent API route estimates may prove every insertion
position exceeds the existing automatic leg policy; that is a scoped application-policy obstacle,
not proof of public inaccessibility. Time-sensitive route estimates with no selected departure do
not prove a whole window impossible. Required identities are exempt from the default leg-policy
filter. Conditional replacement/removal opportunities remain unresolved until atomic construction.
Final two-sided adjacency, time, detour, burden, requirements and acceptance checks remain mandatory.

Independent bipartite identity matching is retained. One identity with two target associations is
still one supply resource without revisit permission. `preparation_reference_met` replaces the
misleading `existing_material_sufficient` local stop label; the reference never proves feasibility or
target completion. Candidate preparation reports target opportunity counts, presentation history and
acquisition stops. Existing original-supply and Repair-unused statistics retain separate meanings.

After no_op_patch/no_measurable_improvement, already presented opportunities lose presentation
priority, not eligibility. First reuse unpresented qualified identities, then normally acquire pending
Details, finally use existing target/anchor discovery when query, position, budget and time permit.
A novel qualified option can end acquisition before reaching the two-alternatives reference.
No-progress is not an unconditional search instruction. Exact failed combinations also change an
opportunity signature, allowing another legal time without requiring new identities or searches.
Discovery target selection retains the B date allocation and stage-wide seen-date history; all
attempts, caches, failures, deadlines and acquisition quotas remain stage-shared.

The material fingerprint covers current protected/editable context, authorization, requirements,
time windows, relevant evidence, routes, spatial policy and concrete failed combinations. It ignores
round numbers, observation timestamps, audit commentary, presentation ordering and internal hashes.
A matching fingerprint stops before the next model call with
`no_material_change_for_remaining_targets`. Corrective operation constraints and alternative legal
time placements count as material differences; merely asking again does not. SDK/provider failures
remain terminal under the existing no-hidden-retry policy.

Presentation history records candidate, target/date, windows, evidence references, round, signature
and selected/not_selected/proposed_not_adopted. It is not an exclusion ledger. Conflict records are
created only from attributable confirmed opening/route/overlap findings or a specific failed spatial
leg, limited to edited activity, identity, time, adjacent activities and mode/routing preference.
A rejected atomic patch does not mark every proposed candidate unsuitable. Concrete constraints are
projected to the model; the existing application validator still decides whether any new patch is
acceptable. The trace records bounded `v3_repair_material_feedback`; truncation remains explicit.

All existing limits remain unchanged: three rounds/calls, 300-second stage, 70-second model cap,
64k/16384 tokens, 28-identity union, acquisition totals and spatial thresholds. No new runtime setting
is needed for internal contract state. Nearby remains once, after final adoption.

### Historical fixture and offline evidence

`backend/tests/fixtures/v3/tokyo_api_feedback.json` records source run ID and result SHA-256.
Original draft, contract, scope, saved patches, Details and selected route facts are extracted without
rewriting historical logs. Route envelopes are reconstructed from saved selected-route facts.
The complete candidate-anchor matrix was not retained in the CLI result. Tests explicitly supply
synthetic candidate-route support to reproduce the observed five-option context; this is not historical
Google evidence. Saved Odaiba Details and its actual acquired route are injected as available evidence,
not replayed network calls. A separate novel-candidate branch uses explicitly synthetic Details.

The real stage accepts the historical Odaiba patch, retains it after the second empty patch, and
skips the third model call when preparation produces no material change. With a synthetic pending
candidate, the third actual projection changes; its empty result still preserves the first adoption.
Neither branch claims the real model would now complete the trip. Other tests exercise rotation
without search, bounded discovery with acceptance, empty query/capacity/deadline stops, identity
matching, UNKNOWN qualification, fixed windows, one-second potential ranges, route-policy scope,
attributable atomic failures, new times without search, multi-date allocation and actual graph/Nearby
closure. No live API is used.

### Actual execution sequence

1. Initial affected service tests: 99 passed, 4 failed. Old tests expected another model call after
   an unchanged empty patch. Updated those expectations; cumulative usage coverage uses actual
   partial improvement before the second model call instead.
2. Expanded tests: 112 passed, 3 failed. Two new fixtures violated existing configuration relations;
   another proposed an unchanged retime rather than a concrete changed failure. Corrected fixtures.
3. New fixture suite: 12 passed, 3 failed. Historical extraction lacked candidate-anchor routes,
   a synthetic DTO used an unvalidated location dict, and a helper import was wrong. Corrected the
   test context transparently; subsequent 15 tests passed.
4. Affected V3 plus opening/provider regressions: 333 passed, 2 failed. Assertions assumed the final
   round always produced an attempted patch/proposal. Updated assertions to preserve the first
   rejected/truncated artifact and explicitly identify the later skipped round.
5. Targeted tests: 74 passed, 1 failed due to a misplaced variable in a new fingerprint test.
   Fixed test scope. Combined affected run: 336 passed.
6. Initial Ruff reported formatting/import issues; corrected only affected files, then checks passed.
7. Compact projection retest: 111 passed, 1 failed because a fixture compared internal authorization
   hashes/defaults with model projection. Updated the projection assertion to retain business fields
   while excluding application-only metadata. Targeted tests then passed 45; a further concrete
   candidate-time/no-search test increased the new feedback suite to 17 passing tests.
8. Final service/graph regression after projection and feedback corrections: 133 passed.
   A final acquisition guard stops Details/search for dates proven to have no authorized insertion
   window (missing window contracts remain unresolved). Targeted opportunity, service, A and B
   regression after that guard: 137 passed. Final affected-file Ruff and Git whitespace checks passed.

### Serializer sizing and boundaries

Actual prompt, DTO, strict schema, serializer and offline tokenizer were used. Initial measurement
included internal opportunity signatures/default unassessed fields in every authorization reference;
that increased two dense samples to 65961 and 67260 tokens. These internal audit fields are now kept
out of model input. Actual opportunity state/windows, protected context, evidence and authorization
remain intact. This is not truncation of facts and no ceiling was raised.

Final representative engineering totals:

| Sample | Total input tokens | Result |
|---|---:|---|
| Three-target actual preparation, 28-identity union | 37778 | Within 64000 |
| Same preparation with no-op feedback | 37894 | Within 64000 |
| Specific new time constraint, 28 identities | 38067 | Within 64000 |
| Dense C route/reorder fixture, 28 identities | 59255 | Within 64000 |
| Dense B dedup/compensation fixture, 28 identities | 60759 | Within 64000 |
| Long-text pressure | 125987 | repair_input_overflow |
| Tokyo control fixture round 1 / round 2 / skipped preparation | 21325 / 17715 / 17580 | Within 64000 |

These are offline engineering sizes, not provider usage or measurements of the historical live input.
System/schema/framing contribute 436/325/2048 tokens. Synthetic 50-edit output is 2956 tokens,
not proof that real completions fit the 16384 output allowance. Dense inputs remain close to the
ceiling; other stress samples also reject. Overflow retains the latest adopted draft. Sizing records
are under artifacts/v3_material_feedback_sizing*.json and v3_tokyo_feedback_offline_sizing*.json.
Earlier measurements are retained, including pre-compaction-of-audit-fields results.

### Remaining limits

Opportunity preparation is intentionally incomplete: exact visit duration, variable-departure transit,
complex insertion chains and unclear requirements still require proposal construction/re-validation
or remain unresolved. No prefilter guarantees an arrangement. Presentation rotation does not prove
preference suitability, and empty patches still do not explain the model's unrecorded reasoning.
Live effectiveness of changed third-round inputs remains untested. The previous seven-day failure's
complete root cause is not claimed solved. All historical artifacts, .gitignore and local thesis notes
remain untouched; no automatic next stage or live is authorized.

## Capacity calibration checkpoint (2026-09-25)

Status before the authorized Honolulu smoke: implemented + offline-validated;
resource limits are an engineering freeze candidate, not a version freeze.
Google total 5 includes a derived ordinary cap of google minus fallback (4),
reserving 1 fallback send. Stage canonical 12, Details 10, Routes requests 6
and elements 32 remain shared across rounds. Per-call union 32/input 72000
are preventive headroom. Output 16384, activity/text limits, three rounds,
300/70/600-second stage/model/request ceilings and all spatial/evidence policies
remain unchanged. No automatic future expansion is authorized.

RepairBudget checks application limits before adapter entry and again at send.
Explicit Google total/discovery/fallback, Details and Routes request/element
reasons are separate from provider_pre_send_error. Canonical exhaustion has
its own stop. Request success/failure/cache state is not reset. Compact
acquisition_audit rows save round, purpose, hashed request key, ordinary target
date/intent, sent flag, outcome, budget snapshots and raw hits where available.
Candidate preparation retains separate duplicate/identity decisions; audit is
not added to model input. Old pending Details reserve both attempt and send
capacity for exploration under the changed 12/10 ratio. No shared cache/client
behavior or V0-V2 mechanism changed.

Test chronology: initial V3 run stopped at 190 passed/8 failed (old capacity
assertions and unsynchronized documentation). Updated fixtures/docs yielded
368 passed/4 failed (remaining old assertions and fixture capacity migration).
After reserving both canonical and Details headroom, focused tests had 68 passed/1
failed (the old canonical stop expectation now correctly becomes Details stop).
Corrected expectation: 372 passed across V3, runtime config, opening-hours and
Google adapter tests. Two additional control tests (later overflow preserves
adoption and cross-round canonical totals), alongside budget tests, passed 4/4.
Initial Ruff found long lines; formatting fixed these. Final static results
and smoke outcome are recorded below when completed. No live preceded offline
acceptance.

Actual DTO/prompt/schema/serializer/offline tokenizer sizing: 32-identity dense
route 69567; dense dedup/compensation 71965; material opportunities 46114; no-op
feedback 46230; specific-time next-round constraints 46403. The dense sample
has only 35 tokens of engineering headroom: fitting one fixture is not a
guarantee for other inputs. Conflicting long evidence 96295 and 32-identity
long text 137547 are explicitly rejected. Historical-size 28-identity pressure
is retained separately. No protection text was removed or ceiling increased
to accept stress. artifacts/v3_capacity_calibration_sizing_final.json contains
component counts and additional A/B/C/time-window samples. Latest Tokyo live
used 19 identities/26454 tokens; it did not prove the old input limit inadequate.

Historical runs and their original policies remain unchanged. The prior
ProviderNotSentError is not retroactively relabeled as a proven budget error.

Final static checks: Ruff passed; git diff --check passed (line-ending notices
only). Historical-size 28-ID long-text pressure measured 125987 and was rejected,
as required. No actual provider calls occurred during offline acceptance.

### Honolulu smoke authorization block

The fixed Honolulu request (2026-09-27..2026-10-05, two travelers, USD 3000)
passed local date validation against backend reference date 2026-09-25. Actual
deployment remained gpt-6-luna. Run-local review overrides, input, command,
source manifest and effective configuration were prepared in
logs/v3_honolulu_9day_capacity_smoke_20260927/. Automatic approval review rejected
the execution before process creation. A second approval submission explicitly
cited the user's attachment authorization and was also rejected. No process
started, no live service request was made, and no alternative execution path
was used. There is no Honolulu run ID, usage, itinerary or live result. The
capacity checkpoint remains offline-validated only and is not formally frozen.
Continuation requires a user confirmation accepted by the approval mechanism;
this is an approval block, not a provider or V3 runtime failure.

### Honolulu capacity smoke (2026-09-25 local; explicit chat confirmation)

Following the documented pre-execution approval blocks, the user explicitly
confirmed execution in chat. Exactly one process ran: a84b4286-8e9b-4665-a9fd-14e7179e29bc,
exit 0, trace span 119.131 seconds. Runtime/config/source hashes are in
logs/v3_honolulu_9day_capacity_smoke_20260927/. The fixed request and gpt-6-luna
deployment were unchanged. No implementation edits or second live followed.

Initial and final primary are identical: 14 visits/13 distinct identities,
five coverage review dates (one with zero main visits), one repeated identity,
two confirmed WALK transfer deficits. Opening 13 PASS (8 current, 5 regular),
1 UNKNOWN; routes 4 PASS, 2 CONFIRMED; visitor suitability 14 UNKNOWN, budget
and open semantics one UNKNOWN each. Both route targets were prioritized over
six deferred review targets. No operating conflict was observed.

Round 1 preparation reached identity union 32 and 30 operation candidates with
202 authorization associations. Actual serializer counted 154653 engineering
tokens (candidate component 85204, evidence 58868, context 5339, requirements/
findings 2398; component counts are diagnostic, not additive partitions).
The 72000 guard skipped before the Repair model. No patch, proposal, comparison,
fingerprint or presentation history was constructed; no multi-round recovery
was exercised. The latest draft and reports were preserved. This is a safe
bounded overflow, not successful repair or an invalid user request.

Repair used ordinary Google 1/4 (total 1/5), fallback 0/1, canonical 10/12,
Details 10/10, Routes 0/6 and 0/32 elements, retrieval/embedding 0. Explicit
stop details_budget_exhausted was recorded, not ProviderNotSentError. There
was no needless attempt to spend the remaining Google quota. However targeted
scope correctness needs attention before engineering closeout:
- Route findings have empty dates. candidate_targets maps them to every scope
  add date; active September 27/October 3 route obligations acquired associations
  on unrelated sparse dates. Actual Google discovery targeted October 1 despite
  its review target being deferred. The local scope expansion is evidenced by
  the saved audit and code; its exact contribution to total overflow is not isolated.
- Per-target opportunity counts do not filter add versus replace, and repeat a
  global independent identity capacity. These rows cannot be read as distinct
  per-operation/date supply counts. This is an audit correctness limitation.

No automatic threshold increase or fix was performed. Keep the resource limits
as freeze candidates, but defer final engineering closeout pending the user's
decision on these scope/accounting findings. There is no evidence that 72k should
be increased to accommodate this payload.

RAG initialized and closed once, four queries/80 positions, 16 resolution
attempts, 12 Details, 4 fallback sends, partial bounded status; 12 new canonical
and 6 mixed-source IDs. Embedding usage 17 tokens. Primary baseline Routes used
6 requests/324 elements plus 3 alternative calls. HTTP logs show 2 model calls,
10 searchText, 54 Details, 1 embedding, 1 Weather, 9 Routes and 3 Nearby calls.
Official Web had zero tasks. Callback usage 132298 input +8040 output =140338;
Repair model usage is zero. Primary engineering input 129829/160000. Repair
preparation/skip snapshot used approximately 17.97 seconds, not the 300s cap.

Nearby ran once after final-primary with three requests and three references:
Pavilion Cafe, Ku's Canoe, Bites & Bev Snack Shop. Primary activities were equal
before/after Nearby. Request-owned RAG closed=true; no invented per-client close
records. Full application result (~10 MB), round audit, initial/final itineraries,
reports and integrity checks were separately saved; truncated trace summaries
are not the sole evidence. Source hashes were unchanged during the live.

### Explicit Details allowance update (2026-09-25)

Following separate user authorization, ordinary primary Details is now 60,
initial RAG Details 30, and Repair stage Details 30. YAML remains authoritative.
The quality_first_1 adapter now uses the configured primary send allowance
instead of r_pool + 8; its new-success goal remains unchanged (32 for seven/nine
days). This shared change applies to V1/V2/V3, not V0. RAG resolution remains
16 entities; Repair canonical attempts remain 12, so neither larger send budget
is a promise to acquire 30 distinct candidates. All time, input, review, search,
route and acceptance limits remain unchanged. Honolulu used the previous limits;
no live was executed for this update. Offline sequence: 135 related tests passed,
then a new real policy-adapter configuration test and its existing companion
passed 2/2; Ruff passed. No prior failure or test retry occurred. This update
does not fix the documented target-scope or payload-overflow issues.


## Active-target locality and capacity follow-up (2026-09-25)

Status: implemented + offline-validated. No live, provider call, commit, formal
comparison or freeze was performed. Historical Honolulu remains a skipped Repair
with two route conflicts, not a repaired itinerary.

### Correctness and scope

The stage used `finding.dates or scope.add_dates`, kept deferred coverage
permissions, and candidate preparation generated ADD edges for any active finding.
Dateless route conflicts therefore borrowed unrelated quantity dates. Opportunity
rows also mixed operations and repeated a global matching result as local capacity.

`repair_targets.localize_scope` now intersects actual activity/date dependencies
with original authorization. When confirmed targets defer reviews, the existing
application operation policy is reapplied to active findings and intersected with
original permissions: a shared activity cannot borrow a deferred repetition
DELETE/REPLACE/MOVE permission. Parent links are remapped across report IDs while
related target IDs remain stable. Only local applicable elastic roots remain
consumable; unrelated context remains protected. Move destinations remain within
original explicit authorization, never a reason for global candidate ADD scope.
Unresolvable dependencies yield no executable acquisition scope rather than a
trip-wide fallback. Named omissions retain their explicit application-granted date
range; this exception is not inferred for route/opening findings.

`repair_candidates.candidate_targets` prepares ADD for active coverage/named
omissions and active conditional compensation, and REPLACE for affected permitted
activities. RETIME, identity-preserving MOVE and DELETE need no new identities.
Active route parents in Honolulu are local to September 27 and October 3; October
1 quantity review cannot independently drive discovery. Deferred reviews stay in
the original report and can be promoted after actual revalidation. No new
validator, ranker, scheduler, evidence or relaxed acceptance rule was introduced.

Audit in `CandidatePreparation` now contains operation-specific
`target_opportunities`, `identity_free_operations`, and a single global
`identity_capacity_summary` (pool and selected-input matching capacity). Local
counts distinguish association edges, unique IDs, selected IDs, TRYABLE,
UNRESOLVED, BLOCKED and presentation state. BLOCKED records retain their scoped
reason, including operation/policy exclusions; they do not all mean physical
inaccessibility. Bipartite matching still consumes a distinct identity once.
Preparation-reference success is never target completion. Presentation history,
specific conflicts, material fingerprints, terminal failures and UNKNOWN semantics
are unchanged.

### Capacity, ownership and time

YAML/schema now allow `v3_repair.max_rounds=4`, `max_model_calls=4`, and
`input.input_tokens=120000`. Ordinary `budget.places.detail_calls=60`, initial
`tripworld_discovery.details_calls=30`, and Repair `acquisition.details=30` were
already implemented in the preceding allowance update and remain unchanged here.
These are resource calibration changes, not V3 mechanism contributions. Shared
primary Details behavior remains attributed to the previous V1/V2/V3 change.

All four rounds share one 300-second stage deadline, request deadline, cache,
failed-attempt state and acquisition counters. Per-call model cap stays 70 seconds;
optional preparation 30, recheck reserve 20, minimum model startup 30, round cap
120, round reference 60 and finalization reserve 1 remain unchanged. Nearby reserve
comes from the existing 10-second reference-discovery setting. At a fresh
300-second stage, four affordable rounds produce a 75-second first allocation,
with at most 55 seconds for the model before preparation elapsed time. Later
allocations adapt to remaining time. Four maximum-length model calls are not
promised. The whole-request development allowance is still explicitly enabled
600 seconds, never restarted by Repair.

Google total 5/ordinary 4/fallback 1, canonical 12, Routes 6 requests/32 elements,
embedding 1, retrieval 1/Top-K 10, identities 32, output 16384, activity cap 120,
per-object text limits 12000, and all spatial/operating policies are unchanged.
Overflow fails before model dispatch and retains the latest adopted itinerary.

The three Details counters have independent phase ownership, with shared cache and
attempt state. Offline send-boundary tests reach 60/30/30 at their ports, reuse
cached responses for free, count sent failures and stop before the next send.
This does NOT mean today's resolver paths can spend 30: initial RAG has 16 entity
attempts plus at most four fallback-assisted second Details calls (at most 20);
Repair has 12 canonical attempts plus at most one such fallback (at most 13).
Primary also stops when its unchanged successful-supply goal is reached. No
coupled resolution/canonical cap was increased to force spending the larger quota.

### Honolulu saved-material reconstruction and attribution

Read-only source: run `a84b4286-8e9b-4665-a9fd-14e7179e29bc`,
`logs/v3_honolulu_9day_capacity_smoke_20260927/result.json`, SHA-256
`bd636bc6e898a2ce9b4f693119f9d8216479cfa24e36cf3ebb201f5b1c6dba4b`.
The compact regression fixture retains draft/contract/scope/schedule, saved ledger
and six selected historical route elements. The original full matrix was not saved
in this artifact. No replacement routes or operating facts are synthesized. The
post-acquisition ledger is reused, so this is not a replay of historical acquisition.

| Measurement | Historical live | Old scope, saved routes | Scope-only ablation | Actual new preparation |
| --- | ---: | ---: | ---: | ---: |
| Active / deferred targets | 2 / 6 | 2 / 6 | 2 / 6 | 2 / 6 |
| Input identity union | 32 | 32 | 28 | 32 |
| Operation candidate IDs | 30 | 30 | 26 | 30 |
| ADD associations | 156 | 156 | 19 | 22 |
| REPLACE associations | 46 | 46 | 46 | 51 |
| Candidate tokens | 85204 | 85204 | 45488 | 53306 |
| Evidence tokens | 58868 | 23454 | 13277 | 15335 |
| Engineering total | 154653 | 119239 | 68635 | 78511 |

Scope-only ablation filters the same saved authorizations to current legal
operations/dates and recomputes their spatial projection, without new facts or
acquisition. Its reduction is 50604 tokens under identical retained route evidence.
The missing historical matrix accounts for another 35414 tokens in the old-scope
reconstruction; that difference cannot be claimed as a locality improvement. The
new preparation legitimately fills freed optional positions using saved material.
Thus the complete historical 154653-to-78511 delta is not a controlled causal
measurement. New input has 41489 tokens of engineering headroom, not a guarantee
for all requests. The union already reaches 32, so identity capacity is the earlier
bound for additional identities in this fixture.

New input has 14 ADD identities and 30 REPLACE identities (overlapping groups, not
44 independent resources), 73 selected authorization edges, and global matching
capacity 12 against preparation reference 12. The eligible pool has 41 unique IDs
and 94 edges; pool capacity is not the number sent to the model. Its per-operation
pool UNRESOLVED counts are ADD 9/13 and REPLACE 32/40 for the two respective dates;
selected REPLACE counts are 22/29. UNKNOWN remains selectable. The real stage with
mock empty patches can rotate existing candidates for a materially different
second input, then stops on duplicate failed patch, preserving the original draft.
The fixture is not evidence of successful route repair or real model behavior.

### Actual serializer sizing

Commands: `python -B -m tools.diagnostics.repair_payload` and the same command
with `--locality`. Actual DTO, system prompt, strict schema, JSON serializer and
offline o200k tokenizer are used. Every row has system 436, schema 325 and framing
2048 tokens; total is user + 2809. Output remains capped at 16384; synthetic
50-edit output is 2956 tokens, not a completion guarantee.

| Sample | User | Total | Result at 120000 |
| --- | ---: | ---: | --- |
| Honolulu actual new preparation | 75702 | 78511 | Within ceiling |
| Retime only | 1197 | 4006 | Within ceiling |
| C opening retime | 2386 | 5195 | Within ceiling |
| C route reorder, 32 IDs | 54038 | 56847 | Within ceiling |
| C replacement/compensation/move | 40041 | 42850 | Within ceiling |
| B repetition/compensation, 32 IDs | 56860 | 59669 | Within ceiling |
| B adjacent move | 28050 | 30859 | Within ceiling |
| Missing date | 29076 | 31885 | Within ceiling |
| Three-target quantity, 32 IDs | 39758 | 42567 | Within ceiling |
| Round 2 feedback | 39874 | 42683 | Within ceiling |
| Round 3 / Round 4 feedback envelope | 39875 | 42684 | Within ceiling |
| Actual material preparation | 43305 | 46114 | Within ceiling |
| No-op feedback | 43421 | 46230 | Within ceiling |
| Changed time constraint | 43594 | 46403 | Within ceiling |
| Dense conflicting hours / 24 requirements | 93486 | 96295 | Within ceiling |
| Separate near-limit 548-unit text sample | 116954 | 119763 | Within ceiling |
| Separate 550-unit text sample | 117266 | 120075 | Overflow |
| Unchanged historical-size 28-ID pressure | 123178 | 125987 | Overflow |
| Unchanged longer 32-ID pressure | 134738 | 137547 | Overflow |

The near-limit pair is separately constructed synthetic text, not truncation of a
rejected historical input. Original 126k/138k samples remain intact. Round-feedback
sizing measures compact envelope capacity; it does not assert that identical
feedback permits another model call. Actual four-round service tests separately
verify material inputs, partial adoption and unchanged shared accounting.

### Offline execution chronology and limits

1. New minimal real-validator locality tests: **2 failed**, exposing trip-wide ADD
   leakage and candidates incorrectly requested by a retime-only scope.
2. Scope/candidate correction plus locality/B/C tests: **56 passed**.
3. Honolulu saved-material test: **2 passed, 1 failed**. The test incorrectly
   expected one call; existing unpresented saved options legitimately caused a
   different second input. Corrected the assertion, not feedback policy.
4. First V3/config regression: **364 passed, 2 failed**. Besides that assertion,
   an old 60000-word overflow fixture now fit under 120k. Raised only that synthetic
   overflow test's text to 140000 words; preserved actual pressure sizing samples.
5. Focused locality/capacity/wiring: **39 passed**.
6. Expanded locality/Details ownership: **11 passed, 1 failed** (fixture omitted
   RAG stage end initialization); next run **12 passed, 1 failed** (test expected
   ordinary exhaustion to return rather than raise its existing budget exception).
   Both fixed in tests; no shared exception contract changed.
7. Added four-round fake-clock test: **13 passed, 1 failed** because its assertion
   used a nonexistent elapsed field. It now checks authoritative remaining time
   and a single shared deadline.
8. Ruff first pass: 47 findings, 6 import fixes applied, 41 long-line findings;
   targeted formatting resolved the remaining findings.
9. Final affected suite: **407 passed**. This includes all V3 tests (real service
   and graph/runner paths, A/B/C, evidence policy, feedback, cancellation, resource
   cleanup and once-only Nearby), runtime config/cache budgets, initial RAG,
   planning supply adapter, opening-hours and Google adapter regressions.
10. Actual sizing/controlled ablation completed; overflow rows above are expected
    guards, not failed acceptance tests. A subsequent Ruff check passed.

No test supplies real providers. Four-round execution uses real stage/acceptance
with fixture model returns, keeps earlier partial improvements on fourth-round
rejection, and verifies one 300-second stage clock (160 simulated seconds elapsed,
140 remaining). Deferred coverage promotion after confirmed route resolution and
no borrowing of deferred operations are tested. Historical logs, .gitignore and
thesis notes are unchanged. Existing unrelated dirty files remain; nothing staged.

This closes the reproduced locality blocker offline. No new correctness blocker
was found by these checks. Engineering closeout can be prepared, but final freeze
or live validation of this revised configuration is not implied. A separately
authorized bounded live would still be useful to verify real candidate acquisition,
provider input support/latency and priority promotion under the unchanged deadline;
it must not be presented as guaranteed four-round completion or overall quality gain.


### Authorized processing and stage-time alignment (2026-09-25)

The follow-up configuration is implemented and offline-validated: initial RAG
resolution_entities 16 -> 30, Repair canonical attempts 12 -> 30, and Repair stage
300 -> 360 seconds. YAML and typed upper-bound validation agree. Initial RAG
changes apply to V2/V3; Repair changes apply only to V3. This is capacity alignment,
not a new research mechanism or live validation.

Preparation stays 30 seconds, rounds/calls 4/4, model cap 70 seconds, explicit whole
request 600 seconds, Routes 6/32, Google 5, both RAG/Repair Details 30, identity
union 32 and input 120000. All other policies are unchanged. Four rounds share one
360-second maximum stage and acquisition state; the entry request deadline and
Nearby reservation may shorten it. First allocation with a full stage is 90
seconds; preparation reduces the model allowance below its 70-second maximum.
The old 16/12 processing caps no longer prevent reaching the 30-send allowance,
but fallback, cache reuse, input capacity, sufficiency and time can still stop work
earlier. No quota is a requirement to spend or a promise of successful candidates.

Validation sequence: 98 tests passed first (initial RAG, runtime config, Repair
capacity and multiround); targeted locality/material-feedback/graph regression
then passed 53 tests. Ruff passed. No runtime service was called. Prompt, DTO and
serializer were unchanged, so no repeated sizing was necessary. Historical live
records and earlier checkpoint numbers remain historical; no live or freeze is
claimed, and no files were staged or committed.


## Mixed transport and joint components (2026-09-25)

Status: **implemented + offline-validated**. No provider/model/embedding/database calls,
new live, formal evaluation, commit or freeze were performed for this revision.
This checkpoint supersedes whole-round atomic acceptance for independent edit components;
it does not rewrite any historical failed or accepted proposal.

### Actual modules and contracts

- `repair_transport.py`: allowed modes, exact directed options, reuse-first bounded acquisition,
  provisional nearest-anchor preparation, actual continuous-window selection and final display.
- `repair_components.py`: application dependency partition, deterministic component order,
  latest-working-state checks, localized rollback, final global revalidation. Same-day edits,
  moves, concrete visit obligations, compensation and changed cost associations stay together.
  Candidate competition across dates is resolved by subsequent legality checks. A shared
  validation kind alone is not a dependency. At most50 parsed edits/components are processed
  once; no subset search or extra model call is introduced.
- `repair_models.py`, `repair_projection.py`: compact target worksheet, target dispositions,
  transport options and adopted bindings. Input remains `repair_input_2`; projection revision
  is `mixed_transport_components_1`. The model cannot supply route facts or mutate bindings.
- Service, routes, schedule, spatial and feedback integrate component proposals, occupied
  intervals, fair evidence reassessment, stage-original daily load, remaining goals and
  precise rejected-combination attribution. Audit records component edit indices/dependencies,
  working input hash, proposal/report/comparison, decision, budget before/after and elapsed.
- Shared `Itinerary.transfers` and frontend types/renderer add compatible optional presentation.
  V0-V2 missing transfers remain empty. Primary generation DTO/prompt and product selection
  are unchanged. V3 final display and validation use the same binding/route selector; Nearby
  retains primary and transfer data. DRIVE duration and access reserve are separate.

### Effective policy and important limits

Soft priority WALK/TRANSIT/DRIVE; supported explicit restrictions and routing preference win.
WALK <=3km and45min; applicable TRANSIT total <=45min; DRIVE <=30min plus10min application
reserve. Reserve must fit a continuous interval and contributes to daily added90min. Unknown
admission/cost does not negate useful route evidence. Missing routes permit only the existing
WALK <=1km/45min conservative allowance. Existing valid motor evidence bypasses a geographic
prefilter; coordinate distance is not a driving estimate. TRANSIT acquisition uses a concrete
reference departure in preparation and rechecks actual departure after proposal. It does not
invent transit lines/stops or vehicle ownership. Explicit DRIVE retains its reserve even when
that reserve creates a confirmed deficit; traffic-aware preference is not silently downgraded.

All rounds share Routes16 sends/32elements; preparation sends <=16-4=12. Zero reserve disables
reservation; zero route allowance requires zero reserved sends. Preparation cap45s is dynamically
shortened for model/rechecks. Other current limits remain5 rounds/calls,360 stage seconds,
70 per model,252000 input,16384 output,32 input identities, Google6/ordinary5/fallback1,
canonical30, Details30. Request deadline and existing Nearby reserve remain authoritative.

Preparation does not prefetch replacement routes merely because a C target permits replacement.
Pure retime/deletion obtains necessary evidence for actual changed chains. An activated
coverage child in a later round can legitimately prepare its own candidate options. No failure
or evidence counter is refunded when a proposal/component is rejected.

### Actual offline execution order

The following batches overlap; pass totals must not be added as independent coverage.

| Order | Invocation/scope | Actual result and correction |
| --- | --- | --- |
| 1 | `test_repair.py test_multiround.py` initial | 94 passed /12 failed. Stale capacity expectations plus rejected-proposal audit and single-component ID compatibility. |
| 2 | New mixed transport tests | 5 passed. Existing DRIVE reuse, reserve/gap, TRANSIT applicability, independent rejection/adoption and shared reserve. |
| 3 | Repair/multiround recheck | 96 passed /10 failed. Remaining old limits, strict output fixture migration, invalid-proposal absence and new identity competition semantics. |
| 4 | Repair/multiround/mixed | 108 passed /3 failed. Empty patch should preserve a constructed unchanged proposal; failed legality should not fabricate one. Corrected audit distinction. |
| 5 | V3 affected suite | 334 passed /15 failed. Identified unnecessary preparation route acquisition; also explicit WALK-only expectation, UTC serialization, optional transfer output comparisons and old overflow stress scale. |
| 6 | C/wiring/material/API/capacity targeted | 109 passed /1 failed. The remaining assertion wrongly prohibited routes in a later activated coverage-child round; first-round deletion still sends none. |
| 7 | Expanded mixed tests | 9 passed /2 failed. Corrected list-vs-tuple assertion and a synthetic blank day needing two visits, not one, for COMPLETE. |
| 8 | Mixed+C | 36 passed. |
| 9 | New actual `run_v3` mixed graph test | 1 passed. DRIVE binding reaches formal PASS, output, Nearby and resource close path. |
| 10 | Initial Ruff | 80 findings (imports, unused imports, formatting, closure/zip hygiene). Fixed narrowly; formatting pass left3 long strings, then passed. |
| 11 | First actual mixed sizing | 80223 /80368 /80370 tokens for first/second/later projections; retained pressure at224459, rejected254459/274459; output4162. |
| 12 | Frontend transfer renderer | 8 passed. Includes legacy omission, all modes, reserve separation and missing facts/references. |
| 13 | V3 + V0/V1/V2 + shared itinerary/primary DTO/config/references | 560 passed. No external service invocation. |
| 14 | Explicit DRIVE preference/reserve correction: mixed+C+wiring | 68 passed. Traffic-aware evidence remains scoped; 28+10 in35min reports a180-second deficit. |
| 15 | Frontend build and changed-file ESLint | TypeScript/Vite build passed. ESLint first used the wrong working directory (no files matched); rerun from frontend passed. |
| 16 | Sizing recheck and near-limit fixture | Original counts unchanged; protected251459-token sample accepted without truncation. |
| 17 | Full affected V3 after component audit/final checks | 357 passed. |
| 18 | Final mixed/material/B and configuration override tests | 59 passed. No unrelated cost-preserving retime is joined solely for having a price; scope/cost checks remain. Final Ruff passed. |
| 19 | Representative sizing diversified to all three selected modes | Final counts below; this is synthetic sizing, not a five-round live or model-quality result. |

Additional observations: the first local frontend test edit helper used the wrong text
encoding and was rerun with explicit UTF-8. Static checks caught a loop-variable binding
following routing-preference adaptation; it was explicitly bound and rechecked. No failed
live/provider request was generated, and no history was altered to improve a test result.

### Final actual serializer sizing

Command: `.venv/Scripts/python.exe -m tools.diagnostics.repair_payload --mixed`.
Uses the actual DTO, system/user prompts, strict output schema, serializer and offline tokenizer.
The dense synthetic fixture has3 active worksheets,32 identity union (29 operation candidates),
87 directed target options, including WALK, TRANSIT and DRIVE, with route evidence filtered
through the actual projection. No provider ports are supplied. It is deliberately dense,
not a statement that87 options or three queries per candidate will be acquired live.

| Sample | System | User | Schema | Framing | Engineering total |
| --- | ---: | ---: | ---: | ---: | ---: |
| First round | 554 | 77060 | 492 | 2048 | 80154 |
| Second-round compact feedback | 554 | 77205 | 492 | 2048 | 80299 |
| Third/fourth/fifth compact feedback | 554 | 77207 | 492 | 2048 | 80301 |
| Long protected context | 554 | 221365 | 492 | 2048 | 224459 |
| Near ceiling, protection retained | 554 | 248365 | 492 | 2048 | 251459 |
| Explicit overflow | 554 | 251365 | 492 | 2048 | 254459: rejected |
| Larger overflow | 554 | 271365 | 492 | 2048 | 274459: rejected |

First-round diagnostic views: context1107, candidate10398, evidence64688,
requirements/findings840 tokens. These JSON views are not an additive token partition.
The synthetic50-edit/50-disposition output is4162 tokens against16384. This does not prove
that every valid maximum-text completion fits; the actual output cap remains authoritative.
Later-round samples measure bounded feedback shapes, not successful live iterations. Input
ceiling breaches remain fail-closed and preserve latest adoption. No protection was removed.

### Completion and remaining evidence

The independent bad-component/good-component counterexample is closed offline, and a real
service call can adopt multiple independent targets. Same-day invalid members remain atomic;
shared identity competition cannot duplicate a visit. Existing A/B/C protection, source/cost,
fixed time, fair comparison and cancellation tests continue passing. Actual graph mocks verify
mode-aware adoption and final Nearby/resource ownership. This is not retrospective proof that
Honolulu's complete historical failure is fixed.

Remaining limits: conservative same-day grouping; nearest-anchor provisional preparation;
no exhaustive insertion search; no parking/vehicle continuity, fare or public admission
verification; no transit instructions. Exact-time provider support, realistic model dispositions,
latency and joint-component throughput still require separately authorized development live.
A252k ceiling and16 requests are bounded engineering headroom, not demonstrated optimal values.
No new correctness blocker remains in the exercised offline paths; this is not a global proof.


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


## Minimum Daily Coverage checkpoint (2026-09-25)

Implementation and offline validation precede the separately authorized single Honolulu live.
See shared_minimum_daily_coverage.md for the product contract. Generic activities retain
occupancy and unknown location; they are not converted to elastic free_time or false route
endpoints. The system offers authorized gaps but does not guarantee an admissible addition.

Actual offline sequence:
1. Initial targeted suite: 197 passed / 5 failed. Legacy unassessed empty-day fixtures lacked
   executable coverage authority; an overfull graph fixture also contained an unrelated empty day.
2. New minimum/B/Repair suite: 109 passed / 1 failed. Fixed a real comparison adaptation:
   unchanged missing coverage on another day now has comparable magnitude instead of None.
3. Minimum/wiring/multiround: 71 passed / 13 failed, then 83 passed / 1 failed. Existing wiring
   fixtures were made explicit about their unrelated second-day coverage; the remaining fake
   source identity was aligned to actual supplied IDs. No production guard was weakened.
4. Combined minimum/wiring/multiround/B/Repair: 181 passed.
5. Shared/API/schedule suite: 198 passed / 3 failed: incomplete new interpretation fixture,
   old prompt-version assertion and old round-status expectation (0->1 now completes its own
   goal before optional 1->2). Targeted fixes: 50 passed.
6. Shared diagnostics, wire/interpreter/Gate, initial mixed routes, V0/V1/V2 and API: 203 passed.
7. Frontend first launch failed with local Vite temp-file EPERM before tests; rerun with normal
   local filesystem access: 24 passed. No external provider used by any offline test.
8. Ruff initially reported import/format issues; corrected only relevant files (final result below).

Historical reconstruction uses run 8b7db82f-9c52-4cdc-b802-2c273406ee66, preserving its source
SHA-256. The small fixture retains original draft/contract and a reduced identity/location
projection, not all route/opening evidence. Oct 5 becomes the active minimum target; Oct 1
and other ordinary reviews are deferred. Fake empty proposals preserve the generic walk and
stop on no material change. This is offline reconstruction, not historical repair success.

Actual serializer/tokenizer: minimum reconstruction rounds 13074 / 13259 tokens; mixed-mode
32-identity rounds 80283 / 80428 / 80430 / 80430 / 80430. Protected-text stress inputs
224502 and 251502 fit; 254502 and 274502 exceed 252000 and retain overflow behavior. Synthetic
output 4162 / 16384. Diagnostic token groups overlap and must not be summed. Updated
interpretation normal input sum 7071 (excluding provider framing), including strict wire
schema 3464. Sizing is offline, not actual usage. Artifacts: logs/minimum_coverage_offline_20260925/.

Known limits: no new experience identity, public-access guarantee, generic-activity relocation,
TRANSIT coverage, or Preference Gate Step 1 blocker fix. No full-day exemption is inferred
from relaxed or partial fixed occupancy. The new full-day interpretation branch remains
without real-model evidence unless the authorized live actually exercises it.

Final affected C/API-evidence/mixed/B/minimum regression: 111 passed / 2 failed initially.
A real interaction was corrected: an actually activated, narrowly scoped hard-obligation
removal may leave a visible minimum-coverage debt, subject to the existing loss-specific
coverage authorization. Ordinary deletions cannot use that exception. The other failure
was a synthetic second-day visit outside its provider fixture's hours; adjusting its time
alone still failed because Sunday hours were absent. The fixture now explicitly supplies
both days. Intermediate reruns: 112 passed / 1 failed, followed by two diagnostic single-test
failures; final affected suite: 113 passed. Final targeted Ruff passed; frontend production
build passed. These are offline results, not provider or live validation.


### Authorized single Honolulu live: minimum coverage

Run `f9bd621d-0eb5-47d7-8af8-03825d57524b`, records in
`logs/v3_honolulu_9day_minimum_coverage_20260927/`. Reference date 2026-09-25;
request Sep 27-Oct 5, two travelers, USD3000, original relaxed preferences.
Actual deployment gpt-6-luna; three run-local reviews on; repository defaults unchanged.
Unchanged effective limits: five calls, 360s stage, 600s request, 252000/16384 tokens,
32 identities, 24 route requests/32 elements (8 requests reserved post-proposal).

Initial main counts: 2,1,3,2,0,0,1,1,0. Final: 2,2,3,2,2,2,1,2,2.
Round 1 prioritizes Oct1/2/5 minimum targets and adds one visit to each; ordinary reviews
are deferred. Round 2 adds one visit, rejecting the separate Chinatown insertion for
insufficient unoccupied transfer window. Round 3 adds three visits; round 4 adds one
with route UNKNOWN and the existing conservative reserve; round 5 returns empty edits.
Final ACCEPTED_PARTIAL / round_or_model_limit retains all eight accepted additions.
All nine minimums satisfied, Oct3 ordinary quantity review remains. Generic Downtown
activity is unchanged, not counted. Authorized free-time fragments retain their lineage.

Repair engineering inputs: 92975,88896,92730,57565,52605; primary87607. All below252000.
Real Repair input/output usage: 373661/11121, already included in callback464989/18848.
Embedding prompt/total16/16. Ordinary Details32/60 (20 cached qualified), initial RAG
resolution30/30, Details25/30, fallback4/4; no Repair discovery/Details sends.
Routes baseline6/324, initial alternatives18/18, Repair24/24 requests/elements.
Repair includes one HTTP400/ProviderHTTPError and three later pre-send budget stops;
no retries or additional run. Final opening16 PASS/3 UNKNOWN; route9 PASS/1 UNKNOWN;
visitor suitability19 UNKNOWN, budget1 UNKNOWN, semantic requirements1 UNKNOWN,
quantity1 NEEDS_REVIEW, zero CONFIRMED. These include the generic area where applicable.

Nearby one stage, three requests, three references; final primary fields unchanged.
Source hashes unchanged; request-owned RAG reports closed. Exit0, process200.969s.
Exact model request strings are not separately captured; full result DTOs and extracted
rounds are authoritative over truncated trace previews. Per-round deadline/remaining
values are not elapsed measurements. No independent socket-level close audit is claimed.

Status: implemented + offline-validated + bounded development-live-validated for the
observed 0->1 priority/repair path. Review-off behavior, exemptions, unassessed restrictions,
and hard-removal coverage-debt exception retain offline evidence only. No benchmark,
freeze, whole-trip feasibility or historical repair claim. Existing Preference Gate Step1
contract mismatch is unchanged and was not exercised by this successful normal input.
