# Evaluation Glossary

This glossary defines shared terms for benchmark construction and travel-plan evaluation. It is not a project-wide context or an implementation specification. [PROJECT.md](../PROJECT.md) remains the current project-level source of truth.

## Language

**Qualifying group**: One request and the four V0-V3 outputs whose respective workflow completion has been established by benchmark construction. Qualification is not a claim of itinerary quality.
_Avoid_: Correct group, evaluator-approved run

**Benchmark candidate list**: The collection of qualifying groups available for later user selection. Adding a candidate does not initiate evaluation.

**Evaluation batch**: The explicitly selected collection of groups handed over by the user for evaluation. Its size is not fixed by the evaluation module.
_Avoid_: Automatically evaluated candidate stream

**Requirement Specification**: Human-reviewed obligations derived independently from the original request. It is distinct from a planner's interpretation of that request.

**Evaluation snapshot**: Preserved independent external evidence used consistently to assess the submitted itineraries. It is an evidence basis, not absolute real-world truth.

## Requirement and schedule units

**Obligation check**: One outcome for one independently reviewed requirement, with
all of its explicit count, date and time conditions retained as components.

**Schedule commitment**: One distinct scheduled visit, journey or fixed activity whose
occupied time is assessed independently; uncertain timing does not erase the commitment.

**Protected blocker**: A reviewed interval restricting specified kinds of scheduled
commitments. Overlapping protections can share a blocked span while remaining separate
user obligations.

**Potential match**: A source-preserved occurrence whose unresolved role or identity
could affect a reviewed place obligation; it is not a confirmed visit to that place.


## Route evaluation concepts

**Route candidate leg**: A directed connection between consecutive scheduled primary
visit occurrences on one delivered day. It remains inventoried when route evidence is
missing or applicability is uncertain.

**Submitted departure**: The departure claimed by the itinerary's authoritative
transport representation. It is distinct from the departure used for an evidence query.

**Query departure**: The departure recorded in the independent route request; omission
is a distinct time basis rather than proof that the submitted departure was queried.

**Continuous travel interval**: One uninterrupted available span for a candidate journey.
Separate spans around an occupied commitment do not form one longer interval.

**Route cap**: An adopted per-mode provider duration or distance threshold. It is
separate from the available time between scheduled commitments.

**Hard route deadline**: An applicable non-travel protection or guaranteed fixed
occupation boundary that permits no schedule grace, including the DRIVE reserve.

**Decisive route verdict**: A combined outcome established by all required PASS components
or any independently proven FAIL. A partial decisive FAIL does not establish complete
component evidence; missing components remain separately visible.
