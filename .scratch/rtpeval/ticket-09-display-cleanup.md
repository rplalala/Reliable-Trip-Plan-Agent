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

## Subsequent user clock-format correction

During closeout, the user explicitly corrected the desired clock format to HH:mm.
This supersedes the earlier HH-mm request for current display. Use colon-separated
24-hour clocks for converted timestamps and valid missing-zone local clocks; retain
dates, source grouping, uncertainty, parsing and Original timestamp removal. Original
source strings, artifacts, answer schemas and scoring remain unchanged. The existing
UI test's expected literals were updated; the selected inferred-arrival regression
first failed for 10:30 because the UI still displayed 10-30 (1 failed, 7 not selected).
The renderer and its instruction now use HH:mm. Actual final results will be recorded
after validation; the earlier 94-test removal gate is a separate checkpoint.

Original timestamp removal commit 6725071 received independent Standards/Spec reviews:
zero documented/actionable Standards findings and zero Spec findings. The Spec reviewer
independently checked converted offsets, missing zones, invalid values and removed raw
valid strings; no full-test rerun or browser acceptance by reviewers is claimed.
After the user format correction, final full frontend: 94 passed / 13 files in 36.49s.
TypeScript, final blind build and lint passed. The format change/direct expected literals
and this accepted correction record are committed separately before its final review.

## Final local closeout checkpoint

7809b33 (fix: display blinded review times as HH:mm) preserves the user's format
correction as a separate commit after 6725071 (fix: remove original timestamp controls
from blinded review). Both Standards and Spec reviewed 6725071...7809b33 and report
zero residual findings. Spec independently rendered converted/local clocks, missing
zones, invalid values and removed controls; no full test or browser pass is inferred.

Generated ignored artifacts/rtpeval/ticket09/public-display-final/review.html from final
assets; validation-display-final.json records HH:mm, removed control, renderer hashes
and code revision. Exact public JSON bytes/presentation hash and private mapping match
the earlier frozen material. Older package checkpoints remain unchanged. This new
package supersedes earlier examples for the remaining manual browser acceptance.
The user's cropped screenshot shows source uncertainty and inference notice text only;
it does not establish the full package's responsive/persistence/export/import gate.

Issue #21 and parent #12 were updated with removal, format correction and clear final
reviews, then independently fetched to verify exact bodies, unchanged labels and open
states. Browser-dependent acceptance remains unchecked. Source uncertainty explains
the uncertain traffic duration; the separate missing-arrival notice identifies display
arithmetic, not a verified arrival. Neither claim was altered to suppress uncertainty.
No backend/planner/scorer/dependency/source/answer change, push, live/native supplement,
real rater session, formal comparison, freeze or later-ticket work occurred.

Final closeout checks: eight English documents and 191 local Markdown target
occurrences passed, along with diff whitespace. Backend executable code, scripts and
dependency manifests are unchanged against the review base. Documentation is a
separate coherent local commit; generated package/validation and the development
archive remain ignored. Manual acceptance is not inferred from automated checks.
