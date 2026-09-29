# Evaluation specification closeout audit

Date: 2026-09-28.
Status: Architecture and score-accounting decisions converged. Returned-route and generic-activity decisions are resolved. Artifact, human-answer and evidence/time contracts are drafted; implementation dependencies remain. Not specification frozen or implementation authorized.
Scope: current evaluation documents, previous code-informed findings, link/whitespace and arithmetic-example checks. No planner execution, provider calls, benchmark creation or experiment analysis.

## Accepted baseline

- Separate benchmark construction and evaluation documents; user-curated batch handoff, not automatic per-candidate execution.
- Benchmark owns qualification/failure records and iteration suggestions; only the user decides iteration.
- Independent requirements prepared upstream; per-group input, four separate full result files and four usage files.
- Independent quality from itinerary, reviewed requirements and frozen evidence; internal mechanism reports cannot decide quality.
- One POI per primary activity; no guessed splitting; only same-day inter-venue routes. Same canonical adjacent visits are route N/A. Uncommitted locationless free time may be travel slack; protected commitments may not.
- Independent identity adjudication preserves wrong-ID evidence even when named venue resolves.
- Opening full containment, no grace, exceptional-date ambiguity UNKNOWN with reasons.
- Routes use stated mode, per-mode caps, DRIVE product reserve600s and two independent 300s tolerances. No-route under applicable successful query is FAIL; provider failure/incompleteness is UNKNOWN.
- Five equal-weight verified-compliance dimensions; P/(P+F+U); group-wide N/A omitted jointly; individual N/A contributes zero without adding a fake failure. UNKNOWN means applicable but undecidable, not just provider data missing.
- Single-rater four-plan rankings with ties, separate preference/pace/usefulness, and no inter-rater claim. Resource and mechanism results are separate from the quality total.

## Consistency repairs in this pass

Replaced stale suppression of incomplete totals and OPEN N/A arithmetic with the accepted numeric profile. Clarified that diagnostic conditional compliance and auxiliary verified-compliance scores use different denominators. Reconciled claims that UNKNOWN must not become zero: it is not an observed zero duration/false fact, but earns zero verified-success credit. Marked old sample counts as benchmark decisions, not renderer quotas. Added the accepted single-POI material boundary.

The score profile is the arithmetic authority; the metrics table supplies observational definitions and links back to that profile. Historical review sections retain their chronological proposals and rejections; later accepted entries supersede them rather than rewriting history.

## Remaining items that change scoring meaning

### S1. Returned-route calculation: resolved

Accepted simplification: use the valid route duration returned by Google for the queried endpoints, direction and stated travel mode, including a fallback traffic-calculation result. Do not classify a valid result UNKNOWN solely because traffic awareness differs from the requested routing preference. Preserve requested/returned context and fallbackInfo for traceability, without adding a separate traffic-fidelity score or promising future road conditions. Do not silently switch endpoints, direction, travel mode or query date. Explicit no-route remains FAIL; provider failure, invalid status or no usable duration remains UNKNOWN. Existing duration thresholds, DRIVE product reserve and five-minute tolerances remain unchanged.

### S2. Generic no-POI activities: resolved as free-time/transition-like

The latest user decision supersedes excluding generic no-POI activities from benchmark delivery: treat such items as free_time/transition-like for evaluation, without counting them as primary visits or inventing a venue. Preserve the original output role/text and record the evaluation classification. This does not erase explicit user-protected time or reclassify a concretely named but unresolved POI as free time. Ordinary no-POI placeholders alone do not disqualify a group.

## Technical work the agent should resolve without further broad interviews

