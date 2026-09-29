# Batch intake and independent projection contract

Status: Ticket 01 specification closed; subsequently implemented under user approval and validated offline on 2026-09-29. See ticket-01-acceptance.md for scope and the platform-dependent skip. Not benchmark frozen.
Date: 2026-09-29.
Inspected checkpoint: 364f91f05f01328266bfb00c5b75885242d93d7d; clean working tree before this documentation pass.

## Scope and inspected facts

This contract specializes the artifact and activity-scope contracts for Ticket 01. It defines projection, not identity resolution, oracle collection or metric verdicts. Existing accepted scoring semantics remain unchanged.

The public Activity supplies role, activity_id, title, optional place_name/source_place_id/location, start/end, costs and notes. It has no structured travel mode or transport endpoint activity references. Transfer supplies endpoint activity IDs, claimed place IDs, mode, departure, optional arrival, provider duration, reserve and internal validation fields. The itinerary schema does not itself validate that Transfer endpoints exist, are adjacent or match the place claims. Activity IDs are unique only within an itinerary.

V0's prompt uses transport activities with mode/endpoints in title or notes and labels estimates. V1's prompt delegates final Transfer construction to the application. Therefore neither representation can be mandatory across all versions. Application output/schedule helpers use candidate membership, generation provenance or interpreted requirements; their judgments cannot be reused by this projector.

Inspected code: public itinerary/planning schemas; V0/V1 prompts; shared initial route binding; itinerary_output and itinerary_schedule policies; V3 state. Source paths are recorded in the existing input-contract review. A lookup initially used the wrong services directory for policy files; file discovery located them under policies before review. No code was executed.

## Intake result and parsing boundary

Accept one explicitly selected batch. Emit material_diagnostics, inventory, projection_diagnostics and track_availability. A material error returns needs_material_correction for the submitted batch; do not silently evaluate a smaller cohort. Projection uncertainty does not revoke benchmark qualification. No producer runner, validator, requirement interpreter or workflow-completion check is invoked.

Fatal material errors: unreadable/ambiguous JSON (including duplicate object keys), missing mandatory input/result/RequirementSpec or required usage envelope, incorrect hashes or group/run/version linkage, unsupported artifact major version, path escaping the resolved batch root (including links/junctions), non-object itinerary, absent/non-array days or activities, non-object activity, missing/non-string required activity identifier/title, nonunique activity IDs or nonunique/unreadable declared day dates. These prevent stable interpretation; do not reconstruct them. A confirmed multi-POI visit block is an existing delivery-contract diagnostic, not a request to split it.

A declared unavailable usage envelope is valid and disables only resource measurements. Missing optional V3 draft/final-primary projections disable paired analysis; never reconstruct them from the selected final. A malformed optional projection records its own unavailable reason without replacing the selected final.

Use a versioned evaluation wire reader rather than running every product validator. itinerary_1 (including historically absent output_version) and itinerary_2 are explicitly recognized; original absence remains recorded. Missing historically optional roles become unknown in the derived view; missing optional transfer/reference arrays become empty with an absent-field marker. Preserve additional result fields without exposing them to quality readers. Unknown major versions require adapter support, not guessing.

Representable content issues remain diagnostic observations: date gaps, empty activities, unsorted records, overlap, output-versus-request date/destination discrepancy, unknown roles, invalid/missing time values, uncertain timezone, unknown place association and bad Transfer links. Do not silently repair, reject for low quality or use current live-request date limits. Retain source records even when dependent metrics cannot judge them. Original request hashes and producer-attested linkage establish which Input was run; a content discrepancy alone does not prove a wrong-file submission.

## Stable source identity and reader separation

A source reference is (batch_id, group_id, run_id, artifact_sha256, JSON pointer). Derived record IDs use this tuple and projection-contract version, not canonical place ID. Preserve original array positions, declared day, original activity ID and raw values. Sorting makes a separate view; it never changes source pointers. Same activity IDs in draft/final or two runs do not imply correspondence.

