# Runtime configuration reference

`config/runtime.yaml` is the single non-secret runtime policy source. This document explains
its current values; it is not another default file. The tables enumerate every YAML leaf.
English names identify application policies, not measured optimal settings or user demands.

## Loading, versions and overrides

`runtime.config_loader` loads and validates an immutable `RuntimeConfig`. The default loader
is process-cached; an explicit `--runtime-config PATH` loads that file once. The request receives
one resolved object through runner, acquisition/factory, V3 stage, round, projection and budget.
There is no per-round YAML reload. Restart/reload before a later request to change policy.
Duplicate/unknown keys and invalid values fail explicitly. V3 fields have strict numeric/boolean
types and finite/range/relationship checks. Legacy policies without `v3_repair` can still load for
V0/V1/V2; V3 refuses a missing group. Typed Repair objects have no independent numeric defaults.
Standalone offline helpers resolve the same default YAML only when no policy is injected.

V0 uses shared local calendar/logging/trace settings and its existing model entry; it does not
acquire external travel evidence. `budget`, `acquisition`, `main_generation`, `web_evidence` and
`reference_discovery` apply to the shared V1/V2/V3 tools path. `tripworld_discovery` applies to
V2/V3 initial discovery; V1 does not initialize RAG. `v3_repair` applies only to V3 after primary
planning. Product version selection and primary prompts/K are unchanged.

The V3 CLI supports `--repair-quantity-review` and `--no-repair-quantity-review`; an explicit
flag overrides YAML, absence retains YAML. No other Repair CLI or environment budget overrides
are introduced. `--development-timeout-seconds` remains explicit, positive, and bounded by
`development_timeout_seconds`; YAML alone never grants 600 seconds. V3 counts from request
entry before dependency assembly. Existing `--reference-date`, input arguments and
`--runtime-config` responsibilities are unchanged. `--rag-env-file` supplies the existing
RAG environment with override disabled. Provider/model credentials and deployment settings stay
in existing environment settings; no secret values belong here or in this README.

`v3_request_policy` records base/effective runtime SHA-256 identifiers, review override source,
effective Repair values, shared Nearby reservation and entry deadline. Existing run configuration
snapshots remain redacted. Each round records cumulative counters and actual callback usage;
missing usage is empty/unavailable, not an offline estimate. Per-round callbacks are additive to
an existing outer usage callback. Do not add per-round totals to that same outer total twice.

## Counting, timing and invariants

Repair acquisition allowances are **stage totals, never multiplied by three**. Cache hits do not
consume new sends. Actual sent failures consume sending budget; failed pre-send reservations do
not become fictitious sends, but remain terminal attempts. Duplicate canonical processing does
not create another attempt. No phase name, round, Top-K change or failed provider call authorizes
hidden retries. The success cache and failure ledger survive every round. Zero acquisition
allowances stop that class of work; other existing materials may still support a model attempt.

At most one model call occurs per round. More rounds can increase model usage even with unchanged
tool budgets. The 28-ID ceiling is a per-input union, not 28 additional POIs. The independent
identity ledger can be larger. Original supply and its unused count retain their original meaning.
No provider call, model explanation or policy pass changes UNKNOWN into a verified fact.
Identity, source, scope, REQUIRED/EXCLUDED, zero hidden retries and UNKNOWN semantics are contract
invariants, not configurable bypass switches. Reviews/Profile and Official Web additions remain
unsupported in Repair; their zero allowance is not an enable switch.

Stage deadline = min(entry request deadline minus `reference_discovery.deadline_seconds`,
stage start plus stage_seconds). Nearby is reserved from its existing authoritative key, not a
second hard-coded ten seconds. Affordable rounds are bounded by remaining rounds and floor of
remaining time / round_reference_seconds. Round allocation is min(round_seconds, remaining time /
affordable rounds). Preparation is capped by preparation_seconds and reserves minimum_model_seconds
plus recheck_reserve_seconds. Model timeout is min(model_seconds, remaining round time minus
recheck_reserve_seconds); insufficient minimum allocation skips the call. Post-proposal I/O ends
before finalization_reserve_seconds. Unused time remains available within the same stage cap.
Minimum model plus recheck must fit round reference, which must fit round cap, which must fit stage
cap. Model minimum must fit model maximum. Request exhaustion/cancellation stops new acquisition;
owned resource cleanup still runs. Later failure preserves the latest accepted itinerary.

