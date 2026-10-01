# Ticket 03 offline identity implementation contract

Status: Implemented for offline observations and adjudication replay; development validation is recorded in ticket-03-acceptance.md. No live acquisition or benchmark freeze.
Date: 2026-09-29.
Base revision: 364f91f05f01328266bfb00c5b75885242d93d7d; Tickets 01/02 and this work are uncommitted.

## Scope and source boundary

Ticket 03 reads accepted Ticket 01 projection records, independently reviewed RequirementSpec subjects, offline identity observations, a predeclared audit plan, and optional human decisions. It does not use planner candidate ranking, V3 findings, Repair metadata or planner evidence. It neither calls Google nor alters any itinerary. Ticket 04 owns acquisition and raw provider snapshot persistence; Ticket 05 owns obligation scoring. This module's observation envelope is the replay handoff, not a claim that live acquisition exists.

Each scheduled `primary_visit` is an applicable grounding unit even without a canonical ID. V3 draft/final-primary records are separate optional projections. Relevant requirement subjects are those cited by resolved REQUIRED/EXCLUDED obligations; their reviewed `place_name` (or legacy `wording`) is used only for identity preparation. Subject associations are always reviewed. Unresolved activity roles remain visible as a separate structural count and are not silently added to the visit denominator. Nearby and transport records are outside main-visit grounding.

## Offline wire inputs

`rtpeval_identity_evidence_1` has `batch_id`, `batch_revision` and `records`. A record is keyed by Ticket 01 `reference_id`, has a unique `observation_id`, declares `source_kind=independent_google_places`, and may carry `details` and/or `search`. Missing records mean unavailable evidence. An available details observation retains `requested_place_id`, `retrieved_at` and `place`; search retains `query`, `requested_page_size`, `actual_result_count`, `retrieved_at` and raw-order `candidates`. Candidates carry Google ID, display name and formatted address; rank, business status and additional provider fields may be retained but rank never acts as confidence. Failed/unavailable/malformed observations retain their status. Invalid envelope linkage, duplicate references or impossible count structure are rejected rather than producing a partial report. A declared independent source is provenance metadata, not proof that an external service was contacted.

`rtpeval_identity_audit_1` has the same batch/revision plus a nonempty seed and positive `sample_count`. The plan is a required, separately frozen input. Among strict automatic proposals, choose the lowest hash of seed, batch/revision and a semantic audit key, then select up to the declared count. The key includes group/version/projection/source pointer and visible place claim, but excludes the result file hash and V3 internal findings. Selected proposals require review before entering resolved grounding counts. An absent plan or zero sample count is rejected. The module verifies deterministic replay and records plan hashes; benchmark preparation must establish that the plan was fixed before result inspection.

`rtpeval_identity_reviews_1` has batch/revision and per-reference decisions. Each decision supplies the current observation hash, consecutive positive revision, reviewer reference, review time, rationale, and `confirm`, `reject` or `unresolved`. A confirmation names an ID present in independent observation candidates. Stale evidence, duplicate/missing review revisions and unsupported candidate IDs are rejected. The report retains the entire history and uses the latest decision. A rejection leaves identity unresolved; it does not automatically prove a fictional place. A new artifact source reference or evidence observation needs new reviewed linkage.

## Strict automatic acceptance

Both V0 name-only and V1-V3 supplied-ID references use the same association standard. Names are compared after Unicode NFC, case folding and whitespace normalization only. Aliases, translations and approximate names are review cases. Destination must equal a comma/semicolon-separated formatted-address component. If an output `location` is present, it must also match an address component; unclear locality wording is reviewed.

- Supplied ID: independent details must return the requested ID exactly, with a valid display name and address that strictly match the output reference and destination. A successful ID lookup alone is insufficient. Without a recognized numbered street output location matching an address component beyond the destination, an independent full-page name search must also return the same sole usable/raw candidate ID; this checks observable same-name branches. If a search is present in either case, contradictory or malformed candidates block automatic acceptance. Search and details display names and complete formatted addresses must agree under the same normalization; uncertain formatting differences also require review.
- No supplied ID: independent search query must strictly equal the submitted place name under the same normalization, request the full supported page size of 20, return exactly one raw candidate and one usable candidate, and meet the same strict name/address association. Provider rank is ignored as confidence. The returned candidate set is the bounded observation, not proof of global uniqueness.
- Named obligations and visits that may match them by exact wording or observed candidate ID are high impact and require review. If a relevant subject has no usable candidate evidence, all visits in that group remain reviewable because an alias association cannot be ruled out from the available evidence.

