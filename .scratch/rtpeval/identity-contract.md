# Independent identity resolution contract — draft

Status: Historical design checkpoint. Ticket 03 automatic acceptance and offline implementation are specialized in [identity-implementation-contract.md](identity-implementation-contract.md); no live acquisition or benchmark freeze.
Date: 2026-09-28.
Source checkpoint: 8a435e2db0198e4fc8928b85e333b45b66c0c981; uncommitted design documents.

## Purpose and boundary

Resolve the places actually described by the submitted itineraries and reviewed RequirementSpec against independent evidence. This does not modify the submitted itinerary or confer Google access on V0 during planning. Work begins from the user's delivered batch; the resolver neither runs planners nor screens workflow completion.

The provider adapter, transport protocols and neutral DTOs can be shared after fixture verification. Planner identity choices, candidate ranking, V3 validation findings and Repair targets cannot determine resolution. Use evaluation-owned requests, cache and persisted observations. Google identity is the adopted evidence namespace, not an assertion of absolute real-world truth.

## Code facts

Activity supplies title, optional place_name, source_place_id and free-text location; it does not supply structured per-activity coordinates. Transfer endpoints contain planner IDs but do not independently confirm the corresponding place. PlaceSearchRequest supports language, a location bias, page size 1-20 and explicit field mask. The current text-search adapter uses a 50 km bias, not a hard destination boundary. Candidate DTOs contain provider rank, ID, name, coordinates and optional address/type/business status; there is no calibrated confidence score or alias registry.

Search normalization can skip malformed entries. PlaceSearchResponse retains actual_result_count, so an empty normalized candidate list must not automatically be treated as a successful search yielding no raw matches. Details provide corresponding identity fields plus timezone/opening data. Neither details success nor the first search result proves association with itinerary text. A closed business can still have a resolved identity; operational status is separate from existence and matching.

Additional adapter limitations: details currently does not enforce equality between requested and returned IDs; retain both and flag a mismatch rather than silently accepting it. Existing DTOs do not expose aliases, moved-place or parent-child relationships, and text search has no pagination contract. Planner normalization can fill details fields from a prior candidate and select an opening basis; prefer preserving direct provider DTO observations or explicit field provenance rather than treating fallback values as independently observed details. Do not reuse planner named-place/destination selection policies as identity judgment.

## Inputs and preserved records

Each place reference is scoped by batch/group/run/artifact/day/activity, retaining original role, title, place_name, claimed ID and location. Requirement subjects use independent subject IDs. Preserve the raw reference, queries, returned candidates, context, timestamps and evidence hashes. Do not let an incorrect generic/unknown role alone hide a concrete named visit. Exact place-bearing role rules remain OPEN; vague generic activities are not assigned an invented venue.

IdentityResolutionRecord separates resolution from supplied-ID consistency:

- resolution: resolved, unresolved, or not_applicable, with reason and adopted canonical ID only when justified;
- route to decision: independent ID-details association, name-search association, or human adjudication;
- claimed-ID association: absent, consistent, conflicting, or unverifiable;
- candidate evidence and decision rationale, reviewer where applicable, rule version, and audit history.

Reason vocabulary distinguishes ambiguity, insufficient description, no candidate found under the recorded search policy, provider failure, malformed response and unresolved ID/name conflict. These are not all hallucinations. A resolved venue with a bad supplied ID must not silently erase that conflict; the accepted handling is specified below.

## Common resolution process

