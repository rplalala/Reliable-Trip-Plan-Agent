# Project documentation

`PROJECT.md` is the current source of truth for project scope and status.
Use `docs/README.md` to locate the design or development document relevant to the task.
Read only the relevant current files; consult historical records when the task requires them.

`logs/` contains local run evidence, and `artifacts/` contains local diagnostic and validation outputs.
Both are ignored by Git. Read them only when a specific implementation or diagnosis needs that evidence.
Neither directory is the issue tracker.

GitHub Issues are the formal location for specs, parent/child tickets and task state.
Detailed enduring contracts and acceptance evidence belong in tracked topic documents:
merge related content into numbered core owners and `docs/contracts/`, with dated
development/milestone/acceptance records under the tracked `docs/records/` tree. Optional `.scratch/` drafts and
local ticket copies are ignored and never formal document owners. Published documents
link only to tracked repository files or accessible remote URLs. Quoted local evidence
paths are historical identifiers, not shared dependencies.

## Domain layout and consumers

This is a single-context modular monolith. `PROJECT.md` remains the current source
of truth; do not create a competing project-context document during skill setup.
There is no project-wide CONTEXT.md. Existing numbered ADRs in `docs/adr/` record
consequential established decisions. Add glossary terms or ADRs only when approved
domain-modeling work needs them, aligned with PROJECT.md.
Use the existing [evaluation terminology](../0006-independent-evaluation.md#scoring-semantics-and-uncertainty) for evaluation terms.
Read only relevant contracts and decisions, use their defined vocabulary, and surface
conflicts with recorded decisions explicitly rather than silently overriding them.

## Record admission and topic ownership

Use `docs/records/v0-v3/` for version and shared engineering evidence,
`docs/records/evaluation/` for evaluation records, and `docs/records/frontend/`
for frontend evidence. Operational commands belong in `docs/guides/`. Benchmark design history belongs
in evaluation with its accepted/proposed/frozen status explicit. Historical failure and
retest sequences are retained even when a later contract changes; current contracts must
not be duplicated there as whole-file backups. Merge new evidence into a relevant owner.
Keep dispatch/preflight packets, handoffs, commit plans, migration inventories and temporary
coverage/link audits in ignored scratch/artifacts. Publish useful decisions/specification
discussion to the relevant Issue; a local working copy is optional. Before retiring a
record, merge still-valid technical rules into core docs and redirect dependencies to
the actual current owner or accessible historical Issue/revision.
