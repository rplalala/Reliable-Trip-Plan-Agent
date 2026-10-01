# Ticket 06 opening specification and interface preflight

Date: 2026-10-02 (Australia/Sydney).
Revision: `ed4c9a9d4724263925748588878eadc22d21978a`, `feature/evaluation`.
The versioned working tree was clean at entry, one local commit ahead of upstream.
Original preflight authorization: specification/interface inspection only. Subsequent
2026-10-02 approval covers the offline implementation scope below and transfer to the
existing receiving conversation; see the final authorization checkpoint. Live acquisition,
formal cases/experiments and Git actions remained unauthorized at that checkpoint.
Later implementation, supplementary tests and local Git closeout authorization are
recorded in [acceptance](ticket-06-acceptance.md); this preflight remains historical.

## Tracker and authority

Read [Ticket 06 #18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18)
and its comments on 2026-10-02: open, ready-for-agent, no comments or implementation.
Its declared predecessor [Ticket 04 #16](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/16)
is closed/completed. Ticket 05's local implementation is available for neutral time
reuse; its commit is not pushed. GitHub remains the live tracker. This local preflight
does not change Issue state, imported history or dependencies.

Authorities: [PROJECT](../../PROJECT.md), [opening](opening-contract.md),
[evidence/time](evidence-time-contract.md), [snapshot](snapshot-contract.md),
[metrics](metrics-contract.md) and the implemented independent projection/identity
contracts. Earlier draft OPEN statements are historical where superseded below.

## Existing interface audit

| Existing seam | Observed behavior | Ticket 06 integration |
| --- | --- | --- |
| `load_batch(manifest)` | Accepted immutable projection with exact source hashes, declared days, original timestamps and independently reviewed roles | Consume accepted material; primary occurrences remain distinct; unresolved role counts prevent a silently reduced denominator |
| `identity_references` / `resolve_identities` | Source-linked canonical decisions, fixed-time subject scope/reference digest, unresolved references and reviewed high-impact/audit decisions | Validate policy/source/reference coverage before looking up hours; unresolved canonical identity gives visit UNKNOWN |
| `build_evidence_plan(intake, identity_report, [], paired=False)` | Canonical Places details union; preserves occurrences; empty route context list is accepted and leaves leg requests pending | Reconstruct the expected evidence plan without acquiring routes; do not create a second snapshot schema or route selector |
| `load_snapshot(directory, expected_plan=...)` | Validates request coverage, raw hashes, safe paths, attempt UTC ordering, derived summaries and oracle ledger; returns manifest/plan/records | Replay an evidence-phase snapshot and check its opening-relevant plan linkage; optional trusted expected plan adds exact whole-plan matching; reject corrupt preparation instead of dropping records |
| Snapshot record `summary.payload` | Full raw Places object retained for available details responses; `available` establishes JSON/object delivery, not correct place/time/hours semantics | Check returned `id` against the requested/adopted canonical ID and parse raw `timeZone`, current and regular hours independently |
| `identity_evidence(snapshot)` | Identity-phase bridge intentionally reduces place fields to ID/name/address/business status | Do not read hours/timezone from this reduced bridge; use canonical details in the evidence snapshot |
| `schedule_time.normalize_interval` | Preserves offsets, independent IANA localization, DST fold/gap/date mismatch and six-digit precision; default end must remain on declared day | Reuse neutral primitives with an explicit opening-only cross-date path; retain the existing Ticket 05 default and regressions |
| `rtpeval_schedule_context_1` | Optional reviewed group timezone linked to Input hash and reviewer/source metadata | Reuse its wire if needed for missing place zone; record zone origin and preserve conflicting independent zones as UNKNOWN |

The snapshot plan already carries `identity_report_hash` and occurrence-source records.
Ticket 06 must check these against the supplied current identity report/intake, including
the current fixed-time subject policy. An identity-phase snapshot or a different paired
scope is not a substitute evidence plan. Route contexts in a supplied plan may be retained
and validated, but Ticket 06 neither chooses them nor needs route observations for opening.
When a snapshot also contains route requests, compare its opening reference/detail-request
subplan with the reconstructed canonical Places plan, rather than demanding equality with
an empty-route-context plan. Also check phase, paired scope, intake hash and identity-report
hash. Loading still validates the whole persisted snapshot; optional `expected_plan` is
the caller's full trusted acquisition plan, including routes when present. This avoids
inventing route selection or rejecting correct mixed-purpose evidence.
The details request descriptor has no built-in Google serializer/field mask: operational
transport must later request the required fields. Missing observed fields remain UNKNOWN.

## Technical rules resolved from accepted decisions and primary sources

Primary documentation checked 2026-10-02; this was public documentation reading, not a
Places API request or a provider fixture run:

- [Places REST reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places#OpeningHours)
  distinguishes an explicit empty periods list from absence. Parse an original applicable
  empty list as known closed; a normalizer-created empty list or missing/null field is not
  the same observation. Use field presence in the preserved raw payload.
- The same reference documents the regular always-open Sunday 00:00/no-close sentinel,
  current request-local seven-day window, local point dates/truncation and `timeZone.id`.
  Do not assume periods-array position means Sunday or apply the regular sentinel to an
  arbitrary current missing-close period. Current truncated endpoints establish bounded
  knowledge, not closure beyond the observed boundary or an invented infinite interval.
- [Official Places proto](https://github.com/googleapis/googleapis/blob/master/google/maps/places/v1/place.proto)
  declares point day/hour/minute as optional fields. Missing endpoint components are not
  automatically zero. [ProtoJSON presence rules](https://protobuf.dev/programming-guides/json/#presence-and-default-values)
  distinguish present optional zero from an absent value. The omitted non-optional
  truncation flag has its default false value; raw absence is retained in provenance.

Full visit containment uses zero grace and half-open intervals, exact seconds and no
display rounding in verdicts. Union only overlapping/touching availability; retain lunch
closures, weekly rollover and previous-date overnight periods. Overnight provider periods
and explicit cross-midnight visit endpoints are supported in this ticket. Never infer a
next-day end from a reversed same-date timestamp or trim a visit at midnight. Both sides
of a cross-date visit need applicable evidence. This does not add inter-day route checks.

Opening uses place-local IANA time with explicit zone provenance. Group context is not
silently preferred over conflicting place evidence. Explicit offset conflicts, DST fold/
gap, incomplete dates, unknown zones and unsupported timestamp precision remain UNKNOWN.
Do not substitute a numeric UTC offset for an IANA zone or use host timezone. A supplied
provider timezone version is retained; replay records the actual installed zone-data basis.

Use applicable current/date-specific periods ahead of regular weekly fallback. Derive
the current window from the selected details attempt's request-local date, not snapshot
completion/retrieval date or host date. If a request/retrieval span crosses the place-local
date boundary and applicability cannot be established from raw dates, preserve uncertainty.
Do not reinterpret current hours collected after a trip as historical hours. Outside the
current scope, regular fallback is weaker labelled evidence, subject to known exceptions.
An absent current object may permit otherwise valid regular fallback; an applicable current
object with invalid/missing periods must not be disguised as valid date-specific evidence.
Invalid affected scope stays unknown rather than using regular data to erase the defect.

A relevant special day without usable applicable current hours stays UNKNOWN with the
accepted explanation; regular hours remain context. A valid applicable complete schedule
with no period on that special day, including an original empty list, can establish closed
hours. `openNow`, business status, descriptions, secondary hours, planner hours/findings and
entry/exterior wording do not independently establish this visit's opening interval.

Partial parsing separates proven open spans, proven closed spans and unknown spans. A
malformed period can hide an opening: do not treat the complement of the remaining valid
periods as closed unless completeness for that bounded scope is established. A valid open
span can still prove containment; a known closed span can prove FAIL. Never merge conflicting
observations or independently prepared context into a convenient complete schedule.

## Resolved result-meaning question — 2026-10-02

**Accepted: a known closure within the scheduled visit establishes FAIL, including
partial evidence; retain that FAIL in the conditional compliance denominator.**
The existing truth table already requires FAIL if a partial observation proves a conflict;
the older metrics wording uses "fully adjudicable" both for evidence coverage and compliance.
Those are different concepts when the whole outside duration remains unknown.

Example: visit 13:00-15:00, independently known closed 13:00-14:00, unknown 14:00-15:00.
The verdict is FAIL; outside seconds are null as a complete magnitude, confirmed outside
lower bound is 3600, unknown seconds are 3600. With two fully observed PASS visits:

| Reviewed policy | Conditional compliance | Complete evidence coverage | Verdict |
| --- | --- | --- | --- |
| Accepted: decisive verdict denominator | 2 / 3 | 2 / 3 | Partial visit remains FAIL |
| Alternative not adopted: complete-evidence-only denominator | 2 / 2; partial FAIL separately reported | 2 / 3 | Partial visit remains FAIL |

The user clarified that any closure inside the scheduled interval makes the visit FAIL.
Apply the established half-open/zero-grace boundary: a positive-duration intersection with
an independently known closed span establishes FAIL, even when another span is unknown.
Ending exactly at closing still passes when the whole visit is covered. Evidence absence
does not establish a closure: without full containment or a known conflict, the visit is
UNKNOWN. The alternative complete-evidence-only denominator above was not adopted.

Conditional compliance is PASS / (PASS + FAIL), including partial decisive FAIL. Report
verdict-decidable coverage and complete-evidence coverage separately; empty denominators
remain unavailable. Unknown time stays unknown; exact full outside duration remains null
when incomplete, with confirmed lower-bound seconds retained. Auxiliary scores and common
masks remain Ticket 08; this closure concerns the descriptive conditional rate only.

## Proposed implementation boundary and output wire

Approved by the user's subsequent 2026-10-02 reply, for execution in the receiving conversation:

- Add a deep offline opening module, provisionally `backend/evaluation/opening.py`, with
  `score_opening(intake, identity_report, snapshot_directory, schedule_context=None, *, paired=False, expected_plan=None)`.
  The scorer loads/verifies the local snapshot and checks its opening subplan against
  intake/current identity, with optional exact full-plan verification. Match existing
  immutable result/`to_dict()` conventions; the public path cannot accept an unchecked
  planner dictionary masquerading as replayed provider evidence.
- Add an offline `opening_cli.py` accepting local manifest, identity report, snapshot directory,
  optional reviewed context/full expected plan and paired flag. CLI hashes local preparation, does not modify it,
  and has no acquisition/provider/model/database path.
- Use schema/rules versioning, stable visit source references and hashes for original material,
  identity report, expected plan, snapshot manifest/raw observation, context and rules. Retain
  per-visit basis segments when current and regular scope differ across the full interval.
- Validate whole-batch material and preparation linkage first. Malformed delivery/context and
  corrupt snapshot require correction; stale identity/policy requires identity replay. Valid
  snapshot records with failed sends or malformed hours produce source-linked visit UNKNOWN.
  A missing response field is not a reason to discard its visit or the batch.
- Output one check per applicable primary occurrence; no Nearby, requirement-subject-only,
  transport or generic activity check. Retain nonapplicable records/reasons and unresolved role
  counts; if the applicable denominator is unresolved, suppress the full-scope percentage.
- Report structure/time evaluability, identity availability, evidence complete/partial/missing,
  decisive verdict availability, current/regular/mixed basis counts and PASS/FAIL/UNKNOWN/N/A.
  Each UNKNOWN includes reason, explanation and exact visit/date/evidence references.
- For exact durations report outside seconds; for incomplete intervals report null exact total,
  known outside lower bound and known/unknown portions. Sum observed per-visit magnitudes as
  a labelled subtotal, never a global-time union or invented full-batch total. Missing duration
  stays null; known zero remains zero. No rounded value changes the verdict.
- Reuse neutral time/identity linkage validation through a narrow documented shared seam if
  needed; do not import planner opening verdicts or Ticket 05 metric decisions. Any time-helper
  extension is opt-in, preserves existing signatures/default behavior and needs regressions.

No opening frontend, live acquisition/client, official-access audit, route verdicts, total/mask,
blind artifacts, Repair delta, formal case construction or overall evaluation redesign is included.
All V0-V3 planner execution paths remain unchanged; only independent evaluator output is added.

## Acceptance checks to implement later

1. Public RED/GREEN parser/scorer slices: boundary equality, positive fractional overrun,
   early arrival, split periods/lunch, overnight/weekly rollover, regular sentinel and current
   truncation; explicit empty vs missing/null; optional zero vs absent component; malformed
   types/ranges/booleans, date-weekday contradictions and DST 23/25-hour days/folds/gaps.
2. Current/request-local applicability, retrieval crossing midnight, post-trip snapshots,
   regular fallback, known special-date uncertainty and mixed cross-date basis.
3. Complete, partial proven FAIL, partial nonconflict UNKNOWN, exact/lower-bound/null durations,
   the user-selected compliance denominator and unresolved role denominator availability.
4. Stale identity/snapshot/paired scope, returned canonical ID mismatch, missing request and
   source/hash corruption. Keep independent unavailability distinct from material corruption.
5. Mutate planner hours/findings/mechanism records and add Nearby; factual opening conclusions
   remain unchanged while provenance hashes may change. Repeated visits remain repeated checks.
6. CLI deterministic replay, no socket construction, no source-byte mutation, structured error
   exits; snapshot/identity/time/intake regression suite; Ruff/compilation and Standards/Spec review.

## Actual checks performed in this preflight

- Read-only code/contract/Issue inspection and primary-document verification above.
- Existing snapshot/time regression: **48 passed in 2.39 seconds**, with
  `TRIPWORLD_TEST_DATABASE=0`. This verifies existing reusable seams only; it is not
  Ticket 06 parser acceptance. No initial test failure or correction occurred in this run.
- Documentation checks: **181 local Markdown targets** exist, new content is English,
  only documentation files changed and `git diff --check` passed. No correction was needed.
- No new code, test fixture, benchmark, provider observation, Issue mutation or Git action.
  This document and related current-context/archive updates are local and uncommitted.

Status at preflight completion: specification/interface inspection complete, including
the accepted closure/denominator rule. No known result-meaning blocker remains for the
offline scope. The implementation approval below was received subsequently.

## Approved execution transfer — 2026-10-02

The user approved the current Ticket 06 scope after the ask-matt recommendation:
offline opening parser/scorer/CLI, TDD and relevant regressions, Standards/Spec review
and corrections, related documentation/thesis archive and GitHub #18 updates. The user
then explicitly requested transfer to an existing conversation because this context
was too long. Receiving thread: `01a0f858-a009-7911-aab2-210762e4e131`, on the same
local repository and branch. The receiving conversation may start without re-approval.

No code implementation is completed at transfer. Preserve the current uncommitted
preflight documents and accepted decisions. No real Google/model/database call, formal
case/experiment, commit/push, branch switch or later-ticket implementation is authorized.
GitHub task updates must disclose that current contracts are local/unpublished; preserve
imported history and completed dependencies. Earlier implementation-pending statements
in dated records describe the pre-approval checkpoint rather than a remaining gate.


## Subsequent implementation checkpoint — 2026-10-02

Execution continued in the approved receiving conversation. The preflight's proposed
seams and acceptance matrix are retained as the original specification checkpoint;
[implementation acceptance](ticket-06-acceptance.md) now owns actual validation results.
The preflight's 48-test run remains inspection evidence, not parser acceptance.