1. Extract candidate place references from all selected finals, available V3 drafts and relevant requirement subjects. Preserve each visit occurrence; evidence reuse does not merge visit counts.
2. With a supplied ID, acquire independent details and check name/address/destination association. With no ID, search the described name and available destination/location context. An invalid/unverifiable ID may also require the name-search path. Neither path gets an automatic PASS solely from successful retrieval.
3. Automatic acceptance requires evidence sufficient to associate this specific output reference with one candidate without a material contradiction. Normalization of case/spacing is not enough to prove identity. Exact thresholds, alias handling and competing-candidate tests must be fixed using development fixtures before formal use; do not invent confidence percentages from provider rank.
4. Send ambiguity, material ID/name conflict and high-impact REQUIRED/EXCLUDED identity decisions to human adjudication as already accepted. Preselect an audit sample of automatic acceptances. High-impact review includes ambiguous itinerary matches that could change an obligation outcome, not only the requirement's own identity.
5. Adjudication receives relevant output wording, original request/location context and independent candidate evidence. Hide version identity and internal findings where practical. It is factual preparation, separate from blinded preference ranking. A reviewer may confirm, reject candidate associations or leave unresolved; insufficient evidence/budget cannot force acceptance.
6. Persist versioned decisions. Reuse evidence for matching canonical IDs, but do not propagate a contextual decision merely because two strings are identical. Never merge separate Google IDs solely because coordinates or addresses match; entrances, complexes and colocated venues need an explicit identity policy/adjudication.

## Downstream behavior

Resolved identity permits lookup of the corresponding evidence; it does not establish opening or route compliance. Identity UNKNOWN propagates only to dependent checks; date coverage and overlap can remain computable from schedule fields.

Canonical Grounding reports the verified fraction with unresolved applicable visits still visible in its denominator, without calling every unresolved reference false. Repetition cannot assume unresolved references are unique; report identity coverage. For REQUIRED/EXCLUDED, a confirmed match can establish satisfaction/violation, but a missing match with relevant unresolved references may remain UNKNOWN rather than automatically proving omission or absence. Exact count rules must account for possible unresolved matches. Formal denominator/count logic remains a requirement-scoring contract item.

Route checks touching unresolved endpoints cannot substitute zero duration. Independent opening evidence is not borrowed from a similarly named candidate without identity confirmation. Nearby remains outside primary-visit scoring.

## Accepted ID/name-conflict handling

If the output clearly names venue A but its supplied ID belongs to venue B, and independent human adjudication can confidently identify A, the accepted handling is: preserve an explicit supplied-ID conflict; resolve the intended named venue A for downstream reality checks; report identity-association errors separately from the named-place grounding fraction. Never rewrite the delivered result or hide the mismatch. If the intended place remains uncertain, leave the reference unresolved. The user accepted this handling. Keep claimed-ID consistency separate from named-place grounding and expose the conflict in reports; do not silently turn it into a clean match. A name-based evaluation binding does not correct planner transfers or other claims made using the wrong ID. Exact aggregation and any auxiliary-score contribution remain OPEN.

## Simple examples

- A V0 output naming a uniquely identifiable museum can resolve after independent search; its lack of a planner ID is not itself a failure.
- A V1 output with a valid ID still needs association with its displayed place. A valid ID for the wrong museum is a conflict, not an automatic match.
- A search returning no usable candidates is insufficient to prove that a place is fictional.

These are documentation examples only, not benchmark cases or observed provider results.

## Future verification

Independent fixtures must cover name-only resolution, valid matching ID, wrong-ID/right-name conflict, multilingual/alias ambiguity, same-name branches, wrong-city retrieval under bias, malformed candidate filtering, provider failure, closed-but-identifiable venues, colocated distinct IDs, role ambiguity and adjudication replay. Test that changing a V3 verdict cannot change resolution. No fixtures, queries or tests were run in this design task.

## Ticket 03 specialization — 2026-09-29

The user accepted separate strict paths for supplied-ID details and name-only search, common to V0-V3. Exact normalized name, destination/address association, no observed competition and a predeclared automatic-acceptance audit are required; aliases, branches, ID/name conflicts, insufficient evidence and potential REQUIRED/EXCLUDED matches go to factual review. The [implementation contract](identity-implementation-contract.md) fixes the offline wire, review replay, conservative acceptance rules and grounding/claimed-ID report. This section records a later implementation decision; the draft statements above remain historical. Ticket 04 still owns real independent acquisition and snapshot persistence, and Ticket 05 owns obligation scoring.
