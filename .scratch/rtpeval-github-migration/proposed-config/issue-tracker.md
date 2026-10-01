# Issue tracker: GitHub with legacy local records

Activation: apply only after approved publication and verified mapping of the RTPEval
parent and all 12 children. Before activation, the current local tracker is authoritative.
Target repository: `rplalala/Reliable-Trip-Plan-Agent`. Use the `gh` CLI with an explicit repository argument.

## Ownership

- GitHub Issues own migrated RTPEval task state, dependencies, assignments and discussion,
  and approved new work. Read the issue body and relevant comments before implementation.
- Repository `.scratch/<feature>/` contracts/specs and acceptance records remain their
  detailed owners. PROJECT.md owns current project scope, status and authorization.
- `.scratch/rtpeval/issues/` becomes a historical migration snapshot with actual Issue
  links and a mapping record; its old Status fields are not a second live tracker.
- Existing non-RTPEval local trackers retain their current authority until explicitly
  migrated. This RTPEval migration does not publish or close those tasks.
- Specification labels, open/closed state and dependency completion do not grant task,
  Git, live-run or research approval. Follow AGENTS.md's authorization boundaries.

## Operations

- Publish an approved task: `gh issue create --repo rplalala/Reliable-Trip-Plan-Agent --title "..." --body-file <file>`.
  Provide labels and parent/dependency links after validating local CLI support.
- Fetch a ticket: `gh issue view <number> --repo rplalala/Reliable-Trip-Plan-Agent --comments`; obtain state, labels,
  assignments and linked current contract versions. Resolve project Ticket numbers
  through the retained mapping; do not assume Ticket 05 means GitHub #5.
- Update discussion with a reviewed English comment file using `--body-file`; update
  labels/state only within approved work. Imported dates/authors are quoted history.
- Resolve: record implementation/acceptance evidence, then close with reason completed.
  Unimplemented tickets remain open even when their specifications are ready.
- PRs as a request surface: no. Issue migration does not expand triage scope to PRs.

## Dependency and claim rules

Retain the approved predecessor graph using native blocked-by relationships. Preserve
references to completed blockers even when GitHub's open-blocker count becomes zero.
Use a body `Blocked by` reference only as a documented fallback if native relationships
are unavailable. Issue numbers and API database IDs are separate identifiers.
A ready ticket is actionable only when its blockers are completed and the human has
approved that scope. Claim via an assignment/current-scope comment after approval;
state and assignment never imply blanket authorization for another ticket.

## Documentation updates

Update the authoritative contract/acceptance record in the repository; record the
substantive change and accessible document revision on its Issue. Git commit/push
requires explicit approval, so local documentation is not automatically published.
During an unpublished revision, mark its availability explicitly instead of presenting
an old GitHub link as the new approved meaning. Final reports remain self-contained.

## Migration records

The migration directory retains preparation hashes and actual publication mappings.
After successful activation, keep source tickets as dated snapshots with GitHub links;
replace dynamic status copies in the old breakdown with pointers to Issue state.
Resumption first checks the live mapping and existing Issues to avoid duplicate creation.
