# Historical preparation checkpoint

This document records preparation before Issue publication and tracker activation.
Its pending/unauthorized/remote-absence statements describe that checkpoint only.
Current outcome: [migration acceptance](migration-acceptance.md) and
[actual mapping](migration-manifest.json); RTPEval is published and activated on 2026-10-01.

---

# RTPEval publication readiness and proposed commit grouping

Date: 2026-10-01 (Australia/Sydney).
Status: Four documentation commit groups and branch push approved;
Issue publication and tracker activation remain unauthorized.
Source checkpoint: 473600254023f7d41648eed02215b6ab84e4ff03 on feature/evaluation.
The approved Issue content, labels, states and dependency graph remain unchanged.

## Tool check

Found gh.exe through the persistent Windows PATH at D:/Tools/GitHub CLI/gh.exe.
The current process PATH does not include it; use its absolute path for this session.
Actual output: gh version 2.102.0 (2026-09-30). Local issue/api/auth help was inspected.
Historical pre-login checks reported no logged-in hosts, no token environment
variables and absent default hosts.yml paths. After the user logged in, the sandbox
reported an invalid token; a direct GET showed a sandbox socket-permission error.
Outside the restricted sandbox, the same credential authenticated as rplalala and
read the repository successfully. No re-login, credential contents or token values
were recorded in project files.

Read-only repository/Issue/label/branch checks are complete. CLI argument validation
initially rejected --slurp with --jq; using --slurp with local JSON projection
preserved complete pagination and passed. No write endpoint was exercised.

## Observed remote state

Evidence: [preflight-record.json](preflight-record.json), collected 2026-10-01.

- Repository is public, not archived, and Issues are enabled. Observed account
  permissions include admin, maintain, push, pull and triage; writes were not tested.
- Complete all-state listing contains zero non-PR Issues, so no current Issue requires
  reuse. Recheck immediately before publication because the snapshot can change.
- Missing proposed labels: needs-triage, needs-info, ready-for-agent, ready-for-human
  and rtpeval. Existing wontfix is reused; the other existing labels stay in place.
