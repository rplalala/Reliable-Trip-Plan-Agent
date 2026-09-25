# Codex Development Rules

This repository is a Capstone / Thesis B travel-planning research project.

Read `PROJECT.md` when project-level context is needed.
Treat `PROJECT.md` as the current source of truth.

Historical proposal, meeting, slide, paper, reference, or thesis-note files may contain older decisions.
Do not read all historical/reference files unless I explicitly ask or they are necessary for the current task.

## Current Responsibility

For now, you are responsible only for:

- system design,
- software architecture,
- implementation,
- implementation testing,
- maintaining independently runnable V0, V1, V2, and V3 versions.

Do **not** start the following unless I explicitly ask later:

- formal benchmark design,
- formal V0/V1/V2/V3 benchmark comparison,
- formal experiment analysis,
- formal thesis writing,
- final research conclusions.

Small development-time pilot scenarios are allowed only to verify that an implementation works.

Historical research-note preservation under `thesis_notes/` is allowed only when I explicitly request thesis/archive work.
This does not authorize formal thesis writing or formal research evaluation.

## Language Policy

All repository content must be written in **English**.

This includes:

- file names,
- directory names,
- source code identifiers,
- class names,
- function names,
- variable names,
- code comments,
- docstrings,
- log messages,
- error messages,
- test names,
- configuration keys,
- database table names,
- database column names,
- API field names,
- README and project documentation,
- Git commit messages when commits are explicitly requested.

Do not write Chinese text inside project files unless I explicitly request Chinese for a specific user-facing feature.

When communicating with me in Codex chat, use **Chinese** for:

- plans,
- confirmations,
- explanations,
- progress reports,
- debugging explanations,
- milestone reports,
- recommendations.

Technical identifiers, file names, API names, library names, and code snippets should remain in English inside Chinese explanations.

## Collaboration Workflow

For every meaningful development task:

1. Inspect only the relevant current files.
2. Before making major changes, briefly tell me in Chinese:
   - what you plan to do,
   - important files you expect to create or modify,
   - the implementation approach,
   - tests/checks you plan to run,
   - whether the change could affect any existing V0/V1/V2/V3 behavior.
3. Wait for my explicit approval.
4. After approval, implement only the agreed scope.
5. Run relevant tests/checks.
6. When finished, report in Chinese:
   - what was implemented,
   - important files changed,
   - test/check results,
   - important limitations or unresolved issues,
   - recommended next step.
7. Do not start the next stage without my approval.

### Self-contained documentation update reports

When updating project documentation, also include a brief, self-contained Chinese summary of
the updated content in the final chat response. The user forwards these responses to ChatGPT
on the web, where local repository links and files are not available.

- Explain the substantive changes, current status, important boundaries and remaining limitations.
- When documenting validation, summarize the actual test sequence, initial failures, corrections
  and retest outcomes at a level sufficient to understand the result without opening the file.
- Local document links are supplementary references, not a substitute for this summary.
- Do not require the user to upload the updated document merely to understand the report.
- Keep the summary concise; do not reproduce the entire document or unrelated project history.

## Git Commit Policy

Only create commits when I explicitly ask.

Before committing:

1. Inspect the relevant diff.
2. Propose a logical commit grouping in Chinese.
3. Wait for my approval unless the grouping has already been approved.
4. Run relevant tests/checks; if they fail, stop and report.

Prefer small, logically coherent commits grouped by responsibility or capability.

Keep implementation and its directly related tests in the same commit.

Avoid mixing unrelated concerns such as feature behavior, shared infrastructure, frontend changes, provider integrations, observability, and documentation when they can be separated cleanly.

Use partial staging when necessary.

Do not change implementation solely to force an artificial commit split.

Do not force-add ignored files unless I explicitly authorize it.

Never commit secrets, `.env` files with real credentials, runtime logs, raw provider/LLM payloads, temporary generated files, or ignored files unless explicitly authorized.

Use concise English Conventional Commit-style messages when appropriate:

- `feat:` new capability
- `fix:` bug fix
- `refactor:` internal restructuring
- `test:` independent test-only change
- `docs:` tracked documentation
- `chore:` maintenance/tooling

Commit messages should describe the logical change, not list files.

