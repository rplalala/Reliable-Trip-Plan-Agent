# Tickets 01/03: structural claims and ordinary-output compatibility

Date: 2026-10-02, Australia/Sydney.
Status: User decisions accepted; specification revision only. Implementation requires
separate approval. Inspected revision: 186fd2488f3c196e4898ab6e2c8d341e6aeeaeb3;
the working tree was clean before this documentation task.

## Authority and scope

[PROJECT](../../PROJECT.md) owns project status. This revision specializes the
[projection contract](intake-projection-contract.md) and
[identity contract](identity-implementation-contract.md). Earlier acceptance records
describe the implemented conservative rules, not implementation of this revision.
GitHub Tickets 01/03 remain their existing work records; no Issue state, body or comment
is changed by this local documentation task.

The user approved specification and acceptance revision after the Tickets 01-09 audit.
The user then accepted structural fields as the primary identity/role claims because
interpreting arbitrary title semantics is unreliable, and accepted a narrow independent
address-component extension with no additional requests or automatic old-data backfill.
No planner, evaluator code, fixture, live acquisition or formal evaluation is authorized
by this specification approval. Ticket 10 implementation remains separately authorized
work; the Ticket 04-to-07 coordinate bridge remains a candidate outside this revision.

## Observed facts and limits

- V0 prompts require origin/destination/mode in transport title or notes. The current
  projector instead excludes endpoint prose from automatic positional association.
- V1-V3 output validation checks supplied IDs and normalizes place_name from the candidate
  ledger. It does not normalize title or guarantee agreement between all free-text fields.
- The projector currently treats main_poi titles beginning with walking as role conflicts.
  Identity accepts separate titles automatically only as the name or Visit plus the name.
- Identity currently uses exact comma/semicolon address components and complete formatted
  address equality. The snapshot identity bridge and identity candidate reader omit typed
  address components. Raw snapshots can retain them, but their presence is not guaranteed.
- The original request destination is free text, not a canonical city or geographic boundary.

Source seams: backend/app/versions/v0/prompts.py, backend/app/policies/itinerary_output.py,
backend/evaluation/projection.py, backend/evaluation/identity.py,
backend/evaluation/snapshot.py and backend/app/schemas/request.py.

The preceding audit ran eight synthetic function probes without changing files: four
title cases passed the product output validator; plain Visit Museum A passed strict
identity association, Morning at Museum A required identity review, Walking tour of
Museum A required role and identity review, and Visit Different Museum required identity
review. Two address variants differed only in address representation and produced strict
association versus destination_unverified. Two V0 transport variants produced one bound
claim for Walking versus one unbound claim for Walking from Museum A to Museum B despite
one candidate gap. These are development reproductions, not full planner runs or measured
production frequencies. No corrected behavior has been executed.

## 1. V0 occurrence association

Use existing day, interval, activity occurrence and explicit endpoint claims before
requesting review. A supported explicit directed phrase such as Walking from Museum A
to Museum B may associate automatically when its normalized names identify the scheduled
endpoints and exactly one same-day candidate gap fully contains the transport interval.
Require resolved chronology and no conflicting endpoint claim in the supported title/notes
fields. A model-estimate disclaimer does not negate a movement mode.

Comparison uses NFC, case folding and whitespace normalization, retaining source pointers.
The bounded endpoint recognizer must match complete scheduled labels, not substrings,
provider IDs invented from prose, or approximate venue names. It does not interpret
arbitrary narrative. Unsupported endpoint syntax keeps the existing review route.
The implementation must publish its finite supported syntax and cover it through the
public projection boundary. No LLM extraction is introduced.

Repeated venue labels alone do not force review if the complete interval and endpoint
conditions select exactly one occurrence pair. Multiple surviving pairs, reversed or
contradictory endpoints, overlaps, an intervening unresolved visit or invalid clocks retain
review/uncertainty. Do not pick the nearest pair or replace an explicit conflicting endpoint
with a convenient positional match. Existing independently reviewed endpoints can still
establish association despite a separate timing conflict.

V1-V3 continue to associate application transfers by directed activity IDs. Association
identifies the submitted journey; independent identity and route evidence determine its
factual endpoints and feasibility. Source selection, occupancy units and scoring stay intact.

## 2. Structural role and place claims

For an explicitly declared main_poi with a usable place_name, those fields define the
submitted visit and place claim. source_place_id remains a claimed identity subject to
independent evidence. Ordinary title wording does not independently veto either claim.
Morning at Museum A, Walking tour of Museum A and A relaxing morning therefore need no
title-equivalence review when the structural visit is Museum A.

Retain original title/notes for display and audit. Do not build an expanding whitelist of
acceptable descriptive titles or attempt to prove every title semantically equivalent to
the place name. Automatic structural interpretation is not certification that all prose
is accurate. This deliberately accepts incomplete detection of implicit prose conflicts.

Keep review for contradictory structural declarations and concretely recognized competing
claims: for example main_poi Museum A paired with an explicit Visit Museum B claim or a
supported directed movement from Museum A to Museum B. Recognizers must expose the exact
source and parsed competing claim, rather than flagging a movement keyword alone. An
independently supplied review can record other semantic contradictions. No general entity
recognizer or multilingual semantic classifier is promised.

Without usable place_name, the existing name-only/title evidence path remains available;
the revision does not manufacture a place from generic prose. Ambiguous structured roles,
multi-POI blocks and genuine identity conflicts retain their existing handling. Apply the
same output-field interpretation across versions, without importing a planner verdict or
candidate ledger as independent factual proof. Independent details/search, branch checks,
high-impact review and the predeclared audit sample remain required as applicable.

## 3. Independent structured address evidence

