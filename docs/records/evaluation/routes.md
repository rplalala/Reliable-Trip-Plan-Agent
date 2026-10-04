# Routes

Dated development evidence; current design and live task state remain in PROJECT.md,
core docs and GitHub Issues. Historical commands grant no new execution permission.

<a id="new-v0-route-plan-2026-10-05"></a>

## New V0 independent-route collection plan — 2026-10-05

Preparation checkpoint: **Prepared only; collection budget and execution were not yet approved.** The user
approved preparing this plan alongside offline fee accounting [#59](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/59).
Subsequent approval and bounded execution are recorded [below](#new-v0-route-execution-2026-10-05);
the frozen preparation artifacts retain their original checkpoint status.
The source is the completed structured-transport V0 smoke; no model rerun, prompt change,
retiming, endpoint substitution, mode optimization or targeted Repair is included.
This is a single-source development diagnostic, not a formal benchmark/comparison.
Review fixed point is `ff2085f6e6dafffa2b02f9b14bb10c89e49b3be8`; preparation occurred
with the approved fee changes and pending documentation in the worktree. Existing route
implementation/rules are unchanged.

### Frozen source and declarations

Original result: `artifacts/v0-transport-live-20261005/result.json`, SHA-256
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`.
Input: Seoul, 2026-10-07 through 10-10, two travelers, KRW 1,200,000; SHA-256
`07be92a51cc1db24d925e04ab16d15c15f2e501cecfd24a151ea9ee6cb6debfa`.
All times below use `Asia/Seoul` (+09:00). The original projection has four bound
transport claims, no unbound claims and no projection diagnostics.

| Date | Original endpoints / activity IDs | Mode | Claimed transport | Next visit starts | Nominal continuous time G |
| --- | --- | --- | --- | --- | --- |
| 10-07 | Gyeongbokgung Palace (`day1-gyeongbokgung`) → National Museum of Korean Contemporary History (`day1-contemporary-history-museum`) | WALK | 12:00–12:20, 20 min | 12:30 | 30 min |
| 10-08 | Bukchon Hanok Village (`day2-bukchon`) → Insadong (`day2-insadong`) | WALK | 12:00–12:25, 25 min | 12:35 | 35 min |
| 10-09 | Seoul Museum of History (`day3-seoul-museum-history`) → Gwangjang Market (`day3-gwangjang-market`) | TRANSIT | 12:00–12:35, 35 min | 12:45 | 45 min |
| 10-10 | Changdeokgung Palace (`day4-changdeokgung`) → Jongmyo Shrine (`day4-jongmyo`) | WALK | 12:00–12:20, 20 min | 12:30 | 30 min |

These G values are source schedule arithmetic before final native occupancy preparation;
they are not independently measured journey durations. The source's own transport is
excluded from competing occupancy. Protected/other commitments and unresolved occupancy
must still pass existing preparation, rather than summing disconnected gaps.

### Prepared source view and evidence protocol

Local plan owner: `artifacts/v0-route-plan-20261005/` contains `plan.json`, the
explicit single-source `diagnostic-view.json`, native `identity-plan.json` and
`route-preflight.json`. Original input/result hashes were checked, and native `project`
recomputed the V0 projection. The view reuses the previously reviewed original-input
requirements, includes only the new V0 source and declares its diagnostic scope. It is
a library preparation view, **not** a new accepted four-version batch or a replacement
for the historical manifest. No old V1-V3 result is inserted to fabricate qualification.

Native `build_identity_plan` produced **9 references / 9 search requests**. The required
Gyeongbokgung subject and its scheduled visit have different source/query contexts and
therefore are not artificially deduplicated. Native `prepare_routes` without identity
evidence returned `identity_replay_required`. No identity, coordinate or route facts have
been acquired, and all four route verdicts remain UNKNOWN.

After budget approval, execution follows the existing seams:

1. Recheck source/view/plan hashes, execution authorization, price snapshot, remaining
   budget and original frozen bytes before creating any client or sending requests.
2. Acquire the frozen identity search plan independently. Use returned names, addresses,
   canonical IDs and typed identity evidence; generated V0 IDs/locations are claims,
   not truth. Retain raw bytes/hashes and every attempt using `acquire_snapshot`.
3. Replay through `load_snapshot`, `identity_evidence` and `resolve_identities` with the
   existing audit/adjudication rules. Real required human adjudication must be supplied
   as such; automated review cannot be relabeled human. Unresolved/audit-pending IDs
   block their affected legs. Report review blockers instead of inventing adoption.
4. Preserve the original linked identity search snapshot and use
   `prepare_snapshot_coordinates`; only adopted, agreeing independent coordinates
   reach route queries. The bridge replays the exact identity plan; do not insert
   newly adopted IDs into that plan or fabricate another identity snapshot. Reusing
   older evidence requires fresh association and applicable context, not just names.
5. Prepare source-linked timezone and original-input mode-policy reviews, then use
   `prepare_routes` and freeze the exact `build_evidence_plan` output before sends.
   Its evidence phase includes at most nine adopted canonical Details requests,
   deduplicated by actual ID, alongside the four eligible route elements.
   Three WALK queries use existing time-independent options; the TRANSIT query uses
   2026-10-09 **03:00 UTC** (12:00 Seoul), explicit departure, original mode and no
   substituted date. Each requested route has one origin and one destination.
6. Acquire the bounded Details/route evidence plan, then replay the exact frozen plan with
   `score_routes`. Report each component/verdict, duration/distance, original claimed
   minutes, G, deadline tolerance, evidence limitations and actual/estimated cost.
   Preserve shortcomings as observations; no new requests seek a preferred verdict.

The iteration conversation owns preparation/adaptation and assessment. Only the prepared,
authorized execution is delegated to `smoke tests`; it must report blockers without code
changes. The ordinary route CLI expects a delivered batch; this diagnostic uses the
existing library seams with its explicitly scoped source view, not a fabricated manifest.

### Existing verdict rules and interpretation

Use `rtpeval_route_rules_1` unchanged. WALK/TRANSIT duration cap is 45 minutes plus
5-minute cap tolerance; WALK distance cap is 3,000 m with zero distance tolerance.
The schedule check uses the independently prepared continuous G, with five-minute
tolerance at the next visit and zero at a protected hard boundary. DRIVE's existing
10-minute reserve is not applicable to these four declared modes.

Matching successful evidence and all applicable components PASS yield PASS. Proven
component failure is decisive FAIL, including a valid successful no-route result.
Missing/corrupt/inapplicable mode, endpoints, date/options, unresolved identity or
incomplete duration/distance yields UNKNOWN unless another component already proves FAIL.
HTTP/provider failure is not proof that no route exists. Use exact existing precision,
source hashes and deadlines; do not add a new penalty or require evidence to fail.

The scorer checks schedule feasibility, not exact equality with the model's stated
transport duration. A provider duration longer than the claimed 20 minutes can still
fit a 30-minute G (or its existing tolerance). Record the difference descriptively
without changing the rule or hiding it. Provider representative points for villages,
shopping streets or markets do not prove a particular entrance, internal walk, waiting
time or service disruption. A matched transit estimate is evidence at the requested
context, not a guarantee of future operations.

### Proposed execution budget and stopping

Maximum **22 sends**: 9 Text Search + up to 9 Details + 4 single-element route requests.
No LLM calls, no retries, one attempt/request, 20-second request timeout and **10-minute**
overall wall limit. Reused evidence/canonical IDs may reduce sends; unused capacity
does not authorize unrelated calls. Using the preserved collection adapter's Enterprise
Places mask and Global first-paid-tier prices read 2026-10-05 gives a retail ceiling
estimate of **USD 0.515**: 9 × $0.035 + 9 × $0.020 + 4 × $0.005.
This excludes credits/free caps/tax and does not assert the eventual invoice amount.
Sources: [Global prices](https://developers.google.com/maps/billing-and-pricing/pricing),
[field-based SKUs](https://developers.google.com/maps/billing-and-pricing/sku-details) and
[route billing](https://developers.google.com/maps/documentation/routes/usage-and-billing).

Stop on authorization/source mismatch, exhausted send/time cap, authentication/billing
failure or unsupported query context. Never shift dates or add fallback modes. Unresolved
identity/coordinate/context stops only its affected leg; other eligible legs may proceed
within the approved total. Preserve partial evidence and UNKNOWNs when limits stop work.
Changing the budget, adding retries/providers or repairing V0 requires separate approval.
**This preparation made zero paid provider calls.**

<a id="new-v0-route-execution-2026-10-05"></a>

## New V0 bounded route diagnostic — 2026-10-05

Status: **Acquisition and offline replay completed; all four routes remain UNKNOWN.**
The user explicitly approved the preceding plan, including execution delegation and
result delivery through PR, under [#61](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/61).
UNKNOWN is an accepted observation for this bounded execution, not a finding that
the original V0 transport is feasible or infeasible. No evaluator rules or production
code were changed, and the original itinerary was not rerun, repaired or retimed.

The execution used revision `0f0120dc63ac25b492fd5d474c1d04826c5ab22f` on
`feature/evaluation`, with a clean tracked worktree and tree
`04684766d16cf2428cdefc2656f5e101c14b773e`, identical to delivered PR #60.
The task-specific execution packet and raw evidence were ignored local artifacts;
the subsequent tracked changes are this record and the project-status summary.
The record date uses Australia/Sydney; acquisition timestamps are retained in UTC.

### Preflight, authorization and observed acquisition

The owner prepared a task-local launcher around existing snapshot/identity/coordinate/
route APIs. It uses the preserved collector's request construction but does not invoke
its historical retrying launcher. A shared counter and deadline cover both acquisition
phases: at most 22 sends, one attempt per request, 20-second request timeout, 600 seconds
overall, no redirects/transport retries and no model client. A one-shot launch marker
prevents accidental replay of the paid collection.

Offline checks verified the 23rd-send and exhausted-wall stops, native empty-result
replay with UNKNOWN preservation, and authentication-failure stop with retained raw
attempt evidence. The three packet tests passed; the combined packet/native snapshot/
coordinate/resource suite passed **81 tests in 5.36 seconds**. These counts overlap.
Initial Ruff import/format findings were corrected before passing the final lint and
format checks. The owner verified source hashes, projection, nine-request identity
plan, original-input mode policy and preserved IANA timezone data before delegation.
Audit seed and sample count were frozen before acquisition; no human identity
adjudication was supplied or fabricated.

`smoke tests` initially encountered automatic approval review rejection before process
creation: the reviewer did not accept cross-conversation authorization for the Google
requests and possible charges. At that checkpoint there were zero sends and no launch.
The human subsequently authorized execution and owner coordination directly in that
conversation. Exactly one accepted prepared launch then completed with exit code 0.
The executor acquired evidence and reported blockers without changing production code.
The earlier blocked-dispatch evidence remains a historical checkpoint.

Observed sends were **9 Places Text Search, 0 Details, 0 Routes and 0 LLM calls**,
with **zero retries**. All nine searches returned HTTP 200 with distinct request keys.
Measured invocation through cleanup was **3.328 seconds**; the acquisition deadline
had **596.656 seconds** remaining. Unused budget did not authorize another launch.
HTTP success for these searches does not verify the uncalled Details/Routes APIs.

### Existing evaluator replay and identity blockers

All nine identity references remain unresolved, with nine human-review queue entries:
two `high_impact_review` references (the required Gyeongbokgung subject and its scheduled
visit) and seven `malformed_address_components` references. The frozen audit selected
no automatic proposal because none reached that stage. No canonical ID was adopted;
the coordinate bridge therefore produced no eligible route context and the frozen
evidence plan contained zero requests. Scoring an empty native evidence snapshot
completed with the existing `rtpeval_route_rules_1`, preserving these unknowns.

| Date / original leg | Mode | Claimed minutes | Prepared continuous G (minutes) | Independent duration / distance | Verdict |
| --- | --- | ---: | ---: | --- | --- |
| 10-07 Gyeongbokgung Palace → National Museum of Korean Contemporary History | WALK | 20 | 30 | Unavailable | UNKNOWN |
| 10-08 Bukchon Hanok Village → Insadong | WALK | 25 | 35 | Unavailable | UNKNOWN |
| 10-09 Seoul Museum of History → Gwangjang Market | TRANSIT | 35 | 45 | Unavailable | UNKNOWN |
| 10-10 Changdeokgung Palace → Jongmyo Shrine | WALK | 20 | 30 | Unavailable | UNKNOWN |

Each leg reports unresolved identity, missing route context and missing route evidence.
The mode-policy component alone is PASS because the original request does not restrict
transport modes; it is not a feasibility PASS. Independent journey times, schedule
sufficiency and transfer burden cannot be established from this acquisition.

The owner's read-only address diagnosis reproduced the seven parser rejections:

- Six reference searches (seven candidate rows, including two Seoul Museum of History
  candidates) have distinct numbered sublocality levels sharing the generic
  `sublocality` tag. The parser treats that shared tag as a unique slot and raises
  `Conflicting address components` when the component values differ, even though the
  numbered hierarchy is distinct. Individual components passed the parser checks.
- The Jongmyo candidate includes an address component without `types`; the parser
  raises `Address component requires types` before later association checks.

These are observed parser outcomes, not proof that the places are incorrect or that
V0's schedule fails. Google documents address components as repeated hierarchical
components whose types and representation can vary; see the
[Places address-component reference](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places#AddressComponent).
The inference is that the current normalization is too restrictive for these returned
structures. Fixing normalization alone would not establish identity: high-impact human
review, aliases, competing candidates and applicable audit requirements still need
their existing checks. No normalization fix or additional acquisition is included here.

### Actual-send cost, integrity and acceptance boundary

The owner rebuilt the cost report from the exact captured `oracle` usage and frozen
price context. All nine events match Places Text Search Enterprise SKU
`E967-44BC-B44D`, with the preserved search field mask. At the Global first paid tier
of **USD 35 per 1,000 requests**, the observed retail estimate is **USD 0.315**
(`9 × 0.035`); Details, Routes, models and Repair had no sends in this run.
Source: [Google Global prices](https://developers.google.com/maps/billing-and-pricing/pricing),
read **2026-10-05**. The earlier USD 0.515 is the prepared maximum retail estimate.
Actual billed amount remains absent; free allowances, credits, account tier and tax
are not inferred. This oracle acquisition is distinct from original planner/model
costs and is not allocated again to V0-V3 planner totals.

Offline assessment reloaded both snapshots against their frozen expected plans,
reproduced the identity evidence and obtained an exactly identical native route
report. The nine usage events agree with the attempt journal and snapshot ledgers;
zero retries and zero model calls were independently checked. All nine raw-response
hashes and all 15 frozen source/packet hashes matched, including the original V0
result and the protected older Seoul input/result/manifest/packet. The original
V0 SHA-256 remains `b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`.

Local evidence identifiers, not published file dependencies:
`artifacts/v0-route-execution-20261005/` contains authorization/preflight, launch,
execution/usage, attempt journal/raw hashes, identity snapshots/reports/review queue,
route preparation/evidence plan/snapshot/report, cost report, owning assessment and
address diagnostics. The earlier prepared view remains under
`artifacts/v0-route-plan-20261005/`. Raw payloads and credentials are excluded from Git.

This bounded execution can be accepted with UNKNOWN as specified in #61, but it does
not complete independent route feasibility validation. Resolving structured identity
handling and genuine required adjudication, followed by a separately authorized
route-evidence acquisition, remains future work. No formal comparison, research
conclusion or version freeze follows from this diagnostic.

<a id="v0-identity-assistance-pilot-2026-10-05"></a>

## V0-only identity-assistance pilot — 2026-10-05

Status: **Executed and owner-assessed bounded development trial** under
[Issue #63](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/63).
The user explicitly approved Issue creation and the proposed model budget after
the bounded route diagnostic above. Execution used developer revision
`90d36999ee6daec2d228b21a07e9be3f530fd83e`, with a clean tracked worktree and
task-local ignored preparation/runner/checks. Production evaluator and planner
V0-V3 code were unchanged. This is not an accepted production identity policy,
formal benchmark, human accuracy measurement, route verification or version freeze.

### Question, frozen inputs and safeguards

Test whether one model request can associate the original V0 place claims with
already acquired independent Google candidates despite name variants and restrictive
native address parsing. The original V0 result remains SHA-256
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`.
The judge input remains
`afd6ad59126bf18ffdb23cf8830228a16c842bd29fa6ec612033d6838c6a6d6d`:
nine references (eight visits and the linked required-place subject), fourteen
candidate occurrences sorted by candidate ID. Candidate text is supplied data;
the prompt excludes planner findings and version labels. Model proposals are
separate from native adopted identities and genuine human adjudication.

Authorized limits: at most one `gpt-6-luna` request, zero retries/tools/new Google
requests, 10,000 input tokens, 4,000 output tokens including reasoning, a 60-second
request timeout and five-minute total deadline. Retail-estimate budget: USD 0.01,
not a provider invoice cap. The isolated runner uses the configured Foundry v1
Responses endpoint, low reasoning effort, strict JSON output and a one-shot launch
marker. It retains failures without a repair request and checks complete unique
reference coverage and supplied candidate membership before retaining proposals.
The serialized request/schema estimate plus 1,024-token framing reserve was 5,646;
this was an estimate, while actual input usage below was provider-reported.

### Execution and per-reference assessment

`smoke tests` executed the owner-prepared package once after offline preflight.
Observed: HTTP 200, model `gpt-6-luna`, one send, zero retries, zero tools and zero
new Google sends. Request through output capture took **6.094 seconds**, not the
whole process duration. Reported usage: **4,213 input / 1,007 output / 5,220 total**,
zero cached input and zero reasoning tokens. All nine references received `match`
proposals, with unique complete coverage and only supplied candidate IDs.

Before reading the model output, the owner agent separately recorded expected
candidate selections from the existing snapshot's names and addresses. Subsequent
checking found all nine proposals consistent with those field-based assessments;
no incorrect selection or unsupported candidate ID was observed in this sample.
This is agent consistency checking, not independent human gold or an accuracy claim.

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

The model's reasons reference supplied names and Seoul/Jongno addresses. Seven
references have exact candidate names and two have name variants; two references
have multiple candidates. No live adversarial/no-supported-match population or
alternative prompt/order/model run was executed. These observations do not establish
general semantic reliability or that all current blockers require an LLM.

### Cost, validation and remaining boundary

Using [official GPT-6 Luna pricing](https://developers.openai.com/api/docs/models/gpt-6-luna)
accessed 2026-10-05, USD 0.10 input / 0.01 cached input / 0.50 output per million,
the observed-token retail estimate is **USD 0.0009248**:
`4,213 * 0.10 / 1,000,000 + 1,007 * 0.50 / 1,000,000`.
Actual Foundry invoice amount is unavailable; this evaluator-only estimate is
separate from planner, V3 Repair and prior Google acquisition costs.

Actual offline sequence: the first HTTP-boundary check failed while the runner
was absent; after implementation, pytest's default temporary/cache location was
unwritable. Using an ignored task-local temporary directory and disabling cache
allowed the first check to pass. Expanded checks initially had three failures from
misplaced HTTP-429 assertions in the test file; correcting their placement produced
**7 passed in 2.36 seconds**. These checks cover HTTP failure without retries,
duplicate launch prevention, redirects/timeouts/invalid output without follow-up,
and unobserved candidates/duplicate or missing references. Runner/check/builder
Ruff checks passed after formatting and bounded lint corrections. Owner-assessment
lint corrections likewise passed. No production/full-suite rerun was needed for
this isolated diagnostic; no model or provider calls occurred during these checks.

Owner replay verified all **61 frozen file hashes**, the captured response SHA-256
`d32064b69732271cd0d89c3aa735df162c7fad4af95ef634183eaa5bec57f00a`, actual
request/token limits, and an identical native identity replay. Original V0, earlier
Seoul evidence, Google snapshots and existing reports remained unchanged. The
native report still has nine unresolved references, **zero adopted identities**,
and the four existing route verdicts remain **UNKNOWN**. No genuine human review,
Details/coordinates, Routes duration/distance, opening validation or itinerary
optimization was added. The required-place review and audit gates remain intact.

Ignored local evidence identifier: `artifacts/v0-identity-prototype-20261005/`,
containing authorization/request/preflight, one-shot launch, raw response and its
hash, proposals, source verification, executor report, owner expectations and
`owning-assessment.json`. Raw provider/model payloads, credentials and temporary
checks are excluded from Git; these identifiers are not fresh-checkout dependencies.

The bounded trial supports proposing a V0-only integration, with explicit model
provenance and residual uncertainty. Production address compatibility, proposal
adoption and mandatory genuine human/audit review still need an approved design.
Independent route acquisition requires its own prepared budget and approval after
sufficient endpoint identities are adopted. No additional live request is authorized
by this record. Issue lifecycle and Git delivery remain distinct from these results.

<a id="v0-adoption-design-preparation-2026-10-05"></a>

## V0 adoption design preparation — 2026-10-05

Status: **Proposed; preparation approved, policy implementation and acquisition pending.**
The user approved creating two follow-ups and preparing their plans.
[Issue #67](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/67) owns
the adoption specification and acceptance; [#66](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/66)
owns the new short-reference response validation. Offline design/implementation
can proceed independently of that live run; adoption of its new response requires
its validation. Closed #63/#64 retain their original completed scopes.

Preparation revision: `def635c7914ce5ca6ddc73c604110e75abfc9c8b` on
`feature/evaluation`, initially clean. Only planning documentation and ignored
offline receipts change at this checkpoint. This record does not replace the
current independent identity contract or introduce an operational model caller.

### Existing obstacle and recommended seam

Observed baseline: the prior model suggested nine matches, while native identity
resolution adopted zero. Two references require high-impact review; seven had
malformed typed-address diagnostics. A shorter ID solves the copying boundary,
not adoption or coordinates. The current coordinate bridge also verifies the
native policy and recomputed report; passing a proposal or relabeling a model as
human would not be a valid extension.

The recommendation is a default-off, separately versioned V0 model-assisted
association policy. Keep native accepted associations and genuine human decisions
first. For unresolved ordinary visits, let the model match the structured V0 claim
against frozen independent candidates using name/location/address evidence. The
program checks exact references, per-reference ownership, hash linkage and actual
allowlisted evidence fields rather than interpreting rationale prose or adding
title/fuzzy-name rules. A valid match remains fallible; no model confidence cutoff
or additional judge is proposed.

Adopt eligible ordinary matches through an explicit `model_assisted` path after
review/audit gates. Keep REQUIRED/EXCLUDED/fixed-time subjects and their high-impact
possible visit matches subject to genuine review. The positive-count, predeclared
audit must also cover model-assisted automatic proposals; sampled cases remain
pending review. In this source, the required Gyeongbokgung subject and its visit
therefore remain review-required, and the audit may block other visits. Approval
of this proposed integration alone would not establish all four route endpoints.

This alternative association policy deliberately permits independently supported
name variants or candidate choice that the default exact-name rule cannot accept.
It leaves the shared policy and V1-V3 unchanged. Optional malformed address
components remain diagnosed and cannot be cited as verified typed facts; valid
independent name/formatted-address fields can support the separate model-assisted
path. Original snapshots are immutable and no synthetic components are introduced.
Unsupported matches preserve UNKNOWN; a missing match is not proof of fabrication.

Hash-bind source/intake/reference population, independent observations, complete
judging instructions/schema/map/response and audit inputs. Extend downstream replay
validation explicitly for this policy; do not replace a policy string to bypass
the current bridge. TDD must cover human precedence, high-impact/audit pending,
wrong/stale/foreign identities and missing cited fields, plus default/V1-V3
invariance. Implementation and tests must be committed before Standards/Spec review.
Score formulas and masks remain unchanged; the report must expose the association
policy and evidence when availability changes.

### Independent route handoff and preparation checks

The four original directed legs/modes/time windows remain exactly those in the
[frozen source table](#new-v0-route-plan-2026-10-05). Acquire new independent Details
only for adopted endpoint IDs, checking requested/returned identity and contradictions,
numeric coordinates and snapshot linkage. Never use model/planner coordinates.
Deduplication by exact adopted venue would allow at most **eight Details plus four
Routes requests** if every endpoint cleared its gates. This is a planning upper
bound, not an approved budget; pending reviews or unsupported modes reduce eligibility.
Freeze actual eligible requests, field masks/SKUs, dated official prices, timeouts,
total deadline and stop conditions before separate acquisition approval.

Use native route preparation/scoring with the original WALK/TRANSIT, direction
and temporal context. Preserve provider limitations as UNKNOWN; do not switch modes,
retime, rerun or optimize V0. Report independent duration, original claimed duration,
available continuous window, rule/margin and evidence limitations separately. An
incorrect time estimate alone is distinct from an infeasible itinerary. Model
matching is not evidence of opening hours or journey duration.

The offline preparation check passed on its first run: all **61** original
pilot-authorized files retained their hashes, the original V0 hash remained
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`,
and nine prior proposals were exactly restored through the new map. The check made
no model/provider requests and added no adopted identity or route evidence.
Local evidence identifier: `artifacts/followup-plans-20261005/offline-preflight.json`;
the linked Issues contain self-contained public plans, not local-file dependencies.
Current observed status stays **zero adopted identities; four UNKNOWN routes**.

<a id="snapshot-coordinate-bridge-2026-10-03"></a>

## Snapshot-coordinate bridge — 2026-10-03

Review fixed point: e8e75b01307fc5ecc39910262249a4cceb5dbaea on feature/evaluation;
the starting tracked tree was clean. The user adopted the preceding audit recommendation,
authorizing a bounded offline coordinate bridge, relevant tests, local commits, dual-axis
review/corrections and related documentation. No live acquisition or publication is included.
Current behavior is owned by the [opening/route contract](../../contracts/0004-opening-routes.md#accepted-snapshot-coordinate-extension-2026-10-03).

### Reproduction and implemented boundary

The audit's three public probes showed 8 resolved visits but no route query context without
a separate coordinate envelope. Preparing already-saved coordinates yielded 1 V0 context
without any additional send. Existing relevant tests passed 48 cases (67 unrelated cases
deselected). These fixtures establish a missing preparation bridge, not live coverage or
a scoring defect. Source/raw preservation and manual route preparation already worked.

`prepare_snapshot_coordinates` now replays an identity-phase snapshot, recomputes its intake
plan and verifies derived evidence against the adopted identity report. Only exact adopted
IDs contribute coordinates. Its immutable `rtpeval_snapshot_coordinates_1` output preserves
manifest/plan/intake/identity hashes and each request/raw hash, candidate pointer and retrieval
time. It declares independent_snapshot provenance without inventing human review metadata.
Finite/ranged agreeing coordinates are usable; missing, malformed or contradictory points
remain local diagnostics, retaining candidate populations. Foreign/corrupt/stale sources
reject preparation atomically. Unresolved identities stay unresolved.

Route prepare/score and the final quality-report API/CLI accept optional
identity_snapshot_directory / --identity-snapshot. Existing reviewed --coordinates remains
supported; selecting both sources is rejected. Automatic extraction uses existing default
query options. Manual and automatic evidence digests differ, so replay uses the corresponding
prepared query plan rather than borrowing an old query. Planner runtime, budgets, provider
field masks, acquisition policy, source IDs and final score/mask rules remain unchanged.

### Actual development validation

1. Initial test setup could not create a nested basetemp because its parent did not exist.
   Creating only the ignored task artifact parent enabled the actual red test.
2. Snapshot-to-route preparation initially failed at the missing keyword interface, then
   passed with linked extraction. Four malformed-coordinate cases then failed; local
   invalid diagnostics fixed them without dropping the unaffected place.
3. Conflicting repeated coordinates incorrectly produced a query; the regression failed,
   then passed after exact agreement checks. Matching duplicates remained accepted.
4. Route CLI, route scoring, quality-report API and quality CLI each failed at the missing
   interface before being connected. A scoring fixture initially omitted independent mode
   review and therefore produced UNKNOWN; supplying its existing review made the intended
   PASS assertion valid without a production scoring change.
5. Additional public checks cover corruption/linkage, absent coordinates, paired optional
   tracks, Search/Details agreement, source-only provenance, competing source inputs,
   unadopted IDs, unresolved identities, deterministic no-socket replay and unchanged bytes.
   A huge out-of-range integer exposed OverflowError in the finite-number check; checking
   range first fixed the reproduction and retained local coordinate uncertainty.
6. Complete evaluator regression: 527 passed, 1 Windows symlink-privilege skip in 85.14s.
   All 25 new cases participate; existing reviewed-coordinate/quality behavior remains
   covered. Ruff and six-file format checks pass; no static typechecker is configured.

Complete backend gate: 2356 passed, 10 skipped in 198.85s, no deselections. Nine opt-in
PostgreSQL tests and one Windows symlink privilege test were skipped; no database supplement
or native elevation was run. Implementation and direct tests were committed before review:
f07b495 — feat: prepare route coordinates from independent snapshots.

Standards review reported 0 hard violations and 0 actionable smells. Spec review found one P2:
Search `places: null` was unavailable in converted identity evidence but raw coordinate
iteration raised TypeError, wrongly rejecting the whole batch even with valid Details.
The public route-preparation regression first failed (1 failed / 25 deselected), then passed
after filtering requests by the existing converted observation status. Valid Details and
other places remain usable; malformed Search evidence remains in the original snapshot.
All 26 coordinate tests passed in 2.69s. Separate correction commit:
5ddf9ae — fix: retain usable coordinates beside malformed search evidence.
Both axes rechecked this committed correction: Standards 0 new findings; Spec P2 closed,
0 new findings. The final evaluator gate passed 528 tests with 1 Windows symlink-privilege
skip in 65.70s. Ruff/format and diff checks passed. The earlier full-backend result above
precedes this bounded correction; the full backend was not repeated after it.

Initial patch inspection found a duplicated contract section after a patch retry; it was
deduplicated before final document validation. No ignored file is a published dependency.

### Remaining limits

Only linked identity-phase snapshots are read. Old snapshots may omit coordinates; no
automatic backfill or follow-up request is made. Independent acquisition still uses a
caller-owned injected transport; no built-in operational Google client is supplied.
Coordinates prove correspondence to observed evidence, not factual perfection or future
route guarantees. Close agreeing-but-different coordinates remain explicitly conflicting,
without an unapproved tolerance policy. Manual reviewed coordinates remain an alternative.
No formal comparison, database/model/provider live call, Ticket 10 implementation, Issue
mutation, push or freeze is claimed by this extension.

<a id="rtpeval-ticket-07-acceptance"></a>

<a id="rtpeval-ticket-07-acceptance--ticket-07-offline-same-day-route-acceptance"></a>

## Ticket 07 offline same-day route acceptance

Date: 2026-10-02, Australia/Sydney. Base revision:
`3427784b87d5864aba25dcba8b48430ec4de9dac` on `feature/evaluation`, plus the
uncommitted approved preflight, implementation, tests and documentation.
Status: Implemented and offline-validated; both review axes are clear. The original
existing-test exception below was subsequently resolved under separate user-approved
repair scope: latest unfiltered gate 2234 passed / 10 skipped / zero deselections.
See the supplemental repair section; original checkpoint results remain historical.
Implementation and the independent test repair are committed locally under the
subsequently approved three-group closeout below. All changes remain unpublished;
this acceptance belongs to the approved documentation group. No freeze is implied.

<a id="rtpeval-ticket-07-acceptance--authority-and-scope"></a>

### Authority and scope

[PROJECT](../../../PROJECT.md), the [approved preflight](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19#issuecomment-5955699412),
[route contract](../../contracts/0004-opening-routes.md#rtpeval-route-contract), [time contract](../../contracts/0001-evaluation-artifacts.md#rtpeval-evidence-time-contract),
[snapshot contract](../../contracts/0002-intake-identity-usage.md#rtpeval-snapshot-contract) and [metrics contract](../../contracts/0005-quality-human-review.md#rtpeval-metrics-contract)
own the approved offline behavior. GitHub [#19](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/19)
owns live task state; [#12](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/12)
owns overall progress. Historical local ticket/import statements remain dated history.

The user approved preparation/scoring/local CLI, synthetic TDD, relevant and full offline
regressions, Standards/Spec review and corrections, and related docs/archive/Issue updates.
No provider/model/database live call, formal case, experiment, auxiliary total, V3 delta,
commit/push, branch switch, freeze or later-ticket implementation was included.
V0-V3 planner behavior and independent entry points are unchanged.

<a id="rtpeval-ticket-07-acceptance--implemented-behavior-and-interfaces"></a>

### Implemented behavior and interfaces

`backend.evaluation.routes` exposes immutable public `prepare_routes` and `score_routes`
results with independent `to_dict()` copies. `backend.evaluation.route_cli` exposes local
JSON `prepare`/`score` commands. Exit 0 includes quality FAIL/UNKNOWN; exit 2 identifies
material correction/identity replay without a partial cohort. Inputs are never rewritten.
The [package guide](../../../backend/evaluation/README.md#ticket-07-offline-same-day-routes)
owns signatures, new route review/coordinate formats and query defaults.

- Preserve same-day consecutive primary occurrences, independent canonical identities
  and version-selected transport: V0 Activity, V1-V3 Transfer, no ignored-source fallback.
  Inter-day legs are excluded; confirmed same-canonical transitions are N/A. Repeated
  occurrences stay separate even when acquisition requests are deduplicated.
- Prepare occupancy, reviewed Input mode restrictions and independently reviewed coordinates
  without route observations. Extract only neutral Ticket 05 validators into
  `_schedule_preparation.py`; keep existing obligation wire/policies unchanged.
- Honor explicit departure. Otherwise allow waiting, select the longest continuous free
  fragment and break ties by earliest UTC start before seeing provider outcomes. Do not
  concatenate gaps, seek a better departure after failure or silently switch modes.
- Applicable non-travel/fixed occupancy deadlines have zero grace. The separate 300-second
  schedule tolerance applies only to the next visit. DRIVE reserve is 600 seconds once;
  cap tolerance is independently 300 seconds, with no WALK distance tolerance. Shared
  `_route_rules.py` constants drive both arithmetic and reported rules/hash.
- Preserve uncertainty locally: known disjoint alternative occupancies do not contaminate
  another leg. A guaranteed common occupation starting at its deadline is a hard boundary;
  a merely possible boundary cannot borrow the next-visit tolerance and stays UNKNOWN.
- Verify raw snapshot integrity and entire identity/occurrence/request/paired linkage.
  Foreign or corrupt material yields no partial cohort; valid inapplicable mode, departure,
  coordinate or option context is UNKNOWN. Deliberate time-independent WALK/basic DRIVE
  and applicable explicit departure contexts stay distinguishable without date shifts.
- Independently parse raw element status/condition and nanosecond duration. Accept valid
  traffic-calculation fallback; explicit no-route FAILs without invented duration.
  Missing WALK distance/duration remains UNKNOWN for that component. Any independently
  proved component FAIL is decisive; all required components must PASS for combined PASS.
- Report components, raw overruns/deficits, source/query/attempt/hash provenance, separate
  structural/response/full-component/decisive/duration coverage and conditional P/(P+F).
  Partial decisive FAIL is not complete evidence. Unknown travel stays null, never zero.
  Daily/request duration sum/median/max are observed subtotals with missing and unresolved
  population counts; reserve stays separate. Unresolved potential legs suppress relevant
  full-scope rates and complete burden claims without discarding observed measurements.

<a id="rtpeval-ticket-07-acceptance--actual-development-and-correction-sequence"></a>

### Actual development and correction sequence

Public preparation/scorer/CLI seams drove synthetic tests. No third-party network was used.
Initial tracer tests were RED for missing modules, then implemented. A default temporary
directory attempt emitted setup errors without a retained complete result; no count or
cause is inferred. Subsequent runs use explicit repository-local `--basetemp`.

1. Neutral validator extraction initially omitted `OBLIGATION_FIELDS`: **27 failed /
   39 passed**, then the import correction yielded **66 passed** across new baseline and
   existing requirement/schedule tests. No Ticket 05 policy change was made.
2. Malformed status message: **1 failed / 21 passed**, corrected to **22 passed**.
   Expanded context tests exposed a fixture carrying modified source state between builds:
   **1 failed / 39 passed**; each build now restores its original source results, and the
   combined subset passed **41 tests**. This fixture correction does not change production.
3. Unresolved adjacency: **1 failed / 44 passed**, corrected to **45 passed**. Missing
   tolerance classification and non-string clock handling produced two RED cases;
   corrections yielded **48 passed**. Further route cases passed **63 tests**.
4. Expanded local CLI and evaluation regression: **392 passed / 1 skipped**. First full
   backend gate before review corrections: **2221 passed / 10 skipped in 158.36s**.
5. Spec review regressions for disjoint alternatives and unresolved population burden:
   **2 failed / 1 passed**, corrected to **3 passed**. Added applicability, provenance,
   precision and repeated-occurrence cases yielded **84 route/CLI tests passed**.
   The intermediate full backend run passed **2232 / 10 skipped in 200.72s**.
6. Follow-up Spec review found possible occupancy starting exactly at a deadline could
   borrow the 300-second tolerance. Both new boundary cases were RED (**2 failed**).
   Guaranteed-boundary/possible-boundary handling corrected them. Final route/CLI subset:
   **86 passed in 20.35s**. Common 10:30 occupation gives FAIL with a raw 120-second deficit;
   alternatives at 10:30/10:35 give UNKNOWN, never a fabricated free interval.
7. A subsequent bare `python` invocation selected host Python 3.13 without pytest and ran
   no tests. Verification immediately used the existing project `.venv` Python 3.12;
   dependencies and host settings were not changed.

The first post-boundary full run stopped making progress in the unchanged
`test_httpx2_embedding_timeout_and_cancel_close_owned_client` cases. Independent execution
also failed to complete; a 10-second faulthandler dump shows the test's asyncio run waiting.
Only these verified test processes were stopped, with exact PID/command identity checks.
The original test has an unbounded `entered.wait()` alongside a 20ms timeout. A handshake
timing race is a hypothesis, not a confirmed runtime diagnosis. No Retrieval code, test
assertion or product budget was changed. Earlier complete full runs passed these cases.

Final broad backend result: **2232 passed / 10 skipped / 2 deselected in 186.17s** after
the boundary correction, explicitly deselecting both parameters of that existing test.
This is a documented validation exception, not a claim that the final workspace passed
every backend test. The earlier unfiltered run was **2232 passed / 10 skipped in 200.72s**
before the last two new boundary tests/fix; these counts must not be merged. Remaining
tests are unchanged. A subsequent English/document link check found **165 existing local
Markdown targets**; AST comparison confirmed all **eight extracted definitions unchanged**.
Backend-wide Ruff, evaluation compilation, route CLI help and diff checks
passed. Incidental formatter changes to unchanged baseline files were removed.

All full-suite checkpoints deliberately set `TRIPWORLD_TEST_DATABASE=0`. Their ten skips
are nine opt-in PostgreSQL integration tests and one host symlink-privilege case. Earlier
Ticket 06 database/UAC supplements do not count as Ticket 07 verification. No new live,
database or elevated-native execution was performed or inferred from prior permissions.

<a id="rtpeval-ticket-07-acceptance--review-axes"></a>

### Review axes

**Standards:** no documented-standard breach. One initial nonblocking duplicated-rule
smell was corrected by centralizing caps, tolerances, reserve and query defaults.
Follow-up review found no remaining Standards issue.

**Spec:** two initial P2 findings (disjoint alternative poisoning and incomplete-population
burden) plus one follow-up P2 deadline-boundary finding were fixed with public regressions.
Final read-only follow-up confirmed all three resolved, with no remaining actionable
Spec issue or scope expansion. Tests are reported by the primary agent, not by reviewers.

<a id="rtpeval-ticket-07-acceptance--evidence-and-remaining-limits"></a>

### Evidence and remaining limits

Ignored local evidence: `thesis_notes/evaluation/ticket-07-validation/` contains separate
pre-review, post-initial-review, interrupted and final broad-regression logs. The local research record
`thesis_notes/evaluation/2026-10-02-ticket-07-implementation.md` preserves development
decisions and failures; neither is a fresh-checkout dependency or project authority.

Synthetic response/coordinate/review fixtures verify engineering behavior, not real
provider availability or coordinate facts. External mode/coordinate review is a supplied
trust boundary; unknown facts remain visible. No formal evaluation, historical/future
travel guarantee, cross-version ranking or version-level retrospective is claimed.
Ticket 08 report/auxiliary-score work requires its own approved preflight/scope.

<a id="rtpeval-ticket-07-acceptance--tracker-closeout"></a>

### Tracker closeout

Issue #19 was updated/read back as closed/completed with all five current acceptance
checks complete, actual validation exception and local/unpublished boundary. Parent #12
was updated/read back as open with 01-07 complete and later tickets unchanged. Imported
ticket/preflight/commit history was preserved. No new Issue, comment, assignment or label
was created. Research evidence remains ignored; no Git staging or commit was performed.

<a id="rtpeval-ticket-07-acceptance--final-workspace-checks"></a>

### Final workspace checks

All six generated Ticket 07 test/diagnostic roots were removed after their processes
ended and four archived regression logs were verified. Final English/local-link check:
**167 existing targets**. Index remains empty; HEAD remains 3427784b on feature/evaluation.
The actual content diff contains only approved Ticket 07 files. Four unchanged baseline
files touched by the formatter show checkout line-ending status entries but have zero
content diff against HEAD; they are not implementation changes or staged content.

<a id="rtpeval-ticket-07-acceptance--subsequent-diagnosis--2026-10-02"></a>

### Subsequent diagnosis — 2026-10-02

After Ticket 07 closeout, the user separately authorized diagnosis of the existing
embedding timeout-test hang. The [record](../v0-v3/v2-embedding-timeout.md#timeout-test-diagnosis-diagnosis) confirms
that SDK cold request preparation can outlast 20ms, leaving the test waiting forever for
a handler event after the embedding task already timed out. A bounded test-only candidate
passed both parameters in memory; no source repair/full-suite retest is yet authorized or
claimed. The Ticket 07 actual skip/deselection checkpoint above remains unchanged.

<a id="rtpeval-ticket-07-acceptance--approved-timeout-test-repair-supplement--2026-10-02"></a>

### Approved timeout-test repair supplement — 2026-10-02

The user subsequently approved applying the concrete test-only patch and targeted/full
offline validation. [Repair acceptance](../v0-v3/v2-embedding-timeout.md#timeout-test-diagnosis-repair-acceptance)
records one affected test function changed, direct timeout observation, bounded cancel
handshake/scenario and child cleanup, with a five-second synthetic deadline and original
assertions retained. Production Retrieval, usage hooks and runtime config are unchanged.

Actual-source feedback loop: pre-fix 1 failed/1 passed/14 deselected in 15.76s, post-fix
2 passed/14 deselected in 8.24s. Both parameters pass alone in separate cold processes;
all 16 module tests pass. Standards and Spec each report zero findings. The new unfiltered
full offline backend gate is **2234 passed / 10 skipped in 196.39s, zero deselections**.
Both formerly excluded parameters now participate and pass. Database/native skips are
not supplemented. Earlier numbers are distinct historical runs, not retroactive passes.
No provider/model/database live call, formal experiment, Git action, freeze or Ticket 08.

<a id="rtpeval-ticket-07-acceptance--approved-local-git-closeout--2026-10-02"></a>

### Approved local Git closeout — 2026-10-02

The user explicitly approved finishing Ticket 07 with the previously proposed three
local groups. This later approval supersedes only the earlier no-commit boundary;
push, branch switching, live/database/native supplements, freezes and Ticket 08 remain
outside scope. No executable correction was made during Git closeout.

1. **2b66c9f889ca8964f97dbc67b2a601ebb56be64c** —
   `feat: evaluate same-day routes from frozen evidence`.
   Seven new route/preparation modules, neutral validator extraction in the existing
   requirement/schedule module, and the two directly related test modules; ten files.
2. **b18daef4af2fecba36d7b84315c8946a772aeae8** —
   `test: bound embedding timeout and cancellation checks`.
   Only the independently approved existing test function; one file.
3. Approved documentation group — `docs: record route validation and local closeout`.
   Current route/metrics contracts, preflight/acceptance, permanent diagnosis/proposal/
   repair records, PROJECT, documentation index/glossary and package guide. The commit
   containing this entry supplies its own revision through Git history; ignored archive
   probes/logs, credentials, raw payloads and generated pytest files are excluded.

Pre-commit offline check: route tests, CLI tests, shared requirement/schedule tests and
the runtime retrieval module passed **166 tests in 34.26s**. Backend Ruff and diff checks
passed. The full unfiltered **2234 passed / 10 skipped / zero deselections** gate remains
the earlier actual run; it was not rerun or supplemented, and no code changed afterward.
The ten skips remain nine opt-in database cases and one host symlink privilege case.
Earlier filtered gates and red/correction/retest sequences remain dated history.
Four baseline files with zero normalized content diff require only index-stat refresh;
they contribute no staged content or commit changes. Generated closeout pytest files
are removed after process completion. No version freeze or later ticket is implied.
Closeout documentation check: English content and **180 existing local Markdown
targets** across ten documents passed. The permanent historical proposal passes
reverse-apply validation against the committed repair. Its unified-diff context markers
are preserved as patch syntax; they are not ordinary prose whitespace.