After committing, report the commit hashes/messages, test results, and final `git status`.

Do not push, merge, create a PR, or switch branches unless I explicitly ask.

## Version Rules

Development sequence:

- V0: Plain LLM
- V1: V0 + External Information / Tools
- V2: V1 + RAG
- V3: V2 + Validation + Targeted Repair + Re-validation

V0, V1, V2, and V3 must remain independently runnable.

Do not overwrite an earlier version when implementing a later version.

Prefer shared components plus version-specific graph/configuration/entry points.

Changes to shared components must not silently change the intended behavior of earlier versions.

At a minimum, preserve independent execution paths such as:

```text
scripts/run_v0.py
scripts/run_v1.py
scripts/run_v2.py
scripts/run_v3.py
```

## Version Freeze Documentation

A version is considered frozen only after I explicitly approve it as final/stable.

Passing tests, live smoke tests, or completing implementation does not automatically freeze a version.

When I explicitly approve a version freeze:

1. Update the corresponding version documentation to match the actual implemented state.
2. Record final architecture, behavior, configuration, test/live-smoke status, known limitations, and approved post-milestone changes.
3. Preserve historical accuracy; do not rewrite later changes as if they existed in the original milestone.
4. Do not document future/unimplemented features as part of the frozen version.
5. Do not begin the next version until the documentation update is complete and I approve moving forward.
6. Do not force-add ignored documentation files or commit/push unless explicitly authorized.

Examples:

- V0 → `docs/v0_milestone.md`
- V1 → `docs/v1_design.md` and any V1 milestone/final-status document
- V2/V3 → corresponding version documentation

## Thesis Research Archive

`thesis_notes/` stores historical research/development records for future thesis work.
It is **not** a project source of truth.

For normal development tasks:

- Do **not** read or modify `thesis_notes/` unless I explicitly request thesis/archive work.
- Do not use thesis notes to determine current requirements or architecture.
- Historical notes may contain rejected, superseded, or outdated designs and must never override current project files.
- If a development task produces a meaningful thesis-relevant experiment, failure, or architecture change, mention it as a possible `Thesis-note candidate`, but do not update the archive automatically.

When I explicitly request thesis/archive work:

- preserve historical sequence, including rejected and superseded approaches;
- distinguish design status such as `Proposed`, `Accepted`, `Implemented`, `Validated`, and `Frozen`;
- do not invent missing prompts, outputs, logs, latency, tokens, costs, or rationale;
- do not describe development smoke tests as formal benchmarks unless they were explicitly conducted as such.

Do not create a final version-level research retrospective unless I explicitly request it, normally after that version has been completed and frozen.

## Milestone Notification

When V0, V1, V2, or V3 is fully implemented and relevant tests pass, explicitly notify me in Chinese.

Use the fixed milestone marker first:

- `V0 milestone completed.`
- `V1 milestone completed.`
- `V2 milestone completed.`
- `V3 milestone completed.`

Then explain in Chinese:

- what that version contains,
- whether relevant tests passed,
- whether all previous versions remain independently runnable,
- important limitations,
- recommended next step.

Do not automatically begin the next version.

A milestone completion report does not mean the version is frozen; freezing requires my explicit approval.

## Architecture Principles

Prefer a modular monolith.

Keep:

- frontend concerns in React,
- API and application logic in FastAPI,
- LLM/RAG/orchestration/validation/repair in the backend,
- PostgreSQL + pgvector as the primary persistence layer.

Do not introduce microservices, queues, caches, or other infrastructure without a concrete project need.

Normalize data from external providers into internal schemas instead of passing provider-specific payloads throughout the application.

Do not call third-party APIs directly from LangGraph nodes when a service/client abstraction is more appropriate.

## Testing

Default:

- module change → run relevant tests,
- shared schema/core graph change → run broader tests,
- V0/V1/V2/V3 milestone → run the full relevant test suite.

Use mocked or fixture responses for third-party API tests where practical.

Do not repeatedly read or test unrelated parts of the repository without a reason.

## General Constraints

- Avoid unrelated refactors.
- Avoid unnecessary complexity.
- Do not implement future-stage mechanisms early.
- Do not automatically commit or push unless explicitly asked.
- Keep explanations concise unless I ask for more detail.
