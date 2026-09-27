# Iteration 2 handoff — 2026-09-27

Archived during authorized workspace cleanup on 2026-09-28. This is the original
transfer checkpoint, not current execution authorization or a current HEAD/status
report. PROJECT.md and later dated records describe subsequent work. The user has
separately authorized committing the remaining workspace records; that does not
resume the deferred investigation described below.

## Ownership and immediate action

The user moved future iteration work from `Iteration 1` (01a0d8d3-b759-7920-957b-a0b144352afe)
to `Iteration 2` (01a0e29d-405e-7d82-b894-d95eb7f67632). Both use
D:/Workspace/Capstone/Reliable-Trip-Plan-Agent. Receive this handoff and await the next user task.
Do not restart the paused food/sparse-day investigation or propose it as a remaining acceptance
blocker. The user explicitly ended acceptance and deferred that investigation. No new live,
implementation, commit, push, branch switch or freeze is authorized by the transfer.

## Project stage

The project has independently runnable V0 (plain LLM), V1 (tools), V2 (RAG), and V3
(validation, bounded targeted Repair, revalidation), with React Product/Dev and FastAPI.
It has moved beyond implementing the four mechanisms into engineering stabilization,
shared contract/UX corrections and bounded development acceptance. V3's engineering closeout
is recorded; later shared updates have their own dated checkpoints. This is not a declaration
of globally verified travel quality, benchmark freeze or completed formal research evaluation.
Read PROJECT.md as current authority and docs/README.md as navigation. Do not read the entire
historical archive or infer current configuration from old checkpoints.

## Progress in the outgoing conversation

- Configured local skill workflow: specs/issues under .scratch; PROJECT is the source of truth,
  not CLAUDE.md/CONTEXT.md. English repository content and Chinese user communication.
- Corrected shared semantic requirements: soft rich-trip preference, named revisit intent,
  evidence references, role/multiplicity checks and completion propagation to the frontend.
- Reused the full eligible comparison pool in quantity Repair under local operation permissions;
  this is general policy, not London/date-specific logic. Enabled quantity review by default
  and removed the obsolete repetition-review path; identity/multiplicity safeguards remain.
- Completed bounded A/B/C/D semantic-development checks and documented limitations. The London
  D quantity pilot achieved counts 3/3/2/2/2/2/2/2. Parent zoo/exhibit concerns were explicitly
  dropped by the user. P3 pending-reason heuristic remains deferred.
- Updated Product/Dev input UX: free GeoDB through backend HTTPS, destination suggestions,
  selectable currency, locale-independent dates, compact weather and preference Polish.
  Polish now uses one bounded model call with per-operation HTTP-client ownership; the user
  explicitly removed the second fidelity review. Suggestions require Apply/Dismiss and normal
  Gate still runs. No claim of guaranteed Gate success or automatic meaning preservation.
- Subsequent Sydney/Melbourne smoke exposed terminal semantic contract errors. Added one
  correction per batch shared across citation/identity/exception errors, within existing
  6-call/120-second request and 45-second per-call limits. Prompt 5 + wire projection 1 assigns
  pNN/eNN short references; application owns exact canonical mapping, coverage and same-candidate
  source checks before downstream acceptance. No silent invalid-output salvage.
- Three authorized sequential prompt-5 live cases completed: Sydney V1 (5 days), Sydney V3
  (5 days), Melbourne V1 (8 days). All four semantic batches passed first attempt. Mapping,
  source ownership and canonical restoration verified. Correction efficacy NOT exercised.
- Reconstructed V3 recorded budgets from 212 events and ledgers: 45 checks passed. Truncated
  run.json and missing billed usage do not permit a full cost/invoice claim.
- Implemented independent bounded budget.json on trace finalization: 64 KiB / 32 per-stage
  call records, deduplicated counters, explicit missing usage, atomic write and failure isolation.
  No planning or API-budget changes. Offline-tested, no new live run for this artifact.

## Validation and Git

Branch feature/v3, HEAD 8f5e9b3. Five local commits, not pushed:
23c3a46 docs: clarify iteration approvals and smoke coordination
0b20d58 test: support independent V1 and V3 semantic acceptance
fc01a9d fix: bound semantic correction with application-owned references
dcb71e8 feat: preserve compact budget summaries outside trace truncation
8f5e9b3 docs: record semantic validation and budget audit outcomes

