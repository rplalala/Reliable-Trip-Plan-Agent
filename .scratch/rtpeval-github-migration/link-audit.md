# Draft link audit

Date: 2026-10-01. Local HEAD: `473600254023f7d41648eed02215b6ab84e4ff03`.
Every repository-file URL is prospective and uses `{{DOCUMENTATION_COMMIT}}`.
Local existence/hash checks do not establish that HEAD or this branch exists on GitHub.
The initial draft inspected locally cached refs only. Subsequent authenticated,
fully paginated remote branch listing confirms feature/evaluation is absent at this
check. [Preflight record](preflight-record.json) retains the live snapshot.

At published feature/v3 commit 364f91f, the complete API tree has 3 identical reviewed
reference files, 9 differing files and 17 absent paths. Git blob comparisons account
for configured Markdown line-ending normalization. These results do not establish
access to the unselected future DOCUMENTATION_COMMIT; the table below describes that
prospective target, whose reviewed links still require approved publication.

| Referenced path | Local content state | GitHub access |
| --- | --- | --- |
| `.scratch/rtpeval/activity-scope-contract.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/artifact-contract.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/evidence-time-contract.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/identity-implementation-contract.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/intake-projection-contract.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/metrics-contract.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/opening-contract.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/requirement-schedule-contract.md` | untracked_local | not verified |
| `.scratch/rtpeval/requirement-spec-contract.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/route-contract.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/score-profile.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/snapshot-contract.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/spec.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/ticket-01-acceptance.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/ticket-02-acceptance.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/ticket-03-acceptance.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/ticket-04-acceptance.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/ticket-breakdown.md` | modified_since_HEAD | not verified |
| `.scratch/rtpeval/transport-correction-acceptance.md` | tracked_at_HEAD | not verified |
| `.scratch/rtpeval/usage-capture-contract.md` | tracked_at_HEAD | not verified |
| `PROJECT.md` | modified_since_HEAD | not verified |
| `backend/evaluation/README.md` | tracked_at_HEAD | not verified |
| `backend/evaluation/identity.py` | tracked_at_HEAD | not verified |
| `backend/evaluation/identity_cli.py` | tracked_at_HEAD | not verified |
| `backend/evaluation/snapshot.py` | tracked_at_HEAD | not verified |
| `backend/evaluation/snapshot_cli.py` | tracked_at_HEAD | not verified |
| `backend/tests/evaluation/test_identity.py` | tracked_at_HEAD | not verified |
| `backend/tests/evaluation/test_snapshot.py` | tracked_at_HEAD | not verified |
| `docs/evaluator_design.md` | modified_since_HEAD | not verified |

## Publication gates

- `modified_since_HEAD` and `untracked_local` require an approved publication version;
  linking HEAD would either show older meaning or a nonexistent file.
- `tracked_at_HEAD` means present in the local commit only; verify that the selected
  documentation commit is published and contains the reviewed version of every path.
- Replace document/Issue tokens only after verified actual targets are recorded.
  Refuse publication while tokens, local relative file links or unresolved paths remain.
- Validate referenced Markdown headings on the selected content. Keep issue dependencies
  as actual Issue links/native edges, not links to old ticket files.
- Ignored logs, provider payloads and research archives are not link targets to upload;
  keep existing descriptive provenance strings without publishing raw evidence.

The initial remote preflight performed no Git writes or Issue mutations. The later
approved document commits selected a6aff13a00af35467b9c88ec2906d10a96095f04 as the
documentation checkpoint. Final published ref/blob verification follows the approved
push; Issue publication is still unauthorized.