Spatial kilometre/minute limits constrain automatic additions, not request execution time.
Coordinate checks are not Routes measurements. Time-applicable directed/mode-compatible Routes
can verify the minimum transfer check. Untimed WALK measurements support layout and burden but
retain future-time UNKNOWN. With no usable Routes, only the configured short WALK/default layout
fallback is allowed; obstacles/explicit unsupported transport requirements cannot be masked.
Daily burden is recomputed cumulatively against stage-original activities and identity changes.
No comparable original measurement means no credit: the conservative gross burden and missing
comparison are visible, not a claim that original travel took zero minutes. Baseline credits currently
cover insertion chains between retained adjacent original anchors. Identity replacement/deletion
without that supported comparison uses conservative gross load. REQUIRED remote visits
are not deleted by default compactness policy. The present adapter requests single-pair matrices,
so it may exhaust four calls before using 32 elements. No live WALK compatibility is claimed.

Schema ceilings below bound the approved engineering envelope, not universal provider limits.
The strict patch DTO separately caps edit count at 50. Runtime values may be lowered within
validated relationships; expanding the envelope requires an explicit code/policy change.
Quality-first keeps its existing coordinated C64/send40/K20/P8 and baseline 400/7/64 requirements;
profile/review capacity relationships and RAG query-position/token relationships still apply.
No historical compatibility field is silently repurposed as a Repair allowance.

## Current YAML values and every effective path

The unit and counting scope are described in each row. Values are copied from the current YAML;
a local documentation coverage test detects a missing path or stale value.

