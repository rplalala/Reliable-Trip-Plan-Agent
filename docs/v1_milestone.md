# V1 milestone checkpoints

## Latest accepted boundary - 2026-09-20

V1 quality_first_1: 24 ordinary successes, 24 compared, 12 supplied, eight scheduled. Nearby remained independent.

Status: implemented + bounded development-live-validated where covered, not production-ready, formal benchmark or automatic re-freeze. Current explicit configuration is quality_first_1 with 160k input guard and 16,384 output. This does not rewrite earlier frozen configurations. Exact implementation/config hashes, offline history, live inputs, failures, artifacts and limitations are maintained once in the [joint event](development_record.md#m-e07748f66be8). Reviews/Profile and ten-day K16 live were not covered; unknown Web reasoner usage stays unknown. No new validation is performed by this migration.

Dated records below preserve original scope, status and evidence; they are not current runtime instructions. Current design is maintained separately. Proposed or unexecuted steps remain unexecuted unless a later explicitly identified record establishes otherwise.

<a id="m-aee7853a6b50"></a>
## V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze

_Source context: original document introduction/navigation. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._



<a id="m-53d332da0236"></a>
## Reopened B2 development checkpoint - 2026-09-19

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-53d332da0236-0"></a>

B2 now implements the active revised V1 path. B1 is retired after the user's explicit
architecture decision. **V1 is not re-frozen. No B2 live validation has occurred.**
Current architecture: [V1 design](v1_development.md) and [POI selection](development_record.md).
Offline results/cleanup: [B2 checkpoint](v1_selector_experiments.md). The three-flow chronology
and reasons are in [POI selection evolution](development_record.md).

<a id="b-53d332da0236-1"></a>

All freeze/validation statements below are historical, including QCGRE descriptions.
V0 and accepted TripWorld Phases 1-5 are preserved; Phase 6 integration remains paused.

<a id="m-ea14c5d6fc29"></a>
## Current Status and Historical Scope

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ea14c5d6fc29-0"></a>

**Original V1-A freeze: explicitly approved on 2026-09-12.**
**Revised V1-A: implemented, development-live-validated, and explicitly re-frozen
on 2026-09-14.**
**Complete V1: explicitly FROZEN on 2026-09-15 after final offline and
cross-country development live validation.**

<a id="b-ea14c5d6fc29-1"></a>

The sections below beginning with "Historical Execution Flow and Comparability"
record the 2026-09-12 as-built checkpoint and its acceptance history. Their
shortlist-first flow, masks, budgets, test counts, and limitations are historical
facts, not the revised selection design or current V1-B completion status.
The revised implementation and final V1 status are recorded separately below.
Actual code remains authoritative for implemented behavior; `docs/v1_design.md`
describes the current architecture.

<a id="b-ea14c5d6fc29-2"></a>

After the original freeze, V1-A was intentionally reopened for Google-backed
rating/review evidence and POI-selection realignment. The revised implementation
progressively narrows candidates, acquires ratings and reviews selectively,
normalizes reviews into `ExperienceProfile`, and selects the final POIs
deterministically. `rating` remains separate from the Profile. The revised path
does not request or use `userRatingCount`; its appearance in a historical mask
below is a record of the original implementation, not current behavior.

<a id="b-ea14c5d6fc29-3"></a>

The former V1-C milestone is retired. Its Places-review responsibility is folded
into V1-A because it affects POI selection. Reddit/TripAdvisor acquisition is not
part of the current approved rating/review direction. V1-B supplements final
selected POIs with official/current evidence. Its accepted Phase 1/2 subsystem
and Phase 3 graph/planner integration are now implemented.

<a id="b-ea14c5d6fc29-4"></a>

The earlier code-based V1-B compatibility assessment in `docs/v1_design.md`
identified integration-only impact (category B); Phase 3 subsequently supplied
the needed projection and graph/planner wiring. Frontend rating/review display
is still not implemented. Later typed semantic extraction and V1 cost projection
are recorded as post-checkpoint changes below.

<a id="b-ea14c5d6fc29-5"></a>

At the original checkpoint, V1-A asked whether normalized live Places, Weather,
and Routes evidence improved the otherwise comparable V0 planner. It implemented
neither Places review enrichment nor official Web Evidence. It included no RAG,
general feasibility-validation/repair loop, or persistent evidence database. The
following record is implementation history, not a formal research conclusion.

<a id="m-9f6bee49adbc"></a>
## Revised V1-A Implementation and Re-Freeze (2026-09-14)

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._



<a id="m-517f004f06d7"></a>
## Weather, Routes, and Evidence Boundary

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Revised V1-A Implementation and Re-Freeze (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-517f004f06d7-0"></a>

Weather remains one Daily Forecast request for the provider horizon, normalized
strictly to requested trip dates. The complete directed baseline Route Matrix
supports `N <= 16` final POIs, with at most **64 elements per request**, **256
baseline elements per run**, and **four baseline calls**. Consecutive origin
chunks retain all destinations; N=16 uses four 4 x 16 chunks rather than dropping
POIs. Partial or unavailable elements remain explicit.

<a id="b-517f004f06d7-1"></a>

An explicitly supported transport mode does not automatically fan out. Default
WALK uses deterministic directed triggers: distance > 3,000 m, duration > 2,700
s, or `ROUTE_NOT_FOUND`, excluding same-place cells. Triggered directions collapse
to logical unordered Place-ID pairs ranked by the more severe directed result.
Sparse TRANSIT acquisition uses one canonical Place-ID direction per selected
pair, bounded by the normal eight logical-pair/eight-call limits; it does not
issue a second full matrix. A provider-observed TRANSIT duration may supply a
reverse **duration-only** `mirrored_reverse_estimate`. The reverse is never
described as provider-measured, and canonical unavailability creates no
fabricated reverse duration. These are representative transport signals, not
line, station, fare, or timetable evidence.

<a id="b-517f004f06d7-2"></a>

The V1-B Phase 1/2 Official Web Evidence subsystem was independent at the
V1-A re-freeze checkpoint. Later Phase 3 integration consumes the final aligned
candidate/structured-evidence projection; Profile objects do not enter the Web
engine or itinerary prompt. Accepted/effective official evidence can now affect
itinerary generation. The former V1-C is retired.

<a id="m-424645500d4f"></a>
## Development Validation and Re-Freeze

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Revised V1-A Implementation and Re-Freeze (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-424645500d4f-0"></a>

These live runs checked integration behavior; they are **not formal benchmarks**
or statistical reliability results.

<a id="b-424645500d4f-1"></a>

- Smoke A first selected Sydney Opera House while its required named identity
  remained unresolved. Typed `NamedPlaceIntent` and exact Place-ID
  reconciliation were implemented and covered offline. The identical Smoke A
  live re-validation then resolved one Opera House Place ID, set `must_visit=true`,
  and removed the `required_place_unresolved` conflict.
- Initial Smoke B showed that a shared three-call candidate search budget left
  six explicit interests out of Q/C metadata. The N=16 chunked Routes path
  succeeded and the planner accepted that large integrated request.
- The identical revised Smoke B re-validation used destination search **1/1**
  and candidate search **9/12**: all nine supported explicit intents were
  generated and executed. It recorded 123 raw search observations and 85
  unique Place IDs before `C_raw`; effective pools were `C_raw=36/36`,
  `R_pool=18/18`, final POIs `16/16`, and review/Profile `6/6`. Retrieved review
  evidence changed one final POI membership. Routes used
  four 4 x 16 WALK baseline chunks (256 elements); structured itinerary
  generation and final date validation succeeded.

<a id="b-424645500d4f-2"></a>

The revised V1-A checkpoint passed **507 backend tests** and Ruff lint.
Standalone V0 and V1-B Phase 1/2 compatibility checks passed. The identical
Smoke A and revised Smoke B live checks supported the user's explicit
2026-09-14 V1-A re-freeze. These checks do not prove that generated
itineraries always obey every supplied feasibility fact. The later full-V1
regression and Web integration are recorded in the next section.

<a id="m-2c74a8837355"></a>
## Known Limits and Pending Work

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Revised V1-A Implementation and Re-Freeze (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-2c74a8837355-0"></a>

Provider-display-name aliases are not fuzzily resolved. The bounded candidate
search budget may leave additional supported intents `budget_not_attempted`.
Places reviews are a small qualitative sample; Profile interpretation remains
model-dependent despite application provenance checks. Regular opening hours
are only a baseline, and some POIs have unknown hours. Selective TRANSIT covers
only bounded logical pairs. The generator may still imperfectly follow route,
hours, or other supplied evidence. V1 does not perform post-generation general
feasibility validation, targeted repair, or re-validation; that mechanism
belongs to V3, not a V1-A loop.

<a id="b-2c74a8837355-1"></a>

Frontend rating/review presentation remains future work: for a final-itinerary
POI, a future Product UI may show only an actually acquired Places rating and,
when available, one concise retrieved-review-derived Profile summary. It must
not invent either or display `userRatingCount`. Full V1 was still unfinished at
this V1-A checkpoint; later V1-B completion is recorded below.

<a id="m-892dce9c65be"></a>
## Final V1-B Integration and Development Validation (2026-09-14)

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._



<a id="m-655d46786997"></a>
## Implemented Boundary

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Final V1-B Integration and Development Validation (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-655d46786997-0"></a>

Phase 3 integrates the accepted Phase 1/2 official-evidence subsystem after
final V1-A selection, Weather, and Routes. It projects final selected Place IDs
and aligned structured Places evidence, preserving typed named/must-visit IDs
and trip-relevant opening-date conflicts. Rating is removed from the official
Web projection; raw reviews and `ExperienceProfile` remain selection-only.

<a id="b-655d46786997-1"></a>

The deterministic trigger creates Web tasks for explicit unresolved official
information needs or concrete decision-relevant operational/date risks. It no
longer creates a proactive exception check for every selected POI. Required
explicit gaps rank first, followed by other named explicit gaps, then concrete
risks for required, other named, and remaining selected POIs. Task identity and
trace reasons are retained, with a normal budget of six Web tasks and six
logical page fetches. Sufficient structured facts do not receive parallel Web
re-verification; weather and routes are never re-checked through this path.

<a id="b-655d46786997-2"></a>

Luna native search exposes bounded observations. Optional PageRetriever fetches
observed official pages when native evidence is insufficient. EvidenceReasoner
proposes scoped candidates from supplied source text; the deterministic Gate
checks authority, source support, subject/scope, and applicability before
creating `OfficialCurrentEvidence`. Resolver composes accepted evidence with
structured facts by date and requested facet. The planner receives only
accepted/effective facts, source references, statuses, and explicit uncertainty,
not raw search URLs/snippets or rejected claims. Absence of a discovered
exception does not establish that no exception exists.

<a id="m-ef4b3e905335"></a>
## Known Limits and Freeze Boundary

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Final V1-B Integration and Development Validation (2026-09-14). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-ef4b3e905335-0"></a>

Aliases such as `MCA` are not fuzzily expanded. Weather and Routes guide
scheduling but do not cause V1 POI re-selection. A selected POI is not
necessarily scheduled by the LLM unless the request or current contract
requires it. The planner can still imperfectly apply supplied hours or route
facts because V1 has no general itinerary validation/repair loop.

<a id="b-ef4b3e905335-1"></a>

One targeted Reasoner response was `incomplete` due to `max_output_tokens`;
truncated JSON caused that source assessment to fail safely while other
sources/tasks continued. Subject binding is deliberately conservative and can
reject plausible claims. Bounded Web/Page acquisition and facet-specific
sufficiency can leave an information need `UNKNOWN`. The earlier
`unsupported_price_field` rejection lacks recoverable cause; a later free
general-admission claim succeeded and Resolver derived fee 0 without changing
the Gate contract. No retry, repair, relaxed parsing, or Gate bypass was added.

<a id="b-ef4b3e905335-2"></a>

At this Phase 3 checkpoint, full V1 implementation and targeted live validation
were complete, but freeze still awaited the later semantic and cross-country
checks. The final complete-V1 freeze is recorded in the next section.

<a id="m-14725ce9982f"></a>
## Complete V1 Freeze (2026-09-15)

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._



<a id="m-1206d3d4abe0"></a>
## Final Implemented Boundary

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Complete V1 Freeze (2026-09-15). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-1206d3d4abe0-0"></a>

One V1 requirements LLM call now returns unchanged base `TravelRequirements`
plus bounded `NamedPlaceIntent`, `RequestedPlaceInformation`,
`ExperiencePreferenceIntent`, typed transport preference, and `PoiInterest`.
The LLM interprets the user's natural-language meaning; deterministic code
validates schemas, enums, copied source spans, and Place identity before using
the typed contracts. The active V1 graph has no raw-text keyword/regex semantic
fallback for these meanings. V0 retains its original requirements contract and
independent execution path. EvidenceReasoner separately interprets what acquired
official source text actually says; it does not reinterpret the user request.

<a id="b-1206d3d4abe0-1"></a>

The final V1-A path performs multi-intent Places discovery, dynamic
`C_raw → R_pool → K_final` narrowing, structured Details/rating enrichment,
selective decision-sensitive reviews and retrieved-review-only
`ExperienceProfile`, then deterministic `Q_rel + C_cov + G_geo + R_rating + E_exp`
selection. `CLOSED_PERMANENTLY` is excluded; `CLOSED_TEMPORARILY` and uncertain
`FUTURE_OPENING` retain explicit date risks where eligible. Current hours apply
only within their supported window; regular hours are a baseline, not proof of
special-date availability. Weather informs scheduling but not POI reselection.
Routes acquire the complete directed baseline for final POIs, chunked to at most
N=16 and 256 baseline elements, plus bounded selective TRANSIT. Measured routes
remain distinct from mirrored-reverse duration estimates, and `not_observed`
remains distinct from an observed `ROUTE_NOT_FOUND`.

<a id="b-1206d3d4abe0-2"></a>

After selection, the V1-B trigger uses explicit unresolved **typed** information
needs, structured residual gaps, and concrete operational/date risks. It does
not broadly Web-check all selected places or repeat sufficient structured,
Weather, or Routes evidence. The bounded path is Luna native Web acquisition →
optional PageRetriever when support is insufficient → EvidenceReasoner →
deterministic Grounding / Evidence Acceptance Gate → claim-scoped Resolver →
accepted/effective evidence and explicit uncertainty in the planner. Raw Web
observations and rejected claims do not become planner facts. No found exception
never means that no exception exists.

<a id="b-1206d3d4abe0-3"></a>

Shared `Money` remains point-valued and `Activity.estimated_cost` remains
optional. The V1-only Foundry mapping preserves valid points, projects a clear
finite same-currency two-endpoint numeric range to its Decimal arithmetic
midpoint, and sets unsupported optional costs to `null`. It adds no planner LLM
repair call and does not change V0. The midpoint is an itinerary estimate, not
accepted official admission-price evidence.

<a id="m-a2037fa14ec6"></a>
## Frozen Scope and Known Limits

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze / Complete V1 Freeze (2026-09-15). Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-a2037fa14ec6-0"></a>

Provider search relevance does not guarantee visitor suitability: the Melbourne
architecture interest yielded professional-service firms. V1 has no explicit
tourism-suitability validator or post-selection repair. Named-place alias
resolution stays conservative without broad fuzzy expansion. Weather and Routes
guide scheduling, not POI reselection. A selected POI need not be scheduled
unless required by the current contract. Official Web facets can legitimately
remain `UNKNOWN`; PageRetriever may encounter inaccessible pages, Reasoner
structured output may truncate and safely degrade, and conservative
subject/scope binding can reject plausible claims. V1 has no V3-style explicit
feasibility validation, targeted repair, or re-validation. V2 RAG and V3
validation remain future directions, not implemented solutions to these limits.

<a id="b-a2037fa14ec6-1"></a>

The user explicitly approved the **complete V1 milestone freeze on 2026-09-15**.
This does not rewrite the original 2026-09-12 V1-A freeze or the revised
2026-09-14 V1-A re-freeze. V2 has not started.

<a id="m-1f52839e92c1"></a>
## Live Discoveries, Follow-Up Fixes, and Known Limits

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-1f52839e92c1-0"></a>

The following were post-design discoveries, not capabilities present in the
initial V1-A proposal:

<a id="b-1f52839e92c1-1"></a>

- **Provider/runtime defects fixed:** real Places `timeZone` is an object with
  `id`/`version`, so normalization extracts its IANA `id`; Weather requests
  the full provider ten-day horizon and then filters to requested dates;
  credential-bearing Google URLs visible in HTTP INFO logging prompted
  console URL redaction and regression tests.
- **Approved architecture follow-ups:** the initial one-mode WALK route design
  evolved first to selective directed alternatives, then to logical-pair
  collapse, stable canonical TRANSIT direction, one observed element per
  logical pair, and labeled mirrored reverse duration. Runtime configuration
  moved from scattered `.env` budget/trace policy to centralized hard limits
  plus one strictly validated global YAML file.
- **Prompt-level evidence-use follow-ups:** live generation exposed incorrect
  route-number attribution across Place IDs and a visit scheduled before
  supplied opening hours. V1's generation prompt gained exact route-pair ID
  matching and whole-visit opening-hours instructions; a later approved edit
  compressed repeated wording without intentionally changing these rules.
  These are model instructions, not deterministic feasibility enforcement.

<a id="b-1f52839e92c1-2"></a>

Unresolved limitations remain explicit:

<a id="b-1f52839e92c1-3"></a>

1. Evidence-following is not guaranteed. In the Sydney follow-up, matching
   WALK evidence required about 28 minutes while the generated schedule
   reserved about 15. V1-A supplies evidence but does not perform deterministic
   post-generation transfer-feasibility validation. The planned V3 mechanism
   is generation -> explicit validation -> targeted repair -> re-validation;
   none of that is implemented in V1-A.
2. Places-only discovery/selection can surface weak activity candidates. A
   `lodging`-typed place was used as a stop although accommodation was not
   requested. This POI relevance limitation was not redesigned during freeze.
3. TRANSIT is a representative duration at one departure time, not exact
   timetable, route, service, station, or fare evidence.
4. A `mirrored_reverse_estimate` may differ from the actual reverse duration;
   its duration is a planning proxy, not a provider observation.
5. At this checkpoint, V1-A had neither official/current Web Evidence nor
   review-derived experience evidence. Those were then planned as V1-B/V1-C;
   the current reopening above supersedes that milestone allocation.

<a id="m-541d26ddaba4"></a>
## Verification and Freeze Boundary

_Source context: V1 Milestones: Historical V1-A Checkpoints and Complete V1 Freeze. Preserved dated record; original acceptance/proposal status applies to this event, not to current runtime instructions._

<a id="b-541d26ddaba4-0"></a>

The final complete live V1 flow completed through Places, Weather, Routes,
Foundry generation, and final date validation. The latest backend offline
regression run after the approved prompt compression reported **158 passed**;
Ruff and `git diff --check` passed. Normal automated tests use fake providers
and do not call live external services. The full live run preceded the final
prompt-only follow-ups; no additional full live flow is claimed afterward.

<a id="b-541d26ddaba4-1"></a>

The 2026-09-12 freeze did not authorize subsequent V1-B or former V1-C work,
a commit, a push, a merge, or a formal benchmark. V0 and V1 remained independently
runnable; V2/V3 were not implemented or frozen at this checkpoint. Later
reopening, implementation, re-freeze, and full-V1 development validation are
recorded separately above and must not be read back into this original
checkpoint.