Quality view exposes itinerary fields, reviewed requirements and later independent records only. Planner requirements, supply, RAG origins, validation findings, cost projections, route diagnostics and Repair records remain outside it. Preserve Transfer mode, endpoint/time/duration claims as claims; validation_state, unknowns, evidence_refs, mode_source and calculation_basis cannot decide quality. Mechanism readers access their own data channel. Human rendering must strip private source/version/provider identifiers while retaining meaningful itinerary text and uncertainty.

## Independent activity classification

Emit evaluation_role (primary_visit, transport, transition, unresolved), role_status (declared_consistent, independently_reviewed, unresolved), source_refs, reason and any versioned review record. Role interpretation is distinct from canonical identity: a named museum can be a primary visit before anyone knows its Google ID.

1. A clear scheduled visit to one concrete named place remains a primary visit, regardless of missing ID or an inconsistent generic/unknown label. A supplied ID alone is a place reference, not proof of identity. An explicit main_poi record stays a visit candidate unless it is clearly a generic no-POI placeholder or a transport-label conflict requiring review.
2. A clear movement activity is transport. Named endpoints in its title/notes do not become extra visits. Explicit transport role is accepted when consistent with its content; contradictory content enters review rather than receiving a version-specific shortcut.
3. Generic no-POI activities and uncommitted free_time are transition-like, with no invented venue. A neighborhood/location string alone does not prove a visit to a distinct venue. Reviewed protected intervals remain blockers even when underlying output is transition-like.
4. For unknown/inconsistent role or place-bearing text, the projector creates an independent role-review record using only original output and reviewed requirements. A reviewer can assign a role or leave it unresolved, with field references and rationale. No online LLM or planner classifier is required. This is factual preparation, not preference evaluation.
5. Never classify a concretely named unresolved place as transition merely because identity lookup fails. Never use costs, RAG membership or candidate-ledger inclusion to infer the role. Nearby remains a separate unscheduled inventory.

Automatic classification is confined to unambiguous structural declarations/content; no unvalidated multilingual semantic classifier is promised by Ticket 01. Ambiguous cases are not silently dropped from scope. Downstream reports retain unresolved role counts; when applicability itself cannot be established they must not invent a denominator or PASS. Freeze/replay any independent review decisions as evaluation preparation records, separate from RequirementSpec authoring and blind rankings.

## Order and candidate transitions

Preserve delivered day membership. For a day with comparable valid timestamps, order visit candidates by start, then end, then original pointer for display stability. Equal/overlapping times remain conflicts/ambiguities, not corrected chronology. Invalid or incomparable clocks cannot establish adjacency by arbitrary lexical sorting; emit an adjacency-unresolved record with involved sources.

Candidate legs connect consecutive primary visits within a day. Nearby, transition placeholders and transport records do not become POI endpoints. Protected intervals remain separate blockers. Possible intervening unresolved-role records prevent declaring a clean complete adjacency list for that span; preserve the candidate and uncertainty instead of skipping them. Canonical same-place N/A is decided later using independent identity, not equality of claimed IDs.

## Transport correspondence: association is not factual agreement

For each candidate leg retain all associated claims plus unbound transport records. Association_status is unique, ambiguous or unbound; agreement is consistent, conflicting or incomplete. This avoids turning two descriptions of one journey into two actual journeys, while keeping contradictions visible.

A Transfer is uniquely associated when its from/to activity IDs identify the directed consecutive visit pair on that day. Place-ID discrepancy is retained for independent identity review and does not break a valid activity-reference association. Dangling IDs, reversed direction, nonadjacent endpoints or cross-day links produce reasoned unbound records; do not retarget them by nearest time/place.

For a transport Activity, independently reviewed explicit origin/destination wording can associate it with one directed leg even when its interval conflicts with the visit gap. Without explicit endpoint association, automatic positional matching requires exactly one same-day candidate leg whose gap fully contains the transport interval, with no contradictory endpoint wording or possible intermediate visit. Mere proximity, overlapping time or equal duration is insufficient. If unique correspondence cannot be established, preserve it as ambiguous/unbound; do not choose the most favorable leg.