| Full configuration path | Current YAML value | Type / bounds | Meaning and scope |
| --- | --- | --- | --- |
| `schema_version` | `6` | integer; = 6 | Runtime loader schema discriminator; exactly 6. Not a planning version selector. Zero is invalid. |
| `reference_discovery.policy_version` | `"nearby_references_1"` | string; = "nearby_references_1" | Final-primary Nearby reference contract identifier. |
| `reference_discovery.max_requests` | `3` | integer; >= 0, <= 3 | Nearby sending allowance per request, after the whole Repair stage. Zero disables the allowance. |
| `reference_discovery.max_result_count` | `10` | integer; >= 1, <= 10 | Provider result count per Nearby request. Zero is invalid. |
| `reference_discovery.radius_metres` | `800` | number; > 0, <= 800 | Nearby search radius around an actual final anchor. Zero is invalid. |
| `reference_discovery.anchor_reuse_metres` | `300` | number; >= 0, <= 300 | Maximum anchor separation for reusing a Nearby result. Zero removes the corresponding tolerance. |
| `reference_discovery.deadline_seconds` | `10` | number; > 0, <= 10 | Independent final Nearby phase cap; Repair subtracts this same value from remaining request time as its reservation. Zero is invalid. |
| `reference_discovery.request_timeout_seconds` | `4` | number; > 0, <= 4 | Per-Nearby-request timeout. Zero is invalid. |
| `reference_discovery.retries` | `0` | integer; = 0 | Fixed zero retry contract. Zero is the only supported value. |
| `reference_discovery.max_references` | `3` | integer; >= 0, <= 3 | Maximum attached references per final anchor policy. Zero disables the allowance. |
| `reference_discovery.rank_preference` | `"DISTANCE"` | string; = "DISTANCE" | Fixed provider distance ranking. |
| `reference_discovery.included_types` | `["restaurant", "cafe", "park", "museum"]` | array; schema-validated | Fixed four reference categories; changes require a reference policy contract change. |
| `app.time_zone` | `"Australia/Sydney"` | string; schema-validated | Backend trusted reference-day calendar. Existing date contract is unchanged. |
| `budget.candidates` | `64` | integer; 1..64 | Primary canonical candidate processing capacity per request, not scheduled visits. Zero is invalid. |
| `budget.final_pois` | `20` | integer; 1..20 | Maximum primary supply capacity. Duration policy selects the effective K; this does not force K20 for shorter trips. Zero is invalid. |
| `budget.places.destination_search_calls` | `1` | integer; 1..1 | Destination resolution searches per primary request. Zero is invalid. |
| `budget.places.candidate_search_calls` | `12` | integer; 1..12 | Initial candidate discovery search calls per primary request. Zero is invalid. |
| `budget.places.detail_calls` | `40` | integer; 1..40 | Shared primary Details sending allowance. Repair has a separate stage allowance and the same request cache/failure state. Zero is invalid. |
| `budget.places.review_detail_calls` | `8` | integer; 0..8 | Primary review-bearing Details allowance. Zero disables the allowance. |
| `budget.weather.calls` | `2` | integer; 0..3 | Primary weather operation allowance; Repair reuses weather. Zero disables the allowance. |
| `budget.routes.matrix_elements` | `64` | integer; 1..100 | Compatibility single-matrix counter retained in ToolBudgetLimits. Active baseline/alternative acquisition uses the dedicated counters below; it is not an extra V3 allowance. Zero is invalid. |
| `budget.routes.baseline_elements_per_request` | `64` | integer; 1..64 | Maximum actual origin count times destination count per primary baseline matrix. Zero is invalid. |
| `budget.routes.baseline_elements_per_run` | `400` | integer; 1..400 | Total directed primary baseline elements per request. Zero is invalid. |
| `budget.routes.baseline_calls` | `7` | integer; 1..7 | Primary baseline matrix calls per request. Zero is invalid. |
| `budget.routes.alternative_pairs` | `16` | integer; 0..16 | Primary alternative selected-pair capacity. Zero disables the allowance. |
| `budget.routes.alternative_matrix_calls` | `16` | integer; 0..16 | Primary alternative matrix call allowance. Zero disables the allowance. |
| `budget.routes.alternative_elements` | `16` | integer; 0..32 | Primary alternative actual matrix element allowance, including unavailable results. Zero disables the allowance. |
| `budget.web.evidence_tasks` | `8` | integer; 0..20 | Primary official-evidence tasks; not individual search tool invocations. Zero disables the allowance. |
| `budget.web.page_fetches` | `8` | integer; 0..20 | Primary page-fetch budget. Zero disables the allowance. |
| `budget.experience.review_enriched_places` | `8` | integer; 0..8 | Primary places selected for review enrichment. Zero disables the allowance. |
| `budget.experience.profile_llm_calls` | `8` | integer; 0..8 | Primary ExperienceProfile model invocations; no new profiles during Repair. Zero disables the allowance. |
| `web_evidence.reasoning_effort` | `"low"` | string; one of ["low", "medium"] | Official evidence reasoning model option, not primary or Repair reasoning. |
| `web_evidence.max_tool_calls` | `2` | integer; >= 1, <= 3 | Native web-search tool call ceiling per reasoning task. Zero is invalid. |
| `web_evidence.search_context_size` | `"low"` | string; one of ["low", "medium", "high"] | Native search response context option. |
| `web_evidence.timeout_seconds` | `20` | integer; >= 1, <= 60 | Official evidence reasoning task timeout. Zero is invalid. |
| `web_evidence.authority_domain_overrides` | `[]` | array; schema-validated | Explicit per-place, per-information-need approved domains. Empty list supplies no overrides; not credentials. |
| `web_evidence.page_retrieval.max_targets_per_need` | `2` | integer; = 2 | Page targets per official information need. Zero is invalid. |
| `web_evidence.page_retrieval.max_redirects` | `2` | integer; = 2 | Redirect hops per page request. Zero is invalid. |
| `web_evidence.page_retrieval.timeout_seconds` | `10` | integer; = 10 | Timeout per page retrieval. Zero is invalid. |
| `web_evidence.page_retrieval.max_response_bytes` | `262144` | integer; = 262144 | Maximum page response bytes. Zero is invalid. |
| `web_evidence.page_retrieval.max_text_chars` | `20000` | integer; >= 1, <= 20000 | Maximum extracted page text characters. Zero is invalid. |
| `web_evidence.claim_extraction.max_native_sources` | `3` | integer; >= 1, <= 3 | Maximum native search sources projected per extraction. Zero is invalid. |
| `web_evidence.claim_extraction.max_native_snippet_chars` | `1200` | integer; >= 1, <= 1200 | Characters retained per native search snippet. Zero is invalid. |
| `web_evidence.claim_extraction.max_candidates_per_call` | `3` | integer; >= 1, <= 3 | Structured claim candidates per extraction call. Zero is invalid. |
| `web_evidence.claim_extraction.max_calls_per_need` | `3` | integer; = 3 | Extraction call allowance per information need. Zero is invalid. |
| `web_evidence.claim_extraction.max_extraction_output_units` | `1200` | integer; >= 1, <= 1200 | Extraction output-unit protection, separate from Repair tokens. Zero is invalid. |
| `logging.level` | `"INFO"` | string; schema-validated | Minimum runtime logging level; uppercase standard value. |
| `logging.console` | `true` | boolean; schema-validated | Console logging switch; false does not disable trace files. |
| `trace.enabled` | `true` | boolean; schema-validated | Request trace switch. |
| `trace.directory` | `"logs"` | string; schema-validated | Trace output path; relative paths resolve against the repository root. |
| `trace.payload_level` | `"metadata"` | structured list; schema-validated | Trace projection mode; metadata is the current selection. |
| `trace.capture_llm` | `true` | boolean; schema-validated | LLM trace capture category, subject to payload level and byte ceiling. |
| `trace.capture_tools` | `true` | boolean; schema-validated | Tool trace capture category. |
| `trace.capture_evidence` | `true` | boolean; schema-validated | Normalized evidence trace capture category. |
| `trace.raw_provider_payloads` | `false` | boolean; schema-validated | Raw provider payload capture switch; remains false. Repair audit does not enable raw responses or internal reasoning. |
| `trace.max_payload_bytes` | `1000000` | integer; schema-validated | Per-artifact serialized UTF-8 byte ceiling. Redaction applies; missing/truncated Repair artifacts carry explicit status. Zero is invalid. |
| `tripworld_discovery.version` | `"tripworld_runtime_1"` | string; = "tripworld_runtime_1" | RAG runtime contract identifier. |
| `tripworld_discovery.top_k` | `20` | integer; >= 1, <= 20 | Initial RAG rows per query, not Repair Top-K. Zero is invalid. |
| `tripworld_discovery.resolution_entities` | `16` | integer; >= 0, <= 16 | Primary RAG canonical resolution work allowance. Zero disables the allowance. |
| `tripworld_discovery.details_calls` | `20` | integer; >= 0, <= 20 | Primary RAG Details allowance. Zero disables the allowance. |
| `tripworld_discovery.fallback_calls` | `4` | integer; >= 0, <= 4 | Primary RAG Google fallback search allowance. Zero disables the allowance. |
| `tripworld_discovery.radius_km` | `15` | integer; = 15 | Initial destination retrieval radius; Repair derives its own target radius from v3_repair.spatial. Zero is invalid. |
| `tripworld_discovery.identity_radius_km` | `1` | integer; = 1 | Google-backed canonical identity matching radius, reused by RepairResolver. Zero is invalid. |
| `tripworld_discovery.deadline_seconds` | `360` | number; > 0, <= 360 | Initial RAG phase deadline; Repair uses its own stage and round deadlines, not this expired phase allocation. Zero is invalid. |
| `tripworld_discovery.embedding_timeout` | `8` | number; > 0, <= 8 | Per-embedding timeout, reused by Repair within its remaining stage time. Zero is invalid. |
| `tripworld_discovery.sql_timeout` | `60` | number; > 0, <= 60 | Per-retrieval timeout, reused by Repair within its remaining stage time. Zero is invalid. |
| `tripworld_discovery.connect_timeout` | `10` | number; > 0, <= 10 | Request-owned RAG database connection establishment tolerance. No independent connectivity probes. Zero is invalid. |
| `tripworld_discovery.google_timeout` | `4` | number; > 0, <= 4 | RAG Google search timeout, also reused by Repair discovery. Zero is invalid. |
| `tripworld_discovery.retries` | `0` | integer; = 0 | Fixed zero retry contract. Failed embedding texts/retrieval keys remain failed across stages/rounds. Zero is the only supported value. |
| `tripworld_discovery.max_queries` | `4` | integer; >= 1, <= 4 | Initial distinct retrieval-query allowance. Zero is invalid. |
| `tripworld_discovery.max_positions` | `80` | integer; >= 1, <= 80 | Initial query-result position processing ceiling; max_queries times top_k must fit. Zero is invalid. |
| `tripworld_discovery.total_query_tokens` | `2048` | integer; >= 1, <= 2048 | Initial query token budget; must cover max_queries times 512. Zero is invalid. |
| `acquisition.policy_id` | `"quality_first_1"` | string; one of ["conservative_1", "quality_first_1"] | Shared primary supply/acquisition policy. quality_first_1 validates the coordinated duration envelope. |
| `acquisition.details_deadline_seconds` | `120` | number; > 0, <= 120 | Primary candidate Details phase wall-clock limit; not reused as a stale Repair deadline. Zero is invalid. |
| `acquisition.details_timeout_seconds` | `20` | number; > 0, <= 20 | Primary Details call wall-clock limit. Zero is invalid. |
| `main_generation.enabled` | `true` | boolean; schema-validated | Shared primary serializer protection switch. Required by quality_first_1. |
| `main_generation.input_tokens` | `160000` | integer; >= 1, <= 160000 | Per-primary-call serialized input engineering ceiling. Zero is invalid. |
| `main_generation.output_tokens` | `16384` | integer; >= 1, <= 16384 | Per-primary-call structured output ceiling. Zero is invalid. |
| `main_generation.framing_tokens` | `2048` | integer; >= 2048, <= 2048 | Per-primary-call message framing token reserve. Zero is invalid. |
| `development_timeout_seconds` | `600` | integer; >= 1, <= 600 | Maximum permitted explicit development CLI request allowance. Presence alone does not enable this timeout; V3 requires an explicit allowance from entry. Zero is invalid. |
| `v3_repair.max_rounds` | `3` | integer; >= 1, <= 3 | Total rounds per Repair stage, shared across dates/targets. Each round has at most one model call. Zero is invalid. |
| `v3_repair.max_model_calls` | `3` | integer; >= 0, <= 3 | Model sending ceiling per entire stage; zero disables Repair model attempts. Must not exceed max_rounds. Zero disables the allowance. |
| `v3_repair.quantity_review_enabled` | `false` | boolean; schema-validated | Default coverage review-target opt-in. It never turns NEEDS_REVIEW into CONFIRMED. |
| `v3_repair.alternatives_per_gap` | `2` | integer; >= 1 | Distinct alternatives per authorized quantity gap as a preparation reference. Fewer options may still be used. Zero is invalid. |
| `v3_repair.exploration_positions` | `2` | integer; >= 0, <= 2 | Reusable exploration positions within the same input union across the stage, not extra candidates or per-date quotas. Zero removes reserved presentation opportunities. Zero removes the corresponding tolerance. |
| `v3_repair.timing.stage_seconds` | `300` | number; > 0, <= 300 | Maximum Repair wall-clock duration, additionally bounded by entry deadline minus Nearby reservation. Zero is invalid. |
| `v3_repair.timing.round_seconds` | `120` | number; > 0, <= 120 | Maximum wall-clock allocation for one candidate/model/recheck round. Zero is invalid. |
| `v3_repair.timing.model_seconds` | `70` | number; > 0, <= 70 | Maximum model wait per call; dynamically shortened by remaining round time minus recheck reserve. Zero is invalid. |
| `v3_repair.timing.preparation_seconds` | `30` | number; >= 0, <= 30 | Maximum optional candidate and pre-proposal route acquisition window per round. Zero disables new preparation work, not cached reuse or the model. Zero removes the corresponding tolerance. |
| `v3_repair.timing.recheck_reserve_seconds` | `20` | number; > 0 | Round time retained after model wait for route acquisition and application revalidation. Zero is invalid. |
| `v3_repair.timing.minimum_model_seconds` | `30` | number; > 0 | Minimum available model allocation required to start a call. Zero is invalid. |
| `v3_repair.timing.round_reference_seconds` | `60` | number; > 0 | Divisor used to estimate affordable remaining rounds; not a promise of completing that many. Zero is invalid. |
| `v3_repair.timing.finalization_reserve_seconds` | `1` | number; > 0 | Time withheld from post-proposal I/O for local finalization. Must be smaller than recheck reserve. Zero is invalid. |
| `v3_repair.input.input_tokens` | `64000` | integer; >= 1, <= 64000 | Per-model-call total system/user/schema/framing engineering ceiling; overflow preserves latest adopted itinerary. Zero is invalid. |
| `v3_repair.input.output_tokens` | `16384` | integer; >= 1, <= 16384 | Per-model-call strict output limit forwarded without mutating primary client defaults. Zero is invalid. |
| `v3_repair.input.framing_tokens` | `2048` | integer; >= 1 | Per-call framing reserve included in input count; must be positive and below input_tokens. Zero is invalid. |
| `v3_repair.input.identity_capacity` | `28` | integer; >= 1, <= 28 | Per-call distinct canonical union: scheduled context plus presented additions plus other operation identities. Ledger is separate and is not serialized wholesale. Zero is invalid. |
| `v3_repair.input.activity_capacity` | `120` | integer; >= 1, <= 120 | Maximum protected plus editable itinerary activities per projection; necessary context is never truncated to pass. Zero is invalid. |
| `v3_repair.input.candidate_characters` | `12000` | integer; >= 1, <= 12000 | Maximum serialized characters per projected candidate; fail closed rather than delete facts. Zero is invalid. |
| `v3_repair.input.feedback_characters` | `12000` | integer; >= 1, <= 12000 | Maximum compact previous-round feedback characters; overflow stops iteration without rollback. Full raw history is not included. Zero is invalid. |
| `v3_repair.acquisition.google` | `2` | integer; >= 0, <= 2 | Stage-wide actual Google discovery/fallback sends; failures after send count. Zero disables the allowance. |
| `v3_repair.acquisition.fallback` | `1` | integer; >= 0, <= 1 | Stage-wide fallback subset of google; cannot exceed google. Zero disables the allowance. |
| `v3_repair.acquisition.embedding` | `1` | integer; >= 0, <= 1 | Stage-wide new query embedding batches; compatible query-vector cache hits do not consume sends. Zero disables the allowance. |
| `v3_repair.acquisition.retrieval` | `1` | integer; >= 0, <= 1 | Stage-wide new RAG retrieval sends. Zero disables the allowance. |
| `v3_repair.acquisition.canonical` | `8` | integer; >= 0, <= 8 | Stage-wide unique canonical processing attempts, including failures. Duplicate identities cannot obtain another attempt by changing round. Zero disables the allowance. |
| `v3_repair.acquisition.details` | `8` | integer; >= 0, <= 8 | Stage-wide actual Details sends; cached success does not consume sends and failure is not retried. Zero disables the allowance. |
| `v3_repair.acquisition.routes` | `4` | integer; >= 0, <= 4 | Stage-wide actual matrix requests, before and after proposals together. Zero disables the allowance. |
| `v3_repair.acquisition.elements` | `32` | integer; >= 0, <= 32 | Stage-wide actual matrix origin count times destination count; counts requested unavailable elements, not just successful returned rows. Zero disables the allowance. |
| `v3_repair.acquisition.top_k` | `10` | integer; >= 1, <= 10 | Rows per Repair RAG query and bounded Google discovery response projection. Does not create another retrieval allowance. Zero is invalid. |
| `v3_repair.acquisition.provider_timeout_seconds` | `20` | number; > 0, <= 20 | Per-Repair Details/Routes call timeout. Google/embedding/SQL timeouts reuse the existing tripworld_discovery values above. Zero is invalid. |
| `v3_repair.spatial.walk_radius_km` | `2` | number; > 0 | Coordinate prefilter and blank-day group diameter for WALK or application nearby default. Zero is invalid. |
| `v3_repair.spatial.motor_radius_km` | `5` | number; > 0 | Coordinate prefilter and blank-day group diameter for explicit DRIVE/TRANSIT. Zero is invalid. |
| `v3_repair.spatial.max_leg_minutes` | `45` | number; > 0 | Maximum automatic-added adjacent-leg layout burden; these are itinerary minutes, not service execution seconds. Zero is invalid. |
| `v3_repair.spatial.detour_floor_km` | `1` | number; >= 0 | Floor for insertion extra-distance allowance between two retained anchors. Zero removes the corresponding tolerance. |
| `v3_repair.spatial.detour_ratio` | `0.5` | number; >= 0 | Relative insertion extra-distance allowance. Maximum allowed increment is max(detour_floor_km, ratio times original direct distance). Zero removes the corresponding tolerance. |
| `v3_repair.spatial.fallback_distance_km` | `1` | number; > 0 | Maximum adjacent straight-line distance for no-route conservative WALK/default layout; not a measured route length. Zero is invalid. |
| `v3_repair.spatial.fallback_reserve_minutes` | `45` | number; > 0 | Required no-route schedule gap and conservative burden reserve. Not a fabricated travel duration. Explicit motor-mode requirements cannot use this fallback. Zero is invalid. |
| `v3_repair.spatial.daily_added_minutes` | `90` | number; > 0 | Stage-cumulative added transport burden per day versus stage-original itinerary. Compatible measured original edges may earn credit; UNKNOWN original edges never earn invented credit. Zero is invalid. |


