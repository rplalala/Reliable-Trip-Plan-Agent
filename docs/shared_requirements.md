# Shared structured input and semantic requirements

## Implemented sourced semantic extension — 2026-09-26

The existing interpreter now uses preference_prompt_16 / preference_draft_10 and emits interpreted_requirements_4. Sourced ExperienceGoal distinguishes one-off/continuing/exact/minimum intent, category/named-place scope, distinct dates, themes and explicit primary exceptions; named VisitRequirement retains the authoritative identity/count/date protection. Older version-3 inputs remain readable and multiplicity remains unassessed. No second interpretation call or keyword classifier was added. See the [checkpoint](shared_poi_semantics_plan.md#12-implementation-checkpoint--2026-09-26) for migration, tests and evidence limitations.

## Soft quality preference boundary (2026-09-26)

Prompt 16 clarifies that ordinary rich/varied/enjoyable/memorable trip wishes remain
source-linked soft semantics, without invented counts, exclusive themes, luxury
spending or feasibility guarantees. Missing a measurable quality threshold alone
does not require clarification. D's mountain preference, one-off zoo goal and rich-trip
wish should coexist under VALID/CLEAR absent another issue. Actual missing mandatory
references, hard contradictions, unsupported scope and safety issues still block.
The same instructions apply to V0-V3. No schema, application gate or budget changed.

The captured D prompt-15 misclassification remains a historical mismatch fixture:
replaying that frozen model output still blocks by design. Controlled SDK/service
tests validate handling and prompt delivery, not real-model compliance. D requires
a separately approved captured live retest before claiming observed improvement.
The subsequent prompt-16 D retest passed this input boundary once but failed at the
downstream POI semantic evidence boundary; it did not validate final itinerary quality.

## POI semantic evidence references and development capture (2026-09-26)

`poi_semantics_prompt_2` now explicitly requires both assessment and match evidence
references to copy the same candidate's exact `source_ref`. Requirement IDs, other
candidate sources and invented field paths are invalid. Supported matches require
evidence; other relations may leave references empty but cannot use invalid ones.
This does not relax membership checks or turn a syntactically valid citation into
proof of support. The data contract stays `poi_semantics_1`; request prompt 16 is unchanged.
Semantic snapshots and calls carry prompt revision/hash; cache keys include prompt text.

The development acceptance entry has a separate default-off `--capture-semantics` flag.
With approval for live execution, it may be combined with `--capture-requirements`.
It writes normalized input, schema-valid output before membership validation, and
outcome under `semantics/`, correlated by call ID, batch number, input hash and prompt
fingerprint. It does not save raw provider envelopes or recover malformed SDK output.
Match-reference errors include bounded candidate/requirement/relation and allowed vs
offending references, capped at 256 characters per identifier and eight offending refs.
Capture uses existing secret redaction, a 1 MiB per-artifact and 4 MiB per-case limit.
Write/size failures are reported separately as incomplete evidence and do not alter
application decisions or trigger another model call. Capture remains development-only;
normal trace may retain bounded error details but not these input/output artifacts.

## Named-visit representation correction (2026-09-26)

`preference_prompt_15` explicitly prioritizes `named_places` + `visit_requirements`
for executable named-place counts and dates. Exactness remains in those fields;
the same obligation must not also become an unsupported hard semantic requirement.
Category goals still use `experience_goal`, and independent non-negotiable meaning
(such as a guaranteed absence of queues) remains hard even in the same sentence.
No schema change, semantic-text equivalence classifier or hard-gate bypass was added.
The prior C failure motivates the change, but its original interpreted draft was
not retained. Offline tests cannot establish that a real model now follows the prompt.

The development-only `tools.validation.poi_semantics_acceptance` entry requires
`--execute` to run one case in a new output directory. `--capture-requirements`
explicitly enables normalized draft and outcome capture using the existing secret
redaction component; it is disabled by default and does not enable raw provider
payload tracing. Draft and canonicalization records share a call ID and input,
prompt and runtime-config fingerprints. Capture errors retain the application's
exit code, mark evidence incomplete and never trigger another interpretation call.
Trace disabled/unavailable states are distinguished. This entry is sequential and
uses scoped CLI factory hooks; it is not an application-server or parallel runner.

After separate live authorization, usage is:

```powershell
.venv/Scripts/python.exe -m tools.validation.poi_semantics_acceptance --input-json <request.json> --output <new-case-directory> --rag-env-file .env.tripworld --capture-requirements --execute
```

Use a new directory under ignored `artifacts/` or `logs/`; the tool stores `request.json`,
`manifest.json`, the effective runtime snapshot, result/stderr, `execution.json`,
optional `requirements/` records and file trace. Successful runs also receive a real
Product projection without an introduction-model call. `completed_pending_review`
is not automatic acceptance. The tool processes one case only; inspect its outcome
and capture health before any separately authorized next case. Existing output
folders are rejected rather than overwritten or silently retried.

## Authoritative form and dates

Current PlanningRequest uses planning_request_2. Destination, date-only start/end, strict positive
traveler count and whole-trip Money are mandatory. Money is a finite non-negative Decimal with
explicit uppercase three-letter currency; boolean amounts are rejected. Empty/null/whitespace
preferences become empty; nonblank text is preserved. Additional preferences are bounded at
24,000 characters and 8,000 engineering tokens. request_id is optional. End cannot precede start.
The selectable window contains 14 calendar dates, from trusted today through today+13 inclusive.
Trip duration is independently limited to 1-10 inclusive days. The trusted date uses the configured
application time zone (currently Australia/Sydney), not the browser or destination clock.
Product requests cannot supply the CLI's research reference-date override.

## One interpretation and canonical identity

Nonempty preferences receive one shared interpretation; empty preferences skip the model.
Form facts are never converted to prose for re-extraction. Conflicts are reported, not used to
override the form. Current canonical contract is interpreted_requirements_3. Historical _2
records retain their original meaning. Model handles (up to 256 characters) are temporary;
application-owned canonical identities are independent of V1/V2 and discovery provider.
Attribution distinguishes party, specified people/subgroups, and unresolved targets. first_ref
does not confer priority. Unknown links fail; empty attribution is not silently made party-wide.

## Open text with structural bounds

SemanticRequirement contains requirement_id, normalized_text (up to 320 characters), kind
(preference/constraint/goal), polarity (favor/avoid), strength (low/medium/high/hard), scope
(individual_poi/selected_poi_set/whole_trip/itinerary_style/transport), subjects and source_refs.
The vocabulary of normalized_text remains open; it is not a fixed interest taxonomy.

Draft bounds: 24 semantic requirements, 24 named intentions, eight subjects, eight discovery
intents, 32 requested-place-information items, 120 linked experience requests, six operational
conflicts and eight extraction issues. Each item has one to three source quotes of at most 320
characters plus occurrence; canonical references retain validated offsets and match mode.
Each semantic item has up to nine canonical subject references. DiscoveryIntent links one to four
requirements, contains at most 200 characters, and has activity_or_category or semantic_discovery
purpose. Runtime query work has its own smaller limit. Source integrity does not itself prove
semantic interpretation correct. Deduplication rewrites links without double reward.

## Operational meanings and enforceability

Named place text (up to 160 characters) retains REQUIRED/OPTIONAL/EXCLUDED; the model cannot invent
Google identity. RequestedPlaceInformation and transport remain typed because acquisition/routing
have mechanical meanings. Experience requests use evidence-specific dimensions with up to three
preferred and avoided values, dimension membership, uniqueness and disjointness checks. They do
not define the whole semantic preference vocabulary or turn category priors into experience facts.

The application owns RequirementAssessment. Current assess_requirements assigns evidence_assessment
for linked review requests and semantic_only otherwise, initially not_acquired/unknown. There is
no registered predicate certifying arbitrary open text. HARD semantics receive clarify and trigger
unsupported_hard_requirements; soft requirements advise. Explicit REQUIRED identity resolution is
a separate operational boundary. Neither an LLM belief nor UNKNOWN can certify satisfaction.
No downstream keyword/regex reinterpretation of raw preferences is introduced.

Source owners: schemas/request.py, schemas/interpreted_requirements.py,
schemas/requirement_boundary.py, policies/interpreted_requirements.py,
services/preference_interpretation.py and the Foundry DTO/mapping. Migration evidence belongs to
[development_record](development_record.md), not this design contract.


## Calendar support versus same-day remaining-time planning

Current trip_dates admits today through today+13, with end-start+1 <=10. The shared validator
serves V0/V1/V2, CLI and development runners; capacity depends on duration, not departure offset.
GET /api/planning/date-window publishes the server's bounds without initializing any model/provider.
The frontend end-date maximum is min(start+9, allowedEnd); backend submission validation is authoritative.
The developer page initializes its explicitly editable research reference date from the same endpoint.
Unavailable date-policy loading disables product submission; no browser-local fallback is guessed.

Same-day remaining-hour planning remains unsupported. Accepting today's date does not claim that
past hours will be avoided. The earlier proposal for future evaluation (start >= reference+2)
was constrained to eight days under the old +9 window. That arithmetic is historical: delayed
10-day trips now fit. No formal evaluation protocol is implemented or authorized by this extension.
The historical Sydney ten-day smoke and its original checkpoint remain unchanged.

## Default generation objective versus user requirements

The shared 2-5 main-POI/full-day objective is application generation guidance, not a new
user HARD requirement or semantic extraction rule. Explicit pace/rest and long REQUIRED
visits may justify fewer visits. Diagnostics preserve linked semantic requirement IDs
without interpreting raw words or converting target misses into clarification or failure.
Same-day remaining-hour feasibility is still unsupported. Named and HARD boundaries
are unchanged; REQUIRED count above 16 still reports a capacity conflict.
