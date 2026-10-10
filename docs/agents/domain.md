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

Use [AGENTS.md Documentation](../../AGENTS.md#documentation) for maintenance principles.
This section defines project-specific ownership and evidence admission; AGENTS.md and
its linked policies retain task approval, publication, Git and research limits.

| Material | Owner | Admission boundary |
| --- | --- | --- |
| Current design, behavior or detailed contract | Existing numbered core doc, `docs/contracts/` or ADR | Maintain the current rule in its topic owner; an archive is not another current specification. |
| Current reproducible operational instructions | `docs/guides/` | Maintain usable commands and prerequisites; link dated results to their evidence owner. |
| Shareable historical engineering evidence | `docs/records/` | Retain a substantive dated decision, failure, rejected approach, implementation or acceptance event with evidence and scope beyond the current contract. |
| Local research context | Ignored `thesis_notes/` | Preserve private interpretation, research questions or thesis preparation context beyond a public engineering record; distinguish hypotheses from observations. Formal thesis writing or research evaluation still needs explicit authorization. |
| Specs, tickets, dependencies and pending decisions | GitHub Issues | Use the tracker for live state; optional local `.scratch/` copies are drafts only. |
| Temporary drafting and execution material | Ignored `.scratch/`, `artifacts/` or `logs/` | Drafts/preflight/handoffs belong in scratch, derived audits/manifests in artifacts, and original runtime evidence in logs. These do not become tracked records by default. |

Admit a public engineering record only when all of the following hold:

- It adds an event-specific rationale, observation or failure/correction/retest sequence;
  a current-design copy, routine dispatch or raw output dump is insufficient.
- It states the event date, code revision and relevant uncommitted context, design/validation
  status, evidence identifiers, actual check scope and limitations. Missing evidence is explicit.
- It distinguishes observed facts, inferences and hypotheses; implementation, validation and
  user-approved freezes remain separate. Historical commands grant no new execution authority.
- It is safe to track: exclude secrets and raw private/provider payloads. Summarize the evidence;
  label local evidence paths as historical identifiers and use only tracked or accessible remote
  destinations for published navigation.

Use `docs/records/v0-v3/` for version/shared engineering evidence, `evaluation/` for evaluator
evidence and historical benchmark decisions, and `frontend/` for frontend evidence. Merge into
the existing relevant topic/event owner before creating a file. File length or ticket count
alone does not justify another record. Existing historical records may retain incomplete metadata
with that limitation identified; never fabricate missing facts to make them meet the new gate.

Keep shareable historical conclusions in their topic record, with local research notes
adding only distinct private context. Promotion from local notes produces a sanitized
public account; original evidence remains unchanged in its existing location. Published
explanations must contain enough context to understand results without local artifacts.

When consolidating an event, retain consequential decisions, results, limitations and
necessary evidence identifiers. Preserve chronology only where it affects interpretation,
and keep compatibility paths or anchors with actual reference dependencies. Historical
rules need dated context; still-supported formats and replay interfaces remain technical
contracts. Missing or overwritten evidence must be explicit. Maintaining records does
not authorize a push, Issue publication or formal run.

## Thesis Research Archive

`thesis_notes/` stores historical research/development records for future thesis work.
It is a local archive, not a project source of truth. Shareable engineering evidence belongs
in `docs/records/`; local research context and private interpretation belong in `thesis_notes/`.
When preserving, promoting or deduplicating a record, apply the
[record admission rules](#record-admission-and-topic-ownership).

For normal development tasks:

- Proactively preserve meaningful failure diagnoses, architecture decisions, rejected approaches and development validation results in the appropriate existing record owner under those admission rules, without requesting separate approval. Read only the relevant archive files needed to place or update the record. Integrate lasting observations into the relevant topic summary; local notes may add distinct research context.
- Do not use thesis notes to determine current requirements or architecture.
- Historical notes may contain rejected, superseded, or outdated designs and must never override current project files.
- Archive updates are part of the current development task, not a separate stage requiring approval. Summarize any archive updates in the final Chinese report.

For all archive updates:

- record the date, relevant code revision and uncommitted-change context, evidence locations, and validation scope or limitations;
- distinguish observed facts from hypotheses and inferences;
- preserve key causal relationships, including consequential rejected or superseded approaches;
- distinguish design status such as `Proposed`, `Accepted`, `Implemented`, `Validated`, and `Frozen`;
- do not invent missing prompts, outputs, logs, latency, tokens, costs, or rationale;
- do not describe development smoke tests as formal benchmarks unless they were explicitly conducted as such.

Do not create a final version-level research retrospective unless I explicitly request it, normally after that version has been completed and frozen.