## A elastic-time contract interaction

A adds no new tunable defaults and does not change `runtime.yaml`. Existing
`v3_repair.spatial.fallback_reserve_minutes` remains the no-route itinerary reserve, not a
measured route duration. Fixed user intervals and already adopted transfer reservations cannot
be consumed as free time. `v3_repair.input.activity_capacity` also bounds the proposed itinerary
after application-owned placeholder splitting; `input_tokens` includes the protected-time,
lineage and residual-window projection. Overflow retains the latest adopted itinerary.

Root authorization, fixed-time provenance, historical unassessed/null semantics and atomic
rollback are invariants, not configuration switches. Shared DTO field cardinalities are contract
limits, not a second runtime budget. B/C review switches, cross-date moves and blank-day default
hours are not activated by this checkpoint. No new credentials or CLI overrides were added.


## B target and operation policy

These values are loaded once with the existing runtime snapshot. Review flags are independent
and default off; new B flags are YAML-only (the existing quantity CLI override is unchanged).
They change V3 post-primary authorization only, never first-generation supply or prompts.

| Configuration path | Current value | Type / units / behavior |
| --- | --- | --- |
| `v3_repair.repetition_review_enabled` | `false` | Boolean, per request. Same-canonical cross-date review; not a fact-conflict declaration. |
| `v3_repair.overfull_review_enabled` | `false` | Boolean, per request. Independent maximum-count review. |
| `v3_repair.daily_main_min` | `2` | Integer, 1..5; per-date Repair coverage reference. Zero invalid. |
| `v3_repair.daily_main_max` | `5` | Integer, 1..10 and >= minimum; per-date Repair upper reference. Exactly this many is allowed. Shared generation diagnostics retain their own 2..5 generation observation. |
| `v3_repair.move_max_days` | `1` | Integer, 0..1; distance from original activity date for each explicitly scoped move. Zero disables moves. Never reset by a later round. |
| `v3_repair.blank_day_start_hour` | `9` | Integer, destination-local hour 0..23; originally empty/missing dates only. Zero means midnight, not disabled. |
| `v3_repair.blank_day_end_hour` | `18` | Integer, destination-local hour 1..24, strictly after start. 24 means next midnight; zero invalid. |

