# Quantity quality through existing comparison-pool reuse

Status: Approved, implemented and offline-validated; separately approved D quantity pilot completed.
Date: 2026-09-26

Pilot outcome: the new sample's three quantity gaps were resolved under existing budgets
and canonical-ID rules. Factual UNKNOWNs remain limitations. The user declined further
parent/exhibit work; that relationship is not an established defect or an open task.
See `artifacts/poi_semantics_acceptance/20260926_D_quantity_review/report.md`.

## Goal and boundaries

Evaluate and, only where a demonstrated defect requires it, minimally improve V3 local
quantity repair using the full existing comparison pool. Preserve the user's accepted
semantic extension/D milestone. The user approved offline implementation and testing.
One subsequent D live pilot was separately approved and completed. Additional live calls,
commits, a version freeze and formal research evaluation remain unauthorized.

For D, quantity review would create four one-visit gaps on October 4, 6, 7 and 8.
This is a regression example, not a fixed list in production. For every request, derive
target dates and counts from the existing validator/scope policy. Keep its existing
addition-only permissions for quantity-only targets. No global rescheduling,
new move/retime/delete/replace permissions, revisits, default-policy changes, prompt quota
hardening, capacity increases or P3 work. V0-V2 behavior remains unchanged.

## Current implementation already available

V3 wiring constructs a canonical-deduplicated pool from enriched_candidates and remaining
admitted_candidates and passes it into run_repair_stage with request cache, route evidence
and request-owned semantic service. prepare_candidates admits qualified comparison-pool
Details before fetching missing Details or discovering new identities. Candidate/date
associations, independent identity capacity, selected input and blocked reasons already
have audit structures. Reuse is an existing capability, not a proposed new subsystem.

The V3 CLI already supports --repair-quantity-review. Default remains false. At proposal
time the development acceptance wrapper lacked a matching explicit override; the approved
implementation adds a thin pass-through, preserving explicit-override provenance.
It must not silently mutate config/runtime.yaml or other review flags.

## Smallest proposed implementation package

1. Add focused offline SDK/service/graph-boundary tests of the existing pool-to-Repair
   path, using external-boundary fixtures. Fix production selection/wiring only if a
   failing test establishes a concrete violation of reuse, authorization or evidence
   rules. If the existing path passes, do not refactor it for its own sake.
2. Add an opt-in, development-only pre-Repair replay snapshot, bounded and redacted,
   containing the original itinerary/requirements, full typed enriched/admitted pool,
   selected IDs, available place/effective evidence, route bundles, semantic assessments
   and cache-key identity information needed to establish reuse, schedule/scope,
   runtime/prompt fingerprints and consumed/remaining request and Repair budgets.
   Never store credentials, live clients, raw provider envelopes or executable cache
   objects. Capture truncation/failure must be explicit and cannot change planning.
3. Build a no-network replay entry that reconstructs typed context and runs scope,
   windows and candidate preparation over the saved pool. Absent evidence stays absent;
   missing cache/context fields must be reported, not silently replaced with a fresh
   budget or model. Synthetic fixtures are labeled synthetic. No repair-model call.
4. Expose existing quantity-review override in the acceptance wrapper if needed for a
   later pilot. Default off. Existing requirement/semantic capture remains available.
   Live authorization remains a separate step after offline review.

Likely files: tools/validation/poi_semantics_acceptance.py and a small replay/capture
helper; tests in backend/tests/versions/v3 and acceptance-tool tests; project status/docs.
A narrow observer seam in V3 wiring is allowed only if existing trace facilities cannot
preserve a reconstructable snapshot. No broad tracing or new runtime infrastructure.
Use a bounded serialized snapshot (proposed maximum 4 MiB per case); overflow marks it
incomplete rather than silently dropping inconvenient candidates. Reuse existing
secret-redaction conventions and immutable file creation.

## Offline verification

