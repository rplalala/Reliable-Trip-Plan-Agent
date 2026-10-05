# Development workflow

These are binding task rules referenced by [AGENTS.md](../../AGENTS.md).
Read the sections relevant to the current operation, rather than loading every policy.
Paths in command examples and backticks are relative to the repository root.

## Collaboration Workflow

For every meaningful development task:

1. Inspect only the relevant current files.
2. Before making major changes, briefly tell me in Chinese:
   - what you plan to do,
   - important files you expect to create or modify,
   - the implementation approach,
   - tests/checks you plan to run,
   - whether the change could affect any existing V0/V1/V2/V3 behavior.
3. Obtain my explicit approval for the proposed scope before major changes. An existing explicit approval for that scope remains valid; do not request it again.
4. Within the approved task, proceed through implementation, relevant tests, local commits, code review, necessary corrections, and related documentation updates without separate approval for each step. Follow the Git Commit Policy for commit/review order. Honor any explicit exclusions or limits, including live-run budgets and no-live instructions.
5. Run relevant tests/checks.
6. When finished, report in Chinese:
   - what was implemented,
   - important files changed,
   - test/check results,
   - important limitations or unresolved issues,
   - recommended next step.
7. Request approval before expanding the agreed scope or starting a separate task. Moving between implementation, testing, review, corrections, and documentation within the approved scope is not a new task.

The separate approval requirements for publication and other restricted Git actions, version freezes and progression, and formal research work below still apply. Local commits follow the Git Commit Policy.

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

Within an approved task, create local commits without requesting separate approval for
each commit or its grouping, unless I explicitly require approval, defer commits or
prohibit them. Implementation scope still requires approval; permission to commit does
not authorize another ticket, a broader change or a live run.

Before committing:

1. Inspect the relevant diff.
2. Briefly explain the logical commit grouping in Chinese; this is informational unless I require approval.
3. Run relevant tests/checks. Commit only after they pass; resolve failures within the approved scope or report a blocker.
4. Stage only the current task's intended files/hunks, preserving unrelated pre-existing work.

### Implementation, review and correction sequence

For implementation tasks, follow Matt's `implement` flow with `tdd` and `code-review`,
using this repository's commit order:

1. Record the starting commit before implementation as the review fixed point, unless I specify another base.
2. Implement with TDD at the agreed seams and complete relevant validation.
3. Commit the implementation and its directly related tests in logical groups **before code review**.
4. Run `code-review` against the recorded fixed point through the committed implementation, on both Standards and Spec axes. Include the task's commit list so the full change is reviewed.
5. If review finds issues, fix them within the approved scope, run relevant checks, and create additional commits such as `fix: correct route boundary handling`. Use `test:` or `docs:` when the correction only changes tests or documentation. Recheck the affected findings; repeat correction and commit as needed.
6. Commit necessary final documentation/acceptance updates in a coherent group and report the implementation and correction history.

This order overrides a skill's default commit-after-review order. Preserve the original
implementation commits and separate review-fix commits; do not amend, squash or rewrite
them merely to absorb review corrections. Routine in-scope corrections and their commits
need no additional approval. Scope expansion and task-specific exclusions still apply.

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

## Testing

- module change → run relevant tests,
- shared schema/core graph change → run broader tests,
- V0/V1/V2/V3 milestone → run the full relevant test suite.

Use mocked or fixture responses for third-party API tests where practical.

Do not repeatedly read or test unrelated parts of the repository without a reason.

## Budget and limit tradeoffs

Treat current budgets and limits as tunable engineering choices. When diagnosing a bottleneck, compare a measured increase in the relevant limit with adding mechanisms under the existing limit. Propose a budget adjustment when evidence suggests it is more effective or simpler to maintain. Explain the observed bottleneck, proposed values, expected benefit, cost and latency impact, risks, and bounded validation and rollback criteria. Distinguish resource limits from correctness requirements; increasing a budget does not relax evidence or acceptance checks. Existing task-specific budget restrictions remain in force until the user approves a change.

## General Constraints

- Avoid unrelated refactors.
- Avoid unnecessary complexity.
- Do not implement future-stage mechanisms early.
- Follow the Git Commit Policy for local commits and explicitly authorized publication.
- Keep explanations concise unless I ask for more detail.

## Agent skills

### Matt skills workflow

- Invoke `$ask-matt` with the task, constraints, and expected result when unsure
  which skill fits, or invoke a specific skill such as `$diagnosing-bugs`.
  Read its `SKILL.md` before use. Matt's `/skill-name` notation refers to the
  corresponding skill; use the invocation supported by the current client.
- Clarify repository ideas with `grill-with-docs`. For a small, clear task, use
  `implement`; for a multi-session build, use `to-spec` -> `to-tickets` ->
  `implement` per ticket, resolving blockers first. `implement` uses `tdd` and
  `code-review` against both project standards and the spec; commit/review/correction
  order follows the Git Commit Policy in this document.
- Use `prototype` when a design question needs runnable evidence, and `handoff`
  when moving findings between directories or sessions.
- Route raw incoming requests through `triage`; tickets from `to-tickets` are
  already prepared. Use `diagnosing-bugs` for hard bugs: reproduce the failure,
  then fix it with a regression test.
- Use `wayfinder` for large efforts with unresolved direction, then return to
  `to-spec` -> `to-tickets` -> `implement` once decisions are clear.
- Use `improve-codebase-architecture` to find improvement candidates,
  `codebase-design` for module interfaces and test seams, `domain-modeling` for
  terminology and ADRs, and `writing-for-agents` for agent-facing documents.
- Keep clarification, spec, and ticket creation in one context when practical;
  start each self-contained implementation ticket with fresh context. Continue,
  clear, hand off, or compact at phase boundaries as needed. Delegate only when
  applicable instructions explicitly authorize it.
- Verify skill availability and the tracker, triage, and documentation
  conventions below before an engineering flow. If setup is missing, use
  `setup-matt-pocock-skills` within an approved scope. Report unavailable skills
  and use an available equivalent, or ask before installing them.
- These workflows follow [AGENTS.md](../../AGENTS.md) and its linked approval,
  Git, live-run, research and version policies. `PROJECT.md` remains the current source of truth; skill-generated
  context, ADRs, and specs must stay aligned with it.

### Issue tracker

Use GitHub Issues for specifications, parent/child tickets, task state and discussion. Keep durable detailed contracts and acceptance records in tracked core `docs/` contracts and dated `docs/records/` documents. `.scratch/` is optional ignored drafting space, never the formal specification or issue-tracker location. See `docs/agents/issue-tracker.md` for skill operations and published-link rules.

### Triage labels

Use the existing default five triage roles as GitHub labels. Local `Status:` fields are historical snapshots, not live task state. See `docs/agents/triage-labels.md`.

### Project documentation

Use `PROJECT.md` for current project state and `docs/README.md` to find tracked design and acceptance documents. GitHub specs link to published documentation revisions; published files must not depend on ignored/local-only files. Preserve the single-context project layout and current source-of-truth hierarchy. See `docs/agents/domain.md`.
