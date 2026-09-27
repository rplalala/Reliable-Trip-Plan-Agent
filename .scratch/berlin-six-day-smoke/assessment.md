# Berlin smoke assessment

## Later itinerary-only blind review authorization and result - 2026-09-28

After the original evidence-gated stop, the user explicitly instructed `smoke tests`
to evaluate itinerary quality and ignore budget for this blind review. Iteration 2
verified that user message and the executor's saved review/mapping. The executor used
one no-history reviewer with only the common input and four anonymous full itinerary
projections, saving the anonymous response before revealing the mapping.

The reported order A > C > B > D maps to V0 > V3 > V2 > V1. The simulated traveler
favored V0's variety and relaxed pacing; V3 offered richer content but more museums
and cross-district movement; V2's final two days were sparse; V1 repeated venues.
These are the reviewer's judgments, not verified geography, general traveler preferences
or causal conclusions. All costs and venue access remained unverified.

Evidence: `logs/berlin_six_day_20260928/blind_packet.md`, `blind_mapping.json`,
`blind_review.md` and the execution report addendum. The original manifest stays
`stopped_budget_evidence`, with its original `blind_review_eligible=false`; the later
review is separately authorized and does not repair that evidence gap. No rerun occurred.
The reviewed V0 itinerary predates the subsequent transport/Nearby prompt adjustment;
the ranking cannot be attributed to or validate that change. V1 repeats remain an
accepted version limitation, not a current implementation task.

## Subsequent user decision - 2026-09-28

The user considers V1 repeats normal for the scope of that intermediate version;
they remain observed output limitations, not a current fix task or a new requirement
for V1. The proposed repeat investigation below is not proceeding.
The user selected a 10 MB (10,000,000-byte) runtime capture threshold instead of the
earlier proposed 8 MB. This configuration-only change is implemented for subsequent
runs; the frozen Berlin artifacts, cap and failed evidence gate are unchanged.
No new live execution or blind assessment was authorized by this adjustment.
Validation: observability, runtime configuration and V3 wiring tests passed (92 tests,
9.68s); `git diff --check` passed. Offline synthetic payloads with 6,041,655 and
9,999,000 data bytes were preserved, while 10,001,000 data bytes triggered truncation;
secret redaction passed in all three cases. No provider was called.

Date: 2026-09-28, Australia/Sydney. Status: Assessed; execution complete, evidence gate
failed. Revision: `e68d8e6a4297d50a98fcacb3241d392781dec022` plus the frozen development
launcher. Documentation-only working changes and older unrelated scratch work remain.
No production change, extra attempt, blind reviewer, commit, or freeze was authorized
or performed during this assessment.

## Verified observations

Iteration 2 checked the executor report against the batch manifest, all four result
files, V1-V3 run/budget records, and V3 original/final validation target counts.
The four independent applications each ran once and exited zero with six nonempty
ordered days. Scheduled activity counts are V0 16, V1 14, V2 14, V3 17.

- V0 policy completion is unassessed by design; successful generation is not policy
  or feasibility validation.
- V1 reports four unauthorized cross-day repeats and one below-target day. It failed
  that output policy despite structural completion. The executor's brief pause was
  corrected by referring to this batch's actual stop conditions; the original V2/V3
  allowance continued without changing the policy, budget, or input.
- V2 reports no repeat-policy failure but two below-target days. V2/V3 RAG ran and
  contributed scheduled places, with partial identity-resolution outcomes. Neither
  contribution nor the four independent stochastic outputs establishes causal benefit.
- V3 changed daily counts from 4/4/3/1/1/1 to 4/4/3/2/2/2 through one accepted Repair
  round. Original validation had three improvement targets; final validation has zero.
  Final findings still include 22 UNKNOWNs: opening 3, visitor suitability 17, budget
  1, semantic requirements 1. This supports targeted shortage repair in this case,
  not fully verified travel feasibility or universal reliability.
- All 61 scheduled cost fields are unknown; the shared EUR 3000 budget is unverified.

## Evidence gate and bounded diagnosis

V3's standalone `budget.json` is complete, and the recorded counters reported by the
executor stayed within limits. However, `run.json` explicitly records `truncated=true`
and `original_bytes=6041655`. The frozen `trace.max_payload_bytes` was 1000000.
`backend/app/observability/run_trace.py` wraps an oversized serialized payload in a
truncated preview at that threshold. This directly explains the missing full run
record; it is not evidence of application failure or excessive provider spending.

The frozen launcher therefore correctly recorded `stopped_budget_evidence` and
`blind_review_eligible=false`. The state name includes budget evidence because the
gate inspects both run and budget records; the budget summary itself is not truncated.
Do not rename this as a successful batch, reconstruct missing trace content, relax
the gate after observing results, or present a winner. No blind review was performed.
The full final itineraries remain readable in the executor's `itineraries.md`.

## Recommended next scope (proposed, not implemented)

First address evidence capture offline. Compare a bounded capture-only increase from
1,000,000 to 8,000,000 bytes against reducing duplicated nested run data. The observed
6,041,655-byte record fits the former with headroom, making it a simpler candidate
before adding new trace mechanisms. This changes local serialization/storage limits,
not LLM tokens, API call allowances, or acceptance requirements. Expected API cost
increase is zero; local I/O, memory, and retained diagnostic volume may increase.
It is not a guarantee that all future records fit, nor permission to enable raw data.

Any approved implementation should use offline synthetic payloads around both limits,
preserve truncation and secret-redaction behavior, and keep the hard cap. Reject or
revert the increase if it causes unacceptable local resource use or capture safety
regression. Do not silently change this frozen batch or use a new cap to claim the
missing old trace was captured. A new live attempt requires a separate bounded scope.

Separately, investigate V1's repeat-policy failure offline with the saved request,
supply and output before proposing changes. V0/V1/V2 version boundaries remain intact;
do not add V3 validation/Repair to earlier versions just to make this case pass.

## Evidence

- `logs/berlin_six_day_20260928/report.md`: execution process, budgets and limitations.
- `logs/berlin_six_day_20260928/manifest.json`: attempts, freeze and failed evidence gate.
- `logs/berlin_six_day_20260928/v*/result.json`: saved outputs and available diagnostics.
- `logs/berlin_six_day_20260928/itineraries.md`: faithful user-readable projections.

This is development smoke assessment, not a formal benchmark or thesis conclusion.