| Check | Required observation |
| --- | --- |
| Full pool reaches preparation | Nonselected enriched and admitted candidates remain represented, canonical IDs deduplicated; selected supply is not the only source |
| Reuse first | Qualified stored Details and matching semantic cache entries require zero new corresponding calls; stale fingerprints do not masquerade as cache hits |
| General local targets | Synthetic one-, three- and five-date cases derive their own addition dates without existing-activity or revisit permissions; D's four dates remain historical evidence only |
| Independent identities | One candidate linked to two dates counts once; four gaps require four compatible distinct additions when moves/revisits are unauthorized |
| Eligibility and windows | Closed/excluded/non-main/future-opening and out-of-scope candidates are rejected; real opening/calendar intersections and typed unknowns retained |
| Transport | Valid available modes considered; long WALK does not imply all modes impossible; missing motor routes are unresolved, not fabricated PASS |
| Budget preservation | Reused data is free of new sends, required missing evidence remains within existing totals/reserves; exhaustion terminates honestly without budget reset |
| Adoption controls | Synthetic patches for compatible additions can improve quantity; repeat, unauthorized edits, confirmed regressions and evidence violations cannot be adopted |
| Observability | Candidate/date decisions distinguish eligible, excluded, missing evidence and capacity omission; incomplete snapshots fail clearly, no automatic retries |
| Default behavior | Review off still produces the original behavior; V0-V2 and other review policies unchanged |

Use realistic synthetic pools containing both already-selected and nonselected choices,
including four geographically distinct date-local candidates, one multi-date identity,
and blocked/unknown controls. These test mechanism behavior, not London's actual supply.
Run focused tests first; broaden shared-boundary testing only if shared code changes.

## Missing historical evidence

- Full enriched/admitted candidate objects and nonselected Details were not preserved in
  replay-ready form. The historical 37-eligible count is not a reconstructed typed pool.
- Semantic captures hold compact candidate identity/type/source projections, not all
  date-specific hours, normalization/factual-gate inputs or request-cache records.
- Saved route projections lack complete raw typed bundles for every insertion pair,
  particularly applicable motor-mode/departure evidence for new insertions.
- No real quantity-enabled Repair proposal/adoption exists for D. The initial generation
  cannot explain every omitted candidate, and offline replay cannot invent that reasoning.

Consequently do not retrospectively declare D repairable or unrepairable. Capture-only
support cannot recreate lost history. A later separately authorized run would be a new
sample, not an exact historical counterfactual.

## Unchanged budgets

Request deadline 600 s; Repair stage 360 s, at most 5 rounds/5 model calls, round 120 s,
model 70 s, preparation 45 s with existing reserves. Input identity union 32, activity
capacity 120. Repair totals: Google 6 including fallback reservation 1, embedding 1,
retrieval 1, canonical 30, Details 30, route sends 24 with 8 reserved post-proposal,
route elements 32. Semantic assessment remains request-wide 6 calls/120 s, sharing usage
already consumed before Repair; never reset it on phase change. Existing geographic,
per-leg and daily added-burden rules remain unchanged.

## Acceptance gates

Offline engineering acceptance: required tests pass; complete synthetic snapshots replay
deterministically without network; real incomplete history remains explicitly incomplete;
full-pool reuse, permissions and budgets are preserved. Passing does not establish live
quantity improvement or authorize a live test.

Future development pilot, separately authorized: fixed D input, explicit quantity-review
override, unchanged budgets, single run with full relevant capture, stop on clear defect
or dependency failure and no automatic retries. Report candidate counts, per-date usable
independent choices, reused versus newly acquired evidence, model/route usage, adopted
changes and remaining gaps. Protect zoo satisfaction, accurate climbing substitution and
canonical nonrepetition.

Full quantity success: all four originally sparse dates reach at least two qualified,
distinct main visits without unauthorized edits/repeats, new confirmed violations or
budget breaches. UNKNOWN facts remain UNKNOWN. Fewer resolved dates means partial
improvement, not full success. No supported additions means an honest remaining limitation,
not justification to increase budgets or bypass constraints. Product complete alone is
not an acceptance criterion. Actual model/provider reliability is not established by
one pilot.

## Approved boundary

The user approved only the offline implementation/testing and bounded replay-capture package above.
Any broader generation/rebalancing change, production default change, new live run or
commit requires separate approval. If a newly failing test requires changes outside this
scope, report the concrete finding before expanding work.
