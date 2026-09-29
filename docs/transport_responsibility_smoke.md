# Transport responsibility development acceptance

Date: 2026-09-30 (Australia/Sydney). Status: bounded development validation completed;
not a formal benchmark, independent factual evaluation or version freeze.

## Implementation boundary

V0 retains model-estimated transport activities. V1-V3 prohibit declared model
transport in their primary DTO and shared output acceptance; initial and Repair
prompts reserve mode selection and transfer timing to the application. Existing
Routes binding and Repair permissions remain unchanged. Independent evaluation
selects V0 activities or V1-V3 transfers, retaining ignored-source provenance
without using it as transport occupancy or fallback. Ticket 05 scoring remains pending.

## Live evidence

The authorized Berlin input covered October 3-5, 2026, two travelers, EUR 1500,
and `We want to have an enjoyable trip in this city.` Each version ran once,
sequentially, against HEAD `1eb441f47cb0de65eb1c687eb56a45dba286aa86` plus the
uncommitted Ticket 04 and transport correction. The evidence manifest froze the
actual source/configuration/input/environment hashes. No code or HEAD changed
during execution. All processes ended before the subsequent authorized commits.

| Version | Main visits by day | Model transport activities | Application transfer coverage | Nearby |
| --- | --- | --- | --- | --- |
| V0 | 3 / 3 / 3 | 6, explicitly estimated | Not applicable; zero transfers | 2 |
| V1 | 4 / 4 / 3 | 0 | 8 / 8 cross-place adjacencies | 3 |
| V2 | 4 / 3 / 2 | 0 | 6 / 6 cross-place adjacencies | 3 |
| V3 | 3 / 2 / 3 | 0 | 5 / 5 cross-place adjacencies | 3 |

All four processes exited successfully and delivered all three dates. The iteration
owner independently replayed structural inspection against the saved results:
no missing/invalid binding, orphan transfer or unlocatable adjacency was observed.
The executor reviewed titles/notes and found no disguised transport activities.
The 19 adopted transfers cite Routes evidence with matching occurrence identities,
direction and chronological bounds. These observations support the source and
binding boundary, not independent real-world travel feasibility or trip quality.

V3 retained its original itinerary: 10 PASS and 13 UNKNOWN findings, with
`scope=null`, `repair=null`, and `no_authorized_targets`. Repair was not exercised
live. V2/V3 each used one embedding send, one retrieval query and 20 returned
positions; both RAG outcomes were partial. Recorded tool budgets were within
limits; primary and requirement billed token usage was missing, not zero.
No total cost claim is made. There was no retry, blind review or extra live case.

## Actual verification sequence

1. Prepared a new bounded launcher and structural inspector; corrected initial
   lint/format issues. Ten mocked packet tests and 60 related readiness tests passed.
2. The first read-only preflight falsely reported environment drift because it
   omitted `local_dependencies()` before hashing. Matching the launcher's local
   environment-loading order resolved it; no live attempt had been consumed and
   no manifest, source or budget was reset.
3. Executed V0-V3 once each. Final manifest was `finished`; the executor confirmed
   frozen hashes still matched and no live process remained.
4. Before the user-authorized workspace commits, ran the full backend suite plus
   the packet tests: **1983 passed, 10 skipped in 125.06 seconds**. Skips were nine
   opt-in database cases and one Windows symlink privilege case. Ruff check,
   format checks for new Python files and diff whitespace checks passed.

Earlier Ticket 04 and transport-correction failures, fixes and retests remain in
their acceptance records; their counts overlap this combined run and are not additive.

## Evidence and preservation

The tracked [execution plan](../.scratch/transport-smoke-20260930/plan.md), launcher,
input and mocked tests preserve the development procedure. Its one-shot allowance
is exhausted; committing the packet does not authorize another execution.
Local evidence remains under `logs/transport_responsibility_20260930/`:
`manifest.json`, `report.md`, `itineraries.md`, per-version result/execution/pair
observations and captures. Logs, raw output, environment files and local research
archives stay Git-ignored and are not included in a fresh checkout.

The historical plan's no-Git execution restriction applied during the smoke. The
user subsequently explicitly authorized classifying and committing all eligible
workspace changes without another approval. This does not authorize a push,
formal evaluation, new ticket, extra live run or version freeze.

## Local commit groups

- `97d02ad` — `feat(evaluation): add bounded evidence snapshots and offline replay`
- `13cce80` — `fix(planner): reserve tool-backed transport for application transfers`
- `dc8b97b` — `fix(evaluation): select transport claims by planner version`
- `9ff8e9b` — `test: preserve bounded three-day transport smoke tooling`
- The documentation closeout commit containing this record preserves cross-module
  status and acceptance history separately from the implementation groups.

Implementation and directly related tests were kept together; the shared intake
test file was partially staged so its snapshot import allowance belongs to Ticket
04 and its transport assertions belong to the transport-source correction.
No ignored evidence or environment file was force-added.
