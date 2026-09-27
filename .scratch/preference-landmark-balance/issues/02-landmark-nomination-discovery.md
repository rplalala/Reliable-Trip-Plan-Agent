# 02: Discover resolved local landmarks within bounded planning resources

**What to build:** V1–V3 travelers gain a destination-based source of representative
landmarks that reaches the existing qualified candidate flow even when many personal
interests are supplied. Model nomination and supplementary place searches are bounded,
identity and admission rules remain authoritative, and auxiliary failure degrades
without discarding otherwise usable planning results.

**Parent:** [Preference coverage and local landmark balance](../spec.md).

**Blocked by:** None (can start immediately).

Status: ready-for-agent
Type: task

## Acceptance criteria

- [ ] After existing input/Gate checks pass and before candidate discovery, V1–V3
  can invoke a dedicated nomination service through the existing model abstraction.
  Provider calls remain behind service/client boundaries and use the configured
  deployment. Invalid or rejected inputs do not trigger nomination.
- [ ] The nomination prompt uses destination identity/context without personal
  positive-interest conditioning. It returns an ordered strict structured list of
  at most twelve representative place names and preserves model-origin rank.
- [ ] Each request has at most one nomination model send, no retry/correction call,
  an 8,000-token total input bound, a 2,000-token output bound and a twenty-second
  call bound shortened by the remaining request allowance. Schema/framing overhead
  is counted using existing token-accounting conventions.
- [ ] Nomination uses independent explicit accounting and the existing request time
  allowance without resetting deadlines or consuming/enlarging semantic-assessment
  limits. Preserve caller-specific deadline behavior and client ownership/cleanup.
- [ ] Existing acquired search results are reused for reliable identity matches
  before supplementary queries. The current exact-name identity boundary remains
  intact: ambiguous/alias-only names stay unresolved, and the first hit or a nearby
  attraction is not automatically substituted.
- [ ] User-named places have first claim on search sends. General attraction
  discovery receives an opportunity even with many preference intents when budget
  remains; exhausted higher-priority work produces an explicit skipped state.
- [ ] All candidate search sends share the existing total of twelve. Supplementary
  nomination name searches consume at most four of that total, not four additional
  sends. They cannot displace user-named processing. Cache reuse consumes no actual
  provider send, and unused allocations remain reusable by discovery work.
- [ ] Nomination candidates enter existing merge, admission, Details, semantic-role
  and factual-eligibility checks. Their origin and rank survive reliable canonical
  deduplication and remain available to selection/generation. They do not become
  user REQUIRED places or automatically qualify as primary visits.
- [ ] Exclusions, exclusive scopes and existing role/identity boundaries reject
  conflicting nominations. Model rank does not establish opening, admission, ticket,
  suitability, travel-time or cost facts.
- [ ] Invalid output, timeout, failed nomination or no resolved candidates can fall
  back to the available qualified pool with a truthful degraded status. Cancellation
  still propagates, and existing unrelated hard failures are not swallowed.
- [ ] Trace and compact budget output account for nomination calls, time, reported
  usage, resolution counts and search-allocation stops. Missing billed usage remains
  missing, bounded artifact behavior is preserved, and credentials/raw envelopes
  are not introduced into outputs.
- [ ] Existing candidate, Details, final-supply, RAG, semantic, route and Repair
  ceilings remain unchanged. Twelve nominations do not imply twelve successfully
  resolved, selected or scheduled places.
- [ ] V0 has no new nomination/provider call or candidate-discovery dependency.
  V1/V2 do not acquire Repair behavior, and V3 can reuse this baseline flow without
  broadening Repair authority or rerunning primary nomination during Repair.
- [ ] Planning/service tests demonstrate successful nomination through resolved
  eligible candidate use, exact-match reuse, ambiguous resolution, admission
  rejection, many preference intents, user-named precedence, unused-allocation reuse
  and exhausted search budgets. Assertions use actual fake collaborator send counts.
- [ ] Narrow adapter tests verify strict output/list limits, presend input limits,
  remaining deadline, one-send behavior on failures, usage propagation and cleanup.
  Cancellation and fallback preserve their distinct external outcomes.
- [ ] Relevant focused and shared-pipeline regressions, lint/format checks and
  Standards/Spec review pass. Related design/configuration/observability documentation
  records actual behavior and unmeasured live cost/quality limits.

## Verification and handoff

Use existing planning entry points with injected fake model and provider services,
plus the accepted narrow nomination adapter seam. Demonstrate a resolved nomination
reaching the existing pipeline and being usable by an independent version run; an
isolated DTO or an unconsumed list is not completion.

This ticket does not require ticket 01's soft-target contract. Use current preference
semantics while delivering nomination/discovery behavior and compatible candidate
metadata. Ticket 03 combines that metadata with ticket 01's soft targets. Shared code
may overlap, so sequential implementation is recommended without inventing a logical
blocking edge. Perform small local prefactoring only when required by the slice.

## Boundaries

No fuzzy/alias/parent-site identity mechanism, automatic admission exceptions, extra
generation pass or existing provider-budget increase. The approved nomination bounds
are configurable starting limits, not live performance measurements. Future tuning
must respect the approved run budget and evidence/rollback requirements. No live
execution, formal benchmark, Git action or version freeze is included.

## Comments

- 2026-09-27: The user approved publication as an independent starting ticket, with
  final integration blocked on both tickets 01 and 02.
