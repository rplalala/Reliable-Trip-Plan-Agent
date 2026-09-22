# V0 design

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
