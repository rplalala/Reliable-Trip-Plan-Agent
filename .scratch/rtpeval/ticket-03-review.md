# Ticket 03 follow-up implementation review

Date: 2026-09-30.
Base revision: `364f91f05f01328266bfb00c5b75885242d93d7d`.
Scope: uncommitted Ticket 03 implementation, tests and accepted identity contracts. Existing Ticket 01/02 changes were preserved. This was a review, not a correction pass.

## Findings

### Standards axis

No explicit repository coding-standard violation was found. One correctness issue was identified on this axis:

- **P1: Generic address components bypass branch checks** (`backend/evaluation/identity.py:298-302`). A supplied ID with `location="Country"`, destination `Example City`, and details address `10 Main St, Example City, Country` qualifies as a specific location. With no independent search, this bypasses competition checking. An accepted synthetic eight-reference batch produced seven `resolved` results and one sampled `audit_pending` result. A country/admin component does not establish a specific branch. Restrict this shortcut to sufficiently specific location evidence; otherwise require search or adjudication.

### Spec axis

- **P1: Search/details contradictions are ignored** (`identity.py:314-318`). Details can match the claimed name/city while search returns the same ID with a different name and city. The code compares candidate IDs/counts but ignores those material contradictory fields. An accepted synthetic batch produced seven automatic resolutions and one audit-pending result. The implementation contract explicitly requires contradictory search evidence to block automatic acceptance.
- **P2: Material title/name contradictions are ignored** (`identity.py:101-105`). A reference titled `Visit National Aviation Museum` with `place_name="Museum A"` is evaluated exclusively as Museum A. Exact independent search evidence for Museum A produces automatic acceptance despite the different named venue in the title. The accepted synthetic batch produced seven automatic resolutions and one audit-pending result. Preserve ordinary descriptive titles, but route materially conflicting venue claims to review under the no-material-contradiction contract.
- **P2: Malformed claimed IDs can abort the batch** (`identity.py:266`). Intake accepts an optional `source_place_id` represented as a dictionary. With an unrelated requirement subject and non-overlapping observed candidate IDs, set membership raises `TypeError: unhashable type: 'dict'` before the malformed-ID guard runs. The CLI consequently reports a batch evidence-correction failure instead of reference-level uncertainty. Validate the optional ID before membership checks and retain per-reference handling.

## Evidence and limitations

- Re-ran `.venv/Scripts/python.exe -m pytest backend/tests/evaluation -q -rs`: **58 passed, 1 skipped**. The skip is the existing Windows symlink privilege case.
- Executed additional synthetic probes from stdin using temporary artifact files and the actual `load_batch`/identity resolver path. The four findings above are observed behavior, not inferred from code alone. Probe output was inspected in the review session; no persistent raw probe log was created.
- The passing suite does not cover these counterexamples. No fixes or corrective retests were performed in this review.
- No Google, model or database calls; no formal benchmark or experiment; no commit/push. No V0-V3 planner behavior was changed.
- The earlier acceptance record remains historical evidence of its stated checks. Its conclusion that no findings remained is superseded by this follow-up review. Correct these issues and add focused regression coverage before continuing downstream identity-dependent work.

Final actionable counts: Standards axis **1 correctness finding** (zero explicit coding-standard violations); Spec axis **3 findings**.


## Correction disposition — 2026-09-30

All four findings above were corrected after explicit user approval. Twenty new synthetic regression cases demonstrate the failure-before/fix-after sequence. Final evaluation suite: 78 passed, one existing Windows symlink skip; Ruff and format checks pass. Standards and Spec follow-up reviews each report zero actionable findings. See [acceptance follow-up](ticket-03-acceptance.md) for the full sequence and conservative recognition limits. Original findings remain historical evidence, not outstanding defects.
