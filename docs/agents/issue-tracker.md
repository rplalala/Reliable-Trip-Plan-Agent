# Issue tracker: Local Markdown

Issues and specs for this repo live as Markdown files in `.scratch/`. Follow the approval rules in `AGENTS.md` before creating or changing project work items.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`.
- The spec is `.scratch/<feature-slug>/spec.md`.
- Implementation issues are separate files at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`.
- Record triage state in a `Status:` line near the top of each issue file, using `docs/agents/triage-labels.md`.
- Append conversation history under `## Comments`.

## Skill operations

- "Publish to the issue tracker": create the appropriate spec or issue file under `.scratch/<feature-slug>/`.
- "Fetch the relevant ticket": read the referenced issue file.

## Wayfinding operations

- Map: `.scratch/<effort>/map.md`, containing Notes, Decisions-so-far, and Fog.
- Child ticket: `.scratch/<effort>/issues/<NN>-<slug>.md`. Record its type in `Type:` (`research`, `prototype`, `grilling`, or `task`).
- Blocking: record `Blocked by: NN, NN` near the top. A ticket is unblocked when each referenced ticket is resolved.
- Frontier: scan open, unblocked, unclaimed child tickets; take the first by number.
- Claim: set `Status: claimed` and save before starting work.
- Resolve: append the answer under `## Answer`, set `Status: resolved`, and add a short context pointer and link to the map's Decisions-so-far.