Same-leg association alone does not prove duplicate content. Multiple transport activities may be journey segments. Exact duplicate semantic claims can share one logical record while preserving every source pointer; sequential segments remain ordered segments. Multiple same-leg records with incompatible times/modes or unclear segment relationships form a correspondence-conflict group. Do not add all durations, choose the shortest or silently replace an estimate with an application claim.

When a unique transport activity and Transfer describe the same leg consistently, expose one logical journey with both source sets. Transfer mode/time are structured claims, not privileged truth. Text-only mode requires explicit supported wording or independent review; conflicting/alternative modes remain unresolved. Absence of a mode stays explicit for the Route contract to handle, never inferred from distance or Google options. Ticket 01 preserves request restrictions but does not interpret new ones or choose a route.

## Time occupancy and display consequences

Keep transport activity intervals and Transfer departure/arrival separately as claims even when grouped. Do not synthesize a planned arrival from provider duration, reserve or Google evidence during projection. A missing Transfer arrival means incomplete claimed occupancy, not zero-length travel. The route checker can still assess available POI-to-POI time under its own contract.

A consistent duplicate journey supplies one logical occupancy record, so its two representations cannot overlap each other. Segmented journeys retain their explicit intervals; conflicting same-leg intervals remain alternatives with unresolved occupancy, not a union asserting both happened. Other independent timed commitments are retained. This records uncertainty for later overlap/route rules rather than inventing new pass/fail semantics. Explicit user-protected time is preserved once by obligation reference, not duplicated by an output placeholder describing the same protection.

For blinded display, a consistent group becomes one transport entry without provider badges or certainty upgrades. Preserve source uncertainty and explicit content. Ambiguous associations remain separate original entries with a neutral ambiguity notice; do not hide inconvenient content or create a fictional merged route. Identity/adjudication results and evaluator judgments are not shown to the rater. Exact renderer styling belongs to Ticket 09.

## Reason categories and future acceptance examples

Stable diagnostic categories include artifact_integrity_error, unsupported_wire_version, duplicate_source_id, invalid_clock, role_review_required, multi_poi_block, dangling_transfer_endpoint, nonadjacent_transfer, ambiguous_transport_association, conflicting_transport_claims, missing_claimed_arrival and optional_projection_unavailable. Each record includes sources and explanation; these are not metric verdicts.

| Documentation example | Required projection |
| --- | --- |
| V0: Museum A ends 10:00, walking activity 10:00-10:20, Museum B starts 10:30 | One candidate A-to-B leg and one transport claim; Google duration is still absent. |
| Same leg also has a Transfer with matching explicit times/mode | One logical journey, two preserved source references, no duplicate occupancy. |
| Activity says walking 10:00-10:20; same-leg Transfer says driving 10:05-10:25 | One leg, conflicting claims; neither version-owned record wins automatically. |
| Two segment activities describe walking then transit | Preserve segments; no automatic single-mode provider query invented by intake. |
| Museum has a name but no ID | Primary visit requiring independent identity resolution, not free time. |
| Relax/explore placeholder has no concrete POI | Transition-like; explicit protected-time obligations still apply. |
| Transfer references an absent activity | Unbound claim with source/reason; no guessed replacement endpoint. |
| Optional draft is missing | Final remains usable; paired analysis unavailable, not zero delta. |

Implementation acceptance must exercise intake-to-inventory behavior, source-stable sorting, classification review replay, duplicate/segment/conflict correspondence, protected intervals and reader isolation. A V3-finding-only mutation must not change the projection. These are documentation examples and future tests, not created benchmark cases or executed fixtures.

## Closure and remaining ownership

Ticket 01 now has a deterministic extraction/association boundary and explicit review/unresolved paths; no new user scoring choice was required. Canonical acceptance is Ticket 03, supported obligation scoring and occupancy outcomes are Ticket 05, departure-window selection is Ticket 07, renderer implementation is Ticket 09, and pre/post correspondence is Ticket 10. Do not claim those tickets are closed by this document. Approval to close this specification does not authorize implementation, formal experiments or benchmark freeze.

## Implemented preparation interface — 2026-09-29

