# Blinded ranking development and acceptance

Ticket [09 / #21](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/21),
2026-10-02. Status: Implemented and accepted after offline checks and user-reported
native browser checks. Current interfaces belong to the
[human-review contract](../../contracts/0005-quality-human-review.md#human).
No actual rater study or formal version comparison is reported here.

<a id="rtpeval-ticket-09-acceptance"></a>

## Blinding, travel representation and answers

Implementation `6095877` / `d36b52d` from base
`541c684a4ae58001b513a9508b65a1d99507b0bf` introduced source-linked package preparation,
private mappings, seeded Latin-block label balancing, revision-aware answer import,
descriptive pair reports and an isolated self-contained React renderer. Hidden duplicates
did not add main-result weight; later drafts did not supersede submitted answers.

Tests exposed free-text leakage, fixed label assignments, invalid duplicate acceptance,
omitted unbound transport and duplicate journey rows. Corrections retained unresolved
claims, meaningful fields and conflicting alternatives, with source-linked redaction.
Date-only departure was wrongly accepted as midnight; requiring a clock corrected it.
Destination labels were restored without exposing private IDs.

Spec review found a P1: V0 Activity/start/end labels differed from Transfer/provider labels,
revealing version identity. `5f43b5d` adopted common travel/departure/arrival/duration
fields and a private batch alias. Inferred arrival remained labelled; `4be6e01` corrected
formatting. Final initial reviews were clear.

## Integrated display revisions

`f600315` added a UTC-default browser-IANA selector from
`dfe26954bfcad7a22f2f7c87c3302dbd767fe9f3`. Explicit-offset instants converted with dates,
cross-day/DST behavior; source-day grouping stayed fixed. Local clocks/date-only values
were not made into instants. Invalid values stayed raw and missing values `Not supplied`.
Strict checks corrected JavaScript rollover/invalid clocks. Spec then found compact
`+0200` / `+02` offsets unconverted; regression and `29df5fd` corrected conversion without
changing original strings. A fractional-offset fixture used Intl's offered Calcutta alias
while preserving independently expected India clocks.

The user subsequently removed Original timestamp controls (`6725071`, base `4c9d572`),
corrected `HH-mm` to `HH:mm` (`7809b33`), then removed dedicated uncertainty fields,
item notices and time-conversion warnings (`f1f0cc0`, base
`925ad71b8c4c360e5af079957c9463674f39e2f7`). The neutral Inferred arrival label,
ordinary notes/preferences and duration basis remained. Frozen unknowns, notices,
source/public/private JSON and answer/scoring linkage were preserved. Hidden hints do
not establish certainty; these later choices superseded the original display requirements.

## Recovery, clear behavior and native acceptance

The package recheck at `290ef203c20fa18e8d4f3ab05aa4e5b5ecf6cda7` matched frozen public/
private objects, public JSON bytes, mapping/presentation hashes, embedded renderer receipts
and offline CSP. Synthetic import twice retained six records once, four effective
submissions and three main tasks; revision 2 superseded 1, draft 3 stayed audit-only.
The hidden duplicate supplied separate six-pair consistency. These were synthetic answers.

After the user confirmed display/time-zone and narrow-window checks, recovery remained
untested pending a reset feature. `3a2e3d9` from
`cbb716a2d0995bcbe062e09c0e07489d87b791f1` added confirmed package-scoped clearing,
failure preservation and backup restoration. Spec found pending FileReader imports
could restore cleared data. Failing regression and `d514508` corrected invalidation
only after successful persisted clear; failed/cancelled clearing did not invalidate import.

At `ff00057`, the user reported submit, refresh/recover, JSON download, clear, blank
refresh and reimport preserving answers/revisions. Combined with prior display checks,
this completed Ticket 09 development acceptance. Browser tooling could not navigate
`file://`; these are user reports, not independent automated browser passes. Issue #21
closed while parent #12 remained open for 10–12 at that checkpoint.

## Validation and evidence

| Checkpoint | Observed result |
| --- | --- |
| Initial implementation | Backend **2299 passed, 10 skipped**, zero deselected, 150.85 seconds; frontend **89 passed** |
| Compact-offset correction | Frontend **94 passed / 13 files**, 39.39 seconds |
| Timestamp-control removal | Frontend **94 passed / 13 files**, 38.28 seconds |
| HH:mm correction | Frontend **94 passed / 13 files**, 36.49 seconds |
| Hint suppression | Frontend **94 passed / 13 files**, 25.49 seconds |
| Source/recovery recheck | UI/answers **11 passed / 2 files**, 5.34 seconds; backend **26 passed**, 3.90 seconds |
| Clear/import-race correction | Frontend **98 passed / 13 files**, 32.64 seconds |

Relevant TypeScript, product/blind builds and lint passed; final review axes were clear.
Later UI gates did not rerun backend or independently establish native acceptance.
Backend skips were nine database opt-ins and one symlink case. These results overlap.

Local packages are under `artifacts/rtpeval/ticket09/`: `public-final/`,
`public-timezone-final/` with `validation-timezone-final.json`, `public-display-final/`,
`public-no-hints/` with `validation-no-hints.json`, and `public-clear-answers-final/`.
The recheck evidence is `acceptance-20261002-1910/` with `backend-junit.xml`,
`integrity.json`, `synthetic-answers.json`, `imported.json`, `report.json`.
Frontend results were observed outputs, not separately saved logs. Each public package
contains only `review.html` / `presentation.json`; private mappings remain separate.
Renderer revisions preserved frozen public JSON and presentation/mapping hashes.
These local identifiers locate evidence, not hosted downloads.

## Limits

Synthetic answer tests and user browser observations establish engineering functionality,
not participant preference or real-world itinerary feasibility. No provider call,
formal comparison or later-ticket execution is established. The subsequent asynchronous
save/navigation import defect is recorded in the
[release review](2026-10-04-evaluation-usage.md#asynchronous-import-correction-during-release-review).
