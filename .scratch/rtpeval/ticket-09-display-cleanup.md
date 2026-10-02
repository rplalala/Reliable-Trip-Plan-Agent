# Ticket 09 user-requested timestamp control removal

Date: 2026-10-02, Australia/Sydney. Review base:
4c9d57218b3c200fc76690a7b8c47f38e2b3c2e4, feature/evaluation; initial tree/index clean.
The user explicitly requested removal of Original timestamp and asked what the
uncertainty/inferred-arrival notices in the screenshot mean. This narrow UI correction
is authorized by that request and overrides the prior inspectable-timestamp UI rule.
Approved local-commit/no-push policy and existing BlindReview React test seam apply.

Remove Original timestamp controls, related page instructions and unused styles.
Keep UTC-default IANA dropdown, converted dates/HH-mm clocks, source-day grouping,
unknown-zone/invalid-time handling and source uncertainty/inferred-arrival notices.
Original source/public/private JSON bytes and hashes, answers, scoring and V0-V3 paths
remain unchanged. Missing/invalid time values still retain their explicit original
value when no conversion is possible; removal concerns the optional timestamp control,
not suppression of malformed source evidence.

Explain in chat that source Travel time uncertain describes uncertain travel duration,
while the inferred-arrival notice describes a missing source arrival supplemented by
departure-plus-duration display arithmetic. These can coexist; no actual arrival is
verified by arithmetic. No wording or factual claim in either notice is changed.

Validate via the existing React seam: converted compact/hour-only offset timestamps
remain correct, and neither the control nor its raw valid ISO strings are displayed.
Run full frontend tests, TypeScript, isolated build and lint; commit implementation/
direct tests before Standards/Spec review, then document actual results and regenerate
a separate synthetic package. Actual file:// browser acceptance remains pending; no
browser policy workaround, live/native run, formal comparison or later ticket is included.

## Actual validation and review

Updated existing UI regression first failed (1 failed/7 passed): two Original timestamp
controls still rendered. Removed controls, helper instruction and unused CSS. Final
full frontend: 94 passed across 13 files in 38.28s; TypeScript, blind build and lint
passed. The same regression verifies compact/hour-only offset conversion remains
correct without exposing valid raw ISO strings. No backend or product-route change.
Implementation/direct tests and this scope record are committed before review;
review and final package evidence will be appended at their actual checkpoints.
