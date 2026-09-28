# Evidence and time parsing contract

Status: Technical design following accepted rules; fixture implementation and provider acquisition remain unauthorized.
Date: 2026-09-28.

## Verified provider facts

Places current hours cover the request-local day plus six days and can clip endpoints at that window. Regular hours describe a weekly pattern; always-open uses Sunday 00:00 with no close. Points carry local dates, weekday/time components and a truncation flag. Preserve these distinctions in the snapshot. Source: [Places reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places).

Routes distinguishes element status from route condition. duration is seconds with possible fractional precision; explicit ROUTE_NOT_FOUND omits route-duration fields. Requests without departure use request time; past departures are only supported for TRANSIT. These constraints do not authorize shifting a planned date. Source: [Route Matrix reference](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRouteMatrix).

## Time interpretation

Preserve original timestamp strings and offsets. Aware timestamps identify instants; use an independently supported place IANA zone to expand opening periods and determine destination-local dates. Never use the computer's timezone. If an explicit offset conflicts with the local visit/date interpretation required by the output, retain the mismatch and mark dependent checks UNKNOWN rather than silently stripping the offset or changing the visit date.

A naive wall timestamp may be localized only with an independently recorded destination/place IANA zone and a unique valid local-time interpretation. Record the localization basis. DST ambiguous/nonexistent wall times, contradictory zones, missing zones or incomplete dates yield a specific UNKNOWN for dependent checks. Date coverage on unambiguous declared day fields can still be reported without inventing instants. Past dated input is not rejected by current planner date-window validation during evaluation.

Use half-open intervals. Equality of visit end and opening close is allowed; positive-duration overlap is required for conflict. Expand multiple and overnight periods onto explicit dates, include the preceding day's overnight contribution, and union only touching/overlapping intervals. Never bridge a lunch closure. Preserve provider precision without rounding a near-boundary conflict into a pass.

## Opening parsing truth table

| Evidence | Independent treatment |
| --- | --- |
| Missing hours or periods | UNKNOWN with missing-field reason; no inferred 24-hour access |
| Invalid endpoint types/ranges, malformed period | UNKNOWN for the affected scope; preserve the invalid raw observation |
| Regular always-open encoding documented above | Expand within the requested evaluation date scope, labelled regular basis |
| Other missing close | Do not infer infinity; UNKNOWN unless a documented bounded current-window truncation supplies an interpretable boundary |
| Valid complete weekly periods with no opening covering a particular date/time | Outside adopted weekly opening; use regular-basis label, subject to known special-date exceptions |
| Empty collection without independently established completeness/closure meaning | UNKNOWN, not automatic closed |
| Interpretable explicit applicable closed schedule | Known closed interval; evaluate visits against it |
| Current periods covering the visit date | Prefer over regular pattern; retain source window and truncation flags |
| Exception date with unusable specific hours | UNKNOWN with accepted explanation; no silent regular substitution |
| Current window does not cover visit date | Regular fallback if interpretable and no unresolved applicable exception; never present it as historical/date-specific fact |

A partial observation may prove a conflict in its known portion; record the confirmed outside duration as a lower bound and the remaining unknown span. For a visit verdict, a demonstrated conflict is FAIL, full covered containment is PASS, otherwise UNKNOWN. No unknown portion is counted as closed. Complete duration totals and lower bounds are distinct report fields.

## Route response truth table

Verify expected origin/destination indices and unique response association before interpreting a leg. Missing/duplicate contradictory elements are UNKNOWN. Keep requested coordinates, identities, mode, departure and returned context in the evidence key.

| Response | Independent treatment |
| --- | --- |
| Request/transport error or missing/invalid element status | UNKNOWN with cause |
| Successful status plus explicit ROUTE_NOT_FOUND | FAIL for the applicable queried leg; duration and deficit stay null |
| Successful status plus ROUTE_EXISTS and finite nonnegative duration | Use returned duration, including accepted traffic fallback; inspect distance separately for WALK cap |
| ROUTE_EXISTS with missing/invalid/negative duration | UNKNOWN; do not substitute staticDuration automatically |
| Contradictory indices/condition/status or unsupported condition | UNKNOWN with the contradictory data retained |

A status object with omitted code uses the provider's default zero semantics; missing status itself is distinct under the frozen extraction rule. Parse durations as decimals rather than flooring; existing shared normalization rounds upward, so retain original value or document that conversion if used. Route tolerance remains exactly 300 seconds per check. A missing WALK distance does not support the distance-cap PASS; a separately proven failure still establishes FAIL.

Query the intended departure where the adopted provider mode supports it. Record omission when a deliberately time-independent route estimate is used; do not claim a historical departure was queried. If a requested historical/future departure is not supported, return UNKNOWN rather than silently querying another day. Fallback traffic calculation alone is accepted, per the user's simplification; wrong endpoints/modes are not. Do not append a second wait duration to a provider total; the current matrix interface supplies no decomposed waiting record.

## Identity and role handling

Keep supplied ID and independently adopted identity separately. Neutral normalization may support candidate comparison but cannot assert alias equivalence or uniqueness. Automatic acceptance requires corroborated association without material conflict; items lacking such corroboration and all high-impact/ambiguous items go to adjudication, never automatic top-one acceptance. Acceptance thresholds and audit sample settings must be explicit configuration validated on development fixtures; no guessed confidence percentages are frozen here.

Generic no-POI items are free-time/transition-like per user instruction. Named but unresolved POIs remain applicable identity UNKNOWN, not free time. Explicit transport stays transport; reviewed protected intervals remain occupied even when a generic placeholder overlaps them. Reconcile transport activity and Transfer by endpoint/time references; if their correspondence is ambiguous, retain the issue rather than duplicating occupancy silently. One primary activity containing multiple POIs is a material diagnostic, not a time-splitting opportunity.

## Implementation checks and limits

Author independent synthetic fixtures for each table row, DST folds/gaps, overnight periods, sparse matrix elements and exact tolerance boundaries before implementing dependent rules. Primary-document inspection is not a live API test and supplies no coverage guarantee. Snapshot storage/retention settings must be checked for the intended provider environment before operational acquisition; this document does not assert unrestricted raw-data retention.

No fixtures, provider responses, executable parser or benchmark cases were created in this step.
