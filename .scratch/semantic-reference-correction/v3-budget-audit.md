# V3 offline budget audit after short-reference smoke

Date: 2026-09-27. Source run: 1eba61e8-ad9b-48cc-9998-6e5d8392b0af.
Status: recorded call/count and selected token/time budgets reconstructed; no recorded
overrun. This is application evidence auditing, not a complete provider billing audit.
No production changes, live requests, commits or quantity Repair changes.

## Method and reproducibility

Run `.venv/Scripts/python.exe .scratch/semantic-reference-correction/audit_v3_budget.py`
from the repository root. It reads the saved result, runtime, execution and events only,
and writes `logs/semantic_short_reference_revalidation_20260927/v3-budget-audit.json`.
The initial reconstruction completed successfully: 45 range checks passed. Event sequences
are continuous from 1 through 212, with no malformed JSON lines. The script preserves
SHA-256 fingerprints of its four source files and a source location for each budget row.
The sequence check supports continuity, not proof of uninstrumented network behavior.

Ordinary send events cross-check the selection-stage tool snapshot and cumulative route
snapshots. RAG sends cross-check the final discovery counters. Repair's 12 successful sent
acquisition records cross-check its counters and round event. Nearby and semantic counts
cross-check their individual call records. Cumulative snapshots and nested round copies
are not added together. Repair routes and RAG Details have separate pools from primary
route/Details budgets; they must not be charged to the primary limits for this audit.

## Recovered budget values

| Pool / metric | Recorded use / limit |
|---|---:|
| Primary destination / candidate searches | 1/1; 3/12 |
| Primary Details / weather | 32/60; 1/2 |
| Primary admitted candidates / final POIs at selection | 64/64; 16/20 |
| Primary review Details / experience model calls at selection | 0/8; 0/8 |
| Primary baseline routes / elements | 4/7; 256/400 |
| Primary alternative route calls / unique pairs / elements | 16/32; 11/32; 16/64 |
| Official web tasks / page fetches | 0/8; 0/8 |
| RAG retrieval queries / returned positions | 2/4; 40/80 |
| RAG Details / fallback | 26/30; 4/4 |
| RAG elapsed | 15.400/360 seconds |
| Semantic calls / elapsed | 2/6; 27.412/120 seconds |
| Semantic per-call elapsed | 15.533 and 11.879, each below 45 seconds |
| Semantic engineering input | 5210 and 4493, each below 32000 |
| Semantic reported output | 3270 and 2229, each below 8192 |
| Primary generation engineering input | 65807/252000 |
| Repair rounds / model calls | 1/5; 1/5 |
| Repair routes / elements | 12/24; 12/32 |
| Repair preparation routes | 12/16 (8 of 24 reserved for post-proposal) |
| Repair new Google / fallback / embedding / retrieval / canonical / Details | all 0, within their separate limits |
| Repair engineering input / reported output | 31970/252000; 1166/16384 |
| Nearby requests / elapsed | 3/3; 1.563/10 seconds |
| Application elapsed | 114.860/600 seconds |

One primary RAG embedding send matches one saved HTTP attempt, with 7 reported tokens;
this was one batched embedding operation for two retrieval queries, not two model calls.
Reported semantic input usage (3023 and 2306) differs from engineering input counts because
the latter include conservative prompt/schema/framing accounting. Do not mix those units.

## Reached limits are not overruns

RAG fallback reached 4/4 and recorded two fallback_budget stops. Nearby used 3/3. Primary
pre-generation alternative routes used 16 calls: the other 16 of the 32-call pool were
reserved for post-generation. The final cumulative route-work snapshot contains 96
alternative_route_matrix_calls stop reasons. These are denied work opportunities, not
96 additional sends or proof that all 32 calls were consumed. Post-generation did not
increase the primary route count; Repair's 12 calls are separately recorded and budgeted.
Thus there are real coverage limits worth considering separately, but no recorded excess.

## Remaining evidence boundaries

The monolithic run.json has original_bytes=4908309 versus max_payload_bytes=1000000;
the 1090256-byte file contains a truncated preview wrapper, not a complete summary.
The event stream is usable; v3_finalized itself is intentionally summarized/truncated,
but its corresponding final result and individual Repair artifacts remain available.

Requirement captures preserve draft/outcome, not usage; dedicated main-generation token
usage is not present in the surviving evidence examined. Therefore complete requirement/
main-model billed token totals, every individual provider latency and a monetary total
cannot be reconstructed here. Engineering input checks and configured output/time caps
are not substitutes for missing actual usage. No claim of complete billed-token or
packet-level auditing is made. The 38 activities' null monetary costs are a separate
travel-budget issue, unrelated to this API resource-budget audit.

## Recommendation

The initial V3 aggregate provider-count gap is now closed at the recorded application
counter level. No further live attempt is needed to establish those recorded counts.
Recommend a small independent, bounded final budget/usage summary (e.g. budget.json),
containing effective limits, per-pool final counters and per-stage reported usage/missing
status, written before any large-payload truncation. Reuse existing counters and call IDs;
do not serialize the full itinerary or payload history into it. An offline test should
force run.json truncation while keeping that summary complete and avoiding double counts.
This is a proposal only, not implemented by this audit.

Raising max_payload_bytes above 4,908,309 would preserve this specific run and is a valid
low-effort temporary option, but duplicates a multi-megabyte result and moves the cutoff;
future growth may lose the same end-of-run fields. A separate compact summary is preferable
for recurring budget audits. Do not change API budgets or quantity Repair based on this
trace-storage issue. Any implementation or limit change needs its own approved scope.
