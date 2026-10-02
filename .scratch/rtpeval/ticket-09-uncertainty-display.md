# Ticket 09 user-requested uncertainty hint removal

Date: 2026-10-02, Australia/Sydney. Review base:
925ad71b8c4c360e5af079957c9463674f39e2f7, feature/evaluation; clean initial tree/index.
The user explicitly requested no uncertainty-factor hints. This authorizes the narrow
display correction and supersedes earlier requirements to show dedicated hint blocks.
Approved local-commit/no-push policy and existing BlindReview React test seam apply.

Remove the dedicated Uncertainty/unknowns field, all item notice blocks and warning
text adjoining displayed times, including missing-zone and invalid-time conversion
notices. Remove unused hint styling. Keep UTC-default IANA selector, converted dates,
24-hour HH:mm clocks, source-day grouping, supplied/missing time values and the neutral
Inferred arrival label. No new time-zone/date/arrival fact is invented; unknown-zone
clocks remain unconverted, invalid values remain raw, null remains Not supplied.
Ordinary source notes/preferences and display duration/basis fields are not rewritten.

Frozen source/public/private JSON, unknowns/notices records, hashes, answers, reports
and V0-V3 behavior remain unchanged. This is UI hint suppression, not source erasure,
provider verification or a claim of certainty. No backend or dependency change.

Use the existing React seam to verify missing hint fields/text while retaining inferred
arrival, correct times, unknown-zone local clocks and invalid/missing values. Update
the old hint-preservation assertions to the user's new display rule. Run full frontend
tests, TypeScript, blind build and lint; commit implementation/direct tests before
Standards/Spec review, then record actual results and regenerate a separate synthetic
renderer. No file:// workaround, live/native supplement, real rater session, formal
comparison, freeze or later-ticket work is included. Manual browser acceptance pending.

## Actual validation and review

The selected existing UI regression first failed because Uncertainty still rendered
(1 failed, 7 not selected). Filtered unknowns fields at the renderer boundary, removed
item notice rendering/time-warning text and unused hint CSS. Parsing and timezone
arithmetic remain unchanged. Final full frontend: 94 passed / 13 files in 25.49s;
TypeScript, blind build and lint passed. Existing regressions verify inference/time-zone/
DST/compact-offset/unknown-zone/raw-invalid values and answer revision behavior.
Implementation/direct tests/scope are committed before Standards/Spec review; actual
review, final artifact and tracker closeout results will be appended when available.
