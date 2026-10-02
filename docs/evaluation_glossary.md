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

## V3 before/after concepts

**V3 stage pair**: The selected V3 run's pre-repair draft and final primary itinerary,
evaluated independently under one compatible frozen snapshot. The draft is a V3 stage,
not an independently executed V2 itinerary.

**Paired dimension mask**: The common included score dimensions for a V3 stage pair;
a dimension is omitted only when neither stage has applicable or unresolved units.
It is separate from the four-version final report's mask.

**Edit provenance**: Source-linked evidence of transformations actually adopted between
V3 stages, including retained activity IDs and parent/fragment relations. It describes
editing history without establishing independent quality or venue identity.

**Occurrence correspondence**: A validated relation between activities in the two V3
stages, established first through edit provenance and then through source-content or
reviewed evidence where needed. Edit continuity is distinct from venue continuity.

**Correspondence review**: Source-linked human verification of an ambiguous or complex
cross-stage relation remaining after provenance validation and content fallback. Complexity
alone does not require review when validated sources establish the relation; independent
quality checks determine compliance.

## Blinded ranking concepts

**Anonymous plan label**: A public A/B/C/D identifier whose plan association remains
fixed across the three ranking dimensions within one assessment task.

**Private label mapping**: The researcher-only association between anonymous labels
and selected source versions, retained outside the rater package and answer export.

**Display preparation**: Researcher review of prospective anonymous content, including
source-linked removal of identity/provenance identifiers while preserving travel facts
and uncertainty. It is separate from the rater's assessment.

**Tie group**: A set of plan labels judged equally for one dimension. Ordered tie
groups in a submitted ranking partition all four labels exactly once.

**Unable-to-judge response**: A whole-dimension response indicating insufficient basis
to rank the plans. It does not mean the plans are tied or that the dimension is inapplicable.

**Not-applicable response**: A whole-dimension response indicating that the dimension
does not apply to this task. It does not supply an ordering.

**Effective answer revision**: The highest valid complete submitted revision for one
task/rater. Earlier revisions remain audit records; drafts are not effective answers.

**Inferred display arrival**: A separately labelled clock time computed from supplied
departure and duration when the itinerary omits arrival. It is not a submitted arrival
claim, independent evidence or an input to quality scoring.

**Hidden duplicate task**: A repeated source group presented under an independent
anonymous assignment, used for within-rater consistency and excluded from main counts.

**Comparable pair**: A version pair with a ranked outcome in both an original task and
its hidden duplicate for the same dimension. No comparable pairs means consistency
is unavailable, not perfect agreement.
