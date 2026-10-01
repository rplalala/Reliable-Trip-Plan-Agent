# RTPEval GitHub Issues migration acceptance

Date: 2026-10-01 (Australia/Sydney).
Final local review: 2026-10-02; activation-verification.json passed after wording review.
Status: Published; local tracker activated; remote and local verification passed.
Branch: feature/evaluation.
Revision: 8a82354c885300eb7c952403ce37da1ccf8e4191 plus uncommitted tracker/snapshot/navigation updates.
Published document checkpoint: a6aff13a00af35467b9c88ec2906d10a96095f04.

## Authorization and outcome

The human separately authorized the parent Issue, all 12 Tickets and the tracker switch.
The scope included missing labels, native parent/dependency relations, imported completion
records and closing Tickets 01-04 for their approved offline scopes. It did not authorize
Ticket 05 implementation or new commit/push, live travel/model/database work, formal
benchmarks, experiment analysis or a version freeze.

Parent: [RTPEval #12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12).
Project Ticket 01-12 map to actual GitHub Issues #13-#24; the
[manifest](migration-manifest.json) records stable project IDs separately from GitHub
numbers, database IDs, node IDs and actual URLs. Original source/body hashes remain
preserved. Existing non-RTPEval local trackers were not migrated.

Migration-time lifecycle:

- 01-04: closed with reason completed after an imported acceptance comment.
- 05/06/08/09: open with ready-for-agent.
- 07/10/11/12: open with needs-info.
- Parent: open. No assignees/claims added.
- Ticket 08 retains open predecessors 05/06/07. Completed predecessors remain native
  dependency links even where GitHub counts no open blockers.

These are observed migration-time states; GitHub owns subsequent task state/discussion.
Readiness, predecessor completion and Issue publication do not authorize implementation.

## Execution and verification sequence

1. Rechecked authenticated repository identity, public visibility, Issues availability,
   permissions, labels and complete paginated all-state listing: zero pre-existing
   non-PR Issues. The original preflight-record.json remains an earlier read-only snapshot.
2. Verified all 29 referenced files at the published document checkpoint through
   Contents API type, Git blob SHA and exact html_url before publication. This followed
   the earlier separately approved documentation commits and non-force branch push.
3. Created only five missing labels: needs-triage, needs-info, ready-for-agent,
   ready-for-human and rtpeval. Reused existing wontfix; other existing labels unchanged.
4. Published parent #12 then children #13-#24 in dependency order, journaling actual
   identities after each creation. Stable markers and paginated lookup support safe
   resumption. The parent bootstrap used explicitly pending child references; after
   all identities existed, replaced it with the final resolved body and updated all
   self/cross references. Original approved issue-drafts remain unchanged.
5. Imported completion comments for 01-04 with pinned dated acceptance links and
   offline-scope limits, then closed each with reason completed. No implementation
   tests were rerun or presented as new acceptance.
6. Authenticated readback passed for all 13 exact titles/bodies, state/reason, approved
   label sets and empty assignments. Verified 12 native parent-child relationships
   and all 13 native blocked-by edges, including closed predecessors; no fallback
   body-only relationships were needed. Checked 113 Markdown link occurrences in
   final Issue bodies: resolved GitHub URLs, no local relative targets, unresolved
   tokens or heading fragments. No duplicate imported Issues were found.
7. Rechecked original source/configuration hashes and the approved AGENTS patch
   before applying exactly two tracker-pointer replacements. Activated tracker/triage
   documents locally. Added dated snapshot headers to 12 local tickets, retaining
   every original source byte. The live breakdown now provides GitHub links and
   preserves the old breakdown/status history in an explicitly historical foldout.
8. Updated PROJECT.md, docs/README.md and migration navigation; preserved older
   preparation records as historical checkpoints. Domain-document ownership and
   non-RTPEval trackers remain unchanged. The active tracker retains legacy local
   operations for unmigrated features only.
9. Final local static checks passed: all 12 original ticket byte sequences, 13 unchanged
   approved drafts, 13 rendered body hashes, four preserved navigation records,
   two AGENTS pointer changes, 223 local Markdown link occurrences, English/whitespace
   checks and git diff --check. Git HEAD/branch and the empty index were unchanged.
   Domain ownership and other feature trackers were unchanged. Evidence is in
   activation-verification.json. Backend tests were not needed for metadata/docs-only
   changes; no runtime files were changed.

Remote readback evidence: [publication-verification.json](publication-verification.json).
Local evidence: [activation-verification.json](activation-verification.json).

## Earlier failures and corrections

The previous read-only preparation initially hit restricted sandbox sockets, producing
a misleading invalid-token status. The same keyring credential worked outside that
restriction; network operations used the approved escalation without recording tokens.
The collector also rejected --slurp combined with --jq; parsing paginated JSON locally
corrected it. These were preparation failures, not failed Issue writes.

The earlier Git preparation discovered an invalid AGENTS patch hunk count and Windows
stdin line-ending changes. It regenerated the same two replacements as an explicit-LF
zero-context patch. Saved-file syntax/base checks passed with --unidiff-zero; the
activation repeated that precheck successfully before applying it. Original hashes
and correction history are retained in the manifest and historical preparation records.

Issue publication, completion-comment readback and relationship verification passed.
No duplicate Issues or relation fallback was required.

The final local checker first failed to invoke because its orchestration string
contained Markdown backticks; corrected the quoting without executing file changes.
Its first executed link pass then encountered its own not-yet-written verification
JSON. Created that report with explicit pending status before the check, then replaced
it with passed results only after every check succeeded. The complete rerun passed;
these were checker sequencing errors, not lost source content or invalid Issue links.

## Preservation, ownership and remaining boundaries

GitHub owns migrated RTPEval and approved new-work task state, labels, dependencies,
assignments and discussion. Repository contracts/specifications/acceptance records
own detailed semantics; PROJECT.md remains current project scope/authorization authority.
Local ticket Status fields and imported dated comments are historical, not a second
live tracker. Original local authors/dates are imported history, not backdated GitHub posts.

Pinned Issue document links identify the reviewed pre-migration checkpoint. Current
tracker activation, mapping/acceptance and project-navigation changes are local,
uncommitted and unpushed. They must not be described as already accessible at the
pinned commit. Future contract changes must explicitly disclose local availability
until separately committed/pushed and record their accessible revision on the Issue.

Ticket 05 remains specification-ready with implementation pending separate approval.
Its explicit reviewed named required visits default to exactly one tripwide visit;
only sourced explicit repeat permission permits at-least-one time matching, with
explicit quotas still binding. Protected intervals are boundaries, not added non-overlap
score units. V0 uses model transport Activities; V1-V3 use application transfers.
The migration changes no scoring semantics or V0-V3 runtime behavior.

The preceding uncommitted/pending-Git statements describe the publication and
activation checkpoint before the separate closeout authorization below.

## Authorized Git closeout and redundant draft cleanup - 2026-10-02

The user separately authorized committing/pushing the migration configuration and
deleting issue-drafts while retaining actual Issue mappings and migration acceptance.
This repository revision carries the active configuration and publication records.

Verified all 13 original drafts against preparation commit
8a82354c885300eb7c952403ce37da1ccf8e4191 before deleting their worktree copies. README
draft links now point to that immutable Git revision. The version 2 manifest replaces
live body_file paths with explicit draft_history entries containing commit/path/URL,
Git blob identity and original checkout hashes. CRLF normalization is recorded;
the approved draft text remains accessible in Git history.

Actual Issue numbers/URLs, labels, state/dependency readback, source hashes, rendered
publication bodies and imported completion comments remain preserved. Original local
tickets and current contracts/acceptance documents remain in the repository. The
README historical foldout rebases draft links reversibly; original text hashes are
retained. Other feature trackers and domain ownership remain unchanged. The entire
.scratch directory stays tracked; no gitignore change or force-add is part of closeout.

Closeout checks are in cleanup-verification.json. Historical publication-verification
and activation-verification records remain dated evidence of their original checks;
they are not rewritten as results of the subsequent cleanup.

Next separate task: review/approve Ticket 05 #17 implementation scope. This Git
closeout does not authorize that implementation or live/formal research work.
