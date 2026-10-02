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
