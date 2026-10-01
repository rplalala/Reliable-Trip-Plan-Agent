# Ticket 05 offline requirement and schedule acceptance

Date: 2026-10-02. Baseline: `fc9996803b05b9b444583f0985274bee75c4ed0f`
on `feature/evaluation`. Working tree was clean before this ticket; implementation,
tests and related documentation were uncommitted at the offline acceptance checkpoint. Tickets 01-04 and planner paths
are preserved. Status: Implemented and validated for the user-approved offline scope.
Live tracker: [Ticket 05 #17](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17).
The original offline task did not change GitHub state. The subsequently authorized
Issue/documentation/local-commit closeout is recorded below.

## Delivered and source boundaries

- `requirement_schedule.py`: runtime semantic validation after accepted intake,
  requirement checks and immutable source-linked report; malformed executable material
  and detectable contradictions return the whole batch for correction.
- `schedule_time.py`: independent instant/local-clock interpretation, unique IANA
  localization, explicit date/offset conflict, DST fold/gap and precision uncertainty.
- `occupancy.py`: source-selected commitments, candidates and same-date/scope protected
  unions; one non-overlap check per established commitment and separate pair/union measures.
- `requirement_schedule_cli.py`: local JSON replay with preparation hashes and no source writes.
- Identity preparation now includes resolved fixed-time-only subjects and records policy
  scope/reference digest. Old or incomplete reports require offline replay, while retained
  unresolved evidence propagates UNKNOWN. Both digest endpoints use the shared canonical
  helper; the historical projection source-ID format is unchanged.

Reviewed exact/minimum/global/date/distinct-date quotas are conjunctive components,
not added obligations. Default named-visit authoring is exact one; fixed-only single
matching includes trip-wide exact one. Sourced repeat permission enables at-least-one
time matching without weakening explicit quotas. One visit must satisfy every time
condition. Exclusion and structural counts use inclusive Input dates and adopted
canonical identities; candidate IDs, names, planner findings and Nearby are not proof.

Protections are boundaries, never additional non-overlap units. Original obligations
are checked separately even after same-scope union. V0 uses model Activities; V1-V3
use Transfers without fallback. Duplicate sources share a journey, V0 segments preserve
gaps, and conflicting claims remain alternatives. All alternatives can establish a
conflict, but common duration evidence remains a lower bound. Unbound explicit times
may exclude unrelated conflicts while their association/denominator stays unresolved.
Missing journeys affect transport structure coverage without synthesized occupancy.

Coverage/density/repetition are descriptive. Requested empty days remain in the
denominator; extra declared dates are diagnostic. Non-overlap duration scope is all
submitted commitments. Unknown identities preserve observed repetition lower bounds;
minimum revisits do not create an invented repetition defect ratio. Completeness and
candidate-unit uncertainty suppress full-scope percentages instead of shrinking units.

## Actual validation sequence

1. TDD public-interface slices first failed for missing identity subject coverage,
   time/occupancy/scoring modules and CLI, then passed after their implementations.
   A fixture initially assumed identity status `prepared`; it was corrected to existing
   `complete`/`needs_adjudication` semantics without changing the resolver's status API.
2. Count and time slices exercised exact/minimum/date/distinct-date conjunctions,
   repeated sources, potential matches, single/multiple selectors, same-visit time
   conjunction, precise endpoints, missing clocks/zones and 23/25-hour DST protections.
   Invalid executable booleans/counts/operators, unhashable malformed fields and unknown
   extra executable fields initially escaped correction or raised a type error; explicit
   semantic/type checks corrected these cases before identity preflight.
3. Completeness tests first reproduced empty unclassified content becoming N/A and an
   unknown unresolved kind receiving an invented weighted unit. Completeness now remains
   unavailable; linked annotations and reviewed soft preferences do not multiply checks.
   Dated upper limits, distinct-date capacity, conflicting single starts and exclusion/time
   contradictions first escaped validation, then passed as whole-batch material correction.
4. Occupancy tests cover protection/commitment conflict, triple overlap (pair sum differs
   from conflict union), version source selection, mode-only uncertainty, duplicates,
   disjoint segments, alternatives, unbound/missing claims, reviewed fixed generic activity
   and exact source-linked protection correspondence. Known contradictory placeholder links
   initially remained candidates; they now require material correction. Uncertain time
   correspondence still preserves candidate applicability rather than choosing a match.
5. Fixed-time uncertainty and candidate-overlap slices reproduced overly conservative
   UNKNOWN when available time proved a candidate could not satisfy a condition/conflict.
   Known nonintersecting candidate time is retained; unsupported/missing temporal facts
   remain UNKNOWN. Missing clocks preserve consistent declared structural counts.
6. Offline CLI tests disable socket construction, replay identical JSON twice and verify
   all temporary source bytes remain unchanged. Missing files return structured material
   diagnostics. Planner requirement/validation/mechanism changes and added Nearby entries
   leave verdicts and numeric measures unchanged; provenance hashes intentionally change.
7. Initial evaluation regression: **1 failed, 231 passed, 1 skipped**. The existing
   standard-library import guard lacked `zoneinfo`. Added only that module; the no-planner/
   no-external-client guard remains. Retest: **232 passed, 1 skipped** before final review fixes.
8. Standards review found one nonblocking duplicated canonical-digest implementation;
   both identity and schedule now share `records.canonical_digest`. Final Standards:
   **0 documented violations, 0 unresolved maintenance findings**.
9. Spec review found two P2 gaps: `start_at + duration` without a window skipped same-day
   capacity validation, and unbound claims discarded available independent time for
   conflict exclusion. Both public-entry regressions failed first, then passed. Capacity
   includes duration-only/local-day boundaries using independent zone; candidate explicit
   time never establishes an endpoint association. An initial direct-helper identity/role
   finding was withdrawn after public preflight made that combination unreachable.
   Final Spec: **0 unresolved actionable findings**; reviewer retest: **74 passed**.
10. Final full offline backend run, explicitly `TRIPWORLD_TEST_DATABASE=0`:
    **2063 passed, 10 skipped in 121.06 seconds**. Nine opt-in database integration
    cases and one Windows symlink-privilege case were skipped. Interim/reviewer tests
    overlap this suite and must not be summed as independent evidence.
11. Ruff initially found formatting/import issues and imported-fixture lint ambiguity;
    corrected local formatting and explicit fixture export. Final Ruff and compilation
    pass. No static typechecker is configured in `pyproject.toml`; no separate static
    typecheck was run or installed. Final checks passed: **190 local Markdown link targets**
    across changed current documentation and relevant archive files, current-status
    consistency, English new implementation/acceptance/archive content, CLI help,
    Ruff format check and `git diff --check`. Compilation is not described as static
    typing verification. The historical local Issue/published-body snapshots remain intact.

## Review scope and practical limitations

Review baseline is the pinned clean HEAD above, compared with the working tree plus
untracked Ticket 05 files, because the user prohibited commits. Reviews use current
AGENTS/project standards and the accepted requirement/schedule contract separately.

Tests use temporary synthetic local artifacts and mocked/recorded independent facts.
No Google/model/database call, operational evidence acquisition, formal benchmark,
experiment, version freeze, commit/push or later-ticket implementation occurred.
Identity/context/review hashes establish consistency with supplied material, not factual
authenticity. IANA interpretation uses the installed timezone data; replay should retain
the same dependency environment. Times beyond six fractional digits and overnight/vague/
ordinal/all-occurrences semantics remain explicitly unsupported/unresolved.

Unknown role/flexibility/correspondence may need reviewed upstream preparation before a
denominator exists. Nonempty unclear placeholder notes conservatively need review.
Occupancy review cannot adjudicate transport endpoints or select alternatives. Missing
transport feasibility, opening/access facts and provider operational integration are
not certified by requirement/non-overlap PASS. Daily slicing can be unavailable while
whole-request instants remain known. No five-dimension total, blind artifact or Repair
comparison is produced.

Next step after closeout: inspect Ticket 06 opening-hours specification/evidence
interfaces and close remaining meaning boundaries before separately approving implementation.

## Authorized closeout — 2026-10-02

After the offline acceptance above, the user requested Ticket 05 closeout, workspace
organization and a local commit, with related documentation, thesis archive and Issue
updates. This authorization supersedes the no-Git boundary only for this local closeout;
The user explicitly approved one logical commit grouping under AGENTS.md:
`feat: add offline requirement and schedule evaluation`. No push is authorized.

- Published the [self-contained completion record](https://github.com/rplalala/Reliable-Trip-Plan-Agent/issues/17#issuecomment-5935469356),
  completed the current Issue acceptance checklist, removed the stale readiness label,
  and closed #17 with reason completed. Parent #12 marks Ticket 05 resolved and remains
  open for Tickets 06-12. Preserved imported history, pinned old document links and
  native dependency relationships; no migration snapshot was rewritten.
- Current PROJECT/spec/contract/design/index documents describe implemented scope,
  offline acceptance and the separate closeout authorization. Existing GitHub links
  are not presented as containing unpublished code or current documents.
- Closeout rerun: `TRIPWORLD_TEST_DATABASE=0`, evaluation suite **234 passed, 1 skipped
  in 13.04 seconds** (Windows symlink privilege). Ruff and compilation passed. These
  tests overlap the full backend checkpoint above and are not additive. An expanded
  format check found mixed line endings in `records.py`; formatting corrected them,
  with identical Python AST before/after. Format retest passed for all ten checked
  implementation/test files; identity regression retest **41 passed in 2.07 seconds**.
  No functional implementation change or extra full-backend
  rerun was needed.
- Closeout documentation check passed **191 local Markdown targets** across changed
  current documentation and relevant archives; English new content passed. Temporary
  GitHub body files are outside the repository. Whitespace checks pass after correction.
- Approved commit scope is one coherent Ticket 05 capability: implementation, direct
  regression tests, package guide, current contracts/spec/design/index, PROJECT and
  this acceptance record, covering 19 versioned files. No unrelated
  planner, provider, frontend or infrastructure changes are present.
- The local archive `thesis_notes/evaluation/2026-10-02-ticket-05-implementation.md`
  preserves the implementation checkpoint and appends the later closeout. Its directory
  is ignored, so the archive stays local without force-add. Detailed acceptance remains
  tracked here. No credential, runtime/provider payload or temporary CLI body is included.

Status: Implemented/Validated, Issue completed, single local commit grouping approved,
code publication pending. The resulting local revision is recorded on the completion
comment; it is not presented as accessible online. This is not a version freeze or a
formal experiment.
