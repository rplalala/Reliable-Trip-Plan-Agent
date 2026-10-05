# Version lifecycle

Read before changing a version boundary, announcing a milestone, freezing a version,
or progressing to the next version. These rules supplement [AGENTS.md](../../AGENTS.md)
and the current implemented state in [PROJECT.md](../../PROJECT.md).

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
6. Commit tracked freeze documentation under the Git Commit Policy. Force-adding ignored documentation and pushing still require explicit authorization.

Examples:

- V0 → `docs/records/v0-v3/v0-milestone.md`
- V1 → the numbered core architecture and `docs/records/v0-v3/v1-milestone.md`
- V2/V3 → corresponding version documentation

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