Final combined backend suite: 1727 passed / 9 skipped; scoped Ruff and diff checks passed.
Prior budget-summary suite: 1726 / 9, then review found missing RAG counters; red regression,
fix and 63 focused passes preceded final full suite. No need rerun tests merely for handoff.

Uncommitted at handoff: PROJECT.md, docs/README.md, docs/development_record.md,
docs/known_issues.md; .scratch/food-sparse-diagnosis/ and this handoff directory.
There is also an ignored historical note:
thesis_notes/V3/events/20260927_food_sparse_offline_diagnosis.md.
The latest modifications are documentation/local diagnosis only. Do not force-add ignored
logs, raw captures, secrets or archives. Prior direct-commit authorization was used for the
five commits; it is not standing authorization for new tasks.

## Paused observations, not unfinished mandatory fixes

Offline diagnosis reproduced four sparse V1 dates: Sydney Oct 2; Melbourne Sep 30, Oct 2/3.
Both selected 16 candidates and left 7/3 unused, so raw supply count is not the immediate
bottleneck; per-date feasibility and model causal rationale are unproven. Food preferences
survived interpretation. Supported food candidates (10/11/12 across the cases) were all
non_main, correctly excluded from named primary supply under current policy. Generic meals
remain optional. Continuing preferences are not mandatory counts; complete policy status does
not assert every preference or default 2-5 guidance is met. No new hard Spec violation proven.
Typed saved-output diagnostic replay, a one-date count probe and 12 existing tests passed;
the explicit no-sparse assertion is deliberately red on the quality observation, not a failing
mandatory production contract test. No production fix was made. Possible non-main food support
is a separate capability proposal and is shelved by the user's latest instruction.

Remaining claim limits: 38 activities in the three live outputs had unknown cost; V3 retained
route/opening/suitability/budget/semantic UNKNOWN and partial RAG discovery. These are not all
new approved tasks. No formal benchmark result or version freeze follows from smoke acceptance.

## Smoke coordination

Execution chat: exact title `smoke tests`, ID 01a0d6a6-6c2a-7401-9531-c260c63b6e9d, host local.
Iteration 2 now owns planning, budgets, criteria, harness/tool adaptation, production code,
offline tests, diagnosis, review and acceptance assessment. Smoke owns ONLY execution of
prepared authorized cases and reporting. It must not invent solutions or modify production code.
User authorization covers coordination messages for this workflow. AGENTS.md still names the
outgoing iteration ID; the user's explicit transfer supersedes that destination. Preserve all
other rules; update the static reference when maintaining agent rules under the relevant skill.

Every dispatch must specify exact input/cases, revision/config, sequence, attempt and budget
limits, allowed network permissions, stop/retry conditions, capture paths, acceptance criteria,
and report destination Iteration 2. Network retry permission is plan-specific: the user allowed
network-failure retries in a previous batch, while other batches expressly prohibited retries.
Do not treat either as universal. Where permission escalation remains blocked, smoke should
ask the user directly in its chat, rather than relay permission requests between chats.

Smoke reports process, outputs, stops/retries, defects needing verification, Spec deviations,
and evidence/document paths; distinguish observed facts, inferences and missing evidence.
Iteration 2 assesses and designs fixes. No new live execution is authorized by this handoff.

## Targeted reading

1. PROJECT.md, AGENTS.md, docs/README.md.
2. docs/development_record.md, section Semantic wire and budget acceptance closeout (2026-09-27).
3. Current relevant design only: docs/shared_poi_semantics_plan.md; docs/v3_design.md;
   docs/v3_milestone.md; config/runtime.yaml and config/README.md when needed.
4. Local specs: .scratch/semantic-reference-correction/{short-reference-spec.md,budget-summary-spec.md,v3-budget-audit.md}.
5. Latest smoke: logs/semantic_short_reference_revalidation_20260927/report.md and manifest.json.
   Earlier failures: logs/live_smoke_20260926/report.md and
   logs/semantic_contract_revalidation_20260927/report.md. Do not overwrite historical outcomes.
6. Paused diagnosis only if the user resumes it: .scratch/food-sparse-diagnosis/diagnosis.md.

Do not confuse prior Codex display issues with travel-backend failures: the outgoing chat's
missing visible answers were present in persisted final messages, including the commit result.
