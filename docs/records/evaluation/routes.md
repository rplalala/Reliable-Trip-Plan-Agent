# Independent route development

This record follows offline route scoring, coordinate bridging and bounded Seoul/Sydney
acquisition. The [opening/route contract](../../contracts/0004-opening-routes.md)
owns current definitions; [identity history](intake-identity-usage.md) records later
changes to endpoint eligibility. The development tools' commands are in the
[package guide](../../../backend/evaluation/README.md). Historical policies and
observations below are not current execution instructions.

Across these cases, UNKNOWN means evidence or applicability was insufficient; it is
neither feasible nor infeasible. Identity correspondence, factual grounding, coordinates,
provider coverage and journey feasibility remain separate. Original outputs/observations
were not retimed, rewritten or replaced to obtain favorable scores. Offline/mock checks
are distinct from real acquisition. Retail references exclude unknown account billing,
credits, taxes and tiers. These are development cases, not formal comparisons or freezes.

<a id="rtpeval-ticket-07-acceptance"></a>

## October 2: same-day route scoring and boundary corrections

Ticket 07 ([#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19))
implemented immutable `prepare_routes`/`score_routes` and local JSON CLI at base
`3427784b87d5864aba25dcba8b48430ec4de9dac`. V0 Activities and V1–V3 Transfers remained
separate projections without fallback. Same-day occurrences stayed distinct, while
requests deduplicated. Independent identities/coordinates and reviewed modes/occupancy
established context. Explicit departures were retained; otherwise the longest continuous
free fragment won, with earliest-UTC ties. This stage used canonical-only endpoints;
later physical-association eligibility did not retroactively change its evidence.
Material/replay errors exited 2 without partial cohort; successful scoring exited 0
including FAIL/UNKNOWN. Neutral extraction preserved eight Ticket 05 validator definitions.

Three consequential Spec findings were corrected: disjoint alternatives poisoned
comparison, unresolved populations understated burden, and possible occupancy at a
deadline could borrow 300-second tolerance. Public regressions preserved interval
uncertainty: common 10:30 occupancy yields FAIL with raw 120-second deficit; alternatives
at 10:30/10:35 yield UNKNOWN, never a fabricated continuous window. Standards centralized
caps/tolerances/reserve/query defaults. Both axes rechecked clear.

| Recorded gate | Actual result / coverage |
| --- | --- |
| Initial neutral extraction | 27 failed/39 passed; import correction yielded 66. |
| Initial route/CLI and evaluator | 63 route tests;392 evaluator passed/1 skipped. |
| Pre-review full backend | 2221 passed/10 skipped, 158.36 seconds. |
| Initial Spec corrections | 84 route/CLI passed; intermediate full 2232/10,200.72 seconds. |
| Deadline-boundary correction | Two RED cases; final 86 route/CLI passed, 20.35 seconds. |
| Post-boundary broad gate | 2232 passed/10 skipped/2 deselected, 186.17 seconds after existing embedding tests hung. |
| Separate approved test repair | Fresh unfiltered 2234 passed/10 skipped/zero deselected, 196.39 seconds. |
| Closeout targeted subset | 166 passed, 34.26 seconds; not another full gate. |

The interrupted full run and two deselections remained real limitations until the
separately approved [embedding test repair](../v0-v3/v2-embedding-timeout.md).
Its diagnosis established cold SDK preparation outlasting 20 ms before an unbounded
handler wait; runtime retrieval/budgets were unchanged. Later full validation is a
new actual gate, not a derived pass from overlapping subsets. All Ticket 07 full runs
kept nine opt-in PostgreSQL cases and one Windows symlink case skipped; prior database
supplements were not counted. Ruff/compilation/CLI/diff checks passed.
Implementation `2b66c9f889ca8964f97dbc67b2a601ebb56be64c` and independent test repair
`b18daef4af2fecba36d7b84315c8946a772aeae8` preserve the distinction.
Evidence identifiers: `thesis_notes/evaluation/ticket-07-validation/` separate
pre/post-review, interrupted and broad logs. Published gate details above remain
understandable without private evidence. Synthetic trust-boundary fixtures did not
establish provider availability or coordinate truth.

<a id="snapshot-coordinate-bridge-2026-10-03"></a>

## October 3: coordinates from independent snapshots

At base `e8e75b01307fc5ecc39910262249a4cceb5dbaea`, public probes found eight resolved
visits but no route context without a coordinate envelope. Preparing saved coordinates
produced one V0 context without another send. The accepted snapshot bridge extracted
only exact adopted IDs, bound manifest/plan/intake/identity/raw hashes and retained
retrieval time/pointers without invented review metadata. Finite/ranged agreeing
coordinates were usable; missing, malformed or contradictory points were local diagnostics.
Foreign/corrupt/stale sources rejected atomically. Reviewed manual coordinates remained
an alternative; selecting both sources rejected. Different evidence digests required
their own prepared query plans rather than borrowing old route observations.

Public regressions covered missing interfaces, malformed values, agreeing/conflicting
duplicates and a huge integer that previously raised OverflowError. Evaluator 527/1
passed in 85.14 seconds; full backend 2356/10 in 198.85 seconds before independent review.
Implementation `f07b495` then Spec P2 found raw Search `places:null` invalidated the
whole coordinate batch despite usable Details. Filtering by converted observation
status preserved raw malformed evidence and other coordinates; 26 bridge tests passed
and final evaluator 528/1 in 65.70 seconds. Correction `5ddf9ae` passed both rechecks; no full
backend repeat followed this bounded correction. Old snapshots may lack coordinates;
no automatic backfill or tolerance for slightly disagreeing points was adopted.
This stage still used caller-owned acquisition transport, not today's installed caller.

<a id="new-v0-route-plan-2026-10-05"></a>

## October 5: Seoul source and first bounded collection

The source was the structured-transport V0 smoke, Seoul October 7–10, two travelers,
KRW 1200000, Asia/Seoul(+09:00). Result SHA-256:
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`;
Input SHA-256:`07be92a51cc1db24d925e04ab16d15c15f2e501cecfd24a151ea9ee6cb6debfa`.
All four declarations were bound and unchanged:

| Date | Original endpoints / activity IDs | Mode | Claimed transport | Next visit starts | Nominal continuous time G |
| --- | --- | --- | --- | --- | --- |
| 10-07 | Gyeongbokgung Palace (`day1-gyeongbokgung`) → National Museum of Korean Contemporary History (`day1-contemporary-history-museum`) | WALK | 12:00–12:20, 20 min | 12:30 | 30 min |
| 10-08 | Bukchon Hanok Village (`day2-bukchon`) → Insadong (`day2-insadong`) | WALK | 12:00–12:25, 25 min | 12:35 | 35 min |
| 10-09 | Seoul Museum of History (`day3-seoul-museum-history`) → Gwangjang Market (`day3-gwangjang-market`) | TRANSIT | 12:00–12:35, 35 min | 12:45 | 45 min |
| 10-10 | Changdeokgung Palace (`day4-changdeokgung`) → Jongmyo Shrine (`day4-jongmyo`) | WALK | 12:00–12:20, 20 min | 12:30 | 30 min |

G is source schedule arithmetic, not independent journey duration; own transport is
excluded from competing occupancy and disconnected gaps cannot be summed.
The Prepared-only plan at `ff2085f6e6dafffa2b02f9b14bb10c89e49b3be8` became separately
approved execution under [#61](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/61).
`rtpeval_route_rules_1` used WALK/TRANSIT cap 45 min plus 5 min cap tolerance, WALK 3000m
with zero distance tolerance, and 5 min grace at next visit but zero at hard protection.
Provider failure stayed UNKNOWN; applicable proven component failure could FAIL.

The frozen maximum was 22 sends: 9 Search, up to 9 Details and 4 single-element matrices,
zero model/retries, 20 seconds/request, 600 seconds overall. TRANSIT bound noon Seoul October 9
(`2026-10-09T03:00:00Z`); WALK was time-independent. Dated retail maximum USD 0.515
used Search Enterprise 0.035, Details 0.020, Matrix 0.005. No coordinate/mode/date substitution
was permitted. Native preparation without identities returned `identity_replay_required`.

### Acquisition outcome and parser diagnosis

Execution revision `0f0120dc63ac25b492fd5d474c1d04826c5ab22f`, tree
`04684766d16cf2428cdefc2656f5e101c14b773e`. Three packet tests and 81 related checks
passed in 5.36 seconds. Approval initially blocked before launch; direct human approval later
admitted one execution. It exited 0 in 3.328 seconds with 9 Search HTTP 200, zero Details/Routes/model
and zero retries. The frozen audit selected no automatic proposal because none reached
that stage. All nine references remained unresolved: two high-impact review and seven
`malformed_address_components`. Zero adoptions meant zero route contexts/requests;
all four route verdicts stayed UNKNOWN. Mode policy alone PASS did not prove feasibility.

Six reference searches(seven candidate rows) had numbered sublocality levels sharing
the generic tag; the parser treated the tag as a unique slot and rejected distinct
values. Jongmyo had a component without types and failed earlier. These were parser
outcomes, not proof of incorrect places. [Google's component reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places#AddressComponent)
supported the inference that normalization was too restrictive; fixing it alone would
not satisfy identity/high-impact/audit gates. No fix or extra acquisition occurred.

Nine exact usage events matched TextSearch Enterprise SKU `E967-44BC-B44D` at USD 35/1000,
retail USD 0.315, distinct from planner costs and the prepared USD 0.515 maximum.
Replay matched identity/native routes exactly;9 raw hashes and 15 frozen source/packet
hashes matched. Evidence: `artifacts/v0-route-plan-20261005/` and
`artifacts/v0-route-execution-20261005/` snapshots, journals, reviews, diagnostics/cost.

## October 5: identity-assistance pilot and specified adoption

[#63](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/63) tested one Luna
low-effort strict-JSON association request against existing independent candidates.
Base `90d36999ee6daec2d228b21a07e9be3f530fd83e`; judge-Input SHA-256
`afd6ad59126bf18ffdb23cf8830228a16c842bd29fa6ec612033d6838c6a6d6d` bound nine references
(eight visits plus REQUIRED subject), fourteen candidate occurrences. Planner findings
and version labels were excluded. Limits were one send, 10000 input/4000 output, 60 seconds request,
300 seconds total, zero new Google/tools/retries, USD 0.01 reference; wire estimate 5646 included1024reserve.

HTTP 200 completed in 6.094 seconds request-to-capture, with 4213 input/1007 output/5220 total,
zero cached/reasoning. All nine matched supplied candidates with unique complete coverage.
Before seeing output, the owner agent independently recorded expected name/address matches;
all nine agreed. This was agent consistency, not human gold or measured accuracy.

| Reference | Native blocker | Model candidate | Owner field assessment |
| --- | --- | --- | --- |
| Required Gyeongbokgung Palace subject | `high_impact_review` | Gyeongbokgung Palace | Exact name/location; avoids the alternate palace and named subvenues |
| Gyeongbokgung Palace visit | `high_impact_review` | Gyeongbokgung Palace | Exact name/location |
| National Museum of Korean Contemporary History | `malformed_address_components` | National Museum of Korean Contemporary History | Exact name/location |
| Bukchon Hanok Village | `malformed_address_components` | Bukchon Hanok Village | Exact name/location |
| Insadong | `malformed_address_components` | Insa-dong | Supported segmentation variant and neighborhood location |
| Seoul Museum of History | `malformed_address_components` | Seoul Museum of History | Exact name/location; avoids the different history museum candidate |
| Gwangjang Market | `malformed_address_components` | Gwangjang Market | Exact name/location |
| Changdeokgung Palace | `malformed_address_components` | Changdeokgung | Supported distinctive name with generic Palace omitted |
| Jongmyo Shrine | `malformed_address_components` | Jongmyo Shrine | Exact name/formatted location despite incomplete typed components |

Seven exact names, two variants and two competing-candidate references were observed;
no adversarial/no-match population or alternate order/prompt/model was tested.
October 5 [Luna retail prices](https://developers.openai.com/api/docs/models/gpt-6-luna)
yielded USD 0.0009248, not an invoice. Seven runner tests passed in 2.36 seconds; all 61 protected
hashes and response SHA-256 `d32064b69732271cd0d89c3aa735df162c7fad4af95ef634183eaa5bec57f00a`
matched. Native adoption stayed zero and four routes UNKNOWN. Evidence:
`artifacts/v0-identity-prototype-20261005/`.

The subsequent [#67](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/67)
design was first Proposed, then Specified with offline slices #69 and #70. It allowed an
explicit default-off, versioned V0 model-assisted path with exact candidate/citation/hash
replay, while native/genuine human decisions, high-impact and predeclared positive audit
retained precedence. This historical policy deliberately differed from later current
version-specific identity. Raw partial/repeated component comparison limitations were
separated from invalid cited wire shapes; independent support was not programmatically
certified geography. Model confidence, title heuristics and policy-stamp substitution
could not create adoption. Short references fixed copying, not adoption or coordinates.
[#66 short-reference validation](../v0-v3/semantic-reference-correction.md) remained
separate. Planning restored nine old proposals and 61 hashes without requests/adoptions.

<a id="v0-identity-adoption-acceptance-2026-10-05"></a>

## October 5: offline adoption and route readiness

[#69](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/69) implemented the
replay-aware resolver/CLI and consumer handoff at base
`5449afc5ef7b5fede61d564cf66b6e0f36d39be8`. Saved #66 material yielded six adopted,
three review-pending, zero unknown/ineligible, without invented human decisions.

| Reference | Original structured claim | Result | Reason |
| --- | --- | --- | --- |
| Requirement subject | Gyeongbokgung Palace | Pending | `high_impact_review` |
| Planned visit | Gyeongbokgung Palace | Pending | `high_impact_review` |
| Planned visit | National Museum of Korean Contemporary History | Adopted | `model_supported_association` |
| Planned visit | Bukchon Hanok Village | Adopted | `model_supported_association` |
| Planned visit | Insadong | Adopted | `model_supported_association` |
| Planned visit | Seoul Museum of History | Adopted | `model_supported_association` |
| Planned visit | Gwangjang Market | Adopted | `model_supported_association` |
| Planned visit | Changdeokgung Palace | Adopted | `model_supported_association` |
| Planned visit | Jongmyo Shrine | Pending | `audit_pending` |

Six existing snapshot coordinates supplied two contexts: October 8 Bukchon→Insadong WALK
and October 9 History Museum→Gwangjang TRANSIT. Gyeongbokgung-origin and Jongmyo-destination
legs remained review-blocked. No new journey evidence existed; all four routes UNKNOWN.
Consumers recomputed full bound reports; changed policy/IDs/audit/review could not bypass
replay. Optional partial address fields retained their actual facts/diagnostics.

| Gate / correction | Actual result |
| --- | --- |
| First full backend | 2745 passed/10 skipped/1 import-guard failure, 336.65 seconds. |
| Guard retained; permitted stdlib schema validation | 382 evaluator/1 skipped; corrected full 2747/10,357.18 seconds before review. |
| Spec P2 corrections | Precise offset-aware authorization timestamps and native decision/audit retention when model freeze absent. |
| After review | 388 evaluator/1 skipped, 38.18 seconds;47 adoption cases; final full 2752/10,250.11 seconds. |

Saved-material replay also exposed provider-order assumptions and provenance compatibility;
complete facts were matched by exact ID, with original wire serialization/timezone binding.
Native-policy relabeling and malformed reports retained replay-required outcomes.
Implementation `6055905`, correction `481d531`; both review rechecks clear. CLI exited 3
and matched the saved report. Evidence: `artifacts/v0-identity-adoption-20261005/`;
all 61 original hashes unchanged. UTF-8 remained necessary for Korean JSON display.

### Route inventory after historical adoption

[#70](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/70), base
`f011a2929f9235f30a546f872f3a879cd6aaeed6`, followed #69 publication through PR 71,
merge `5d21d6b4685c7793f27954d7c175bed9524b3803`. Two adopted legs had saved coordinates,
zero missing-coordinate venues/Details. The October 8 WALK inventory was region-blocked;
October 9 TRANSIT conditional; two review-blocked legs had no invented endpoints.
Ready Routes were zero, proposed USD 0; two unready items hypothetical USD 0.01, not allowance.
Historical 8 Details+4 Routes ceiling was USD 0.06 at dated USD 0.005 Essentials/item.

Preparation used exact-ID `id, location` Details and 1×1 Matrix indices/status/condition/
distance/duration/fallback. It preserved original TRANSIT departure and did not import
Compute Routes' 7/100-day horizon into Matrix. [Country coverage](https://developers.google.com/maps/coverage)
marked KR WALK/DRIVE unavailable or low quality and did not attest TRANSIT support.
No NO_ROUTE or infeasibility was inferred from that coverage table.

Focused 25 request tests, 72 adoption/request and full 2777/10 in 399.30 seconds passed;
implementation `677a7e2` passed both independent reviews. Actual CLI exited 3 with
blocked/conditional inventory. Evidence: `artifacts/v0-route-requests-20261005/`.
No acquisition executor existed; 20 seconds per-call/300 seconds total/zero retries were proposed bounds.

## October 6–7: current identity and regional readiness

#78 introduced `rtpeval_v0_route_requests_2` at base
`769a066ac73f71fb4bbc4b6987522a42d57bb0ea`, implementation
`571ed9506ae08cbd70cb5cce736a5acbab05d59a`. Current version-specific replay became
the default; explicit `legacy=True`/`--legacy` preserved historical adoption replay.
Current policy had no mandatory human/audit identity gate. An absent report retained
all original legs and missing-model blockers instead of silently using six old adoptions.
Grounding FAIL/UNKNOWN excluded canonical endpoints and did not manufacture route FAIL.

Public regressions covered missing current evidence, legacy-report rejection, grounding
metadata and optional CLI reports. Related 178 tests passed in 55.46 seconds; full 2945/10 in
414.43 seconds; both reviews clear. Repeated synthetic visits retained 3 legs/6 endpoint occurrences
but 2 venue IDs/2 queries. The real #77 material had eight V0 UNKNOWNs, zero eligible endpoints,
coordinates/Details/routes/inventory and USD 0 proposed/hypothetical. Empty-population zero
missing venues did not mean coordinate completeness. All 81 protected hashes remained.
Package/inventory SHA-256:
`239df2ee99c95540fc6ff37835c9ad51c080dccc40f23058a8bbb442f98fffb3` /
`d085383d3250835891b2b67e8e7a95418bd30445d4de14f0f495f6c97c21ab61`.
Evidence: `artifacts/v0-route-requests-78-20261006/`. The old #77 implementation freeze
was stale after two preparation files changed; it could not authorize execution.

<a id="accepted-v0-identity-route-refresh-2026-10-07"></a>

#86 refreshed only offline evidence at `d26be76b111ed275e0cde70658a0bbecebf018a4` using
accepted #85 `versioned_api_identity_2`/`v0_identity_correspondence_3`: eight V0 visits plus
one requirement PASS. Eight independent coordinates made all 4 legs identity/coordinate
ready, with zero Details. Three WALK remained blocked and TRANSIT conditional under the
unchanged October 5 KR profile. Four materialized unready requests cost hypothetical
USD 0.020000; ready budget USD 0, historical upper bound USD 0.060000.
Actual CLI/library replay matched at exit 3; preflight stayed unauthorised. Focused 182
passed in 39.58 seconds; prior unchanged-code 2998/10 full gate was reused. Both reviews clear.
All 120 protected files/69 implementation hashes and 10 newly prepared outputs verified.

Evidence: `artifacts/v0-route-requests-86-20261007/`.
Inventory SHA-256:`3d138539bb3fafdb218f53313028450913bc86839f838b95c0669758ef1617b1`;
package: `ff16aa3bd539a08938df691e43d9b5645914282e3d6b78c3a34061884c10a3f5`;
accepted identity: `068631d1a1a484f9be25074401f560d08861f0435007060b62280a6f4f254da9`.
The requirement's null address was retained, not substituted for an endpoint.
All four route verdicts remained UNKNOWN despite identity/coordinate readiness.

<a id="kr-route-support-budget-2026-10-07"></a>

### Alternative Korean sources: assessed, not integrated

Free official-documentation assessment at `49a6fef135945e3612722a10b4394e6afe49d846`
retained the four original legs/options and eight source coordinates. No API/account
probe was performed. [Kakao REST](https://developers.kakao.com/docs/en/kakaomap/rest-api)
WALK/publictraffic used WGS84 and meters/seconds without departure-time parameters;
proposed WALK fixed BROAD_FIRST before results. [TMAP pedestrian](https://tmap-skopenapi.readme.io/reference/%EB%B3%B4%ED%96%89%EC%9E%90-%EA%B2%BD%EB%A1%9C%EC%95%88%EB%82%B4)
was a `WGS84GEO` alternative with encoded endpoint names. Neither attested future TRANSIT.
[ODsay](https://lab.odsay.com/guide/releaseReference) MaaS SearchTime only constructs
displayed times from durations per its [July 21 clarification](https://lab.odsay.com/community/boardView?seq=718),
not timetable routing; total minutes differ from Kakao/TMAP seconds and pointDistance
is not a journey. Reviewed [Naver Directions 5](https://api.ncloud-docs.com/docs/en/ai-naver-mapsdirections-driving)
was DRIVE, not a compatible substitute.

| Source / method | Current engineering use | Remaining limitation |
| --- | --- | --- |
| Kakao Map V2 WALK | Primary technical candidate for the three WALK estimates | Exact pairs untested; account, retention and adapter unresolved |
| TMAP pedestrian | Alternative WALK source, not automatic fallback | Exact pairs untested; account, retention and adapter unresolved |
| Google Matrix WALK | Keep existing blocked profile | KR coverage marked unavailable or low quality |
| Google Matrix TRANSIT | Conditional time-aware candidate only | Exact KR coverage and schedule applicability unconfirmed |
| Kakao TRANSIT / ODsay general or MaaS TRANSIT | General route references only | Do not bind the original explicit departure |
| Naver reviewed Directions API | No compatible inventory | DRIVE mode does not preserve submitted mode |

[Kakao usage/price](https://developers.kakao.com/docs/en/getting-started/quota) offered
1000 daily WALK/TRANSIT only for the first activated app; eligibility/remaining quota
were unknown. Its [operating policy](https://developers.kakao.com/terms/en/site-policies)
5(20)/5(30) did not establish immutable long-term raw retention for this evaluator.
[TMAP terms](https://openapi.sk.com/stplat/usage/indexView) were not accessible enough
to confirm retention. [ODsay conditions](https://lab.odsay.com/contact/contact) required
consultation for analysis/research;25 KRW/call plus VAT was not a purpose license.

| Mutually exclusive planning scenario | Units | Published retail reference | Selected proposal |
| --- | --- | --- | --- |
| Kakao V2 WALK | Three calls at 10 KRW | **30 KRW**, tax treatment unconfirmed | Yes, pending prerequisites |
| TMAP pedestrian Premium | Three calls at 11 KRW | 33 KRW, tax treatment unconfirmed | Alternative only |
| ODsay Flex general TRANSIT | One call at 25 KRW | 25 KRW plus VAT; purpose quote unresolved | No; not date-applicable evidence |
| Google Matrix conditional TRANSIT | One Essentials element | USD 0.005, account/taxes unknown | No; support unresolved |

These are mutually exclusive currency scenarios, not summed or approved budgets.
TMAP's [price](https://openapi.sk.com/products/calc?menuSeq=5&svcSeq=4) listed 1,000 free/day;
Google's [price](https://developers.google.com/maps/billing-and-pricing/pricing) listed
Matrix Essentials 5 USD/1000 with 10000 monthly free; neither available quota was assumed.
The non-executable draft proposed at most 3 Kakao WALK, zero TRANSIT/alternatives/Details/models/
retries, 20 seconds/request/300 seconds total and 30 KRW reference, pending account/tax/use/retention and
source-specific adapter tests. No ready source or new route evidence resulted.
Evidence: `artifacts/kr-route-support-budget-20261007/`; 136 protected files/69 code hashes
passed. No runtime suite was rerun for this documentary assessment.

<a id="sydney-offline-route-preparation-2026-10-07"></a>

## October 7: Australian preparation and development-tool boundary

The explicit AU profile at review base `c49e9819f69ce2465d43cdc5bd6d2176a35f5028`
required an original declaration such as Sydney, Australia; it did not infer country
from names/coordinates. Default/explicit KR retained exact old serialization and dated
metadata. AU profile changed inventory digest and was replay-bound. AU WALK required
current identity, independent coordinates, free span and no leg blocker; missing coordinates
could propose Details, TRANSIT stayed conditional and DRIVE unsupported. Same-canonical
N/A got no allowance. Deduplicated request budgeting retained occurrence population.
Three synthetic legs with two queries reserved two sends/USD 0.010000, not three.

The original tracked [Sydney request](../../../tools/validation/packets/sydney-v0-route-smoke/request.json)
for October 14–17, two travelers, AUD 1600 included exactly-two daily visits. It was a
preparation input, not established user intent. The later [generation stop and correction](../v0-v3/development-pilots.md#sydney-v0-generation-smoke-2026-10-07)
removed this confounding count; the original counted source/evidence remained preserved.
A September 25 five-day output lacked a reusable identity bundle and was not truncated
into an 8 venue/4 leg plan. At preparation, no new output, reviewed requirements, identity
snapshot or real route inventory existed; synthetic outputs could not fill those gaps.

Hypothetical non-generation pricing was 9 Search Pro USD 0.288, one identity USD 0.0042,
up to 8 Details USD 0.040 and four Matrix USD 0.020, total USD 0.3522. Generation cost/explicit wire caps
were not yet frozen, so no complete execution allowance existed. The identity limit
18000 input/3000 output low-effort estimated USD 0.003750 (all cache-write) or USD 0.004125 regional,
within USD 0.0042. Dated masks/rates differed from October 5 Enterprise collection;
no free quotas/pagination/retries were assumed. Actual inventories had to follow raw
output; exceeding 8 venues/4 legs stopped preparation rather than choosing a favorable subset.

Public region/CLI/dedup regressions passed 121 in 28.46 seconds; full 3017/10 in 341.21 seconds.
Implementation `6fc9a2a091f19e757c8f3ed0dcbd6345f18f3635` passed both reviews.
All 146 original/preparation files and 7 new outputs stayed intact; 67/69 code hashes
matched, with only authorized preparation/CLI changes. Evidence: `artifacts/sydney-offline-20261007/`.

The later directory-boundary migration at `0e52c28691ebd1775b254c646f13c38a4f01a500`
moved two utilities into `backend/evaluation/tools/`, retaining core scorers/legitimate
CLIs and V3's planning repair. Product/final scoring did not import development tools.
AST comparison showed only import/path/order changes in 2 modules/4 test consumers.
Focused 109 passed in 23.92 seconds; full 3017/10 in 435.91 seconds, not the earlier full receipt.
Implementation `2a2b1e1a04a052b84ff51911871486a41af307d7` passed both reviews.
Default KR library replay matched old digest/four UNKNOWNs without rebinding old code
manifests.146 protected files/7 outputs remained exact. Evidence:
`artifacts/evaluation-tools-move-20261007/`. Historical paths/hashes still describe
original revisions; current callers use `backend.evaluation.tools.route_requests`.

<a id="sydney-v0-opening-routes-smoke-2026-10-08"></a>

## October 8: Sydney component acquisition and physical follow-up

Natural V0 generation and [identity assessment](intake-identity-usage.md#sydney-v0-identity-smoke-2026-10-07)
provided a single-source diagnostic, not qualified four-version intake. Requirement
review was identity-focused and agent-origin. Reviewed IANA Sydney timezone and soft,
nonexclusive walking/public-transport preference did not introduce a default mode.
The original fourth WALK pointed to unnamed generic food; it stayed unbound instead
of becoming a fictitious venue/leg. Six adopted IDs provided saved coordinates; the
failed Australian Museum endpoint had no request under the then-canonical policy.

At `8b70852431631f32a87c2c49bd0838c2570f38b4`, bounded execution made 6 Enterprise Details
and 2 Essentials Matrix sends, all HTTP 200, zero retries in 2.551 seconds (00:44:27.270733–29.821421 UTC).
Masks were `id, businessStatus, timeZone, currentOpeningHours, regularOpeningHours` and
Matrix indices/status/condition/distance/duration. Limits 8 sends, 20 seconds HTTP/200 seconds overall,
retail USD 0.130. Two mock snapshots separately made 16 synthetic sends; they were not live
evidence. Executable preparation/adapter SHA-256:
`e29f7d9fa5bfb1ed9edb1e63c6a53879432e7b6c2c38ec5357b3ba438112d036` /
`e9546af3c32189a277e85ee79a852ade56760e77dd9ee938957f454f2e0c06d4`.
All 8 raw hashes/182 source hashes remained exact.

| Check | Result | Evidence or limitation |
| --- | --- | --- |
| MCA visit opening | PASS | Applicable current hours cover the full October 14 visit |
| QVB, Art Gallery, Mrs Macquarie's Chair opening | PASS each | Weaker regular-hours fallback for dates outside the acquisition current window |
| Opera House opening | UNKNOWN | Both hours fields absent; operational business status does not establish hours |
| Powerhouse opening | UNKNOWN | `CLOSED_TEMPORARILY`, both hours fields absent; no fabricated empty-period closure |
| Australian Museum opening | UNKNOWN, not queried | Retained identity FAIL prevents independent opening validation |
| Opera House to MCA WALK | PASS | 893 seconds / 1,108 metres against the original 20-minute interval |
| Art Gallery to Mrs Macquarie's Chair WALK | PASS | 1,083 seconds / 1,384 metres against the original 20-minute interval |
| Australian Museum to QVB route | UNKNOWN, not queried | Failed canonical endpoint remains null |

Totals 4 opening PASS/0 FAIL/3 UNKNOWN; two route PASS/0 FAIL/1 UNKNOWN among 3 primary-pair checks.
Exact-once Opera House remained UNKNOWN (one confirmed, upper 3 from failed museum and
unresolved generic), despite target identity PASS. Ten known commitment checks passed,
but 2 unresolved units/null denominator left non-overlap UNKNOWN. Main counts 2/2/2/1
and generic uncertainty were retained. [Powerhouse official inspection](https://powerhouse.com.au/visit/ultimo)
confirmed current revitalisation closure without a reopening date/literal October 17
period; it was not imported into Google hours as fabricated factual FAIL.
Twice native replay matched; quality consumer rejected `Exactly four versions required`
with `needs_material_correction`, not an overall score. Evidence:
`artifacts/sydney-v0-opening-routes-smoke-20261008-r2/` plus initial preparation.
Prior unchanged-code 3017/10 gate was reused, not rerun.

<a id="sydney-museum-follow-up-preparation-2026-10-08"></a>
<a id="sydney-museum-follow-up-execution-2026-10-08"></a>

### Incremental Museum acquisition after physical-association correction

At base `cc454bb292cbc099c823b32dc231eb6d6122c1ed`, current `versioned_api_identity_3`
kept Museum grounding FAIL/null canonical claim but verified physical ID
`ChIJlwsH0RWuEmsR3Cg3WEDw76I`, QVB `ChIJISz8NjyuEmsRFTQ9Iw7Ear8`.
Original October 15 Museum→QVB was WALK, departure `2026-10-15T01:15:00Z`, 1,200 seconds;
no conditional DRIVE adaptation was needed. Existing saved coordinates made Details
coordinate acquisition unnecessary. The full plan now had 7 Details/3 matrices; eight old
observations were reused byte/time-exact in a separate union plus 2 incremental sends.
Cumulative 10 sends and fresh 2 remained distinct.

Prepared 2 send/zero-retry/USD 0.025,20 seconds whole HTTP/60 seconds total. 69 existing public tests passed
in 29.30 seconds. Four mock scenarios preserved address FAIL while hours/route yielded PASS/PASS,
UNKNOWN/PASS, PASS/FAIL(3600 seconds) and PASS/FAIL(valid NO_ROUTE). Reviews found a P2:
the generic collector swallowed timeout and advanced, while HTTPX bounded individual
phases. One real stopping exception plus whole HTTP deadline corrected it; isolated mock
collector/HTTP timeouts each sent once, stopped and made no second request. A normal
2 request mock still completed, with receipt/raw/snapshot/native linkage verified.
The 240 protected files and prior raw sources stayed exact; no product implementation changed.

The exact approved execution at `3f608c7a76be31054cdfd18ab088eec47399c64f` used manifest
`081a118ae8adfec91e0c53c618beceecd3fe9288437261b8be3f23cdcb38001a`, adapter
`9e1af279e3ac33d4c6532fb90a52a859253071777371df95431c4c26e688a924`.
Two HTTP 200 completed in 1.046 seconds (02:38:51.344865–52.390529 UTC), zero retries,
retail USD 0.025. Raw SHA-256 Matrix/Details:
`225e6432b6093c91a28531f851b2065c4d8b5202f07cd5125c1ccb7df486f9b1` /
`a975a321e4b627e6d566060f5217b8337d0778d49cb5f11c30410a8362620ad5`.

| Native check | Result | Evidence and boundary |
| --- | --- | --- |
| Australian Museum grounding | FAIL | Original address and null canonical claim ID retained; physical association is independently verified |
| Museum opening | PASS | Regular-hours fallback covers the original October 15, 10:00-12:15 Australia/Sydney visit; no confirmed outside or unknown seconds |
| Museum to QVB WALK | PASS | 562 seconds, 678 metres; fits the original 1,200-second reservation, with zero raw deficit and no DRIVE reserve |
| Combined opening | Five PASS, zero FAIL, two UNKNOWN | Opera House and Powerhouse still lack usable opening periods |
| Combined evaluable routes | Three PASS, zero FAIL/UNKNOWN | The separate day-four transport to an unnamed generic food activity stays unbound |

Twice native replay preserved requirements/non-overlap/descriptive/occupancy sections
exactly. Opera House exact-once and full non-overlap remained UNKNOWN; main 2/2/2/1
unchanged. The V0-only quality consumer still rejected without invented companion runs.
Regular hours are weaker than current date-specific hours; time-independent WALK cannot
certify future conditions. Physical PASS did not change grounding FAIL.
All 240 frozen hashes and 8 reused byte/record/time checks passed. Evidence:
`artifacts/sydney-v0-museum-followup-20261008/`. No new full backend gate was claimed.
Missing-hours, occupancy review and qualified intake remained unresolved at this dated
checkpoint; subsequent four-version acceptance is in the identity history.
