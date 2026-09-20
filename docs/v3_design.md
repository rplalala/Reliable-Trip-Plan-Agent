# V3 validation and targeted repair roadmap

Status: design scope approved for documentation on 2026-09-20; runtime, schemas,
validators, repair prompts, budgets and runner are **not implemented**. This is the
single V3 design/scope/TODO entry point. Exact thresholds and implementation require
separate approval. No formal evaluation is authorized by this roadmap.

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

## Conceptual structured findings (not production schema)

Each future finding should express violation_id, violation_type, severity/priority if
needed, affected date, activity IDs, place IDs, related requirement IDs, evidence refs,
status (confirmed, probable, unknown/insufficient_evidence), repairability and suggested
repair scope. UNKNOWN entries should be findings of uncertainty, not confirmed violations.
Names/enums, severity ordering, evidence sufficiency and repair authorization remain
future design decisions. No production violation model is added in this package.

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

Approve finite repair rounds, additional candidate searches, additional Details,
route rechecks, Web/evidence work, model repair calls and a global deadline before
implementation. Numerical values remain undecided. Reuse compatible evidence and
record failed attempts; no hidden retry or unlimited search to fill a quota.
Propagate user cancellation. Preserve the initial draft and return partially repaired
with remaining findings when budgets, evidence or repairability prevent completion.

## Re-validation

Re-check repaired findings and global date, identity, REQUIRED/EXCLUDED, duplicate,
opening, route, overlap, coverage and budget invariants. A repair is not success until
the applicable checks are rerun. Retain unresolved UNKNOWN and record new conflicts
introduced by repair. Exact dependency-based recheck scope is still a design task.

## Future TODO (all unimplemented)

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
