# Codex development rules

## Scope and authority

- `PROJECT.md` is the current source of truth; `docs/README.md` locates current
  contracts and records. Read relevant current files; use historical/reference
  material only when the task requires it or the user requests it.
- Work covers system design, architecture, implementation/testing and independently
  runnable V0-V3. Small implementation pilots are allowed. Formal benchmark design,
  formal version comparisons/experiment analysis/thesis writing, final research conclusions
  and final version-level research retrospectives require explicit authorization.
- All repository content (including code, configuration, comments, docs and Git
  messages) is English. Chinese in project files requires explicit approval for the
  specific user-facing feature. Communicate with the user in Chinese; keep
  technical identifiers and code in English. Keep explanations concise unless asked.

## Task boundaries

- Before major changes, explain scope, files, approach, checks and V0-V3 impact in
  Chinese; obtain explicit scope approval. Existing approval remains valid. Complete
  implementation, tests, local commits, review, corrections and related docs within
  that scope without repeated approval. Scope expansion or a separate task needs approval.
- Local commits are authorized within approved work unless deferred/prohibited.
  Push, PR creation, merge and branch switching require explicit authorization.
  Preserve unrelated work; honor task-specific exclusions and live budgets.
- Consolidate related documentation updates into one coherent commit per task or
  completed stage. Fold minor additions and wording corrections into that group
  instead of making consecutive small docs-only commits. Separate commits remain
  appropriate for distinct scopes, required review corrections or explicit user requests.
- Keep V0-V3 independently runnable with their intended behavior. A milestone/test
  pass is not a freeze. Freeze and next-version progression require explicit approval.

## Architecture

Use a modular monolith: React frontend; FastAPI API/application logic; backend
LLM/RAG/orchestration/validation/repair; PostgreSQL + pgvector persistence. Introduce
microservices, queues, caches or other infrastructure only for a concrete need.
Normalize provider payloads into internal schemas; use service/client abstractions
rather than direct third-party calls from LangGraph nodes where appropriate. Avoid
unrelated refactors, unnecessary complexity and premature future-stage mechanisms.

## Required policies on demand

These linked rules are binding. Read the applicable sections before the listed
operation; do not preload every policy or historical record.

| When | Read |
| --- | --- |
| Meaningful development, scope, testing or completion reports | [Collaboration](docs/agents/workflow.md#collaboration-workflow), [testing](docs/agents/workflow.md#testing); use [budget tradeoffs](docs/agents/workflow.md#budget-and-limit-tradeoffs) when diagnosing limits |
| Staging, committing, reviewing or Git delivery | [Git policy](docs/agents/workflow.md#git-commit-policy): fixed base, TDD, implementation/test commits before Standards/Spec review, separate correction commits |
| Engineering flow: skill selection, planning or implementation | [Matt workflow](docs/agents/workflow.md#matt-skills-workflow); [GitHub tracker](docs/agents/issue-tracker.md) and [triage labels](docs/agents/triage-labels.md) before tracker operations |
| Version boundaries, milestone, freeze or next-version progression | [Version lifecycle](docs/agents/versions.md) |
| Live smoke planning or execution | [Smoke policy](docs/agents/smoke-tests.md): current-session execution child, `gpt-6.1-sol`, `medium`; prepared/approved scope only |
| Documentation, evidence or archive maintenance | [Document ownership/admission](docs/agents/domain.md), including [archive rules](docs/agents/domain.md#thesis-research-archive); proactively preserve meaningful events within approved work |

GitHub Issues own specs, tickets and live task state; current contracts belong in
tracked `docs/`, dated evidence in `docs/records/`. `.scratch/`, raw runtime artifacts
and thesis notes are local aids, not competing project authorities or published
requirements. Final documentation reports must be self-contained in Chinese.
