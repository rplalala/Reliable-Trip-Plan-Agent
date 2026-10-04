# Evaluation offline CLI usage acceptance — 2026-10-04

Tracker: [Issue #49](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/49).
Status: Offline workflow checks validated; fixed-base dual-axis review completed.
The user approved this separate usage task after Tickets 01-12 and parent #12 were closed.
Starting review fixed point: `b003c49e7f79c9d38dd8cf896673fcf1dca4ee07` on
`feature/evaluation`, with clean tracked worktree/index. No production module is changed.
Unrelated concurrent documentation commits `65f151e` and `0d616c5` appeared during
execution and are excluded from the task review. The task's committed implementation is
`c877b6ec9dc78e4803fb7f6df10a4a31bbd8f2ed`
(`test: validate offline evaluation CLI usage (#49)`).

## Scope and observed behavior

The new subprocess tests exercise public `python -m backend.evaluation...` commands,
reusing the existing synthetic development fixtures. They retain input JSON, snapshots,
command argv/exit code and UTF-8 stdout/stderr in ignored `artifacts/evaluation-usage/`.
Each invocation checks pre-existing packet source hashes for immutability. External socket
connections are guarded; loopback is permitted for the event loop's internal socket pair.
The controlled executor additionally retains its existing frozen ports/clock/network guard.
Regression subprocesses use the same synthetic tokenization convention as the parent
test suite, avoiding a dependency on downloaded vocabulary. No payload measurement is claimed.

| Workflow | Bounded result |
| --- | --- |
| Four-version quality and resources | All V0-V3 appear. Synthetic V1 auxiliary score is 50; its two opening checks remain UNKNOWN. Unavailable token usage is null and adds no quality penalty. Reviewed empty hard obligations are N/A; the architecture preference is not promoted to a hard requirement. |
| V3 paired overlap/retime | An adopted edit moves visit B from 09:30-10:30 to 11:00-12:00 while visit A remains 09:00-10:00. Confirmed overlap is resolved through source lineage, with no removed visits. Grounding delta is exactly 0/1. Other incomplete route/occupancy evidence leaves the auxiliary-total delta null. |
| Controlled overlap | Real frozen V3 replay retimes B from 10:30-11:30 to 11:30-12:30, resolving its overlap with A at 10:00-11:00. Independent target outcome is `resolved`. |
| Unchanged control | A valid one-visit fixture stays unchanged: `valid_no_change`, with zero model attempts. |
| Lawful addition | Independent checks support adding a second visit: `lawful_change`, with one frozen model attempt. |
| Exclusive addition | Original text says “Exactly one primary visit on this day.” The fixture deliberately omits this restriction from the planner interpretation. Internal Repair accepts the addition, but the independent guard changes PASS to FAIL and reports `regressed`. |
| Mechanism and official audit | Actual controlled preparations yield one V3 run rather than invented V0-V2 runs. Separately simulated complete capture channels across V1-V3 give three run-bound claim units, two occurrences each. Simulated reviews cover all three. Missing captures leave total qualifying population null and observed count zero. Other absent optional channels remain unavailable. |
| Blinded package/import/report | The acceptance packet embeds the existing built React renderer, keeps private mapping outside the public directory and exposes labels A-D. Synthetic answers import at revision 1 and produce one descriptive main task. No actual rater session occurs. |
| Invalid input | A missing manifest and a disposable changed-result copy with its old expected hash both exit 2. Diagnostics identify the file; the latter says `Artifact hash mismatch`. Original selected files remain unchanged. |

Complete processing is distinct from independent PASS. The regression control and UNKNOWN
examples intentionally process successfully. Synthetic capture occurrences/verdicts and
ranking answers demonstrate linkage and reporting only; they are not actual recorded model
submissions, an independent human truth audit, or research observations.

## Validation sequence

The first slice initially failed at pytest setup because the parent of the requested
`--basetemp` directory did not exist. Creating that parent allowed the intake/quality/resource
slice to pass. Later new-test failures and inspection exposed mistaken assertions: `accepted` versus
`complete`, `resolved` versus `resolved_conflict`, the target's `independent_outcome` field,
the intake's `material_diagnostics` field, and per-run audit units rather than global merging.
The assertions were corrected against existing public contracts and observed JSON.

An attempted four-final report using the paired snapshot exited 2 with
`unsupported_snapshot_scope`. This was correct existing behavior. The examples now use
their separate final-only and paired scopes, and the guide makes the distinction explicit.
These were acceptance-harness/material mistakes; no production defect is inferred.

An intermediate complete packet passed **9 tests in 83.71 seconds**, using the real built
renderer and the existing local tokenizer vocabulary. The final regression harness also
uses synthetic tokenization so a clean checkout needs no tokenizer download, and tightens
the invalid-material diagnostic assertions.

Final checks before the implementation commit:

- Usage file with real renderer selected: **9 passed in 92.25 seconds**. Forty actual
  module processes completed: 38 exited 0 and the two intended invalid-input examples
  exited 2. No external-network block appeared in their retained stderr.
- Full backend gate: **2490 passed, 10 skipped in 319.18 seconds**. The skipped checks
  include guarded local PostgreSQL cases and the host symlink-privilege check;
  this was not a live-service acceptance.
- Ruff check and format check on the new file passed; `git diff --check` passed.
- `npm --prefix frontend run build:blind-review` passed its TypeScript check and Vite build.
  Rebuilt JS and CSS were confirmed verbatim in the acceptance packet's HTML. Their byte
  SHA-256 values were `cab999fb2c18f5979d4a033ea4f095f61c95727817d57925d4f9b12ade5d3a7c`
  and `14c23164703086562b4fabebf5d845ede3c7713ea76058ded3e3eba5eb97b71d` respectively.

Standards and Spec reviewed the committed implementation independently against the original
fixed point, excluding the unrelated concurrent documentation commits. Both axes reported
zero blocking findings; Standards found no documented violation or required smell cleanup.
Spec also checked the actual packet and real embedded renderer. Its optional suggestion
was to assert more non-overlap count deltas in addition to the existing exact grounding
delta. The current packet already preserves those counts, and the guide explains that
resolving one conflict does not establish whole-itinerary PASS. No correction was required.
No production module changed, and there is no review-fix commit to invent or absorb.

Final documentation updates add the executable demo and report-reading table to the existing
package guide, use PowerShell 7 UTF-8 JSON saving instead of encoding-dependent redirection,
index this record, and record bounded usage acceptance in PROJECT.md. Local document links
were checked against tracked or current-task intended files; none were missing or depended
on ignored material. `git diff --check` passed. Local thesis notes retain a pointer and
private evidence identifiers rather than duplicate this record.
The PowerShell 7 saving example was also checked with an accented English JSON string;
the resulting bytes decoded as UTF-8, had no BOM and parsed successfully.

Local evidence identifiers (not publication dependencies):
`artifacts/evaluation-usage/first-slice-2/`, `second-slice/`, `third-slice/`,
`accepted-packet/`, `final-packet/`, `usage-gate.txt`, `backend-gate.txt` and their
per-test `cli-output/` folders.
The [package guide](../../../backend/evaluation/README.md#start-with-the-synthetic-usage-packet)
contains the reproducible demonstration command and report-reading examples.

## Boundaries

No live Google/LLM/database run, real trip generation, new API fee, budget increase,
formal corpus construction, statistical comparison, thesis conclusion or version freeze
is authorized or claimed. Source contracts, V0-V3 execution paths and production behavior
remain unchanged. The existing native browser acceptance is reused; package generation
does not establish a new native storage/download acceptance result. There is no new universal
CLI, UI or evidence acquisition system. Publication needs separate approval; new commits
and documents stay local until an authorized push.
