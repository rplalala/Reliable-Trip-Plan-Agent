# Bounded landmark nomination and discovery

## Implemented behavior - 2026-09-27

Ticket 02 adds one destination-only auxiliary model call to initial V1-V3 candidate
acquisition after input/Gate acceptance. It uses the existing configured deployment,
strict names-only output and request-owned client lifecycle. V0 makes no nomination
call. V3 Repair reuses initial supply and does not repeat nomination.

The default bounds are one send, twelve names, 8,000 input tokens including prompt,
schema and framing, 2,000 output tokens and twenty seconds shortened by the remaining
caller request deadline. There is no retry or correction call. Configured limits can
be lowered within their validated ranges. Accounting is independent of POI semantics.

## Discovery and identity

User-named search intents run first. General top-attractions discovery gets the next
opportunity when the shared search pool remains, including requests with eight interests.
Ordinary discovery then leaves up to four opportunities for unresolved nominations;
unused opportunities return to ordinary work. Supplementary sends are part of the existing
twelve candidate-search sends, never an additional pool. Cache hits consume no sends.

Existing exact normalized provider display-name matching resolves names against acquired
results. Ambiguous names, aliases and unmatched names remain unresolved; first hits and
nearby/parent attractions are not substitutes. Identity is reconciled again after RAG
source expansion, clearing metadata if a later same-name, different-ID result is ambiguous.

Resolved candidates retain model origin and earliest rank through merge, Details,
qualification, selection input and generation projection. They do not become user REQUIRED
places. Existing exclusions, exclusive scopes, role and factual eligibility still apply.
Nomination is not evidence of opening hours, tickets, costs, suitability or feasibility.
Existing C/G/K, Details, RAG, semantic, route and Repair limits remain unchanged.

## Failure and observability

Invalid output, empty output, auxiliary provider failure, timeout and unresolved nominations
fall back to the available qualified pool with recorded degraded status. Cancellation
propagates; unrelated identity/qualification failures retain their existing behavior.

Trace events `landmark_nomination` and `landmark_discovery` record attempts, elapsed time,
reported usage, resolution/reuse counts, qualification/selection counts and allocation stops.
The independent `budget.json` stage `landmark_nomination` retains numeric observations,
limits and allowlisted statuses. Missing billed usage stays missing. Existing 32-call-record
and 64-KiB artifact limits remain; no names, prompts or raw provider envelopes are added
to the compact summary. Token engineering estimates are not billed usage.

## Boundaries and handoff

Ticket 03 integrated soft-target opportunity saturation and landmark-aware supply on
2026-09-28; see [current supply policy](shared_poi_supply.md#preference-and-landmark-balance---2026-09-28).
This ticket supplies eligible metadata and opportunities; twelve nominations do not promise
twelve resolved, selected or scheduled places. Offline mocked validation establishes the
mechanisms, not live nomination quality, itinerary improvement, latency or cost. No live
run, formal benchmark or version freeze is included.

See [configuration](../config/README.md#landmark-nomination) and the
[development record](development_record.md#landmark-nomination-ticket-02---2026-09-27).
