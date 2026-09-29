# Dimension scores and auxiliary total — accepted scoring structure

Status: Five equal-weight dimensions accepted. The user requires a numeric result for each group/version without rewarding missing evidence. Verified-compliance formula PASS/(PASS+FAIL+UNKNOWN) is accepted; group-wide N/A exclusion and single-version zero contribution are accepted. Not implemented.
Date: 2026-09-28.

## Purpose

Provide a readable 0-100 summary alongside the primary metric vector. The total represents measured reliability/constraint compliance, not overall usefulness or proof that a version is best. Resources and blinded human rankings remain separate. All settings must be fixed before results are inspected; no version-specific weighting or post-result tuning.

## Accepted five dimensions

| Dimension | Score and unit | Required companion information |
| --- | --- | --- |
| Explicit requirement fulfillment | 100 * passed / all applicable supported reviewed obligations (REQUIRED, EXCLUDED and supported explicit time obligations) | Applicable/decidable/UNKNOWN counts; obligation-kind breakdown. No obligations gives N/A, not 100. Keep date/count components within their parent obligation rather than multiplying its weight. |
| Canonical grounding | 100 * resolved / applicable main visits, as already specified | Unresolved reasons, role coverage and supplied-ID conflicts separately. Unresolved lowers verified coverage, not proof of fabrication. |
| Schedule non-overlap | 100 * confirmed conflict-free timed commitments / applicable distinct timed commitments | Count a commitment once if it overlaps any other; do not score every pair of nonoverlapping activities, which would dilute conflicts. Report pair counts and union conflict minutes separately. Deduplicate transfer representations. |
| Opening compliance | 100 * confirmed compliant / all applicable visits | Structural/evidence coverage and basis, UNKNOWN and conflict minutes; zero grace. |
| Route compliance | 100 * confirmed compliant / all applicable same-day inter-venue legs | Each leg combines applicable product-cap and scheduled-feasibility checks; explicit no-route is FAIL. A known failing check makes the leg FAIL, all applicable checks must pass for PASS, otherwise UNKNOWN. Missing duration on a no-route FAIL remains missing, not zero. |

Route scores use the accepted mode thresholds, DRIVE reserve and independently applied five-minute cap/schedule tolerances. No cap and timing double penalty inside the route dimension: one leg contributes one outcome. Time overlap and route feasibility can still capture related consequences in different dimensions; equal weighting is transparent, not proof of statistical independence. Report constituent metrics and do not claim the total perfectly removes correlation.

Date coverage, density, repetition, observed transfer burden and supplied-ID consistency remain visible metrics rather than extra penalties silently inserted into the five-score profile. Any later decision to include them requires explicit specification. More activities, fewer repeated visits and shorter transfers are not automatically higher subjective quality.

## Accepted verified-compliance score

The earlier proposal to suppress totals whenever evidence is incomplete is superseded by the user's objective: each selected group/version needs a quantitative result, without missing evidence improving it.

For a dimension with applicable check units, the accepted score = 100 * PASS / (PASS + FAIL + UNKNOWN). Retain UNKNOWN in the denominator, including structurally unresolved applicable units; never silently delete them or redistribute their weight. For grounding, use verified identities / all applicable main visits. The auxiliary total is the equal-weight mean of the common included dimension scores, 20 percent each when all five apply.

This is a verified-compliance lower-bound score. FAIL and UNKNOWN earn no verified-success credit but remain different factual outcomes, with separate counts and reasons. It does not assert that unknown items are wrong. Continue reporting conditional compliance PASS/(PASS+FAIL) and coverage alongside the score; neither replaces its fixed applicable denominator.

Example: A has 9 PASS, 1 FAIL and 0 UNKNOWN opening checks: verified score90, conditional compliance90, coverage100 percent. B has 2 PASS, 0 FAIL and 8 UNKNOWN: verified score20, conditional compliance100, coverage20 percent. B does not receive a higher verified score merely because only its easy observations are known. All10 UNKNOWN gives score0 with an explicit no-verified-success explanation, not ten confirmed failures.

For a fixed applicable set, replacing PASS with UNKNOWN reduces the score; replacing FAIL with UNKNOWN leaves it unchanged; learning a previously unknown PASS increases the score. Thus evidence removal alone cannot improve the score. This does not prove immunity to activity deletion, changed applicability, or missing denominator units; preserve date coverage, visit counts and structural uncertainty and settle the edge rules below before implementation.

## Accepted applicability and zero-opportunity rules

N/A means no applicable check; UNKNOWN means a check applies but semantics, structure or evidence cannot establish its outcome. Missing evidence never makes an applicable check N/A. A dimension's applicability is determined over the whole itinerary, not one empty day.

For each submitted group, determine one common included-dimension mask. A dimension genuinely N/A for all four versions is omitted for all four; remaining dimensions share equal weights. For example, no supported explicit obligations in the shared RequirementSpec makes requirement fulfillment N/A for every version. Do not drop one version's dimension merely because its data is missing.

If a dimension is applicable for some versions but has no check units for another, retain the common weight and give that version a zero score contribution with status N/A/no-checks. This is an accepted accounting convention, not a fabricated FAIL, not an observed rate of zero, and not a change to P/F/U counts. Keep raw rate and coverage N/A while numeric contribution is zero. A legal single-venue itinerary can therefore receive no route verification credit; this limitation must be visible.

Compute total_v = sum of dimension contributions over the group's common mask / number of included dimensions. Weights and mask are identical across its four versions. Unknowns remain in applicable denominators. For an entirely empty common mask, an arithmetic mean is undefined; return an explicit no-scorable-dimensions diagnostic rather than inventing 100 or dividing by zero. Such a package has no meaningful primary itinerary checks and must be reconciled upstream; this is not an ordinary accepted itinerary total.

Do not compare totals with different masks as if they measured identical content. Report masks and counts and preserve request-level paired comparisons. Equal totals can conceal different FAIL/UNKNOWN composition. Evidence-rich places can receive more verified credit; this is a verified-reliability score, not unconditional actual travel quality.

## Accepted structure and implementation boundary

Five dimensions, equal weighting, PASS/(PASS+FAIL+UNKNOWN), common-N/A exclusion and single-version N/A zero contribution are accepted. Resource metrics, subjective rankings and the primary metric vector remain separate. Detailed rule implementations and technical contracts are still incomplete; no implementation, provider calls or experiments are authorized.

## Terminology and companion rates

For N = PASS + FAIL + UNKNOWN > 0, report verified-compliance score = 100*PASS/N, verification coverage = 100*(PASS+FAIL)/N, unknown rate = 100*UNKNOWN/N, and confirmed violation rate = 100*FAIL/N. Unknown rate is not verification coverage; they sum to 100 percent. Verification coverage includes confirmed failures because their outcomes are known. Verified-compliance score plus confirmed violation rate plus unknown rate sums to 100 percent.

If called reliability in presentation, label it verified reliability/verified compliance, not unconditional real-world reliability. Conditional compliance remains 100*PASS/(PASS+FAIL) when that denominator is nonzero and is not the auxiliary-score input. For a zero-applicability dimension, raw rates are N/A; the separate accepted common-mask/zero-contribution rule determines the auxiliary accounting.
