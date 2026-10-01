# RTPEval GitHub Issues migration

Published and tracker activated 2026-10-01 (Australia/Sydney) under separate explicit
authorization. [Parent Issue #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12) and all 12 child Issues
are live. GitHub owns task state/discussion; repository contracts and acceptance records
own detailed meaning. Source tickets are preserved historical snapshots.

## Verified publication and records

- [Migration acceptance](migration-acceptance.md): scope, sequence, results and limitations.
- [Actual mapping and execution journal](migration-manifest.json): IDs, URLs and original hashes.
- [Authenticated publication readback](publication-verification.json): 13 bodies/states/labels,
  12 native parent-child relationships and 13 native dependency edges, including completed predecessors.
- [Local activation verification](activation-verification.json): configuration, source preservation,
  navigation and Git invariants.
- Original approved [body drafts](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/00-rtpeval-parent.md) are retained in Git at preparation commit 8a82354;
  working-tree issue-drafts were removed during the authorized 2026-10-02 closeout.
  Actual rendered bodies and completion comments remain permanent publication evidence
  in published-bodies/.
- Pinned document checkpoint: a6aff13a00af35467b9c88ec2906d10a96095f04; all 29 reference
  files were verified through the GitHub Contents API before publication.
- [Active tracker](../../docs/agents/issue-tracker.md) and
  [labels](../../docs/agents/triage-labels.md) are applied. This repository revision contains the activation/configuration
  and post-publication records; the 2026-10-02 closeout separately authorizes commit/push.

| Project Ticket | GitHub Issue | Original predecessors |
| --- | --- | --- |
| 01 | [#13](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/13) | None |
| 02 | [#14](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/14) | None |
| 03 | [#15](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/15) | 01 |
| 04 | [#16](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/16) | 03 |
| 05 | [#17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17) | 01, 03 |
| 06 | [#18](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/18) | 04 |
| 07 | [#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19) | 04 |
| 08 | [#20](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/20) | 05, 06, 07 |
| 09 | [#21](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21) | 01 |
| 10 | [#22](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/22) | 08 |
| 11 | [#23](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/23) | 10 |
| 12 | [#24](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/24) | 01 |

Migration outcome: Tickets 01-04 were closed/completed using imported offline acceptance;
05/06/08/09 retained ready-for-agent and 07/10/11/12 retained needs-info. These are
migration-time observations; consult GitHub for later changes. Ticket 05 implementation
remains pending separate approval. No live travel/model/database run, benchmark, commit,
push, PR or version freeze occurred in the publication/activation task.

## Git closeout and preserved preparation history

The original preparation record below describes earlier checkpoints. Its pending
publication/configuration statements were superseded by this activation and acceptance.

Original draft links below now point to the preparation commit. The manifest retains
original draft hashes, Git blob identities and historical URLs, with actual Issue
mappings and acceptance evidence unchanged. The earlier pending/uncommitted statements
remain dated history. See cleanup-verification.json for closeout checks.

<details>
<summary>Pre-migration record (historical; not current task state)</summary>

# RTPEval GitHub Issues migration draft

Prepared 2026-10-01 (Australia/Sydney). Status: Draft and four documentation commits/
branch push approved; Issue publication/tracker activation remain unauthorized.
Target: `rplalala/Reliable-Trip-Plan-Agent`.
Original source checkpoint: `473600254023f7d41648eed02215b6ab84e4ff03` plus then-uncommitted documents; branch: `feature/evaluation`.
Current local tracker and source files remain active. No Issue/configuration was applied.

The user approved the draft content and migration plan, then separately approved
the four documentation commit groups and a push of feature/evaluation containing the
nine recorded existing commits. Issue publication and tracker activation remain
separately gated. Original snapshot hashes are retained; reviewed Issue bodies and
proposed tracker configuration are unchanged. No credentials are stored here.

All 29 reference files are included in selected documentation checkpoint
a6aff13a00af35467b9c88ec2906d10a96095f04. This preparation commit records the approved
push plan; actual push/ref/blob verification is reported after execution. Document/Issue
tokens remain templates for the later authorized Issue-publication step.

## Review entry points

- [Parent Issue body](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/00-rtpeval-parent.md): plan, scope and 12 child links.
- [Mapping/metadata](migration-manifest.json): original/draft hashes, states, labels,
  dependencies and null future GitHub identifiers. Null does not mean publication.
- [Document link audit](link-audit.md): local availability and remote publication gates.
- Proposed configuration: [tracker](proposed-config/issue-tracker.md),
  [labels](proposed-config/triage-labels.md), [AGENTS patch](proposed-config/AGENTS.patch).
- [Publication readiness and commit grouping](publication-plan.md): current tool check,
  proposed documentation commits and the remaining publication gates.
- [Read-only GitHub preflight record](preflight-record.json): observed repository state,
  remote branches, outgoing commits and reference availability at published V3.
  Domain-document ownership stays in the existing docs/agents/domain.md; no new glossary
  or ADR layout is part of this tracker migration.

| Local ticket | Body draft | Specification status | GitHub state | Predecessors | Actual Issue |
| --- | --- | --- | --- | --- | --- |
| 01 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/01-batch-intake-projection.md) | resolved | closed | None | Pending |
| 02 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/02-usage-capture-report.md) | resolved | closed | None | Pending |
| 03 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/03-identity-adjudication.md) | resolved | closed | 01 | Pending |
| 04 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/04-evidence-snapshot.md) | resolved | closed | 03 | Pending |
| 05 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/05-requirement-schedule-metrics.md) | ready-for-agent | open | 01, 03 | Pending |
| 06 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/06-opening-checks.md) | ready-for-agent | open | 04 | Pending |
| 07 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/07-route-checks.md) | needs-info | open | 04 | Pending |
| 08 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/08-quality-report-scores.md) | ready-for-agent | open | 05, 06, 07 | Pending |
| 09 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/09-blinded-ranking.md) | ready-for-agent | open | 01 | Pending |
| 10 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/10-v3-pre-post.md) | needs-info | open | 08 | Pending |
| 11 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/11-controlled-repair.md) | needs-info | open | 10 | Pending |
| 12 | [draft](https://github.com/rplalala/Reliable-Trip-Plan-Agent/blob/8a82354c885300eb7c952403ce37da1ccf8e4191/.scratch/rtpeval-github-migration/issue-drafts/12-mechanism-official-audit.md) | needs-info | open | 01 | Pending |

Four completed tickets become closed/completed after evidence is recorded. Four ready
specifications (05/06/08/09) and four needs-info specifications (07/10/11/12) stay open.
Ticket 08 retains its three unfinished blockers. The parent stays open. All later
implementation/live/research scopes need explicit approval; an Issue label is not approval.

## Draft construction and preservation

Each child includes current summary/acceptance criteria and the full local ticket in a
clearly marked historical foldout. Source text changes only its Markdown link destinations;
source-byte SHA-256 and reversible link substitutions are recorded. Original comments and
work dates are retained as imported history, without pretending they were posted on those
dates by the original authors. Current summaries supersede dated pending-status prose.
The newly corrected Ticket 05 single-visit/default-exact-one rule is included.

Detailed contracts and acceptance records remain repository documents. This is a migration
snapshot rather than another live tracker; source changes require regenerating/reviewing
affected drafts before publication. Existing worktree changes and source tickets are preserved.

## Tool/environment readiness

After the user configured the CLI, a 2026-10-01 check found
`D:/Tools/GitHub CLI/gh.exe` through the persistent Windows PATH: version 2.102.0.
The current process PATH remains stale; the full path works. After the user's login,
authentication succeeded as rplalala outside the network-restricted sandbox. The
sandbox's invalid-token report was superseded by the successful read-only check;
no re-login was necessary. No token was recorded in project files.

Read-only GitHub checks found a public, unarchived repository with Issues enabled
and admin/push/triage permissions. Complete listing found zero non-PR Issues and
five missing proposed labels; existing wontfix will be reused. Remote
feature/evaluation does not exist at this check. Nine existing local commits are
not reachable from the six observed remote branch tips; a first push of the current
branch would publish these alongside the proposed documentation commits.

The published feature/v3 tree contains identical reviewed content for only 3 of the
29 reference paths; 9 differ and 17 are absent. This is a published-base comparison,
not selection of DOCUMENTATION_COMMIT. Issue publication and tracker activation
remain pending separate approval and accessible reviewed document links.

## Execution and remaining approval gates

1. Revalidate exact source/config hashes and current states; inspect live repository,
   matching Issues/labels, visibility and permissions. Resolve tool/login readiness.
   Completion: migration inputs are current and duplicate/reuse decisions recorded.
2. Execute the separately approved four documentation commits and branch push,
   including the nine recorded existing commits. Verify every referenced file at the
   selected documentation commit. Issue publication and tracker activation remain pending.
   Completion: actual DOCUMENTATION_COMMIT and accessible reviewed links are recorded.
3. After explicit Issue publication approval, create or reuse the parent and children in
   recorded dependency order, preserving project Ticket numbers in titles. Record each actual
   number/database ID/URL immediately; resume by verifying mappings rather than creating duplicates.
   Completion: 13 real Issue identities and resolved document/Issue links are verified.
4. Set parent/sub-issue and native blocked-by relations, intended labels and state. Close 01-04
   with an imported completion/evidence summary and reason completed; keep pending work open.
   Completion: each state/label/edge matches this approved map, including closed predecessors.
5. Apply the reviewed configuration only after publication verification; add real Issue links
   and historical-snapshot markers to source tickets; make the breakdown point to live states.
   Completion: one authoritative task tracker, preserved local evidence and verified mapping.
6. Record migration acceptance and update PROJECT/docs navigation. Resume Ticket 05 only when
   its implementation scope is separately approved. No migration outcome freezes a version.

## Constraints

This batch covers RTPEval only; other local feature trackers are not migrated. The future
configuration proposes GitHub for migrated RTPEval/new work while retaining unmigrated
legacy records. AGENTS approval, language, Git and live-run boundaries still apply.
No publication command is executed by opening these documents. Unresolved tokens deliberately
make the raw drafts unsuitable for direct `gh issue create --body-file` publication.

## Validation record

Local static verification passed: 13 Issue bodies, 12 preserved source tickets, 13
dependency edges, 29 referenced repository paths and 119 Markdown link occurrences.
The drafts contain no heading-fragment links; published target access still needs live
verification. Source/body hashes, visible acceptance criteria, label/state mappings,
publication order, placeholders, active configuration hashes and existing worktree
status were checked. The proposed AGENTS patch matches the current working tree and
changes only its two tracker pointers. git diff --check passed with existing CRLF/LF
normalization warnings; new Markdown/JSON drafts also passed whitespace checks.

Review narrowed the Ticket 05 summaries to explicit reviewed named required visits,
preserving the exclusion of planner choices and soft interests. Verification first
hit the shell's default text encoding and two checker assumptions (an incorrect
hand-count of dependency edges and required blank context lines in a unified diff).
The checker was corrected to use UTF-8, the 13 recorded edges and patch-aware checks;
the complete check then passed. Original source tickets and active configuration
were unchanged. Backend tests/live services and real GitHub publication were not run.

## Approved Git execution checkpoint

Pre-commit checks passed for 62 preserved hashes, 78 local link occurrences,
2 heading fragments, 51 prospective file links and diff whitespace. Partial staging
first failed before index changes because Windows text input changed patch line
endings; binary patch input passed and preserved the worktree. Each of the first
three commits passed staged scope/content and whitespace checks. Backend tests
were not rerun for this documentation-only change. Manifest source branch/HEAD/status
fields describe the original snapshot, not a permanent execution gate.

## Migration patch format correction

The group 4 staged check found the original AGENTS patch had one missing blank
context line, so its hunk count was invalid. Regenerated a complete zero-context
diff preserving exactly the same two tracker-pointer replacements. Syntax/base
validation passed with git apply --check --unidiff-zero using binary input. No patch
was applied to active AGENTS. Activation requires separate approval, exact source
hash verification and the --unidiff-zero flag. This corrects the earlier draft
checker, which had not validated the hunk count. Strict whitespace checks now apply
to every migration file, including the patch. The old/new hashes are recorded.

</details>