The [package guide](../../backend/evaluation/README.md) defines concrete wire schema identifiers and the optional projection-review envelope. Rich/ambiguous text uses an independent review path; the implementation does not claim complete semantic language understanding. Automatic positional transport binding is deliberately limited to simple movement labels with no endpoint prose. Unresolved role records conservatively mark same-day candidate adjacency unresolved. The quality projection preserves protected obligations once, separate from transition placeholders, for future scoring.

Semantic projection is invariant to internal findings; original artifact hashes and derived source IDs correctly change whenever original file bytes change. Full metric-specific RequirementSpec operator validation remains Ticket 05. Final outputs remain usable if optional paired projections are unavailable. No quality score, Google query, blind HTML or Repair execution is implemented here.


## Follow-up correction boundary - 2026-09-30

Selected runs now require the `rtpeval_provenance_1` sidecar specified in artifact-contract.md; its complete input/result/group/run/version association is verified and its exact hash retained. This restores required full-input linkage without rerunning planners. Existing sidecars/fixtures must include this wire.

Overlapping visit intervals (including equal starts) emit a source-linked `overlapping_visit_intervals` diagnostic. Candidate legs touching those visits retain delivered claims and gaps but have unresolved adjacency, preventing automatic positional transport binding. Explicit Transfer activity-ID association remains a claim and does not resolve chronology. End-to-start touching intervals are not an overlap. No activity is moved, removed or split, and no quality verdict is computed.

Independently reviewed transport endpoints can still associate with a same-day directed candidate pair despite unresolved chronology. Only automatic positional matching requires resolved candidate adjacency; a reviewed association never clears the time conflict.


## Superseding transport-source decision - 2026-09-30

Accepted user decision: V0 has no Routes API and uses model-generated transport activities as its submitted transport claims. V1-V3 use application-owned `transfers`; model-generated transport activities in these versions must not supply evaluated transport mode, time, occupancy or fallback evidence. Preserve those original records for traceability and an ignored-source diagnostic, without treating them as additional transport commitments or merging them with authoritative transfers. Missing/incomplete V1-V3 transfers stay missing/incomplete; do not substitute an LLM transport activity. This authority selects the submitted transport representation, not factual route truth: independent snapshot evidence still determines route evaluation.

This supersedes the earlier version-neutral rule that Activity and Transfer representations have equal authority and must be reconciled with neither preferred. Repeated actual journeys between different visit occurrences remain separate. The earlier question about merging conflicting Activity/Transfer representations into one UNKNOWN commitment is superseded for V1-V3 by the user's source-selection rule.

Implementation status: decision accepted; existing Ticket 01 projection still reconciles both representations and requires correction before Ticket 05 occupancy scoring. Existing acceptance tests describe the previous behavior and must be revised with the implementation. No implementation or corrective test execution is claimed by this documentation update.


## Transport responsibility correction - 2026-09-30

Implemented in the current uncommitted workspace. Projection now requires the selected planner version independently of immutable source context. V0 uses transport activities only; V1-V3 use transfers only, including V3 draft/final_primary. `transport_source` identifies the selected representation; `ignored_transport` preserves allowlisted source records and `ignored_transport_source` diagnostics. Activities retain independently assigned roles and a `transport_applicable` flag, which is true only for V0 transport records. Ignored transport records must not supply occupancy, mode, time, fallback or an additional commitment. Ambiguous activity roles still require independent review; this is not automatic semantic recognition of disguised transport prose. Missing transfers remain missing. Same-source duplicate/conflicting claims retain reconciliation; journeys between different visit occurrences remain distinct. Earlier acceptance results and the preceding pending-status note describe historical checkpoints.

Generation now has a V1-V3-only structured activity schema excluding transport, explicit initial/Repair prompt prohibitions, and shared output acceptance rejecting declared model transport before initial transfer binding. V0 keeps its transport schema and version-specific transport instructions; the shared policy no longer suggests transport roles to tool-backed versions. Existing Repair patch permissions already prohibit arbitrary activity/transfer authoring. Visits may be spaced using supplied route evidence; application route selection and transfer binding remain unchanged. No extra model call or automatic repair is introduced.