The numbered-street shortcut conservatively recognizes a leading house number and an English street suffix (street/st, road/rd, avenue/ave, lane/ln, drive/dr, boulevard/blvd, way, court/ct). Country, state, postcode and unsupported address forms cannot activate it; they need competition search or review. This is a narrow recognition rule, not a worldwide address parser.

When a separate `place_name` is present, a nonempty title is automatically compatible only when it equals that name or `Visit <name>` under the same normalization. Other prose, multiple named venues and conflicting titles require factual review (`title_association_unverified`); the module does not infer a contradiction solely from differing prose. Original title participates in the semantic audit key.

Malformed optional claimed IDs are guarded before set membership and remain reference-level uncertainty; they do not abort other records. Malformed IDs, ID/name mismatches, returned-ID discrepancies, same-name branches, competing candidates, wrong-city addresses, unsupported aliases and missing evidence do not get an automatic binding. Closed business status is retained but does not negate a valid identity association. Distinct Google IDs are not merged merely because names or addresses coincide. These strict rules can leave valid places unresolved; that is an explicit coverage limitation.

## Review outcome and reporting

The review queue presents opaque reference IDs, original title/name/location and claimed ID, original request context, independent candidate fields, observation metadata and reasons. It omits version labels and planner findings. Its purpose is factual adjudication, separate from blinded itinerary preference rating. A reviewer may confirm an independently observed intended venue despite a wrong claimed ID. The report then uses the reviewed named venue for downstream identity binding while retaining `claimed_id_association=conflicting`; the original output and Transfer claims remain untouched.

Each identity record has resolution (`resolved`/`unresolved`), reason, adopted canonical ID if justified, decision route, claimed-ID association (`absent`/`consistent`/`conflicting`/`unverifiable`), evidence hash, review history and audit state. The request-level report gives final and optional V3 grounding counts/fractions and claimed-ID counts, with unresolved role counts separately. The fraction is resolved applicable visits / all applicable visits. UNKNOWN is not called a hallucination or FAIL. An empty visit denominator yields a null fraction. This report does not calculate requirement outcomes, opening/route checks, auxiliary totals, or formal comparisons.

`python -m backend.evaluation.identity_cli MANIFEST EVIDENCE AUDIT_PLAN [--reviews REVIEWS]` replays local JSON. Exit 0 means no pending queue, 3 means adjudication is pending, and 2 means intake/evidence correction is needed. CLI output adds exact-byte SHA-256 hashes for the evidence, plan and review files; the Python API also records canonical-JSON hashes of the supplied objects. No provider connection is made.

## Verification and limits

Offline fixtures cover strict ID/name paths, wrong cities, aliases, branches, wrong IDs, malformed/failed evidence, reviewed conflict, high-impact routing, versioned review replay, audit determinism and V3-finding isolation. The provider namespace is still Google Places, so this is consistency with recorded evidence, not absolute real-world truth. The search adapter has no pagination/alias guarantee, and `requested_page_size=20` only limits one known truncation risk. Human adjudication can remain unresolved. No live coverage, formal benchmark or model/database behavior is established by these fixtures.

## Ticket 05 subject-scope extension — specification only, 2026-10-01

The accepted [fixed-visit-time contract](requirement-schedule-contract.md) makes resolved
`fixed_visit_time.subject_ref` another high-impact independent requirement subject,
even when no separate REQUIRED/EXCLUDED entry exists. The future Ticket 05 change must
include it in `identity_references` and preserve the existing strict association,
manual review, automatic audit and source/revision linkage. Unresolved/unsupported
subjects remain uncertainty rather than fabricated identities. No identity code or
acceptance result is changed by this specification update.
