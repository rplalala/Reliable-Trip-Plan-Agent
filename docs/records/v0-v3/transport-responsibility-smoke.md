# Transport Responsibility Smoke

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

## Implementation boundary

V0 retains model-estimated transport activities. V1-V3 prohibit declared model
transport in their primary DTO and shared output acceptance; initial and Repair
prompts reserve mode selection and transfer timing to the application. Existing
Routes binding and Repair permissions remain unchanged. Independent evaluation
selects V0 activities or V1-V3 transfers, retaining ignored-source provenance
without using it as transport occupancy or fallback. Ticket 05 scoring had not yet been implemented at this checkpoint.

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

## Verification and source integrity

The bounded launcher/inspector passed **10 mocked packet tests** and **60 related
readiness tests**. Preparation initially reported environment drift because its hash
probe omitted the launcher's `local_dependencies()` loading order. Matching that order
resolved the discrepancy before execution, without resetting frozen sources or budgets.
Each V0-V3 invocation then ran once. The finished manifest verified unchanged source/
configuration hashes and no remaining process.

Full backend plus packet tests: **1983 passed, 10 skipped**, 125.06 seconds. Nine database
opt-ins and one Windows symlink case skipped. Ruff, changed-file formatting and diff
checks passed. Earlier Ticket 04/transport gates overlap this result and are not additive.

## Evidence and preservation

The tracked [execution plan](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/39), launcher,
input and mocked tests preserve the development procedure. Its one-shot allowance
is exhausted; committing the packet does not authorize another execution.
Local evidence remains under `logs/transport_responsibility_20260930/`:
`manifest.json`, `report.md`, `itineraries.md`, per-version result/execution/pair
observations and captures. Logs, raw output, environment files and local research
archives stay Git-ignored and are not included in a fresh checkout.