| Work | Required evidence/output | Dependency |
| --- | --- | --- |
| Provider encodings | Primary-doc verification and independent truth-table fixtures for opening windows/24h/closed/truncated periods, Routes status/fallback/time support | Required before provider rules implementation; no live runs implied |
| Time normalization | Explicit naive/local/IANA/offset/DST rules preserving source data; ambiguous cases use existing UNKNOWN principle rather than silent corrections | Needs provider context, not new overall research design |
| Identity automation | Conservative acceptance criteria, candidate context, adjudication queue and audit selection; no provider rank as confidence | Develop/validate on fixtures; never held-out tuning |
| Input/report serialization | Versioned manifests, hashes, identifiers, reason codes and cross-file linkage; input-date validation must not use current live-run date limits | Uses accepted ownership and per-version files |
| Role and transport normalization | Independent role review, reconcile duplicate activity/Transfer, protected occupancy and stable source correspondence | Apply the accepted no-POI classification, preserving protected time and original artifacts |
| Human artifact format | Complete fixed renderer, private mapping, save/resume/import validation and deterministic ties-to-pairs transformation | Sample count supplied externally |
| Mechanism extraction | Exact trigger/acceptance/round denominators, stage/resource attribution and official fact exposure extraction | Never used by scorer |
| Independent Repair contracts | Before/after correspondence, target/control invariants and regression units | Final case construction is benchmark work; dependent reporter cannot be called ready before definition |

These are real specification tasks, not claims of implemented capabilities. Resolve them in contract-focused work before implementation of dependent components, rather than repeatedly asking the user for facts available in code or provider documentation.

## Usage collection readiness

Still outstanding: symmetric V0-V3 outer attempt timing, run/result/usage linkage, actual model token and provider-send capture, retry/cache/element accounting, stage attribution, final V3 resource capture and explicit missingness. Existing trace can be absent/truncated and V0 lacks symmetric metadata. Do not call this a completed collector or reconstruct missing tokens from itineraries.

## Work outside evaluator-module freeze

Benchmark counts/cities/inputs/repeats, qualification stop-reason mapping, user-approved iteration policy, final matched checkpoint, formal sampling/statistical analysis plan and Codex harness details belong to their own approved stages. They do not justify reopening accepted evaluator boundaries, but formal experiment readiness still depends on them.

## Readiness conclusion

The specification is ready to plan contract-first work packages if requested; it is not ready to label every implementation ticket ready-for-agent. The two semantic frontiers S1/S2 are resolved. Complete technical contracts and acceptance fixtures, then assess implementation readiness. No coding, test suite execution, dry runs, API acquisition or benchmark freeze is authorized by this audit.

## Arithmetic checks

Documentation calculations checked in-memory: unknown retention (9P/1F=90, 2P/8U=20); five equal scores average88; common N/A produces the same mask for all versions; individual route N/A contributes0 with fixed shared weight; Routes deficits at300s pass while301s fail, and two tolerances never sum. These are formula sanity checks only, not evaluator tests or experiment results.

## Technical contract checkpoint — 2026-09-28

- [Artifact and human-answer contract](artifact-contract.md): batch references/hashes, reviewed requirement linkage, usage envelope, report missingness, blinded ranking export/import and private mappings.
- [Evidence and time contract](evidence-time-contract.md): timezone interpretation, opening-period precedence/completeness and per-leg Routes truth tables, with official provider references.

These drafts support contract-first task decomposition. They do not establish implemented collectors, tested parsers, frozen identity thresholds or complete Controlled Repair reporting. No new user decision is required for the already accepted route fallback and generic-activity boundaries. Dependent tasks must resolve the specific remaining technical definitions before being marked implementation-ready.

## Specification closure and resume boundary — 2026-09-28

The user approved the 12-ticket granularity/dependencies and requested a documentation checkpoint before taking a break. Ticket 01 closure has not started; no ticket is claimed. Resume with its specification closure only after the user resumes work, not with implementation.

needs-info denotes a bounded missing technical definition, not necessarily a question awaiting the user. Before implementing each ticket, inspect current relevant code, resolve factual gaps, document the contract and acceptance criteria, and ask the user only about unresolved choices affecting result meaning. Settle cross-cutting rules before dependent implementations. Waiting for another ticket is expressed by Blocked by; specification readiness does not remove that dependency or grant implementation authorization.

The next intended work is Ticket 01's independent activity-role classification, transport/Transfer correspondence and source linkage. Do not decide those details during this pause checkpoint. Usage capture remains a supporting prerequisite for usable resource comparisons, not a prerequisite for itinerary quality scoring or blinded review.