- Remote feature/evaluation is absent. Six remote branches were enumerated completely.
- Local gh create/edit help exposes parent and blocked-by operations. Official
  [sub-issue](https://docs.github.com/en/rest/issues/sub-issues) and
  [dependency](https://docs.github.com/en/rest/issues/issue-dependencies) documentation
  describes the APIs. Actual relation creation/readback remains untested because no
  Issues exist and mutation is not authorized.
- At the published feature/v3 commit 364f91f, among 29 reviewed reference paths,
  3 have matching Git blob content, 9 differ and 17 are absent. The API tree was not
  truncated. This reference check identifies publication needs; it does not select
  the future documentation commit or make current draft URLs usable.

## Existing commits included by a first branch push

The following nine local commits are not reachable from any of the six observed
remote branch tips. Relative to published feature/v3, their net changes cover 75
files, with 7422 insertions and 118 deletions. These are previously committed
implementation/testing/documentation changes; the proposed four new groups below
have not been staged or committed. Full hashes are retained in the preflight record.

| Commit | Subject |
| --- | --- |
| 1d467ec | feat(evaluation): add source-linked batch intake and projection |
| b102445 | feat(evaluation): capture attempt usage and compare resources |
| 0e41478 | feat(evaluation): resolve identities with independent adjudication |
| 1eb441f | docs(evaluation): record contracts and offline acceptance checkpoint |
| 97d02ad | feat(evaluation): add bounded evidence snapshots and offline replay |
| 13cce80 | fix(planner): reserve tool-backed transport for application transfers |
| dc8b97b | fix(evaluation): select transport claims by planner version |
| 9ff8e9b | test: preserve bounded three-day transport smoke tooling |
| 4736002 | docs: close out snapshots and transport smoke validation |

## Read-only checks after login

1. Recheck auth status without displaying tokens. Verify repository identity,
   visibility, Issues availability, archive status and account permissions.
2. List existing Issues in all states and existing labels, with complete pagination.
   Compare the approved parent/child titles and RTPEval identifiers before deciding
   create versus reuse; title similarity alone does not establish equivalence.
3. Recheck the observed remote branch snapshot before a separately approved push.
   The complete existing outgoing commit set is recorded above; future approved
   commits extend that set. Local branches and remote-tracking refs were not updated.
4. Confirm supported parent/sub-issue and blocked-by API operations through current
   official documentation or read-only API schema checks. Do not probe with mutations.
5. Revalidate document/body/source/configuration hashes. Publish nothing while any
   documentation commit or Issue URL placeholder remains unresolved.

## Approved local commit groups

The user explicitly approved these four groups and the branch push on 2026-10-01.
Groups 1-3 are committed; group 4 saves preparation and authorization records.
The current changes are documentation only. Partial staging separated the two
independent additions in closeout-audit.md without changing its working-tree text.

### 1. Ticket 05 specification closure

Proposed message: docs: finalize RTPEval requirement and schedule contract

- New .scratch/rtpeval/requirement-schedule-contract.md.
- .scratch/rtpeval/activity-scope-contract.md, artifact-contract.md,
  identity-implementation-contract.md, metrics-contract.md,
  requirement-spec-contract.md, review.md, score-profile.md and spec.md.
- .scratch/rtpeval/issues/05-requirement-schedule-metrics.md and ticket-breakdown.md.
- Ticket 05 closure/cardinality additions in .scratch/rtpeval/closeout-audit.md.
- docs/evaluator_design.md and docs/evaluation_glossary.md.

Scope: accepted protected blockers, exact-one/single-visit default for reviewed
explicit named required visits, sourced multiple-visit time matching, typed fields,
uncertainty and future implementation seams. No scoring implementation is included.

### 2. Current project context and preserved history

Proposed message: docs: streamline project context and preserve historical records

- PROJECT.md, docs/README.md and docs/development_record.md.
- docs/shared_poi_semantics_plan.md.
- .scratch/semantic-reference-correction/live-acceptance-plan.md.
- Historical evaluation branch checkpoint section in
  .scratch/rtpeval/closeout-audit.md; exclude its Ticket 05 additions from this group.

Scope: concise current entry, existing responsibility owners and recovered historical
observations. PROJECT/index retain the latest Ticket 05 status from group 1. Earlier
validation counts remain dated records rather than checks performed for publication.

### 3. Existing Matt workflow instructions

Proposed message: docs: document Matt skill workflow

- Existing AGENTS.md Matt skills workflow addition only.

The proposed GitHub tracker patch is not applied here. Current local tracker pointers
remain authoritative until separate approved migration activation.

### 4. Approved migration preparation record

Proposed message: docs: prepare RTPEval GitHub issue migration

- .scratch/rtpeval-github-migration/ drafts, mapping, link audit, proposed configuration
  and local readiness records.

Issue bodies intentionally retain unresolved placeholders until verified publication
targets exist. This commit records preparation, not actual migrated Issues. Ignored
thesis_notes, runtime artifacts, logs and credentials are outside every group.

## Approved Git publication route

After the required local documentation checks, save the reviewed groups on the current
feature/evaluation branch. Revalidate the complete outgoing commit set and push to
origin/feature/evaluation within the approved scope. No force push, branch switch or
merge is authorized.
Use a verified published commit containing all reviewed reference files as
DOCUMENTATION_COMMIT. Check all 29 referenced paths against that published revision;
Git's Markdown line-ending normalization must not change their reviewed meaning.

Commit grouping and push scope were explicitly approved under AGENTS.md. Once the
document links and read-only repository preflight pass, obtain separate authorization
to publish/reuse the 13 Issues and then activate the reviewed tracker configuration.
The user superseded the original no-commit/no-push boundary for these four groups and
the recorded nine existing commits only. The no-Issue-publication boundary remains
active. Ticket 05 implementation remains a separate task.

## Current verification and remaining evidence

Source/body/reference/configuration hashes and the worktree baseline will be checked
before the next authorized operation. The earlier full migration static verification
is recorded in README.md and migration-manifest.json. Current preparation checks
passed: all 62 source/body/reference/configuration hashes, new local navigation,
English/whitespace checks, unchanged branch/HEAD/worktree baseline and empty index,
and git diff --check. No backend tests or live travel/model/database services ran.
Read-only duplicate/label/branch/reference checks and existing outgoing-commit
enumeration passed after login. Future publication-link validation and actual
relation/state/label readback remain pending authorized publication. The four commit
groups are approved, with execution checkpoints recorded below. Issue publication,
relations/state/label mutation and tracker activation remain pending.

## Documentation execution checkpoints

- 5fb4278: docs: finalize RTPEval requirement and schedule contract.
- 6766830: docs: streamline project context and preserve historical records.
- a6aff13: docs: document Matt skill workflow.
- Group 4 saves this migration package; its hash and push result are reported
  after execution rather than guessed inside its own commit.

Selected documentation commit: a6aff13a00af35467b9c88ec2906d10a96095f04.
All 29 reviewed reference paths are present in that local commit. Remote verification
follows the approved push; body placeholders remain unresolved until rendering.
Original source snapshot identifiers/hashes remain historical provenance. Later
preflight compares current hashes and published content, rather than requiring HEAD
to remain at the original 4736002 checkpoint.

## Migration patch format correction

The group 4 staged check found the original AGENTS patch had one missing blank
context line, so its hunk count was invalid. Regenerated a complete zero-context
diff preserving exactly the same two tracker-pointer replacements. Syntax/base
validation passed with git apply --check --unidiff-zero using binary input. No patch
was applied to active AGENTS. Activation requires separate approval, exact source
hash verification and the --unidiff-zero flag. This corrects the earlier draft
checker, which had not validated the hunk count. Strict whitespace checks now apply
to every migration file, including the patch. The old/new hashes are recorded.
