# V0 design

## Shared semantic guidance implemented — 2026-09-26

V0 shares sourced goal/count/date interpretation and generation guidance while remaining tool-free. It does not call candidate semantic assessment, RAG or Repair. Name-based observations are not reliable canonical/role verification, so absence of external judgments cannot establish semantic policy completion. Independent V0 offline regressions pass; no new live evidence. See the [checkpoint](shared_poi_semantics_plan.md#12-implementation-checkpoint--2026-09-26).

Current shared/V3 engineering checkpoint (2026-09-25): see [closeout](v3_closeout.md)
for current configuration, shared ownership and artifact-verified evidence. Earlier dated
implementation/live statements below retain their original scope. V0 remains tool-free;
V1/V2 do not run Repair; the product default remains V0. Provider recovery UI is offline-only.


V0 uses the shared structured form, optional one-call preference interpretation and one plain-LLM
itinerary generation. Graph node names remain extract_requirements and generate_itinerary;
the first now interprets optional preferences rather than re-extracting authoritative form facts.
The runner owns validation/resources and the graph validates output source rules. Shared Foundry
DTO/mapping remains behind StructuredLLMClient. Boundary/date errors retain classification;
other model failures retain stage-specific wrapping.

No external travel tools, RAG, database, Reviews, Weather, Routes or Nearby are acquired. References
are optional subordinate model knowledge from the same generation; no current verification or
Google identity is invented. scripts/run_v0.py remains independent; both APIs currently use V0.

[Requirements](shared_requirements.md) and [output](shared_itinerary_output.md) define common contracts.
[Milestones](v0_milestone.md) preserve original free-text freeze and later authorized changes.

## Shared first-draft objective

V0 uses the same full-date-range and default 2-5 main-visit guidance as V1/V2. New model
activities declare their role; historical missing roles remain unknown. Runner diagnostics
use name_proxy rather than canonical identity and never perform external lookup, additional
model calls or repair. Supply metrics are not applicable. Details are maintained in
[shared output](shared_itinerary_output.md#first-generation-roles-and-diagnostics).


## Compatible transfer output update (2026-09-25)

The shared itinerary DTO now accepts optional `transfers` (missing defaults empty).
Current V3 binds and presents verified/unknown per-leg route estimates and separate
application reserves; V0-V2 do not fabricate transfers or acquire additional routes for
this field. Primary model DTO/prompt, K, existing version entry points and product default
are unchanged. The frontend can render this optional data when supplied; this does not
implement the deferred Product V3/API selection or the whole frontend backlog.
See [V3 design](v3_design.md#shared-output-and-frontend) and the
[development verification record](v3_development.md#mixed-transport-and-joint-components-2026-09-25).
This is shared output compatibility, not evidence of a V3-only quality gain or a re-freeze.


Shared mixed-transport output compatibility: application-owned `route_diagnostics` defaults
to empty, like transfers. The V0 wire DTO does not generate these provider facts and V0
does not initialize Google/RAG. Shared transport upgrade has no V0 route acquisition.


## Shared preference input gate checkpoint (2026-09-25)

Implemented + offline-validated only. All V0-V3 entries reuse the existing single preference
interpretation call to assess request-level input issues before travel acquisition. Application
policy checks exact provenance and returns rewrite/clarification or dedicated safety outcomes;
VALID does not certify feasibility or override hard-requirement/capability checks. Empty input
still skips interpretation. Model contract/provider failures remain system failures. Product
engine selection and travel budgets are unchanged. Historical live runs were not retroactively
validated with this feature. See [shared preference input checkpoint](shared_preference_input.md)
for contracts, compatibility, API/UI behavior, actual test chronology and serializer limits.


### Minimum daily coverage update (2026-09-25)

Shared output now reports the one-primary-visit minimum independently of 2-5 review
quantity guidance. V0-V2 remain diagnostic-only; V3 prioritizes confirmed minimum gaps
below hard protections and above optional reviews. Explicit source-linked full-day time
protections support exemptions; uncertain applicability remains unknown. Product output
includes coverage status without research metadata or source quotations. The primary
prompt, default engine and budgets are unchanged. See [shared minimum coverage](shared_minimum_daily_coverage.md)
for counting, compatibility, exemption and partial-result boundaries, and the V3 development
checkpoint for offline and live evidence. This does not retroactively validate historical runs.