Extend only the evaluator's independent observation bridge/candidate representation to
retain typed address components when present in linked independent responses. Preserve
original formatted address, component types/text and observation hashes. The existing
planner DTO/cache is not the independent source. This is a required narrow future interface
change, not a capability already present in Ticket 03 or the snapshot bridge.

For a city destination such as Sydney, an independently returned locality component with
the same normalized name can establish the city association even when formattedAddress
contains Sydney NSW 2000 as one segment. Match components by type, never array position.
Country/state/postcode/street occurrences of the same word do not substitute for locality.
Explicit destination qualifiers must also agree; unsupported composite wording, aliases
and metropolitan-area interpretations remain reviewable rather than silently simplified.

Apply the new evidence consistently at all three affected checks: destination association,
output location association and search/details address agreement. A street location can
match the independently supplied street-number/route component combination, including
provider-supplied short forms. Generic locality agreement cannot activate the existing
numbered-street branch-search shortcut.

For search/details with the same ID and compatible name, differing formatted strings may
be equivalent when their complete usable typed address evidence agrees. Require agreement
on street number, route, locality and country for this street-address path; administrative
and postal components, when present, must agree on both sides as well. Missing or conflicting
components do not prove equivalence. Different street numbers, routes or localities retain
review even if the ID is equal. This narrow path does not promise normalization of every
address type; exact legacy address agreement remains usable when components are absent.

No substring-only city test, inferred geocoding, silent alias translation or fabricated
component is allowed. Missing components retain the existing strict fallback or review.
Do not rewrite old snapshots. Malformed supplied components must be diagnosed rather than
silently converted to favorable evidence. New rule/observation revisions must participate
in report and review linkage: replay old evidence under the selected new rules, reject stale
derived reports, and preserve historical acceptance records without new network requests.

## 4. Accepted cost boundary

There is no new request, retry, reverse-geocoding call or LLM call for this extension.
Future authorized independent acquisition may add addressComponents to an already required
Places request that retrieves displayName/formattedAddress. Missing fields or old snapshots
never trigger automatic follow-up acquisition. Planner budgets and field masks are outside
this specification change. Local payload storage/parsing increases slightly; no size or
latency measurement is claimed.

Official documentation checked 2026-10-02: addressComponents is Place Details Essentials
and Text Search Pro; displayName is Place Details Pro and Text Search Pro. Requests are
billed at their highest requested SKU. Thus adding this field to the described existing
requests does not raise their SKU under the checked policy. Future live integration must
verify its actual field mask and the then-current policy; this is not a blanket statement
that a separate request or an IDs-only query upgrade is free.

Sources: [Place data fields](https://developers.google.com/maps/documentation/places/web-service/data-fields),
[billing rules](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing),
and [address component wire](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places#AddressComponent).
Public documentation reads made no authenticated Places calls.

## 5. Acceptance examples for later implementation

Automatic in this table means eligible without the removed ambiguity trigger; independent
identity requirements and audit/high-impact review can still apply.

| Input and evidence | Required result |
| --- | --- |
| V0 A ends 10:00, Walking from A to B occupies 10:00-10:20, B starts 10:30; one matching gap | Associate with that directed occurrence pair; retain estimated mode/time claims. |
| The same names occur later but only one gap contains this transport interval | Select the unique occurrence pair; no name-only ambiguity. |
| Transport explicitly says B to A while the available gap is A to B | Review; no positional override. |
| Several candidate pairs remain or chronology is unresolved | Review/uncertainty; no favorable selection. |
| main_poi Museum A with Morning at Museum A, Walking tour of Museum A or A relaxing morning | Keep primary visit and Museum A claim; no keyword/title-whitelist rejection. |
| Museum A fields with a concretely recognized Visit Museum B or A-to-B movement claim | Retain an explicit conflict and review its interpretation. |
| Generic text with no usable structured place | Preserve existing role/name-only handling; no invented identity. |
| Sydney destination; formatted city segment Sydney NSW 2000; independent locality Sydney | Accept city association, subject to the remaining identity checks. |
| Melbourne locality and Sydney Road street | Do not accept Sydney destination. |
| Same ID/name and equal complete typed street address, differently formatted search/details strings | Accept address equivalence without rewriting originals. |
| Same ID but conflicting street number or locality | Review; ID equality cannot erase the conflict. |
| Old snapshot lacks address components | Exact legacy fallback or review; zero automatic backfill requests. |

Later TDD must cover public intake/projection and snapshot-to-identity replay, including
the new ordinary-output cases and the retained conflicting cases. Verify source pointers,
rule/evidence revisions, stale-review rejection, V0/V1-V3 source selection, unchanged
branch/audit requirements and downstream requirement/opening/route/report regressions.
Use synthetic offline evidence and a network guard; request-plan counts and model-call
counts must not increase because of this feature. Test old snapshots without backfill.

The future implementation scope is projection.py, identity.py, the narrow snapshot identity
bridge and affected replay-policy validation, directly related tests and documentation.
No planner behavior change or new operational provider client is proposed. Record a starting
commit, run TDD, commit implementation/tests before Standards and Spec review, then commit
any review fixes and final acceptance documents under the repository Git policy.

## Documentation validation

This record captures accepted decisions and future acceptance criteria. The current task
runs English-content, local Markdown target and diff checks only. Implementation test
results, production coverage and corrected-output claims must be added only after the
separately authorized implementation occurs.

Completed checks: nine documentation/archive files, 213 local Markdown targets, zero
English-content or missing-target errors; diff whitespace checks passed. Inspection found
and removed duplicated introductory notes left by a partial patch application, and applied
the missing package-guide notice before validation. No source or test file changed.
