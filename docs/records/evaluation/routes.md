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

<a id="v0-adoption-specification-finalization-2026-10-05"></a>

## V0 adoption specification finalization — 2026-10-05

Status: **Specified; implementation and acquisition not yet approved.** The user
approved finalizing [parent #67](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/67)
and publishing implementation slices. The first is
[offline identity adoption #69](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/69);
the second is [route request preparation #70](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/70).
GitHub native sub-issue links attach both to #67; a native blocking dependency
makes #70 wait for #69. All three remain open. The preceding Proposed record is
historical; the finalized specification and ticket acceptance live in GitHub.

Inspected revision: `1326970a2aff91248761a16290288d3cd62a2a67` on
`feature/evaluation`. An unrelated untracked `.archify/` directory was present
and excluded; an unrelated `.gitignore` change appeared during planning and was
also excluded. This checkpoint changes planning records and project status only,
with ignored tracker drafts/receipts; no implementation or runtime policy changed.

Observed during targeted inspection: identity readiness and evidence-plan
preparation currently require the native association policy. A proposal cannot
become an accepted downstream report merely by replacing its policy stamp. The
first slice therefore includes explicit replay-aware consumer validation along
with offline adoption. The second consumes that handoff to prepare actual Details
and conditional/ready directed route requests. Neither slice includes live collection.

The saved #66 response cites claim fields and independent candidate name/address
fields, including raw address components. The earlier seven ordinary-reference
diagnostics report `Conflicting address components`, with no shape-invalid items
listed in their diagnostic examples. The native comparator requires one consistent
value set per address type; repeated provider types can violate that comparison
rule. The accepted specification distinguishes this comparison limitation from
invalid wire shapes. The new policy will validate field presence/types and preserve
diagnostics without giving the native comparator another semantic veto; it will
not declare cited raw geography programmatically verified. Structurally invalid
cited fields remain ineligible, and historical snapshots/citations cannot be repaired
to force adoption. This is a specified boundary, not a validated accuracy claim.

The audit seed/count were already included in the saved #63 authorization and
#66 frozen packet. Implementation must verify that linkage and pre-response freeze,
not retrospectively choose a favorable audit. Genuine human decisions, high-impact
review and selected audits retain precedence. Actual adoption and eligible-leg counts
may remain partial; ticket acceptance does not require nine adoptions or four PASS results.

Checks at this planning checkpoint: parent/child bodies were read back exactly,
existing labels and native relationships verified, original V0 and the 61 pilot
source hashes checked, and tracked documentation links/whitespace checked. No
implementation tests or new model/Google calls were run. Local evidence identifiers:
`artifacts/short-id-live-20261005/packet/live/execution.json`,
`artifacts/v0-route-execution-20261005/address-diagnostics.json` and
`artifacts/v0-identity-prototype-20261005/authorization.json`.
Current observed state remains **zero adopted identities; four UNKNOWN routes**.

<a id="v0-identity-adoption-acceptance-2026-10-05"></a>

## V0 offline identity adoption acceptance — 2026-10-05

Status: **Implemented and offline validated; Git delivery pending.** The user explicitly
authorized [#69](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/69) through
`implement`, after specification finalization. This authorization covers offline adoption,
consumer handoff, tests, local commits, review and related documentation; it does not cover
[#70](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/70), new live calls or Git
publication. Parent #67 and both children remain open at this local checkpoint.

Review fixed point: `5449afc5ef7b5fede61d564cf66b6e0f36d39be8` on `feature/evaluation`.
Implementation/tests were committed before review as `6055905` (`feat: adopt V0 identity
proposals through offline replay (#69)`). Review corrections are separately retained in
`481d531` (`fix: preserve native decisions and exact audit chronology (#69)`). An unrelated
pre-existing `.gitignore` change remains excluded. Ignored sources/new derived artifacts
are local evidence, not fresh-clone dependencies; raw payloads were not force-added.
The [identity contract](../../contracts/0002-intake-identity-usage.md#v0-only-model-assisted-offline-adoption)
owns current policy; this dated record preserves observed validation.

### Implemented boundary and actual replay

The explicit resolver and CLI replay original V0 input/result/provenance/projection,
independent snapshot, saved judge request/schema, short-reference map and actual #66
response. Candidate facts are matched by exact canonical ID rather than provider ordering.
Saved raw partial/repeated address components retain their wire facts and native diagnosis;
no components/citations are invented or stripped. Allowlisted field presence/types and
independent name/address support gate model adoption without a rationale/title classifier.
Consumers recompute the whole bound report before identity readiness, coordinate extraction
and evidence/route preparation. Changed IDs, policy labels or audit/review state are rejected.
Default/native and V1-V3 paths, score/mask formulas and all planner entry points are unchanged.

Actual replay has nine references: **six adopted, three review-pending, zero
unknown/ineligible**. No genuine human decisions were fabricated. The saved historical
audit seed/count were retained; its authorized packet and exact send/response binding were
verified. Local receipts are supplied evidence, not cryptographic certification of time or
reviewer identity. Six existing independent snapshot coordinates passed the native bridge,
with zero diagnostics; native route preparation produced two query contexts.

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

| Date | Directed endpoints | Mode | Declared / nominal gap minutes | Identity/context result | Route feasibility |
| --- | --- | --- | --- | --- | --- |
| 2026-10-07 | Gyeongbokgung -> National Museum of Korean Contemporary History | WALK | 20 / 30 | Blocked by origin high-impact review | UNKNOWN |
| 2026-10-08 | Bukchon Hanok Village -> Insadong | WALK | 25 / 35 | Both adopted; verified saved coordinates; query context prepared | UNKNOWN |
| 2026-10-09 | Seoul Museum of History -> Gwangjang Market | TRANSIT | 35 / 45 | Both adopted; verified saved coordinates; query context prepared | UNKNOWN |
| 2026-10-10 | Changdeokgung -> Jongmyo | WALK | 20 / 30 | Blocked by destination audit review | UNKNOWN |

No new journey observations or route feasibility score were produced. UNKNOWN describes
the unchanged absence of independent route evidence, not a newly measured journey result.
The original itinerary was preserved, including its estimated durations and nominal gaps.
Issue #70 still must prepare concrete requests, budget and conditional dependencies; these
two contexts alone do not authorize or define live collection.

Original V0 SHA-256 remains
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`.
All 61 protected historical pilot hashes are unchanged. This task made **zero model,
Places or Routes sends**, adding no charges for those APIs and fetching no bill. Existing
historical usage/cost records remain unchanged. Local evidence identifiers are
`artifacts/v0-identity-adoption-20261005/{material.json,identity-report.json,coordinate-preparation.json,route-preparation.json,offline-acceptance.json,execution-report.md}`.
The bundle and its source files must remain locally available for consumer replay.

### Development failures, corrections and checks

1. Public-boundary TDD began with a missing resolver/import gate. Windows global-temp
   permissions required task-local pytest temp/cache directories; fixture transport had
   to match the existing async acquisition interface and snapshot filename convention.
2. Actual saved-material replay exposed candidate ordering and historical provenance
   compatibility. Match complete candidate facts by exact ID, verify original provenance
   independently, and retain the original historical freeze's actual source population.
   Existing SDK wire hashes use their saved JSON serialization, distinct from compact
   RTPEval digests. UTC send dates use the declared Sydney authorization timezone.
3. Raw partial address components initially left one proposal ineligible. The accepted
   wire policy allows absent optional provider types, preserves raw fields and rejects
   malformed cited types; no synthetic components or semantic comparator veto were added.
   Actual replay then became six adopted/three pending. Initial expectations about missing
   coordinates were corrected after inspecting the saved independent snapshot: it already
   contains six valid adopted-venue coordinates, yielding two contexts without Details calls.
4. Consumer regressions exposed a substituted native policy stamp and malformed native
   `records` handling. Structured assistance markers require replay even when relabeled;
   malformed native reports retain the existing replay-required result. Response provenance
   and unexpected tool output are checked. Provider timestamp skew cannot substitute for
   the saved authorized preflight/send binding.
5. First full backend gate: **2745 passed, 10 skipped, 1 failed in 336.65s**. The evaluator
   dependency guard rejected new framework/typing dependencies. The guard was retained;
   strict saved-schema validation now uses only permitted standard-library imports.
   Related retest: **382 passed, 1 skipped**; the corrected full run passed **2747 with
   10 skips in 357.18s**, before subsequent review regressions.
6. Initial Standards review: zero findings. Initial Spec review: two findings—precise
   authorization timestamps were reduced to dates, and missing model freeze downgraded
   accepted native decisions. Three regression cases reproduced the errors. The separate
   correction commit compares offset-aware precise timestamps and retains native decisions/
   audit selection when model freeze is absent. Additional cases cover naive timestamps
   and valid earlier authorization. Related retest: **388 passed, 1 skipped in 38.18s**;
   the adoption suite now contains **47 cases**. Both review rechecks have zero findings.
7. Actual module CLI replay returns exit 3 and exactly the saved identity report. The first
   subprocess used Windows GBK and failed on Korean output; the documented UTF-8 environment
   setting produced valid JSON without changing production behavior. Ruff passes. Final
   full backend validation after review corrections: **2752 passed, 10 skipped in 250.11s**.
   The skips are existing environment/opt-in cases. Tracked link/anchor and whitespace
   checks passed; the final documentation/acceptance commit is separate from implementation
   and review corrections.

These are implementation checks over one saved development sample, not formal accuracy,
human gold, a version freeze or evidence that any journey is feasible. Genuine high-impact
and audit review remains the blocker for three references; collecting independent route
evidence remains separate from matching and preparation.

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


<a id="v0-route-request-preparation-2026-10-05"></a>

## V0 independent route request and budget preparation — 2026-10-05

Issue #69 was merged through PR #71 at merge commit `5d21d6b4685c7793f27954d7c175bed9524b3803`.
Issue #70 is implemented locally for offline preparation only; Git publication and live execution remain unapproved.
Review base: `f011a2929f9235f30a546f872f3a879cd6aaeed6`.

The unchanged saved V0/#66 material replays six adopted identities and three genuine-review-pending references.
All four original legs remain UNKNOWN. Native occupancy, continuous windows, mode, original estimate and timing remain in the JSON package.

| Date | Directed endpoints | Mode | Original estimate / nominal gap (min) | Identity / coordinates | Request state | Reasons |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-07 | Gyeongbokgung Palace -> National Museum of Korean Contemporary History | WALK | 20 / 30 | False / False | blocked | identity_unresolved, regional_walk_unavailable_or_low_quality, independent_coordinates_missing |
| 2026-10-08 | Bukchon Hanok Village -> Insadong | WALK | 25 / 35 | True / True | blocked | regional_walk_unavailable_or_low_quality |
| 2026-10-09 | Seoul Museum of History -> Gwangjang Market | TRANSIT | 35 / 45 | True / True | conditional | regional_transit_coverage_unverified |
| 2026-10-10 | Changdeokgung Palace -> Jongmyo Shrine | WALK | 20 / 30 | False / False | blocked | identity_unresolved, regional_walk_unavailable_or_low_quality, independent_coordinates_missing |

Six independent saved coordinates were reused. Two legs have adopted identities and complete coordinates.
Missing coordinate venues: zero. Proposed Details: zero. Directed request inventory: two;
one WALK request is blocked by regional coverage and one TRANSIT request is conditional on verified region support.
Executable/approval-ready Routes: zero. Identity-blocked legs have no invented request or endpoint ID.

### Frozen request and price assumptions

- Details: `id,location`, Place Details Essentials; exact returned ID must match the replay-adopted canonical ID.
- Routes: 1x1 Compute Route Matrix, preserving WALK or TRANSIT. Mask:
  `originIndex,destinationIndex,status,condition,distanceMeters,duration,fallbackInfo`.
  TRANSIT retains its original `2026-10-09T03:00:00+00:00` departure; WALK sends no historical departure.
- Global first paid tier checked 2026-10-05: USD 5 per 1,000 Details requests or matrix elements;
  USD 0.005 per item. No free credit, volume discount, tax or actual invoice is assumed.
- Current proposed retail budget: **USD 0.00**, zero sends. Two unready inventory items total USD 0.01 hypothetically;
  this is not an allowance. The ticket's 8 Details + 4 Routes ceiling would be USD 0.06 at these rates.
- Single-call timeout: 20 seconds; total deadline: 300 seconds; zero retries/searches/model calls.
  Counters reserve the next item before a send; changed input/inventory, unsupported context, identity/coordinate mismatch,
  any provider failure/timeout or limit stops execution. No acquisition executor was implemented.

### Provider limitations and approval boundary

The [official country coverage table](https://developers.google.com/maps/coverage) labels KR walking/driving
unavailable or low quality and omits transit coverage. This is not proof that a route does not exist.
TRANSIT is in the [matrix method](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRouteMatrix),
but country support and actual schedule availability are unverified. The matrix reference allows past TRANSIT times
without a guaranteed horizon; the Compute Routes 7/100-day horizon is not imported.
No mode substitution, retiming, itinerary optimization, genuine review fabrication or new feasibility score occurred.
[Official prices](https://developers.google.com/maps/billing-and-pricing/pricing) and
[SKU triggers](https://developers.google.com/maps/billing-and-pricing/sku-details) support the dated estimates.

Actual module CLI exits 3 with a complete blocked/conditional JSON package. Exact library replay and request preflight
passed with network/DNS blocked and zero attempts. All 61 protected original hashes are unchanged.
Local evidence identifiers: `artifacts/v0-route-requests-20261005/request-package.json`, `offline-acceptance.json` and `preparation-report.md`. These ignored artifacts are not fresh-clone dependencies; the synthetic fixture suite is tracked.

Later execution needs a revised, demonstrably supported exact inventory, a separately approved budget and a current-session
execution child configured `gpt-6.1-sol` / `medium`. Genuine pending identity/audit reviews remain prerequisites for their legs.
This is engineering preparation, not a formal benchmark, accuracy result or version freeze.


### Implementation, validation and review sequence

Review fixed point: `f011a2929f9235f30a546f872f3a879cd6aaeed6`.
Implementation/tests were committed as `677a7e2` before independent Standards and Spec review.
TDD first failed at the absent public request entry point. Later red cases exposed missing
Details/conditional inventories, supplied-Details validation, same-canonical N/A handling,
evidence chronology and absent preflight. Those boundaries were implemented without changing
native scoring or relaxing existing snapshot/identity guards. Focused request gate: 23 passed;
then CLI/conflicting-coordinate checks brought the suite to 25 and the combined adoption/request
gate to **72 passed**. Ruff passed. The full backend gate passed **2777, 10 skipped in 399.30s**.
The skips are existing environment/opt-in cases. No mypy/pyright gate is configured.
Actual public module execution produced complete JSON and exit 3; exact library replay,
network/DNS blocking and budget preflight passed. Zero network attempts/sends were observed;
all 61 protected source hashes remain unchanged and original V0 SHA-256 is still
`b9cf2d4c5ed9b50d2a73e87f93d3631021a0abf7cdea19d1fcc9d5c83d87582b`.

Standards and Spec independent reviews both found zero actionable findings; no correction
commit was needed. The final contract, CLI instructions, PROJECT state and dated evidence
were checked for tracked links/anchors, English additions and whitespace before their
separate documentation commit. Issue #70 acceptance describes this local checkpoint and
remains OPEN pending separate Git publication. Its prior dedicated `smoke tests` wording
was updated to the current-session `gpt-6.1-sol` / `medium` execution-child policy.
No acquisition executor or paid request was implemented or run; execution needs separate approval.

<a id="versioned-v0-route-readiness-2026-10-06"></a>

## Version-specific V0 route readiness (#78, 2026-10-06)

The user authorized #78 implementation with offline work only and zero paid calls,
after #75/#76 corrections and #77 preparation. Fixed review base is
`769a066ac73f71fb4bbc4b6987522a42d57bb0ea`, on `feature/evaluation`.
Implementation/tests are committed as `571ed9506ae08cbd70cb5cce736a5acbab05d59a`.
The unrelated existing `.gitignore` edit remains excluded. This is local development
acceptance, not a live smoke, route feasibility result, score comparison, formal benchmark,
version freeze or Git publication. #79 requires separate scope and action authorization.

The existing #70 preparation capability is reused. Package schema is now
`rtpeval_v0_route_requests_2`: the default requires exact current version-specific identity
replay, and explicit `legacy=True`/`--legacy` preserves historical input replay. Historical
saved artifacts are not relabeled or rewritten. An omitted current report derives pending
identity from verified independent material with no model result, retaining original legs
and model-evidence blockers. Current reports have no mandatory human identity/audit gate.
Per-leg endpoint declarations retain original claims, candidate correspondence and separate
grounding verdicts. FAIL/UNKNOWN exclude canonical endpoints and candidate-coordinate repair;
they do not manufacture a route-feasibility FAIL. Eligible occurrence and unique-venue
counts remain separate from coordinate readiness and deduplicated request counts.

Public-interface TDD reproduced four integration gaps: missing current evidence discarded
all original legs; a historical adoption report was accepted by default; output omitted
current policy/endpoint counts; and endpoint blockers omitted grounding verdict metadata.
Each slice was corrected and retested through `prepare_v0_route_requests`. The CLI test
first failed because the identity-report positional argument was mandatory; it now supports
the same missing-evidence preparation and explicit historical selection. Historical tests
select legacy replay instead of silently exercising it as current policy.

The synthetic current-policy suite demonstrates PASS without human review, confirmed
wrong-address FAIL and legitimate UNKNOWN exclusion, stale/forged reports, corrupt original
or snapshot sources, invalid/missing/wrong-ID/conflicting coordinates, exact Details ID
checks, repeated occurrence/query deduplication, original TRANSIT departures, blocked DRIVE
coverage and preflight that never grants execution. A repeated-visit fixture retains three
directed legs and six endpoint occurrences while deduplicating to two venue IDs and two
WALK matrix queries. No planner or model coordinate backfill is supplied. The related
current/historical identity, adoption, route request and snapshot-coordinate gate passed
**178 tests in 55.46s**. Global Ruff lint passed; `.scratch/pytest-78-related.txt` is an
ignored local evidence identifier.

The real package uses #77's exact current pending identity report with eight V0 UNKNOWN
references, not the six historical #70 adoptions. Ignored evidence identifier:
`artifacts/v0-route-requests-78-20261006`. Preparation timestamp is
`2026-10-05T23:53:05.083299+00:00` (2026-10-06 in the user's Australia/Sydney timezone).
It binds the verified original bundle and original reviewed context. All **four original
directed legs** retain their source IDs, mode, date/time, estimates, occupancy, gap and
selected window values. They remain **UNKNOWN/blocked** with zero identity-eligible legs,
eligible endpoint occurrences/venues, reused coordinates, Details, conditional/ready
Routes or directed request inventory. Proposed and hypothetical inventory budgets are
**USD 0**. Zero missing-coordinate venues describes the empty eligible population; it
does not establish complete endpoints or coordinate readiness. The old 8-Details/4-Routes
planning ceiling and 2026-10-05 price assumptions remain a historical bound, not a new
allowance or provider invoice. Actual model/Google/Routes/planner sends and incremental
charges during preparation are **zero**.

Inventory SHA-256:
`d085383d3250835891b2b67e8e7a95418bd30445d4de14f0f495f6c97c21ab61`.
Request-package file SHA-256:
`239df2ee99c95540fc6ff37835c9ad51c080dccc40f23058a8bbb442f98fffb3`.
The private offline audit confirms **81 protected file hashes unchanged**, including
original #70/#73/#77 material and the consumed #73 execution evidence. These ignored paths
are historical evidence identifiers, not fresh-clone or published documentation dependencies.
No real provider payload is promoted into reusable test fixtures or tracked docs.

Actual module CLI replay, with DNS and socket connections prohibited, produced the same
JSON package as the library and **exit 3**, meaning complete blocked preparation. The
first CLI harness incorrectly supplied a JSON-null optional occupancy-review file, which
was rejected as a non-object envelope. Its output is preserved as `cli-package.json`;
the corrected harness omits that absent optional flag and saves `cli-package-corrected.json`.
No production code change was needed for this harness correction. Exact preflight is
stopped/not authorized because no ready request exists. No acquisition executor is added.

Independent implementation Standards and Spec reviews each found **zero findings**;
no tracked correction commit was needed. The final serial full backend gate at `571ed95`
passed **2945 tests, 10 skipped in 414.43s**:
`.venv/Scripts/python.exe -m pytest backend/tests -q -p no:cacheprovider
--basetemp .scratch/pytest-78-full --tb=short --show-capture=no`.
The evidence identifier `.scratch/pytest-78-full.txt` is ignored and not a public dependency.
Global Ruff and five changed Python format checks pass. No configured mypy/pyright or
remote CI outcome is claimed. Independent final documentation Standards and Spec reviews
each found **zero findings**. All 162 tracked local Markdown targets and anchors pass;
added documentation is English, and the 81 protected file hashes remain unchanged.
Documentation is committed separately from implementation and tests. The pre-existing
unrelated `.gitignore` edit is excluded from both commits.
The [official coverage table](https://developers.google.com/maps/coverage) and
[matrix method](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRouteMatrix)
were reread on 2026-10-06: KR WALK/DRIVE remain unavailable or low quality, transit is
absent from the coverage table, and the matrix accepts past TRANSIT departure timestamps
without certifying actual historical schedule availability. Unsupported context remains
UNKNOWN; no alternate DRIVE query, date shift, planner rerun or route score is introduced.

The preserved #77 plan and request hashes remain unchanged, but #78 modifies two files
in its frozen implementation set (`route_requests.py`, `route_requests_cli.py`). That old
manifest therefore cannot pass current execution preflight. No new smoke manifest is
generated under #78; future execution requires a fresh exact freeze and separate approval,
then the current-session `gpt-6.1-sol` / `medium` execution child. Only genuinely accepted
new current identity evidence can remove actual endpoint blockers. Any future Places or
Routes acquisition also needs a demonstrably supported exact inventory and separate budget
approval. Original artifacts, planner V0-V3 behavior and score arithmetic are unchanged.

<a id="accepted-v0-identity-route-refresh-2026-10-07"></a>

## Offline route refresh from accepted #85 identity (#86, 2026-10-07)

Status: prepared and verified offline. The user approved Issue creation and route-package
refresh with zero paid calls on 2026-10-07 in Australia/Sydney. Fixed source revision:
`d26be76b111ed275e0cde70658a0bbecebf018a4`. No production implementation, test fixture,
generation, V1-V3 identity behavior, score formula or dependency changes are required.
The only pre-existing tracked change is the unrelated `.gitignore` edit; it remains
excluded and byte-identical. The Issue owns lifecycle and the approved preparation scope;
no live, Git publication, research comparison or version-freeze authorization is added.

The previous #78 real package used a current pending report and had zero eligible
endpoints. This fresh package uses #85's accepted `versioned_api_identity_2` report and
its `v0_identity_correspondence_3` saved response: eight V0 primary visits and one
V0-owned requirement target PASS. The response, model envelope and report replay exactly
through the public resolver against the original bundle and API evidence. The historical
#70/#78 packages and #82/#85 consumed executions are preserved, not overwritten or
relabeled. The V0 target's original missing address stays null; target identity is not
substituted for endpoint occurrences or turned into another journey leg.

The parent blocks DNS, connection APIs and live SDK construction while preparing.
Preparation timestamp is `2026-10-06T13:05:17.093816+00:00`, or 00:05:17 AEDT on
2026-10-07. Both `prepare_v0_route_requests` and the actual module CLI use this exact
time and the original bundle, accepted #85 report, schedule context and route reviews.
The absent optional occupancy review is omitted from the CLI rather than written as
a JSON-null review envelope. No new human review is fabricated.

All four original directed legs retain source reference IDs, modes, dates/times,
estimates, occupancy/blocker fields, gap and selected continuous interval. Eight
endpoint occurrences have eight distinct canonical venues, and all four legs are
identity-eligible with no identity blockers. Eight source-linked independent snapshot
coordinates pass replay, exact-ID, strict numeric and timestamp checks. All four legs
are coordinate-ready, with zero missing-coordinate venues and zero proposed Details
requests. No model/planner coordinate is accepted and no additional Details is fetched.

| Original day | Mode | Original gap (minutes) | Identity / coordinates | Request state | Feasibility |
| --- | --- | --- | --- | --- | --- |
| 2026-10-07 | WALK | 30 | Eligible / ready | blocked | UNKNOWN |
| 2026-10-08 | WALK | 35 | Eligible / ready | blocked | UNKNOWN |
| 2026-10-09 | TRANSIT | 45 | Eligible / ready | conditional | UNKNOWN |
| 2026-10-10 | WALK | 30 | Eligible / ready | blocked | UNKNOWN |

All four directed Routes requests have materialized coordinate-backed bodies and exact
keys, without execution. The existing KR preparation profile remains explicitly dated
2026-10-05: WALK carries `regional_walk_unavailable_or_low_quality`, TRANSIT carries
`regional_transit_coverage_unverified`. These are frozen contract assumptions, not a
fresh coverage check on the event date or an API NO_ROUTE observation. Provider-supported
legs and `ready_for_approval` Routes are both zero. No mode substitution, DRIVE fallback,
date shift, planner rerun, removal of blocked legs or favorable route score is introduced.

The package's existing price profile is also dated 2026-10-05, global first paid tier
USD 5/1,000 Details requests or matrix elements, without credits/discounts. **Proposed
ready-send budget is USD 0** (zero Details and zero ready Routes). The **four unready
requests have hypothetical inventory cost USD 0.020000**; this field includes all three
blocked WALK requests and the one conditional TRANSIT, not just the TRANSIT request.
The **historical eight-Details/four-Routes planning bound is USD 0.060000**, not this
package's proposed budget, an approved allowance or actual billing. No live pricing or
coverage fetch occurs; account tier, free usage, taxes and invoice remain unavailable.

The zero-send ledger remains empty. Prepared limits allow zero Details, zero Routes,
zero search/model/retry sends and USD 0, with the unchanged 20-second per-call timeout
and 300-second deadline. Preflight recomputes the exact frozen package for each of its
four request keys, stops each as not ready with the zero-send limit exhausted, and
always returns `live_authorized=false`. No live acquisition executor or execution child
is created. Actual provider/model/planner sends and incremental charges are **zero**.

The actual module CLI runs in a separate process with DNS and connections prohibited.
Its UTF-8 output exactly matches the library package and its stderr is empty. Exit
**3** means a complete inventory containing blocked/conditional applicable legs, not
invalid material or completed route acquisition. No production correction is needed.
The unchanged-code full backend gate remains **2998 passed / 10 skipped / zero failures**
from the approved clock correction; it is reused and not rerun for this preparation.
The focused identity adoption, current V0 contract, historical/current route preparation
and smoke-tool gate passed **182 tests / zero failures in 39.58s** under the repository's
external-network guard and mock transports. Two sandbox launches returned no pytest
output before interruption; no test result is claimed for them. Running the same offline
gate with an approved sandbox override produced the successful result. These launcher
attempts did not send provider requests or alter the package; no code correction was
needed. Local check evidence is `focused-tests-01.txt` (empty interrupted launch) and
`focused-tests-03.txt` (command, successful terminal result and explicit capture limits)
under the private package directory.

The fresh private evidence identifier is `artifacts/v0-route-requests-86-20261007`.
It contains the request package, exact present context/review envelopes, source binding,
protected/output hashes, empty ledger, four preflight results, actual CLI output/stderr,
offline acceptance, focused check log and a non-executable handoff. The handoff explicitly
forbids sending and states remaining support/budget/approval prerequisites; private raw
payloads, credentials and endpoints stay untracked. **120 protected original/source/
preparation/execution files** and **69 implementation/dependency hashes** verify unchanged,
including all #85 raw/model/report/receipt outputs and consumed-directory evidence.
Ten new prepared output files are frozen separately, without overwriting old receipts.

Inventory SHA-256:
`3d138539bb3fafdb218f53313028450913bc86839f838b95c0669758ef1617b1`.
Request-package file SHA-256:
`ff16aa3bd539a08938df691e43d9b5645914282e3d6b78c3a34061884c10a3f5`.
Accepted #85 identity-report file SHA-256:
`068631d1a1a484f9be25074401f560d08861f0435007060b62280a6f4f254da9`.
This is a new offline identity/coordinate-readiness observation, not independent journey
validation. All four original route UNKNOWN results remain. Any future acquisition must
first establish exact provider/method support and original departure applicability,
regenerate the supported inventory and obtain separate budget/execution approval under
the smoke policy. No all-PASS route requirement or paid retry is implied by preparation.


Independent Standards and Spec reviews of fixed base
`d26be76b111ed275e0cde70658a0bbecebf018a4` through preparation-document commit
`a4dfc2e5cec282d218ab832f7ca24fc3647fa688` each report **zero findings**. Both independently
verify the 120 protected files, 69 implementation/dependency hashes and 10 prepared
outputs; Spec also checks preserved leg fields, coordinate provenance and input binding.
No correction is required. Final tracked-document checks validate **183 local targets/
anchors**, English additions and excluded private endpoint. The review acceptance is
recorded separately after the reviewed commit; it changes no implementation or frozen
preparation. #86's six offline acceptance criteria are satisfied, with its reconciled
lifecycle owned by GitHub. The zero-ready inventory and route UNKNOWN outcomes remain
explicit limitations, not unfinished work inside this preparation-only scope.

<a id="kr-route-support-budget-2026-10-07"></a>

## Free Korean route-source verification and budget preparation (2026-10-07)

Status: public-documentation assessment complete; budget proposed, no provider
integration or execution. The user approved free support verification, independent
source selection and budget preparation. Fixed source revision is
`49a6fef135945e3612722a10b4394e6afe49d846`; the unrelated pre-existing `.gitignore` edit
is excluded and unchanged. The client date is 2026-10-07 in Australia/Sydney. Only
public official documentation was browsed. No account/credential probe, provider API,
model, planner, paid request, provider contact or tracker/Git publication occurred.
This engineering assessment is not a formal benchmark or a comparison of V0-V3.

Inputs remain #86's four original directed Seoul legs and accepted #85 identity report:
WALK at noon KST on October 7, 8 and 10, with gaps of 30, 35 and 30 minutes; TRANSIT at
noon KST on October 9, with a 45-minute gap. Eight independent coordinates are already
bound to exact endpoint identities. No Details lookup is needed. The assessment does
not repair original names, IDs, dates, modes, estimates, occupancy, windows or gaps.
Public documentation supports technical candidates; it does not establish successful
responses for these exact pairs, account entitlement or independently measured travel.

### Sources and applicability

Google's current [coverage table](https://developers.google.com/maps/coverage) still
marks KR Walking Directions with a dash: unavailable or low quality/availability.
It explicitly excludes public transit coverage and consumer Google Maps availability.
Thus three Google WALK requests remain blocked, without a NO_ROUTE observation.
The [Matrix method](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRouteMatrix)
accepts TRANSIT and RFC3339 departure time, including past departures, but the reviewed
documentation does not confirm this KR transit pair or its timetable availability.
The separate [Compute Routes transit guide](https://developers.google.com/maps/documentation/routes/transit-route)
documents a seven-day past/100-day future window; that window is not transferred to
Matrix. No method switch or API support probe occurred.

The current [Kakao Map REST reference](https://developers.kakao.com/docs/en/kakaomap/rest-api)
documents `GET /v2/routing/walk` and `/v2/routing/publictraffic`, with coordinate endpoints
and WGS84. WALK success returns one route with distance in meters and time in seconds.
The proposed WALK option is fixed `BROAD_FIRST`, with WGS84 input/output, before any
response; alternative route modes are not tried after failure. Neither endpoint exposes
a departure date/time parameter. WALK is therefore a candidate for the existing
time-independent route-estimate contract, with the original itinerary time retained in
the evidence envelope, not a claim of future conditions. General TRANSIT output cannot
prove service at the original October 9 noon departure. These public V2 endpoints must
not be confused with Kakao Mobility's separately contracted affiliate walking API.

[TMAP pedestrian routing](https://tmap-skopenapi.readme.io/reference/%EB%B3%B4%ED%96%89%EC%9E%90-%EA%B2%BD%EB%A1%9C%EC%95%88%EB%82%B4)
is a WALK alternative: it requires an app key, endpoint coordinates and encoded endpoint
names, and supports WGS84GEO. Its [response specification](https://tmap-skopenapi.readme.io/reference/%EA%B2%BD%EB%A1%9C%EC%95%88%EB%82%B4-%EC%83%98%ED%94%8C%EC%98%88%EC%A0%9C)
provides meters/seconds and route geometry. Its request has no departure date/time;
the automobile time-machine API is not a WALK substitute. Reviewed
[Naver Directions 5](https://api.ncloud-docs.com/docs/en/ai-naver-mapsdirections-driving)
is driving routing, so it cannot preserve these WALK/TRANSIT modes. This is a conclusion
about the reviewed public APIs, not all possible private products.

ODsay's [reference](https://lab.odsay.com/guide/releaseReference) supports Seoul transit,
general WALK and `maasRP` mode selection. The ordinary transit endpoint has no date/time
input. `maasRP` accepts `SearchTime=yyyyMMddHHmm`, but the
[operator clarification dated 2026-07-21](https://lab.odsay.com/community/boardView?seq=718)
explicitly says this only constructs displayed departure/arrival fields by applying
segment durations; it does not perform timetable-based routing. Consequently the
presence of that parameter is not evidence of applicability to the original TRANSIT
departure. Its total time is minutes, unlike Kakao/TMAP seconds; straight-line
`pointDistance` is not a journey measurement. Subway timetable-only searches also do
not establish a complete POI-to-POI leg with access/egress and the original date.

| Source / method | Current engineering use | Remaining limitation |
| --- | --- | --- |
| Kakao Map V2 WALK | Primary technical candidate for the three WALK estimates | Exact pairs untested; account, retention and adapter unresolved |
| TMAP pedestrian | Alternative WALK source, not automatic fallback | Exact pairs untested; account, retention and adapter unresolved |
| Google Matrix WALK | Keep existing blocked profile | KR coverage marked unavailable or low quality |
| Google Matrix TRANSIT | Conditional time-aware candidate only | Exact KR coverage and schedule applicability unconfirmed |
| Kakao TRANSIT / ODsay general or MaaS TRANSIT | General route references only | Do not bind the original explicit departure |
| Naver reviewed Directions API | No compatible inventory | DRIVE mode does not preserve submitted mode |

Source independence also requires future acquisition directly from the selected
provider for the preserved directed coordinates, with acquisition time, exact options,
raw byte hash and source-linked normalization. The planner's own estimates, a map page,
model inference or straight-line distance cannot substitute. Raw response formats must
not be labeled as Google Matrix output. An alternative adapter is not implemented by
this assessment. Error/status semantics require source-specific offline regressions;
authentication, search-limit, snapping and malformed-response errors must not all be
mapped to factual NO_ROUTE FAIL. The current route/scoring contract is unchanged.

### Access, evidence retention and cost

[Kakao usage policy](https://developers.kakao.com/docs/en/kakaomap/common) grants the
free allowance only to the first activated app per developer account; other apps or
excess use need the applicable paid configuration. The policy changed on July 21, 2026.
The [quota/price page](https://developers.kakao.com/docs/en/getting-started/quota) lists
1,000 daily calls each for WALK/TRANSIT and 10 KRW per additional call. No account was
inspected, so eligibility and unused allowance remain unknown; free usage is not assumed.
The reviewed price page does not establish tax treatment for this budget.

[Kakao Operating Policy](https://developers.kakao.com/terms/en/site-policies) Article
5(20) restricts caching purposes/currentness, and Article 5(30) restricts copying/use of
obtained information without the applicable prior approval. Public documentation does
not establish that this evaluator may keep immutable raw responses for long-lived
replay. Applicability and an admissible retention strategy remain unresolved, rather
than a finding that all evaluator use is prohibited. TMAP's
[public terms entry](https://openapi.sk.com/stplat/usage/indexView) did not expose
substantive retention clauses to the browsing tool; permission is likewise unconfirmed.
No inquiry was sent or permanent archival right assumed.

[ODsay prices and use-purpose conditions](https://lab.odsay.com/contact/contact) list
Basic 30 calls/day free for specified users and Flex 25 KRW/call, VAT excluded. The
same page requires prior consultation for analysis/research or other uses outside
building its route-search service. That advertised unit price is not a quote or
license for this evaluator purpose; its free allowance cannot be assumed applicable.
No provider consultation, payment-card registration or account setup occurred.

| Mutually exclusive planning scenario | Units | Published retail reference | Selected proposal |
| --- | --- | --- | --- |
| Kakao V2 WALK | Three calls at 10 KRW | **30 KRW**, tax treatment unconfirmed | Yes, pending prerequisites |
| TMAP pedestrian Premium | Three calls at 11 KRW | 33 KRW, tax treatment unconfirmed | Alternative only |
| ODsay Flex general TRANSIT | One call at 25 KRW | 25 KRW plus VAT; purpose quote unresolved | No; not date-applicable evidence |
| Google Matrix conditional TRANSIT | One Essentials element | USD 0.005, account/taxes unknown | No; support unresolved |

TMAP's [published pricing](https://openapi.sk.com/products/calc?menuSeq=5&svcSeq=4) places
pedestrian routing in the route-guidance group with Free 1,000/day and Premium 11 KRW
per call. Group sharing, remaining quota and applicable tax treatment are unverified.
Google's [current pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
lists Matrix Essentials at USD 5/1,000 elements with 10,000 monthly free units; the
[SKU conditions](https://developers.google.com/maps/billing-and-pricing/sku-details)
distinguish higher-feature pricing. The unchanged simple TRANSIT matrix options have
no higher-feature trigger identified. Neither published allowance is assumed available.
These figures are separate currency scenarios, not summed or converted, provider quotes,
guaranteed invoice ceilings or approved execution budgets. The original #86 USD 0.02
unready inventory and USD 0.06 historical bound remain historical figures, not replaced
with a false all-supported four-route budget.

### Prepared draft and validation boundary

The new private identifier is `artifacts/kr-route-support-budget-20261007`. Its
`kr_route_support_budget_draft_1` contains three WALK draft parameter sets linked to
the original source coordinates, an exact copy of all four original legs, source binding,
protected/output hashes, empty ledger and non-executable handoff. It is not an
`rtpeval_v0_route_requests_2` acquisition manifest or authenticated HTTP request.
The proposed future inventory is at most **three Kakao WALK sends**, zero TRANSIT,
alternative-provider, Details, geocoding, model, planner, health/probe or retry sends.
Suggested limits retain 20 seconds per call and a 300-second total deadline, with
one attempt reserved before each send and no automatic source switching. The 30 KRW
reference needs confirmed account/tax/use conditions before an enforceable ceiling.
No new source is `ready_for_execution`; current authorized sends and incremental
spend are **zero**, including calls that might qualify for a free quota.

Before execution, separately approved work must resolve admissible raw retention/use
and account costs, implement/test the source-specific offline adapter, then freeze
exact sources, parameters, units, time basis, implementation and budget for approval.
Any later live task follows the current-session smoke execution policy. The TRANSIT
leg needs a confirmed independent source preserving its original explicit departure;
general route duration is not promoted into that evidence. No formal comparison,
new Issue, provider contact, push, PR, merge or branch switch is included here.

The original #86 request package and all 16 files in that completed preparation remain
byte-identical. Together with the prior 120 protected files, **136 protected files** and
**69 implementation/dependency hashes** pass preservation checks; the unrelated
`.gitignore` hash also matches. Six new preparation outputs are frozen separately.
The budget arithmetic and original-leg/coordinate bindings pass offline checks.
All **168 tracked local Markdown targets/anchors** in the three changed documents,
English additions and whitespace checks pass before commit;
private endpoints/raw payloads remain excluded. This is a documentation-only assessment:
no pytest gate is rerun and no new runtime validation is claimed. Prior focused
182-pass and full 2998-pass/10-skipped gates describe the unchanged implementation.
All four original route feasibility results remain **UNKNOWN**; generation, identity
behavior for independently runnable V0-V3 and score formulas are unchanged.

<a id="sydney-offline-route-preparation-2026-10-07"></a>

## Sydney AU preparation and preserved KR replay (2026-10-07)

Status: implemented and prepared offline; live execution is not authorized. The user
approved a new Sydney V0 scenario, explicit AU preparation/CLI selection, evidence and
budget preparation, regressions, local commits and independent Standards/Spec review,
with unchanged generation/scoring and zero paid calls. They first requested squashing
the five latest consecutive docs commits. Those were `eac3b621`, `d26be76`, `a4dfc2e`,
`49a6fef` and `bc4de3e`, all unpublished locally. They are replaced by `c49e9819f69ce2465d43cdc5bd6d2176a35f5028`
(`docs: consolidate V0 smoke acceptance and route readiness`), whose parent is the
unchanged `f4499f2` test commit. Its tree equals the former `bc4de3e` tree exactly.
Original objects remain under local recovery ref
`refs/codex-backups/docs-before-squash-20261007`; historical evidence hashes are not
rewritten. The source/review fixed point for this implementation is `c49e981`.
The unrelated `.gitignore` edit remains excluded and byte-identical. No remote history,
branch switch, push, PR, merge, tracker operation or provider contact is included.

### Explicit country profile and preserved behavior

[Google's current coverage table](https://developers.google.com/maps/coverage) marks AU
WALK/DRIVE available with good quality/availability, while excluding TRANSIT coverage.
The [Matrix method](https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRouteMatrix)
supports explicit TRANSIT departure, but national or pair-level transit support is not
assumed from the consumer map or that coverage row. No API probe occurred.

The public `prepare_v0_route_requests(..., region_code="AU")` and CLI `--region AU`
select the new dated Australian profile. The original input must explicitly declare
Australia, such as `Sydney, Australia`; other/unknown declarations and unsupported
region values reject all inventory. This binds a declared country, not geographic
inference, geocoding or proof of coordinate-country membership. Default/explicit KR
retains its dated 2026-10-05 metadata and exact serialization, including omission of
a new region replay field. AU selection is replay-bound and participates in the
inventory digest; changing it stops preflight.

AU WALK needs replayed current identity, independent coordinates, a continuous free
span and no original leg blocker before becoming ready for approval. Missing points
can propose exact Details and keep the route conditional; failed/unknown identity
remains blocked without model/planner coordinate repair. A same-canonical N/A leg
gets no route allowance. TRANSIT stays conditional with original explicit departure
and additional historical-availability checks when applicable. DRIVE remains unsupported
by this existing WALK/TRANSIT acquisition path, without a new route implementation.
There is no regional, mode, time or model fallback. All factual route components remain
UNKNOWN without acquired independent route observations, and original FAIL/UNKNOWN
identity outcomes continue downstream unchanged.

Matrix budgets/counters count deduplicated sends, not repeated leg occurrences. Three
synthetic legs containing two unique WALK queries therefore reserve two sends and
USD 0.010000, retaining all three occurrences and their source links. A duplicate link
cannot promote a blocked/conditional query into a ready query. Request options, masks,
WALK time-independence, TRANSIT time binding, scoring formulas, V0-only LLM identity
and deterministic V1-V3 identity remain unchanged. No generation/runtime or shared
score implementation was modified.

### New scene and output-dependent budget

The tracked [Sydney request](../../../tools/validation/packets/sydney-v0-route-smoke/request.json)
uses October 14-17, 2026, two travelers, AUD 1600, exactly two primary sightseeing
visits per day and a required Sydney Opera House visit, with architecture, museums,
harbour views, food and walking/public transport preferences. Its schema and trip-date
window pass offline validation against the trusted planning reference October 7 in
Australia/Sydney. Later execution must validate the actual trusted day; frozen dates
must not be silently shifted after expiry. The request is scenario input, not a
guarantee of what the unchanged generator will produce.

A historical five-day Sydney V0 `itinerary_2` result exists from September 25, but no
current reusable identity bundle/snapshot/report accompanies it. It is protected and
not truncated into the current eight-Details/four-leg ceiling, regenerated, repaired or
presented as a new result. There is currently no new Sydney V0 output, independently
reviewed RequirementSpec, identity API snapshot, current V0 correspondence response,
canonical venue list or actual route package. Synthetic test output cannot fill those
gaps. Original Seoul packages and all four original UNKNOWN route results remain intact.

The fresh private identifier `artifacts/sydney-offline-20261007` contains source binding,
protected/output hashes, a staged price draft, empty ledger, exact default-KR replay,
foreign-AU rejection and non-executable handoff. It is not a live acquisition manifest.
The source input and request inventory are separate: the latter must be frozen from
actual future raw output and eligible independent evidence. Exceeding the existing
eight endpoint venues/four original legs stops preparation; it never selects a favorable
subset or increases limits automatically.

| Future stage / hypothetical inventory | Public-price reference | Present readiness |
| --- | --- | --- |
| V0 two-node generation | Unknown; no exact wire/token/output ceilings frozen | No generation allowance |
| Nine initial identity Text Searches (8 visits + 1 named subject) | USD 0.288 | Queries/output-dependent; not acquired |
| V0-only identity correspondence, one send | USD 0.0042 reference allowance | Exact packet absent |
| Up to eight missing-coordinate Details | USD 0.040 | May be zero with valid future search coordinates |
| Up to four unique matrix elements | USD 0.020 | Hypothetical; TRANSIT not counted as ready |
| Non-generation scenario subtotal | **USD 0.3522** | Not executable or an invoice ceiling |

The [Google price list](https://developers.google.com/maps/billing-and-pricing/pricing)
gives global first paid-tier Text Search Pro at USD 32/1,000 and Details/Matrix
Essentials at USD 5/1,000. The proposed identity
[Text Search mask](https://developers.google.com/maps/documentation/places/web-service/text-search)
contains ID, display name, formatted address/components, business status, coordinates
and next-page token, without opening/review fields that elevate the SKU. No remaining
free allowance, tax, discount or invoice is assumed. No pagination or retry sends are
reserved; incomplete evidence is retained as unresolved, not repaired by another send.
Actual distinct reference/query counts may differ, so this is a bounded planning
scenario for later exact preparation, not a claim that nine queries are already ready.

[OpenAI's current GPT-6 Luna page](https://developers.openai.com/api/docs/models/gpt-6-luna)
lists per-million token references USD 0.10 input, 0.01 cached input, 0.125 cache write
and 0.50 output. Keeping the existing identity proposal at 18,000 input/3,000 output
with low reasoning gives USD 0.003750 worst retail reference when all input is cache
write, or USD 0.004125 under the regional +10% scenario, within the unchanged USD
0.0042 reference allowance. Reasoning is included in output, not added twice. That
identity-only limit does not cap generation. The current V0 two-node default generation
calls have no explicit per-call output ceiling or frozen payload in this preparation;
their actual model configuration/usage and Foundry billing remain unverified. A bounded
generation handoff must precede any paid approval, without changing generation flow.
No total execution ceiling is claimed by summing an unknown generation cost with the
non-generation subtotal. Existing #85's consumed allowance is not reused.

All current provider/model/probe/retry send limits and incremental spend are **zero**;
no SDK client, live executor or execution child is constructed by preparation. Future
approved stages require exact inputs, usable evidence, implementation/request hashes,
masks/SKUs, supported departure/mode and separate budgets under the smoke policy.
Changing to Sydney does not waive uncertainty, certify every route or authorize another
request. This development preparation introduces no formal benchmark or version freeze.

### Validation sequence

Public-interface TDD first failed for the missing `region_code` keyword, then passed
after explicit AU preparation was implemented (31 tests including current KR checks).
The CLI slice failed for missing `--region AU`, then its two public-interface checks
passed. The duplicate-query slice failed because three leg occurrences reserved three
sends rather than two; deduplicated budgeting made all three slices pass. Negative
regressions cover invalid/foreign region, unchanged default KR, missing current model
evidence/coordinates, TRANSIT original time, unsupported DRIVE, N/A and tampered profile.
The focused route/identity-adoption gate passes **121 tests / zero failures** in 28.46s.
A Ruff ambiguous test variable was corrected before final global lint and four-file
format checks passed. No configured mypy/pyright gate is present.

The first local preparation launch lacked the repository import path and stopped before
writing outputs. Correcting its local launcher path allowed network-prohibited preparation
to pass. The saved #86 package replays exactly under default KR, and attempting AU on
the original Seoul input rejects it without partial inventory. **146 protected original
and preparation files** remain byte-identical; of the prior 69 implementation/dependency
hashes, **67 are unchanged** and only the two authorized route-preparation/CLI files
changed. Seven new preparation outputs are frozen separately; `.gitignore` is unchanged.
The fresh full backend offline gate passes **3017 tests, 10 skipped, zero failures**
in 341.21s. The repository external-network guard remains active; provider/model tests
use synthetic or mocked evidence. The log is preserved separately from the seven frozen
preparation outputs. The implementation, direct regressions and tracked Sydney source
request were committed together as `6fc9a2a091f19e757c8f3ed0dcbd6345f18f3635`
(`feat(evaluation): prepare Sydney routes with explicit AU profile`) before review.

Independent read-only Standards and Spec agents reviewed all five committed files
from fixed point `c49e9819f69ce2465d43cdc5bd6d2176a35f5028` through that implementation
commit. Standards reports **zero documented-standard violations and zero actionable
code smells**; Spec reports **zero missing/incorrect requirements or scope expansions**.
Both checked explicit AU selection, conservative readiness and unique-request budgets,
profile replay and default-KR preservation against the approved offline scope. Neither
review ran tests or contacted providers; the reported test gate is the preserved parent
run. Uncommitted final docs and the unrelated `.gitignore` were outside their review
scope. No implementation correction commit is needed.

The final four-document check validates **190 actual tracked local targets/anchors**,
English additions, retained existing anchors and whitespace. Protected source files,
all seven frozen preparation outputs and `.gitignore` pass SHA-256 preservation again.
Final acceptance documentation is committed separately after implementation review.
Remaining execution prerequisites are a bounded generation plan, actual new Sydney V0
output, reviewed independent requirements, API identity evidence and an exact separately
approved route inventory/budget; this acceptance does not certify live AU routes.

<a id="evaluation-development-tool-boundary-2026-10-07"></a>

## Development tool boundary within evaluation (2026-10-07)

The user clarified that V0 smoke is a development verification activity, not an actual
system execution stage, and requested `tools/` inside `backend/evaluation` to separate
responsibilities. The approved local migration starts from
`0e52c28691ebd1775b254c646f13c38a4f01a500`. The pre-existing `.gitignore` edit remains
outside scope. No paid/live call, push, PR, merge, branch switch or tracker update is
authorized or performed. This is a directory boundary, not a new country-inference
feature, execution plan or formal benchmark.

The V0 `route_requests.py` and `route_requests_cli.py` development utilities now live
under `backend/evaluation/tools/`, with a package marker. They prepare smoke request
inventories, budgets and preflight checks using existing evaluator materials. Neither
Product planning nor final quality scoring imports them. Core identity/snapshots,
schedule/opening/route scorers, quality consumers and their legitimate CLI entries stay
at the evaluation root. V3's internal validation/repair stays in `backend/app` as part
of planning. Repository-level data/validation/diagnostic tools are not moved.

Current callers use `backend.evaluation.tools.route_requests`; the development command
uses `python -m backend.evaluation.tools.route_requests_cli`. The former root-level tool
modules are retired. Current guide/contracts/README navigation give the new paths;
historical commands, raw artifacts and frozen manifests retain the identifiers/hashes
of their original revisions. They are not rewritten to pretend the migration existed
when their evidence was acquired. Preparation behavior, AU/KR rules, wire schema,
source integrity, limits, uncertainty and scoring formulas are unchanged.

The existing public regression import was first pointed at the new package and failed
collection because it did not yet exist. Moving the two modules, fixing relative core
imports and updating the four existing test consumers resolved that missing-package
failure. An initial focused run then had **109 fixture setup errors** because its new
basetemp parent directory had not been created; no behavior assertion ran. Creating
the dedicated parent and using a fresh basetemp yielded **109 passed / zero failures**
in 23.92s. Initial lint found three import-order issues; Ruff fixed them and normalized
the changed files. Global Ruff, the seven-file format check and the new module's actual
`--help` entry all pass. No new behavior or mirror tests were added for this relocation.

Static AST comparison against the fixed base confirms the two tool bodies and four
existing regression bodies differ only in import paths and test import ordering. Its
first comparison treated Ruff's sorted imports as a body mismatch; normalizing import
order in that local checker resolves the diagnostic without a source behavior change.
**146 protected original/preparation files** and **seven frozen Sydney preparation
outputs** remain byte-identical, as does the excluded `.gitignore`. Private evidence is
kept under the new identifier `artifacts/evaluation-tools-move-20261007`, separate from
earlier frozen evidence. Implementation-path hashes from old manifests continue to
describe their old revisions; they are not relabeled as current bindings.

With DNS/socket connections prohibited, the moved public library replays the original
saved #86 KR request package exactly, including its inventory digest and all four
UNKNOWN route verdicts. This is a replay of existing independent material, not new
route acquisition or authority to execute a frozen manifest at a changed code revision.

The fresh full backend offline gate passes **3017 tests, 10 skipped, zero failures**
in 435.91s, with the external-network test guard active. Its new log is retained separately
from old frozen outputs. The pure module migration and four existing regression import
updates were committed before review as
`2a2b1e1a04a052b84ff51911871486a41af307d7`
(`refactor(evaluation): isolate development route tools`). No planner or evaluator
scoring implementation changed.

Independent read-only Standards and Spec agents reviewed the complete committed diff
from the fixed base through `2a2b1e1`. Standards reports **zero documented-standard
violations and zero actionable code smells**. Spec reports **zero missing/incorrect
requirements or scope expansions**. Both excluded unstaged final documentation and
the unrelated `.gitignore`, and neither independently executed tests or network calls.
No correction commit is needed. Final acceptance documentation follows separately.

The six-document check passes **242 actual tracked local targets/anchors**, English
additions, retained historical anchors and whitespace. The migration-only AST and
original/frozen file checks pass again after the implementation commit. Existing source
claims, FAIL/UNKNOWN outcomes and Sydney's pending live prerequisites are unchanged.
This completes the requested development-tool directory boundary, without making smoke
a product stage, changing evaluation formulas or authorizing another execution.