Blank windows need reliable destination timezone and assessed time protection; fixed rest wins.
Existing activity days retain their real occupancy, elastic roots and unoccupied calendar gaps,
without being clipped to the blank-day default. All B targets and conditional children share
the unchanged phase budget/deadline, cache/failure state and model-call ceiling. The obsolete
whole-stage coverage waiver field is compatibility-only and no longer grants permission.


## C confirmed operating and transfer obligations

C adds no new adjustable values or review switch. Confirmed opening/transfer targets are
independent of the three default-off review flags. Rounds prioritize confirmed obligations and
record deferred review target IDs. All C targets and activated coverage children share the same
`v3_repair` phase totals, deadlines, identity/token ceilings and `move_max_days` boundary.
There are no new Reviews/Profile or Official Web acquisitions in Repair.

Opening confirmation requires application-owned whole-venue entry intent and the existing
resolver's applicable, traceable, nonconflicting date-specific evidence. Intent is not an
operating fact. Ordinary unbound visits and exterior/public-access questions remain limited.
Timed directed route evidence, untimed WALK measurements and policy layout reserves retain
distinct meanings; provider failures or missing evidence cannot be turned into PASS.

Coverage regression permission for confirmed optional-visit removal names the parent, date,
trigger activities and removable canonical identities. It is not a blanket C deletion waiver.
Generated notes on changed retained/replaced activities are preserved verbatim under an explicit
historical/not-revalidated label; original notes also remain in proposal/draft audit. No text
classifier deletes risk warnings or rewrites user requirements. Notes-only changes cannot count
as arrangement improvement. These provenance/safety boundaries are not configurable bypasses.
