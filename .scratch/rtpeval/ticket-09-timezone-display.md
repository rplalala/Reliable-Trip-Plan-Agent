# Ticket 09 approved time-zone display extension

Date: 2026-10-02, Australia/Sydney. Review base:
dfe26954bfcad7a22f2f7c87c3302dbd767fe9f3, feature/evaluation; clean initial tree/index.
The user approved the following extension, local commits and no push.

## Accepted scope and test seam

Add a time-zone dropdown to the independent blind-review page, defaulting to UTC,
with available IANA zones. Explicit-offset activity start/end, travel departure/supplied
arrival and inferred arrival convert to the selected zone. Display a 24-hour HH-mm
clock together with its date, including converted cross-day dates. Keep original source
day grouping and indicate it as such; selecting a display zone does not move activities
between source days. Preserve original timestamps as inspectable source information.
Date-only request/day values do not identify instants and are not shifted.

Missing-zone local timestamps/clocks remain unconverted, use HH-mm when valid and state
that their time zone was not supplied. Missing/invalid values remain visible without
inventing a date, offset or clock. Free-text notes and preferences are not rewritten.
Inferred-arrival notices and source uncertainty remain. Presentation/source hashes,
private mapping, imported/exported answers and automatic scoring do not change.

Use browser Intl data without a provider call or new dependency. This is display-only;
the original preflight's source-preservation requirements still apply. No planner/scorer,
real rater, live/native supplement, formal comparison or later-ticket change is included.

Approved seam: the existing BlindReview React interface. Observe dropdown changes,
displayed clocks/dates, cross-day and daylight-saving transitions, missing-zone/invalid
source handling, retained uncertainty and unchanged answer/presentation linkage. Use
literal expected times independent of implementation and real Intl behavior. Run related
UI tests, full frontend tests, TypeScript, both builds and lint. Commit implementation/
direct tests before independent Standards and Spec review; preserve correction commits.
Regenerate a separate final synthetic package after the renderer build. Actual file://
browser acceptance remains a pending user check because tool navigation is prohibited.

## Validation and review

Initial UI red: 2 failed / 2 passed, because the dropdown and formatted inferred arrival
did not exist. The first sandbox run could not write Vite's bundled config; an authorized
normal-permission retry reached those observed behavior failures. After implementation,
4 UI tests passed. Added missing-zone/invalid-time checks exposed JS date rollover and
invalid clocks; strict date/clock validation corrected them, with 6 UI tests passed.
Daylight-saving departure/inferred-arrival checks passed with real Intl.

The first full frontend run passed 92 tests and failed 1: the new fractional-offset test
selected Asia/Kolkata even though the runtime's enumerated option was Asia/Calcutta.
The test now selects the actual offered IANA alias at the UI seam, retaining literal
expected India clocks. Final full frontend: 93 passed across 13 files in 38.99s;
7 BlindReview tests plus 3 existing answer tests participate. TypeScript, isolated
blind-review build, product build and lint passed. No new dependency or backend change.
Implementation/direct tests and this approved scope record will be committed before
Standards/Spec review; review results and the final synthetic artifact remain pending.
No new full backend run is claimed for this frontend-only extension.

## Committed review, correction and final acceptance checkpoint

f600315 (feat: add time zone selection to blinded review) commits implementation,
direct UI tests and the accepted scope before independent review. Standards: zero
documented breaches and zero actionable heuristics. Spec: one P2, explicit compact
offsets accepted at the existing projection boundary were not converted by the UI.
New UI regression failed for +0200/+02 before correction; offset normalization now
converts both while retaining exact original strings. Separate fix 29df5fd preserves
implementation history. Related 11 UI/answer tests passed in 4.44s; TypeScript,
blind build and lint passed. Final committed full frontend: 94 passed / 13 files
in 39.39s. Earlier 93-test gate above is a separate pre-correction run.

Both reviewers rechecked f600315...29df5fd: original P2 resolved, zero residual findings
on either axis. Spec independently checked positive/negative compact/hour offsets,
existing colon/Z offsets, invalid offsets and missing-zone behavior. No edits or
full-test rerun by reviewers are claimed.

Generated ignored artifacts/rtpeval/ticket09/public-timezone-final/review.html with
the final renderer; exact public JSON bytes, presentation hash and private mapping
remain unchanged from public-final. Separate validation-timezone-final.json records
renderer hashes, revision and the pending browser gate. Earlier renderer checkpoints
remain unchanged. Manual check request now targets this final package, including zone
switching, HH-mm/date/inference display, narrow layout, refresh and JSON backup/import.
Browser Use's file:// prohibition is unchanged; no circumvention or actual browser pass.

Issue #21 and parent #12 were updated with approved extension and review/fix status,
then independently fetched to verify exact bodies, unchanged labels and open states.
The browser-dependent acceptance criteria/parent checkbox remain unchecked. No push,
branch switch, planner/scorer change, source/answer rewrite or later-ticket work occurred.

Final documentation checks: eight English documents and 195 local Markdown target
occurrences passed; diff whitespace passed. Backend executable code, scripts and
frontend dependency files have no diff against the review base. Final documentation
is a separate coherent local commit; ignored renderer/validation/archive files are
excluded. Pending manual browser acceptance is not converted into a completion claim.
