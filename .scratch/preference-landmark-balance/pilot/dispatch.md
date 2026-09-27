# Authorized V3 landmark pilot execution packet

Prepared 2026-09-28 by iteration 2. User authorized preparation through live completion
without further confirmation, within plan.md's three sequential single attempts and stops.
No commit/push/freeze. Read plan.md and this packet before execution. No changes to source,
inputs, environment files or runtime; source hashes cover the validated dirty implementation.

## Readiness

Base HEAD cc4d5a0, with ticket 03 uncommitted. Full implementation regression 1793 passed /
9 skipped. New pilot-tool plus existing acceptance tests: 25 passed. Ruff/diff checks and
Standards/Spec review passed. Pure local configuration/corpus checks passed, no connections.
The batch is already prepared at logs/preference_landmark_pilot_20260928/manifest.json.
Do not prepare again. The launcher freezes source/input/runtime/environment-file hashes.

## Execute from repository root

Use authorized network access from the outset. If sandbox escalation is needed, request it
in the execution conversation citing the user's existing live authorization. Do not consume
an attempt to test whether network access works. Never print credentials or raw payloads.

Run each command in its own process, strictly in this order, once each:

```powershell
.venv/Scripts/python.exe -B -m tools.validation.landmark_pilot execute --case ordinary_sydney_v3
.venv/Scripts/python.exe -B -m tools.validation.landmark_pilot execute --case focus_melbourne_v3
.venv/Scripts/python.exe -B -m tools.validation.landmark_pilot execute --case short_brisbane_v3
```

Do not invoke `child` directly. Do not delete or reset started/finished/lock markers, capture
files or case directories. A launched failure consumes the sole attempt. Tools own the
600-second application / 660-second outer deadline. No connectivity probe or extra retry.
If preflight is blocked, report the error type/reason; do not fix code or alter dependencies.

## Between-case gate

Inspect <case>.finished.json, <case>.capture.json, <case>/execution.json, the independent
trace budget.json, result.json and normalized lineage captures. `continue_allowed` only
establishes process/capture completion; inspect for budget breaches, secret exposure,
confirmed identity/restriction violations or changed inputs before the next case. Any such
finding stops the entire batch. Soft gaps, UNKNOWNs and a legitimately skipped Repair do
not by themselves violate the contract. Read plan.md for all stopping rules.

Preserve results and report a terminal failure; do not automatically start later cases.
For successful cases, compare v3.draft/original_report with v3.final_primary/final_report,
using Repair rounds to explain accepted/rejected changes and missing evidence. Nomination
lineage is under <case>.lineage. Identify each stage by validation_stage, not UUID filename.

## Reporting and coordination

Write logs/preference_landmark_pilot_20260928/report.md in English and provide a concise
Chinese handoff: process, outcomes, real counts/timing/available usage, observed issues/Spec
deviations, missing evidence, follow-up needs and paths. Distinguish facts from inference.
Do not declare live quality superiority or change implementation. Notify iteration 2 at
thread 01a0e29d-405e-7d82-b894-d95eb7f67632; the user authorizes this coordination. This
supersedes the older iteration-1 destination for this pilot only.
