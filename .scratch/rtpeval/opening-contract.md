# Opening evaluator contract — draft

Status: Accepted principles consolidated; zero-grace boundary handling accepted; special-date UNKNOWN with explicit reasons accepted. Provider encoding and timezone edge rules remain OPEN. No implementation or live calls.
Date: 2026-09-28.

## Inputs and independence

Consume the scheduled visit interval, independently resolved place, frozen provider observations, and versioned rules. Do not consume V3 opening findings or planner-selected opening_hours as ground truth. Scope is scheduled primary place visits under the shared activity-role contract; Nearby is excluded. V1 does not distinguish entry/exterior intent and no exemption is inferred from wording. Here v1 means RTPEval v1, not planner V1.

Opening compliance establishes containment in adopted evidence only; it does not establish bookings, access permissions or future factual certainty. Missing hours never imply always open or closed. open_now does not establish opening at the scheduled visit time.

## Code-informed evidence boundary

Current PlaceDetailsDTO retains time_zone, current_opening_hours, regular_opening_hours, requested_at and retrieved_at. Planner normalization also exposes periods_state, source dates and special days, derives a current window from collection-local date plus six days, and sets opening_hours to current-or-regular. These are existing code behaviors, not independently verified evaluation rules.

Freeze the original current/regular objects and timestamps separately. The normalizer's present state only verifies a list of dictionaries, not correct endpoint meaning. Its special-day projection retains dates but drops other raw attributes; it cannot by itself determine the complete exception semantics. The independent evaluator must check endpoint structure and temporal applicability. Exact provider encodings for continuous 24-hour periods, missing closes, truncated endpoints and closed schedules require primary-document verification and independent fixtures before implementation. This inspection made no live provider calls.

## Proposed processing order

1. Determine whether the visit is structurally evaluable: actual start/end, positive duration, applicable role, and a consistent timezone interpretation. Preserve raw timestamps. Never silently fix an interval or invent a missing time.
2. Resolve identity independently. Missing identity prevents place-hours lookup without changing unrelated schedule metrics.
3. Determine the evidence basis for the entire visit interval, including a date boundary when relevant. Use applicable interpretable date-specific/current evidence before regular weekly evidence. A snapshot collected after the trip cannot retroactively turn its current hours into historical visit-date evidence.
4. Expand valid periods into timezone-aware intervals. Preserve multiple daily periods, cross-midnight periods and closures between periods. Merge only touching/overlapping valid intervals. Do not combine first opening and last closing across a lunch break.
5. Apply the adopted evidence to the full planned visit, retaining basis and missingness. For partial evidence, expose known conflicting portions separately; do not label the complete visit compliant without full applicable evidence.

## Interval and timezone semantics

Proposed containment uses half-open visit/availability intervals: arrival exactly at opening and departure exactly at closing are compliant, provided the full positive-duration visit is covered. A split schedule of 09:00-12:00 and 13:00-17:00 does not contain an 11:30-13:30 visit; the known unavailable portion is 60 minutes.

Record the place's independently supported IANA timezone. Handling of naive itinerary timestamps, contradictory explicit offsets, missing place timezone, and DST ambiguous/nonexistent wall times must be fixed before implementation. Do not assume the machine timezone or discard supplied offsets. Ambiguity without a supported resolution prevents a definitive judgment. Overnight visits require evidence spanning all affected dates, rather than trimming them at midnight.

## Evidence states and metrics

Separate date-specific/current basis, regular-weekly fallback, and unavailable/uninterpretable basis. A missing periods field, invalid periods, explicit closed evidence and a confirmed interpretable empty schedule are not interchangeable. Do not infer closure merely from an empty normalized collection until provider meaning and completeness are established.

Report structural evaluability, identity/evidence availability, and compliance independently. Opening evidence coverage uses applicable visits as its declared denominator with structural exclusions/unknowns visible; compliance uses fully adjudicable visits. Report counts and evidence basis, not only a percentage. An empty compliance denominator is unavailable, not 100 percent.

For fully known intervals, outside-opening duration is the measure of the visit interval not covered by the union of adopted open intervals. It includes early arrival and within-visit closure, not only late departure. Preserve seconds before any display rounding. With partial evidence, any known unavailable duration is a lower bound and must be labelled partial; unknown portions are not counted as closed. Exact partial-conflict aggregation remains OPEN.

No automatic improvement is inferred from fewer visits or lower evidence coverage; report before/after denominator and visit changes alongside any compliance delta.

## Accepted decisions

1. Special-date exceptions: record UNKNOWN when the frozen evidence flags a relevant exception but lacks interpretable applicable hours. Do not use regular hours to override a known unresolved exception or an explicit closure. Regular fallback remains allowed for otherwise eligible dates beyond the current evidence window, with its weaker basis clearly labelled.
2. Accepted boundary tolerance: zero grace minutes for the main metric, using exact recorded times and the boundary convention above. Do not silently forgive a five-minute overrun. Display rounding does not alter the judgment. Any later nonzero tolerance belongs to a predeclared sensitivity profile, not a post-result adjustment.

## Documentation examples

Hours 09:00-17:00, visit 16:00-17:00: compliant under the accepted zero-grace convention. Visit 16:00-17:05: five minutes outside adopted hours. No interpretable opening evidence: UNKNOWN, not five or zero minutes of confirmed conflict. These are explanatory examples, not benchmark cases or observed outputs.

## Future checks

Independent fixtures should cover boundary equality, positive overrun, early arrival, split periods, overnight/24-hour encodings, weekly rollover, missing/invalid/closed evidence, known exceptions, current-window applicability, timezone/DST ambiguity, and incomplete cross-date evidence. Test pure replay without provider calls and independence from V3 verdicts. No fixtures or tests are implemented by this document.


## Special-date clarification example

Hypothetical evidence: a museum's regular Monday hours are 09:00-17:00; the frozen provider data marks the planned Monday as having exceptional hours but provides no interpretable schedule for that date. A 10:00-12:00 visit fits the regular weekly pattern, but that pattern does not establish the exceptional day's opening. The accepted outcome is UNKNOWN, not confirmed compliance or confirmed closure, with an explicit reason and evidence reference. If the date-specific evidence instead gives 13:00-17:00, the same visit conflicts with those known hours. This is explanatory only, not an actual Google response or benchmark case.


## Required UNKNOWN explanation

Every opening UNKNOWN includes a machine-readable reason, a concise human-readable explanation, and the relevant visit/date and snapshot evidence references. For the special-date case, the explanation must state that the evidence indicates exceptional hours for the planned date, the applicable schedule is missing or uninterpretable, and regular weekly hours therefore cannot establish compliance. Preserve regular hours as context, not as a replacement verdict. Do not assert that the venue is closed or that the visit fails.

Illustrative report: "UNKNOWN — the frozen evidence marks this visit date as having exceptional hours, but provides no usable schedule for that date. Regular Monday hours (09:00-17:00) do not confirm the planned 10:00-12:00 visit." Exact reason-code spelling belongs to the report schema; distinct causes such as missing hours, invalid periods, unresolved identity and timezone ambiguity must remain distinguishable.

Provider encoding and time interpretation are specified in [evidence-time-contract.md](evidence-time-contract.md). Public documentation has been checked; independent fixtures remain future implementation work, not completed validation.
